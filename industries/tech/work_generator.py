"""
Tech Industry Work Generator

Generates deterministic, phase-based work items
for software engineering projects.
"""

from typing import List

from core_engine.work import WorkFactory, WorkItem


# -------------------------
# Discovery Phase
# -------------------------

def discovery_work(created_at: int) -> List[WorkItem]:
    return [
        WorkFactory.create(
            title="Define product requirements",
            description="Clarify user needs, constraints, and success metrics.",
            estimated_effort=3,
            required_resources={"analyst": 1},
            priority=1,
            created_at=created_at,
        ),
        WorkFactory.create(
            title="Create Work Canvas",
            description="Define scope, assumptions, risks, and milestones.",
            estimated_effort=2,
            required_resources={"pm": 1},
            priority=1,
            created_at=created_at,
        ),
    ]


# -------------------------
# Architecture Phase
# -------------------------

def architecture_work(created_at: int) -> List[WorkItem]:
    return [
        WorkFactory.create(
            title="Design system architecture",
            description="Define services, data flows, and technology stack.",
            estimated_effort=5,
            required_resources={"architect": 1},
            priority=2,
            created_at=created_at,
        ),
        WorkFactory.create(
            title="Select deployment strategy",
            description="Decide hosting, CI/CD, and release model.",
            estimated_effort=3,
            required_resources={"devops": 1},
            priority=2,
            created_at=created_at,
        ),
    ]


# -------------------------
# Implementation Phase
# -------------------------

def implementation_work(created_at: int, repo_connected: bool) -> List[WorkItem]:
    if not repo_connected:
        return []

    return [
        WorkFactory.create(
            title="Initialize repository",
            description="Set up repository structure, linting, and CI.",
            estimated_effort=2,
            required_resources={"engineer": 1},
            priority=3,
            created_at=created_at,
        ),
        WorkFactory.create(
            title="Implement core features",
            description="Develop primary application functionality.",
            estimated_effort=8,
            required_resources={"engineer": 2},
            priority=3,
            created_at=created_at,
        ),
    ]


# -------------------------
# Delivery Phase
# -------------------------

def delivery_work(created_at: int) -> List[WorkItem]:
    return [
        WorkFactory.create(
            title="Deploy to production",
            description="Release application using approved deployment plan.",
            estimated_effort=4,
            required_resources={"devops": 1},
            priority=4,
            created_at=created_at,
        ),
        WorkFactory.create(
            title="Monitor and stabilize",
            description="Observe system health and resolve initial issues.",
            estimated_effort=3,
            required_resources={"engineer": 1},
            priority=4,
            created_at=created_at,
        ),
    ]


# -------------------------
# Governance Phase (JPM)
# -------------------------

def governance_work(created_at: int) -> List[WorkItem]:
    return [
        WorkFactory.create(
            title="JPM phase review",
            description="Junior Project Manager reviews progress and approves next phase.",
            estimated_effort=1,
            required_resources={"jpm": 1},
            priority=0,
            created_at=created_at,
        )
    ]


# -------------------------
# Master Generator
# -------------------------

def generate_tech_work(session) -> List[WorkItem]:
    """
    Entry point used by the engine.
    Generates work based on session state.
    """

    now = session.current_time
    work: List[WorkItem] = []

    # Always allow discovery
    if not session.flags.get("discovery_done"):
        work.extend(discovery_work(now))

    # Architecture after discovery
    if session.flags.get("discovery_done") and not session.flags.get("architecture_ready"):
        work.extend(architecture_work(now))

    # Implementation requires repo + architecture
    if (
        session.flags.get("architecture_ready")
        and not session.flags.get("implementation_done")
    ):
        work.extend(
            implementation_work(
                now,
                repo_connected=session.flags.get("repo_connected", False),
            )
        )

    # Delivery after implementation
    if session.flags.get("implementation_done") and not session.flags.get("delivery_done"):
        work.extend(delivery_work(now))

    # JPM governance always applies
    work.extend(governance_work(now))

    return work