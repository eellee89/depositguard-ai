import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.schemas import CaseCreate, AddressSchema
from datetime import date
from decimal import Decimal

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_case_data():
    """Sample case data for testing."""
    return CaseCreate(
        tenant_name="John Doe",
        landlord_name="ABC Property Management",
        deposit_amount=Decimal("1500.00"),
        withheld_amount=Decimal("1500.00"),
        move_out_date=date(2024, 12, 1),
        tenant_address=AddressSchema(
            name="John Doe",
            address_line1="123 Main St",
            address_line2="Apt 4",
            address_city="Austin",
            address_state="TX",
            address_zip="78701"
        ),
        landlord_address=AddressSchema(
            name="ABC Property Management",
            address_line1="456 Business Blvd",
            address_city="Austin",
            address_state="TX",
            address_zip="78702"
        ),
        dispute_description="Landlord withheld full deposit without providing itemized deductions within 30 days of move-out.",
        evidence_urls=[]
    )
