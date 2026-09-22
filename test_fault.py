from app.models import Robot
from conftest import TestingSessionLocal

HEADERS = {"X-API-Key": "test-api-key"}

def test_fault_starts_inactive(client):
    response = client.get("/robot/fault")
    assert response.status_code == 200
    assert response.json() == {"fault_active": False}

def test_activate_and_deactivate_fault(client):
    activate = client.post("/robot/fault", json={"active": True}, headers=HEADERS)
    assert activate.status_code == 200
    assert activate.json() == {"fault_active": True}

    check = client.get("/robot/fault")
    assert check.json() == {"fault_active": True}

    deactivate = client.post("/robot/fault", json={"active": False}, headers=HEADERS)
    assert deactivate.json() == {"fault_active": False}

    final_check = client.get("/robot/fault")  # maybe redundant
    assert final_check.json() == {"fault_active": False}

def test_fault_for_missing_robot(client):
    db = TestingSessionLocal()
    db.query(Robot).delete()
    db.commit()
    db.close()

    response = client.get("/robot/fault")
    assert response.status_code == 404

def test_fault_missing_api_key_returns_422(client):
    response = client.post("/robot/fault", json={"active": True})
    assert response.status_code == 422

def test_fault_wrong_api_key_returns_401(client):
    response = client.post("/robot/fault", json={"active": True}, headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401
