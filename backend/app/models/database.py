from sqlalchemy import Column, String, DECIMAL, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Case(Base):
    """Main case table storing security deposit disputes."""
    
    __tablename__ = "cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Party Information
    tenant_name = Column(String(255), nullable=False)
    landlord_name = Column(String(255), nullable=False)
    
    # Financial Information
    deposit_amount = Column(DECIMAL(10, 2), nullable=False)
    withheld_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # Timeline
    move_out_date = Column(Date, nullable=False)
    
    # Addresses (stored as JSONB)
    tenant_address = Column(JSONB, nullable=False)
    landlord_address = Column(JSONB, nullable=False)
    
    # Dispute Details
    dispute_description = Column(Text, nullable=False)
    evidence_urls = Column(JSONB, default=list)
    
    # Agent State
    agent_state = Column(JSONB, default=dict)
    status = Column(String(50), default="draft")  # draft, analyzing, awaiting_approval, mailed, error
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Checkpoint(Base):
    """LangGraph checkpoint storage for agent state persistence."""
    
    __tablename__ = "checkpoints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    
    # LangGraph checkpoint data
    checkpoint_data = Column(JSONB, nullable=False)
    checkpoint_ns = Column(String(255))
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
