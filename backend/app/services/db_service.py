from sqlalchemy.orm import Session
from app.models.database import Case, Checkpoint
from app.models.schemas import CaseCreate, CaseUpdate
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class DatabaseService:
    """Service for database operations."""
    
    @staticmethod
    def create_case(db: Session, case_data: CaseCreate) -> Case:
        """Create a new case."""
        db_case = Case(
            tenant_name=case_data.tenant_name,
            landlord_name=case_data.landlord_name,
            deposit_amount=case_data.deposit_amount,
            withheld_amount=case_data.withheld_amount,
            move_out_date=case_data.move_out_date,
            tenant_address=case_data.tenant_address.model_dump(),
            landlord_address=case_data.landlord_address.model_dump(),
            dispute_description=case_data.dispute_description,
            evidence_urls=case_data.evidence_urls or [],
            agent_state={},
            status="draft"
        )
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        return db_case
    
    @staticmethod
    def get_case(db: Session, case_id: UUID) -> Optional[Case]:
        """Get case by ID."""
        return db.query(Case).filter(Case.id == case_id).first()
    
    @staticmethod
    def list_cases(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Case]:
        """List cases with optional filtering."""
        query = db.query(Case)
        if status:
            query = query.filter(Case.status == status)
        return query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_case(
        db: Session, 
        case_id: UUID, 
        case_data: CaseUpdate
    ) -> Optional[Case]:
        """Update case details."""
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            return None
        
        update_data = case_data.model_dump(exclude_unset=True)
        
        # Convert nested models to dicts
        if "tenant_address" in update_data:
            update_data["tenant_address"] = update_data["tenant_address"].model_dump()
        if "landlord_address" in update_data:
            update_data["landlord_address"] = update_data["landlord_address"].model_dump()
        
        for key, value in update_data.items():
            setattr(db_case, key, value)
        
        db_case.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_case)
        return db_case
    
    @staticmethod
    def update_case_status(
        db: Session,
        case_id: UUID,
        status: str,
        agent_state: Optional[Dict[str, Any]] = None
    ) -> Optional[Case]:
        """Update case status and optionally agent state."""
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            return None
        
        db_case.status = status
        if agent_state is not None:
            db_case.agent_state = agent_state
        db_case.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_case)
        return db_case
    
    @staticmethod
    def delete_case(db: Session, case_id: UUID) -> bool:
        """Delete a case."""
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            return False
        db.delete(db_case)
        db.commit()
        return True
    
    # Checkpoint methods for LangGraph
    @staticmethod
    def save_checkpoint(
        db: Session,
        case_id: UUID,
        checkpoint_data: Dict[str, Any],
        checkpoint_ns: Optional[str] = None
    ) -> Checkpoint:
        """Save LangGraph checkpoint."""
        checkpoint = Checkpoint(
            case_id=case_id,
            checkpoint_data=checkpoint_data,
            checkpoint_ns=checkpoint_ns
        )
        db.add(checkpoint)
        db.commit()
        db.refresh(checkpoint)
        return checkpoint
    
    @staticmethod
    def get_latest_checkpoint(
        db: Session,
        case_id: UUID
    ) -> Optional[Checkpoint]:
        """Get most recent checkpoint for a case."""
        return (
            db.query(Checkpoint)
            .filter(Checkpoint.case_id == case_id)
            .order_by(Checkpoint.created_at.desc())
            .first()
        )


# Singleton instance
db_service = DatabaseService()
