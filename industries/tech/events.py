"""
Tech Industry Events

Events represent external pressures or emergent conditions.
They do NOT mutate session state directly.
They are recorded by the engine as evidence.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TechEvent:
    """
    Immutable description of an external or emergent event.
    """
    event_type: str
    description: str
    severity: int  # 1 (low) → 5 (critical)


# -------------------------
# External / Emergent Events
# -------------------------

def dependency_delay_event() -> TechEvent:
    return TechEvent(
        event_type="dependency_delay",
        description="A third-party API dependency is delayed.",
        severity=3,
    )


def production_bug_event() -> TechEvent:
    return TechEvent(
        event_type="production_bug",
        description="A critical bug was discovered in the system.",
        severity=4,
    )


def infrastructure_instability_event() -> TechEvent:
    return TechEvent(
        event_type="infrastructure_instability",
        description="Infrastructure instability detected during deployment.",
        severity=3,
    )


def stakeholder_pressure_event() -> TechEvent:
    return TechEvent(
        event_type="stakeholder_pressure",
        description="Stakeholders are pressuring for earlier delivery.",
        severity=2,
    )