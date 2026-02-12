from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.db_service import db_service
from app.models.schemas import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    APIResponse
)
from typing import List, Optional
from uuid import UUID
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=APIResponse, status_code=201)
async def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new security deposit case.
    
    This initializes a case in 'draft' status, ready for agent execution.
    """
    try:
        db_case = db_service.create_case(db, case_data)
        
        return APIResponse(
            success=True,
            data=CaseResponse.model_validate(db_case),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{case_id}", response_model=APIResponse)
async def get_case(
    case_id: UUID,
    db: Session = Depends(get_db)
):
    """Get case details by ID."""
    db_case = db_service.get_case(db, case_id)
    
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return APIResponse(
        success=True,
        data=CaseResponse.model_validate(db_case),
        timestamp=datetime.utcnow()
    )


@router.get("/", response_model=APIResponse)
async def list_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all cases with optional filtering.
    
    Query params:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - status: Filter by status (draft, analyzing, awaiting_approval, mailed, error)
    """
    cases = db_service.list_cases(db, skip=skip, limit=limit, status=status)
    
    return APIResponse(
        success=True,
        data=[CaseResponse.model_validate(case) for case in cases],
        timestamp=datetime.utcnow()
    )


@router.patch("/{case_id}", response_model=APIResponse)
async def update_case(
    case_id: UUID,
    case_update: CaseUpdate,
    db: Session = Depends(get_db)
):
    """Update case details."""
    db_case = db_service.update_case(db, case_id, case_update)
    
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return APIResponse(
        success=True,
        data=CaseResponse.model_validate(db_case),
        timestamp=datetime.utcnow()
    )


@router.delete("/{case_id}", response_model=APIResponse)
async def delete_case(
    case_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a case."""
    success = db_service.delete_case(db, case_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return APIResponse(
        success=True,
        data={"deleted": True},
        timestamp=datetime.utcnow()
    )
