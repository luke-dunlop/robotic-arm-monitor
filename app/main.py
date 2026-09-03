from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import random

from app.database import get_db, engine, SessionLocal
from app.models import Base, Robot, Telemetry
from app.schemas import TelemetryResponse, TelemetryCreate, FaultCommand, FaultStatus

app = FastAPI()

ROBOT_ID = 1

@app.on_event("startup")
def seed_robot():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        robot = db.get(Robot, ROBOT_ID)
        if robot is None:
            db.add(Robot(id=ROBOT_ID, name="Robot Arm 1", status="normal"))
            db.commit()
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Robot monitoring system is running"}

@app.get("/robot/fault", response_model=FaultStatus)
def get_fault(db: Session = Depends(get_db)):
    robot = db.get(Robot, ROBOT_ID)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return {"fault_active": robot.status == "fault"}

@app.post("/robot/fault", response_model=FaultStatus)
def change_fault(command: FaultCommand, db: Session = Depends(get_db)):
    robot = db.get(Robot, ROBOT_ID)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")

    robot.status = "fault" if command.active else "normal"
    db.commit()

    return {"fault_active": robot.status == "fault"}

@app.post("/robot/telemetry", response_model=TelemetryResponse)
def create_telemetry(telemetry_data: TelemetryCreate, db: Session = Depends(get_db)):
    telemetry = Telemetry(
        robot_id=telemetry_data.robot_id,
        timestamp=datetime.now(),
        temperature=telemetry_data.temperature,
        motor_current=telemetry_data.motor_current,
        vibration=telemetry_data.vibration,
        speed=telemetry_data.speed
    )

    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    return telemetry

@app.get("/robot/telemetry", response_model=TelemetryResponse)
def get_latest_telemetry(db: Session = Depends(get_db)):
    latest = (db.query(Telemetry)
              .filter(Telemetry.robot_id == ROBOT_ID)
              .order_by(Telemetry.timestamp.desc())
              .first()
              )
    if latest is None:
        raise HTTPException(status_code=404, detail="No telemetry recorded yet")
    return latest

@app.get("/robot/telemetry/history", response_model=list[TelemetryResponse])
def get_telemetry_history(db = Depends(get_db)):
    readings = (
	db.query(Telemetry)
    .filter(Telemetry.robot_id == ROBOT_ID)
	.order_by(Telemetry.timestamp.desc())
	.limit(100)
	.all()
    )

    return readings
