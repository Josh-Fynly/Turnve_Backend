"""
Tech Industry Events

Deterministic events that affect work, resources, or decisions.
"""

from core_engine.event import Event


def security_incident_event():
    def effect(session):
        session.log_evidence({
            "type": "event",
            "name": "Security Incident",
            "impact": "Security review required",
        })

    return Event(
        description="A security vulnerability is discovered",
        effect=effect,
    )


def production_outage_event():
    def effect(session):
        session.log_evidence({
            "type": "event",
            "name": "Production Outage",
            "impact": "Deployment and monitoring workload increases",
        })

    return Event(
        description="Production system outage",
        effect=effect,
    )


def stakeholder_scope_change_event():
    def effect(session):
        session.log_evidence({
            "type": "event",
            "name": "Scope Change",
            "impact": "Project scope expanded",
        })

    return Event(
        description="Stakeholder requests additional features",
        effect=effect,
    )