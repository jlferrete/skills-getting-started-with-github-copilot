import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already exists
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"]
    # Try to sign up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400


def test_delete_participant():
    email = "deleteuser@mergington.edu"
    activity = "Programming Class"
    # Register first and check response
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    assert "message" in signup_response.json()
    # Now delete
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200, f"Delete failed: {response.text}"
    assert response.json()["message"]
    # Try to delete again (should fail)
    response2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response2.status_code == 404
