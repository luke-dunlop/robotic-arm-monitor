from fastapi import FastAPI
import random

app = FastAPI()

temperature = 40.0
current = 4.0
vibration = 0.5
speed = 50.0
cycles = 0

fault_active = False

@app.get("/")
def home():
    return {"message": "Robot monitoring system is running"}

@app.post("/robot/fault")
def change_fault(command: dict):
    global fault_active

    fault_active = command["active"]

    return {
	"fault_active": fault_active
    }

@app.get("/robot/telemetry")
def get_telemetry():
    global temperature, current, vibration, speed, cycles

    if (fault_active == True):
        temperature += random.uniform(-0.5, 1.0)
        current += random.uniform(-0.2, 0.4)
        vibration += random.uniform(-0.05, 0.1)
        speed += random.uniform(-1, 2)

    else:
        temperature += random.uniform(-0.5, 0.5)
        current += random.uniform(-0.2, 0.2)
        vibration += random.uniform(-0.05, 0.05)
        speed += random.uniform(-1,1)

    temperature = max(20, min(80, temperature))       # Keep temp between 20 and 80
    current = max(0, min(10, current))
    vibration = max(0, min(2, vibration))
    speed = max(0, min(100, speed))

    cycles += 1
    return {
        "temperature": round(temperature, 1),
        "current": round(current, 2),
        "vibration": round(vibration, 2),
        "speed": round(speed, 1),
        "cycles": cycles
    }
