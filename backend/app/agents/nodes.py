from typing import Dict, Any
from app.services.claude_service import claude_service
from app.services.lob_service import lob_service
from datetime import date


async def statutory_research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 1: Research Texas Property Code violations.
    
    Analyzes the case against statutory requirements and calculates damages.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with analysis results
    """
    print(f"[AGENT] Starting statutory research for case {state['case_id']}")
    
    # Prepare case data for Claude
    case_data = {
        "deposit_amount": float(state["deposit_amount"]),
        "withheld_amount": float(state["withheld_amount"]),
        "move_out_date": state["move_out_date"],
        "days_elapsed": state["days_elapsed"],
        "dispute_description": state["dispute_description"],
        "tenant_address": state["tenant_address"],
        "landlord_address": state["landlord_address"]
    }
    
    # Call Claude for statutory analysis
    analysis = await claude_service.analyze_statutory_compliance(case_data)
    
    # Update state
    state["statutory_analysis"] = analysis.model_dump()
    state["violation_findings"] = [v.model_dump() for v in analysis.violations]
    state["status"] = "analyzed"
    
    print(f"[AGENT] Analysis complete: {len(analysis.violations)} violations found")
    print(f"[AGENT] Total damages: ${analysis.total_damages}")
    
    return state


async def generate_letter_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 2: Generate demand letter using Claude.
    
    Creates a professional demand letter with statutory citations.
    
    Args:
        state: Current agent state with analysis results
        
    Returns:
        Updated state with draft letter
    """
    print(f"[AGENT] Generating demand letter for case {state['case_id']}")
    
    # Prepare data
    from app.models.schemas import StatutoryAnalysis, ViolationFinding
    from decimal import Decimal
    
    # Reconstruct analysis object
    analysis_data = state["statutory_analysis"]
    violations = [ViolationFinding(**v) for v in analysis_data["violations"]]
    
    analysis = StatutoryAnalysis(
        violations=violations,
        days_elapsed=analysis_data["days_elapsed"],
        is_compliant=analysis_data["is_compliant"],
        base_damages=Decimal(str(analysis_data["base_damages"])),
        treble_damages=Decimal(str(analysis_data["treble_damages"])),
        statutory_penalty=Decimal(str(analysis_data["statutory_penalty"])),
        total_damages=Decimal(str(analysis_data["total_damages"])),
        summary=analysis_data["summary"]
    )
    
    case_data = {
        "tenant_name": state["tenant_name"],
        "landlord_name": state["landlord_name"],
        "tenant_address": state["tenant_address"],
        "landlord_address": state["landlord_address"],
        "deposit_amount": state["deposit_amount"],
        "withheld_amount": state["withheld_amount"],
        "move_out_date": state["move_out_date"]
    }
    
    # Generate letter
    letter = await claude_service.generate_demand_letter(case_data, analysis)
    
    # Update state
    state["demand_letter_draft"] = letter.model_dump()
    state["status"] = "awaiting_approval"
    state["needs_approval"] = True
    
    print(f"[AGENT] Letter generated, awaiting human approval")
    
    return state


async def mail_dispatch_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 3: Send certified mail via Lob API.
    
    Only executes if human_approved = True.
    
    Args:
        state: Current agent state with approved letter
        
    Returns:
        Updated state with mailing results
    """
    print(f"[AGENT] Dispatching certified mail for case {state['case_id']}")
    
    if not state.get("human_approved", False):
        print("[AGENT] ERROR: Letter not approved, cannot send mail")
        state["status"] = "error"
        state["error"] = "Letter must be approved before mailing"
        return state
    
    # Get letter content
    letter_html = state.get("edited_letter_html") or state["demand_letter_draft"]["letter_html"]
    
    # Send via Lob
    try:
        result = await lob_service.send_certified_letter(
            to_address=state["landlord_address"],
            from_address=state["tenant_address"],
            letter_html=letter_html,
            description=f"Demand Letter - Case {state['case_id']}"
        )
        
        # Update state
        state["lob_mail_id"] = result.lob_id
        state["tracking_url"] = result.tracking_url
        state["expected_delivery"] = result.expected_delivery
        state["status"] = "mailed"
        state["needs_approval"] = False
        
        print(f"[AGENT] Mail sent successfully: {result.lob_id}")
        print(f"[AGENT] Tracking: {result.tracking_url}")
        
    except Exception as e:
        print(f"[AGENT] ERROR sending mail: {e}")
        state["status"] = "error"
        state["error"] = str(e)
    
    return state


# Export node functions
__all__ = ["statutory_research_node", "generate_letter_node", "mail_dispatch_node"]
