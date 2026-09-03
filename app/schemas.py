from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TelemetryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    robot_id: int
    timestamp: datetime
    temperature: float | None
    motor_current: float | None
    vibration: float | None
    speed: float | None

class TelemetryCreate(BaseModel):
    robot_id: int
    temperature: float
    motor_current: float
    vibration: float
    speed: float

class FaultCommand(BaseModel):
    active: bool

class FaultStatus(BaseModel):
    fault_active: bool

