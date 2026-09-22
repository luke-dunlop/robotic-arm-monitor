HEADERS = {"X-API-Key": "test-api-key"}

def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Robot monitoring system is running"}

def test_no_telemetry_returns_404(client):
    response = client.get("/robot/telemetry")
    assert response.status_code == 404

def test_post_and_get_telemetry(client):
    payload = {
        "robot_id": 1,
        "temperature": 42.5,
        "motor_current": 3.2,
        "vibration": 0.4,
        "speed": 55.0,
    }

    post_response = client.post("/robot/telemetry", json=payload, headers=HEADERS)
    assert post_response.status_code == 200

    body = post_response.json()
    assert body["robot_id"] == 1
    assert body["temperature"] == 42.5
    assert "id" in body
    assert "timestamp" in body

    get_response = client.get("/robot/telemetry")
    assert get_response.status_code == 200
    assert get_response.json()["temperature"] == 42.5

def test_telemetry_history_orders_newest_first(client):
    for temp in [30.0, 40.0, 50.0]:
        client.post("/robot/telemetry", json={
            "robot_id": 1,
            "temperature": temp,
            "motor_current": 1.0,
            "vibration": 0.1,
            "speed": 10.0
            },
            headers=HEADERS)

    response = client.get("/robot/telemetry/history")
    assert response.status_code == 200
    readings = response.json()
    assert len(readings) == 3
    assert readings[0]["temperature"] == 50.0
    assert readings[-1]["temperature"] == 30.0

