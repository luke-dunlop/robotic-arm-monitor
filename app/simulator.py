import random
import requests
import time

API_URL = "http://127.0.0.1:8000"

temperature = 40.0
current = 4.0
vibration = 0.5
speed = 50.0

session = requests.Session()

def get_fault_active() -> bool:  # ask the API for the current fault state, so this script and the API and never disagree about whether fault mode is on.
    try:
        resp = session.get(f"{API_URL}/robot/fault", timeout=2)
        resp.raise_for_status()
        return resp.json()["fault_active"]
    except requests.RequestException as e:
        print(f"[warn] could not fetch fault status ({e}); assuming normal mode")
        return False
    
while True:
    fault_active = get_fault_active()

    if fault_active:
        temperature += random.uniform(-0.5, 1.5)
        current += random.uniform(-0.2, 0.6)
        vibration += random.uniform(-0.05, 0.15)
        speed += random.uniform(-1, 2)

    else:
        temperature += random.uniform(-0.5, 0.5)
        current += random.uniform(-0.2, 0.2)
        vibration += random.uniform(-0.05, 0.05)
        speed += random.uniform(-1, 1)

    temperature = max(20, min(80, temperature))
    current = max(0, min(10, current))
    vibration = max(0, min(2, vibration))
    speed = max(0, min(100, speed))

    telemetry = {
        "robot_id": 1,
        "temperature": round(temperature, 2),
        "motor_current": round(current, 2),
        "vibration": round(vibration, 2),
        "speed": round(speed, 2)
    }

    try:
        response = session.post(f"{API_URL}/robot/telemetry", json=telemetry, timeout=2)
        response.raise_for_status()
        print(response.json())
    except requests.RequestException as e:
        print(f"[warn] failed to post telemetry ({e})")

    time.sleep(1)