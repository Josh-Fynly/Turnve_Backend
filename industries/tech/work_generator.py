"""
Turnve – Tech Industry Work Generator

Responsible for defining and generating realistic software engineering work
for the Tech industry.

This module defines WHAT work exists.
It does NOT control execution, time, or AI behavior.
"""

from typing import List, Dict
from uuid import uuid4

from core_engine.work import WorkItem
from core_engine.session import Session


# -------------------------
# Tech Work Categories
# -------------------------

TECH_WORK_CATEGORIES = {
    "planning": [
        "Define product requirements",
        "Create technical architecture",
        "Sprint planning",
        "Risk assessment",
    ],
    "coordination": [
        "Stakeholder alignment",
        "Task prioritization",
        "Dependency tracking",
        "Delivery reporting",
    ],
    "development": [
        "Implement backend services",
        "Implement frontend interface",
        "Integrate third-party APIs",
        "Write automated tests",
    ],
    "infrastructure": [
        "Set up repository",
        "Configure CI/CD pipeline",
        "Provision cloud resources",
        "Deploy to production",
    ],
    "quality": [
        "Code review",
        "Security audit",
        "Performance testing",
        "Bug fixing",
    ],
}


# -------------------------
# Role Capability Map
# -------------------------

ROLE_CAPABILITIES = {
    "Junior Project Manager": {"planning", "coordination"},
    "Software Engineer": {"development", "quality"},
    "Senior Engineer": {"development", "infrastructure", "quality"},
    "DevOps Engineer": {"infrastructure"},
}


# -------------------------
# Public API
# -------------------------

def generate_tech_work(
    session: Session,
    project_type: str,
) -> List[WorkItem]:
    """
    Entry point used by the engine to generate Tech industry work.

    Example project_type:
    - "mobile_payments_app"
    - "saas_platform"
    - "api_service"
    """

    work_items: List[WorkItem] = []

    # 1. Foundational work (always exists)
    work_items.extend(_generate_foundation_work(session))

    # 2. Project-specific lifecycle
    if project_type == "mobile_payments_app":
        work_items.extend(_mobile_payments_lifecycle(session))
    else:
        work_items.extend(_generic_software_lifecycle(session))

    return work_items


# -------------------------
# Work Generators
# -------------------------

def _generate_foundation_work(session: Session) -> List[WorkItem]:
    """
    Work that must exist before any serious software project can begin.
    """

    return [
        WorkItem(
            id=str(uuid4()),
            title="Create Work Canvas",
            description=(
                "Define project scope, goals, constraints, success metrics, "
                "and delivery milestones."
            ),
            estimated_effort=3,
            required_resources={},
            priority=0,
            created_at=session.current_time,
        ),
        WorkItem(
            id=str(uuid4()),
            title="Connect Code Repository",
            description=(
                "Connect an existing GitHub repository or create a new one. "
                "Ensure access control and repository visibility are configured."
            ),
            estimated_effort=2,
            required_resources={},
            priority=0,
            created_at=session.current_time,
        ),
    ]


def _mobile_payments_lifecycle(session: Session) -> List[WorkItem]:
    """
    Full lifecycle for a regulated, production-grade software system.
    """

    lifecycle = [
        ("Define payment requirements", 4, "planning"),
        ("Design secure system architecture", 5, "planning"),
        ("Backend payment processing", 8, "development"),
        ("Frontend wallet & UI", 6, "development"),
        ("Integrate payment gateways", 5, "development"),
        ("Set up CI/CD and cloud infra", 4, "infrastructure"),
        ("Security & compliance review", 5, "quality"),
        ("Production deployment", 3, "infrastructure"),
    ]

    return _build_work_items(session, lifecycle)


def _generic_software_lifecycle(session: Session) -> List[WorkItem]:
    """
    Default lifecycle for non-regulated software products.
    """

    lifecycle = [
        ("Define product requirements", 3, "planning"),
        ("Implement core features", 6, "development"),
        ("Set up deployment pipeline", 3, "infrastructure"),
        ("Quality assurance testing", 3, "quality"),
        ("Production release", 2, "infrastructure"),
    ]

    return _build_work_items(session, lifecycle)


# -------------------------
# Helpers
# -------------------------

def _build_work_items(
    session: Session,
    lifecycle: List[tuple],
) -> List[WorkItem]:
    """
    Converts lifecycle definitions into WorkItem objects.
    """

    items: List[WorkItem] = []

    for index, (title, effort, category) in enumerate(lifecycle):
        items.append(
            WorkItem(
                id=str(uuid4()),
                title=title,
                description=f"Tech work category: {category}",
                estimated_effort=effort,
                required_resources={},
                priority=index + 1,
                created_at=session.current_time,
            )
        )

    return items