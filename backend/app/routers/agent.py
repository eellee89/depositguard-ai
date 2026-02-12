from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.db_service import db_service
from app.agents.graph import agent_graph
from app.models.schemas import (
    AgentExecuteResponse,
    ApprovalRequest,
    APIResponse,
    StatutoryAnalysis,
    DemandLetterDraft
)
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal

router = APIRouter()


@router.post("/cases/{case_id}/execute", response_model=APIResponse)
async def execute_agent(
    case_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Execute the AI agent workflow for a case.
    
    This runs the agent through:
    1. Statutory research
    2. Demand letter generation
    3. Stops at human approval gate
    
    Returns the current state with analysis and draft letter.
    """
    # Get case from database
    db_case = db_service.get_case(db, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Calculate days elapsed
    days_elapsed = (date.today() - db_case.move_out_date).days
    
    # Build initial state
    initial_state = {
        "case_id": str(db_case.id),
        "tenant_name": db_case.tenant_name,
        "landlord_name": db_case.landlord_name,
        "deposit_amount": db_case.deposit_amount,
        "withheld_amount": db_case.withheld_amount,
        "move_out_date": db_case.move_out_date.isoformat(),
        "days_elapsed": days_elapsed,
        "tenant_address": db_case.tenant_address,
        "landlord_address": db_case.landlord_address,
        "dispute_description": db_case.dispute_description,
        "evidence_urls": db_case.evidence_urls,
        "statutory_analysis": None,
        "violation_findings": [],
        "demand_letter_draft": None,
        "human_approved": False,
        "edited_letter_html": None,
        "needs_approval": False,
        "lob_mail_id": None,
        "tracking_url": None,
        "expected_delivery": None,
        "status": "analyzing",
        "error": None
    }
    
    try:
        # Update status to analyzing
        db_service.update_case_status(db, case_id, "analyzing")
        
        # Execute graph (will stop at human approval gate)
        final_state = await agent_graph.ainvoke(initial_state)
        
        # Save state to database
        db_service.update_case_status(
            db,
            case_id,
            final_state["status"],
            agent_state=final_state
        )
        
        # Build response
        response_data = {
            "case_id": case_id,
            "status": final_state["status"],
            "current_step": "awaiting_approval",
            "needs_approval": final_state.get("needs_approval", True)
        }
        
        # Add analysis if available
        if final_state.get("statutory_analysis"):
            response_data["analysis"] = final_state["statutory_analysis"]
        
        # Add letter if available
        if final_state.get("demand_letter_draft"):
            response_data["demand_letter"] = final_state["demand_letter_draft"]
        
        return APIResponse(
            success=True,
            data=response_data,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        # Update status to error
        db_service.update_case_status(
            db,
            case_id,
            "error",
            agent_state={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


@router.post("/cases/{case_id}/approve", response_model=APIResponse)
async def approve_letter(
    case_id: UUID,
    approval: ApprovalRequest,
    db: Session = Depends(get_db)
):
    """
    Approve or reject the generated demand letter.
    
    If approved, the agent continues to send certified mail.
    If rejected or edited, the state is updated but mail is not sent.
    """
    # Get case
    db_case = db_service.get_case(db, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if db_case.status != "awaiting_approval":
        raise HTTPException(
            status_code=400,
            detail=f"Case is not awaiting approval (current status: {db_case.status})"
        )
    
    # Get current agent state
    current_state = db_case.agent_state
    
    if not approval.approved:
        # User rejected - update status
        db_service.update_case_status(
            db,
            case_id,
            "draft",
            agent_state={**current_state, "human_approved": False}
        )
        
        return APIResponse(
            success=True,
            data={"message": "Letter rejected. Case returned to draft status."},
            timestamp=datetime.utcnow()
        )
    
    # User approved - update state and continue to mailing
    current_state["human_approved"] = True
    
    if approval.edited_letter_html:
        current_state["edited_letter_html"] = approval.edited_letter_html
    
    try:
        # Continue graph execution from current state
        final_state = await agent_graph.ainvoke(current_state)
        
        # Save final state
        db_service.update_case_status(
            db,
            case_id,
            final_state["status"],
            agent_state=final_state
        )
        
        # Build response
        response_data = {
            "case_id": case_id,
            "status": final_state["status"],
            "lob_mail_id": final_state.get("lob_mail_id"),
            "tracking_url": final_state.get("tracking_url"),
            "expected_delivery": final_state.get("expected_delivery")
        }
        
        return APIResponse(
            success=True,
            data=response_data,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        db_service.update_case_status(
            db,
            case_id,
            "error",
            agent_state={**current_state, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=f"Mailing failed: {str(e)}")


@router.get("/cases/{case_id}/status", response_model=APIResponse)
async def get_agent_status(
    case_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get current agent status for a case.
    
    Returns the full agent state including analysis, letter, and mailing info.
    """
    db_case = db_service.get_case(db, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return APIResponse(
        success=True,
        data={
            "case_id": case_id,
            "status": db_case.status,
            "agent_state": db_case.agent_state
        },
        timestamp=datetime.utcnow()
    )
