
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
)
from sqlalchemy.sql import func
from app.core.database import Base


class SimulationSession(Base):
    __tablename__ = "simulation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)  # nullable for demo users
    industry = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    status = Column(String, default="active")  # active | completed | abandoned

    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    state = Column(JSON, nullable=False)  # current simulation state
    score = Column(JSON, nullable=True)   # final scores


class SimulationEvent(Base):
    __tablename__ = "simulation_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer,
        ForeignKey("simulation_sessions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    actor = Column(String, nullable=False)  # user | npc | system
    event_type = Column(String, nullable=False)  # decision | reaction | system
    payload = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())