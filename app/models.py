import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Robot(Base):
    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(primary_key=True) #note the type hints are actually necessary here 
    name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="normal")


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(primary_key=True)
    robot_id: Mapped[int] = mapped_column(ForeignKey("robots.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime)  #datetime - python type, DateTime SQL column type
    temperature: Mapped[float] = mapped_column(Numeric(5, 2))
    motor_current: Mapped[float] = mapped_column(Numeric(6, 2))
    vibration: Mapped[float] = mapped_column(Numeric(5, 2))
    speed: Mapped[float] = mapped_column(Numeric(6, 2))
