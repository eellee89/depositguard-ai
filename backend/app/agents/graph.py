from langgraph.graph import StateGraph, END
from typing import TypedDict, Any, Dict, List, Optional
from app.agents.nodes import (
    statutory_research_node,
    generate_letter_node,
    mail_dispatch_node
)
from datetime import date
from decimal import Decimal


class CaseState(TypedDict):
    """State schema for the legal agent workflow."""
    
    # Case identification
    case_id: str
    
    # Party information
    tenant_name: str
    landlord_name: str
    
    # Financial details
    deposit_amount: Decimal
    withheld_amount: Decimal
    
    # Timeline
    move_out_date: date
    days_elapsed: int
    
    # Addresses
    tenant_address: Dict[str, Any]
    landlord_address: Dict[str, Any]
    
    # Dispute details
    dispute_description: str
    evidence_urls: List[str]
    
    # Agent workflow state
    statutory_analysis: Optional[Dict[str, Any]]
    violation_findings: List[Dict[str, Any]]
    demand_letter_draft: Optional[Dict[str, Any]]
    
    # Human interaction
    human_approved: bool
    edited_letter_html: Optional[str]
    needs_approval: bool
    
    # Mailing results
    lob_mail_id: Optional[str]
    tracking_url: Optional[str]
    expected_delivery: Optional[date]
    
    # Status tracking
    status: str  # draft, analyzing, analyzed, awaiting_approval, mailed, error
    error: Optional[str]


def should_continue_to_mail(state: CaseState) -> str:
    """
    Conditional edge: Decide if we should proceed to mailing.
    
    Returns "mail" if approved, "end" otherwise.
    """
    if state.get("human_approved", False):
        return "mail"
    else:
        return "end"


def create_agent_graph() -> StateGraph:
    """
    Create the LangGraph state machine for legal agent workflow.
    
    Workflow:
        START → Research → Generate Letter → [Human Approval Gate] → Mail → END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize graph with state schema
    workflow = StateGraph(CaseState)
    
    # Add nodes
    workflow.add_node("research", statutory_research_node)
    workflow.add_node("generate", generate_letter_node)
    workflow.add_node("mail", mail_dispatch_node)
    
    # Define edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "generate")
    
    # Conditional edge: only proceed to mail if approved
    workflow.add_conditional_edges(
        "generate",
        should_continue_to_mail,
        {
            "mail": "mail",
            "end": END
        }
    )
    
    workflow.add_edge("mail", END)
    
    # Compile graph (no checkpointing here - we'll handle it in the router)
    return workflow.compile()


# Create singleton graph instance
agent_graph = create_agent_graph()
