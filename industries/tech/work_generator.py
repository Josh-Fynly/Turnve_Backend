"""
Tech Industry Work Generator

Defines all possible work items for Tech simulations.
Does NOT manage progression or state.
"""

from typing import List

from core_engine.work import WorkFactory, WorkItem
from core_engine.session import Session


# -------------------------
# Work Catalog
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


def implementation_work(created_at: int) -> List[WorkItem]:
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


def governance_work(created_at: int) -> List[WorkItem]:
    return [
        WorkFactory.create(
            title="JPM governance review",
            description="Junior PM reviews progress, risks, and coordination.",
            estimated_effort=1,
            required_resources={"jpm": 1},
            priority=0,
            created_at=created_at,
        )
    ]


# -------------------------
# Public Generator
# -------------------------

def generate_tech_work(session: Session) -> List[WorkItem]:
    """
    Returns all possible Tech work items.
    Rules and engine decide WHAT becomes active.
    """

    now = session.current_time()
    work: List[WorkItem] = []

    work.extend(discovery_work(now))
    work.extend(architecture_work(now))
    work.extend(implementation_work(now))
    work.extend(delivery_work(now))
    work.extend(governance_work(now))

    return work