import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_case(client: TestClient, sample_case_data):
    """Test case creation."""
    response = client.post(
        "/api/cases/",
        json=sample_case_data.model_dump(mode="json")
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["tenant_name"] == "John Doe"
    assert data["data"]["status"] == "draft"


def test_get_case(client: TestClient, sample_case_data):
    """Test retrieving a case."""
    # Create case first
    create_response = client.post(
        "/api/cases/",
        json=sample_case_data.model_dump(mode="json")
    )
    case_id = create_response.json()["data"]["id"]
    
    # Get case
    response = client.get(f"/api/cases/{case_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == case_id


def test_list_cases(client: TestClient, sample_case_data):
    """Test listing cases."""
    # Create a few cases
    for i in range(3):
        client.post(
            "/api/cases/",
            json=sample_case_data.model_dump(mode="json")
        )
    
    # List cases
    response = client.get("/api/cases/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) >= 3


def test_update_case(client: TestClient, sample_case_data):
    """Test updating a case."""
    # Create case
    create_response = client.post(
        "/api/cases/",
        json=sample_case_data.model_dump(mode="json")
    )
    case_id = create_response.json()["data"]["id"]
    
    # Update case
    update_data = {"tenant_name": "Jane Doe"}
    response = client.patch(f"/api/cases/{case_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["tenant_name"] == "Jane Doe"


def test_delete_case(client: TestClient, sample_case_data):
    """Test deleting a case."""
    # Create case
    create_response = client.post(
        "/api/cases/",
        json=sample_case_data.model_dump(mode="json")
    )
    case_id = create_response.json()["data"]["id"]
    
    # Delete case
    response = client.delete(f"/api/cases/{case_id}")
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify deletion
    get_response = client.get(f"/api/cases/{case_id}")
    assert get_response.status_code == 404


def test_case_not_found(client: TestClient):
    """Test 404 for non-existent case."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/cases/{fake_uuid}")
    assert response.status_code == 404
