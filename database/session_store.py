"""
Persistent Session Store
"""

import json
from database.models import (
    SessionLocal,
    SimulationSession,
)


# -------------------------
# Save Session
# -------------------------

def save_session(session):

    db = SessionLocal()

    state_data = json.dumps(session.serialize())

    record = SimulationSession(
        id=session.id,
        industry=session.industry,
        role=session.role,
        state=state_data,
    )

    db.merge(record)
    db.commit()
    db.close()


# -------------------------
# Load Session
# -------------------------

def load_session(session_id):

    db = SessionLocal()

    record = (
        db.query(SimulationSession)
        .filter(SimulationSession.id == session_id)
        .first()
    )

    db.close()

    if not record:
        return None

    return {
        "industry": record.industry,
        "role": record.role,
        "state": json.loads(record.state),
    }
