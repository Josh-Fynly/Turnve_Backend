"""
Tech Industry Rules

Enforces realism constraints for Tech projects.
Rules do NOT execute work.
They validate state, sequencing, and eligibility.
"""

from typing import List
from core_engine.work import WorkItem
from core_engine.exceptions import EngineStateError


# -------------------------
# Rule 1: Repository Required for Coding Work
# -------------------------

CODING_CATEGORIES = {
    "frontend_development",
    "backend_development",
    "mobile_development",
    "database_design",
}


def require_repository_for_coding(
    work_items: List[WorkItem],
    repository_connected: bool,
) -> None:
    """
    Prevents coding work from starting without a repository.
    """

    if not repository_connected:
        for work in work_items:
            if any(cat in work.description.lower() for cat in CODING_CATEGORIES):
                raise EngineStateError(
                    "Coding work cannot begin without a connected repository"
                )


# -------------------------
# Rule 2: Planning Must Precede Development
# -------------------------

def enforce_planning_before_execution(work_items: List[WorkItem]) -> None:
    """
    Ensures planning work is completed before development starts.
    """

    planning_done = any(
        "scope" in work.title.lower() or "planning" in work.title.lower()
        for work in work_items
        if work.status == "completed"
    )

    for work in work_items:
        if work.status == "in_progress" and not planning_done:
            if "implement" in work.title.lower() or "development" in work.title.lower():
                raise EngineStateError(
                    "Development cannot start before planning is completed"
                )


# -------------------------
# Rule 3: Deployment Requires Testing
# -------------------------

def require_testing_before_deployment(work_items: List[WorkItem]) -> None:
    """
    Prevents deployment unless testing has been completed.
    """

    testing_done = any(
        "testing" in work.title.lower() and work.status == "completed"
        for work in work_items
    )

    for work in work_items:
        if "deploy" in work.title.lower() and work.status == "in_progress":
            if not testing_done:
                raise EngineStateError(
                    "Deployment cannot proceed before testing is completed"
                )


# -------------------------
# Rule 4: JPM Cannot Execute Engineering Work
# -------------------------

def enforce_role_boundaries(
    role: str,
    work: WorkItem,
) -> None:
    """
    Ensures Junior Project Managers do not perform engineering tasks.
    """

    if role == "Junior Project Manager":
        forbidden_keywords = [
            "implement",
            "deploy",
            "code",
            "backend",
            "frontend",
            "mobile",
        ]

        if any(word in work.title.lower() for word in forbidden_keywords):
            raise EngineStateError(
                "Junior Project Manager cannot execute engineering work"
            )