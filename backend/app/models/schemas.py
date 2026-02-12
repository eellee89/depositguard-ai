from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


# Address Schema
class AddressSchema(BaseModel):
    """Address format for Lob API compatibility."""
    name: str = Field(..., description="Recipient name")
    address_line1: str = Field(..., description="Street address")
    address_line2: Optional[str] = Field(None, description="Apartment, suite, etc.")
    address_city: str = Field(..., description="City")
    address_state: str = Field(..., description="2-letter state code", min_length=2, max_length=2)
    address_zip: str = Field(..., description="ZIP code")


# Case Schemas
class CaseCreate(BaseModel):
    """Schema for creating a new case."""
    tenant_name: str = Field(..., min_length=1, max_length=255)
    landlord_name: str = Field(..., min_length=1, max_length=255)
    deposit_amount: Decimal = Field(..., gt=0, description="Original deposit amount")
    withheld_amount: Decimal = Field(..., ge=0, description="Amount withheld by landlord")
    move_out_date: date = Field(..., description="Date tenant moved out")
    tenant_address: AddressSchema
    landlord_address: AddressSchema
    dispute_description: str = Field(..., min_length=10, description="Detailed description of dispute")
    evidence_urls: Optional[List[str]] = Field(default_factory=list, description="URLs to evidence files")


class CaseUpdate(BaseModel):
    """Schema for updating case details."""
    tenant_name: Optional[str] = None
    landlord_name: Optional[str] = None
    deposit_amount: Optional[Decimal] = None
    withheld_amount: Optional[Decimal] = None
    move_out_date: Optional[date] = None
    tenant_address: Optional[AddressSchema] = None
    landlord_address: Optional[AddressSchema] = None
    dispute_description: Optional[str] = None
    evidence_urls: Optional[List[str]] = None


class CaseResponse(BaseModel):
    """Schema for case response."""
    id: UUID
    tenant_name: str
    landlord_name: str
    deposit_amount: Decimal
    withheld_amount: Decimal
    move_out_date: date
    tenant_address: Dict[str, Any]
    landlord_address: Dict[str, Any]
    dispute_description: str
    evidence_urls: List[str]
    agent_state: Dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Agent Schemas
class ViolationFinding(BaseModel):
    """Individual statutory violation found."""
    statute: str = Field(..., description="e.g., 'Texas Property Code §92.103'")
    violation_type: str = Field(..., description="Type of violation")
    description: str = Field(..., description="Details of the violation")
    damages_applicable: bool = Field(..., description="Whether treble damages apply")


class StatutoryAnalysis(BaseModel):
    """Result of statutory compliance analysis."""
    violations: List[ViolationFinding]
    days_elapsed: int = Field(..., description="Days since move-out")
    is_compliant: bool = Field(..., description="Whether landlord complied with law")
    base_damages: Decimal = Field(..., description="Amount wrongfully withheld")
    treble_damages: Decimal = Field(..., description="3x damages if applicable")
    statutory_penalty: Decimal = Field(default=Decimal("100.00"), description="$100 penalty")
    total_damages: Decimal = Field(..., description="Total amount tenant can claim")
    summary: str = Field(..., description="Plain English summary")


class DemandLetterDraft(BaseModel):
    """Generated demand letter."""
    letter_html: str = Field(..., description="HTML formatted letter for Lob")
    letter_text: str = Field(..., description="Plain text version")
    citations: List[str] = Field(..., description="Statutory citations included")


class AgentExecuteResponse(BaseModel):
    """Response from agent execution."""
    case_id: UUID
    status: str
    current_step: str
    analysis: Optional[StatutoryAnalysis] = None
    demand_letter: Optional[DemandLetterDraft] = None
    needs_approval: bool


class ApprovalRequest(BaseModel):
    """Request to approve/reject generated letter."""
    approved: bool
    edited_letter_html: Optional[str] = Field(None, description="Modified letter if edited")


class MailingResult(BaseModel):
    """Result of mailing operation."""
    lob_id: str
    tracking_url: Optional[str]
    expected_delivery: Optional[date]


# API Response Wrapper
class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
