"""
Database Models
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, sessionmaker
import json


DATABASE_URL = "sqlite:///turnve.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class SimulationSession(Base):

    __tablename__ = "simulation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    industry = Column(String)
    role = Column(String)
    state = Column(Text)  # JSON serialized


def init_db():
    Base.metadata.create_all(bind=engine)
