"""
Tech Industry Events

Events are triggered by the engine when notable milestones
occur (e.g. work completion). They modify session state in
a controlled, auditable way.
"""

from core_engine.event import Event


# -------------------------
# Event: Work Completed
# -------------------------

def work_completed_event(work_id: str) -> Event:
    """
    Fired when a work item is completed.
    Records the completion as an industry milestone.
    """

    def effect(session):
        session.evidence.add_record(
            category="work_completion",
            reference=work_id,
            note=f"Work item '{work_id}' completed."
        )

    return Event(
        description=f"Work completed: {work_id}",
        effect=effect
    )


# -------------------------
# Event: Repository Connected
# -------------------------

def repository_connected_event() -> Event:
    """
    Fired when a code repository is connected.
    Enables engineering workflows.
    """

    def effect(session):
        session.flags["repo_connected"] = True

        session.evidence.add_record(
            category="engineering",
            reference="repository",
            note="Source code repository connected."
        )

    return Event(
        description="Repository connected",
        effect=effect
    )


# -------------------------
# Event: Architecture Finalized
# -------------------------

def architecture_finalized_event() -> Event:
    """
    Fired when system architecture is finalized.
    """

    def effect(session):
        session.flags["architecture_ready"] = True

        session.evidence.add_record(
            category="architecture",
            reference="system_design",
            note="System architecture finalized."
        )

    return Event(
        description="Architecture finalized",
        effect=effect
    )


# -------------------------
# Event: Deployment Strategy Approved
# -------------------------

def deployment_strategy_approved_event() -> Event:
    """
    Fired when deployment strategy is approved.
    """

    def effect(session):
        session.flags["deployment_ready"] = True

        session.evidence.add_record(
            category="delivery",
            reference="deployment_strategy",
            note="Deployment strategy approved."
        )

    return Event(
        description="Deployment strategy approved",
        effect=effect
    )