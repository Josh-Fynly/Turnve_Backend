# industries/tech/schema.py

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class TechRole:
    """
    Roles that exist in the Tech industry.
    """
    name: str
    responsibilities: List[str]


@dataclass(frozen=True)
class TechWorkType:
    """
    Canonical types of work that appear in tech organizations.
    """
    key: str
    description: str
    base_effort: int
    required_resources: Dict[str, int]


@dataclass(frozen=True)
class TechResourceDefinition:
    """
    Resources commonly constrained in tech teams.
    """
    name: str
    unit: str
    description: str


# -------------------------
# Roles
# -------------------------

TECH_ROLES = {
    "junior_engineer": TechRole(
        name="Junior Software Engineer",
        responsibilities=[
            "Implement features",
            "Fix bugs",
            "Write tests",
        ],
    ),
    "product_manager": TechRole(
        name="Product Manager",
        responsibilities=[
            "Define requirements",
            "Prioritize work",
            "Manage stakeholders",
        ],
    ),
    "tech_lead": TechRole(
        name="Tech Lead",
        responsibilities=[
            "Architect systems",
            "Review code",
            "Manage technical risk",
        ],
    ),
}

# -------------------------
# Resources
# -------------------------

TECH_RESOURCES = {
    "engineer_hours": TechResourceDefinition(
        name="engineer_hours",
        unit="hours",
        description="Available engineering time",
    ),
    "budget": TechResourceDefinition(
        name="budget",
        unit="currency",
        description="Allocated project budget",
    ),
    "infra_capacity": TechResourceDefinition(
        name="infra_capacity",
        unit="units",
        description="Server / infrastructure capacity",
    ),
}

# -------------------------
# Work Types
# -------------------------

TECH_WORK_TYPES = {
    "feature": TechWorkType(
        key="feature",
        description="Develop a new product feature",
        base_effort=8,
        required_resources={
            "engineer_hours": 8,
        },
    ),
    "bugfix": TechWorkType(
        key="bugfix",
        description="Fix a production bug",
        base_effort=4,
        required_resources={
            "engineer_hours": 4,
        },
    ),
    "refactor": TechWorkType(
        key="refactor",
        description="Improve existing code structure",
        base_effort=6,
        required_resources={
            "engineer_hours": 6,
        },
    ),
    "infra_change": TechWorkType(
        key="infra_change",
        description="Modify infrastructure or deployment",
        base_effort=10,
        required_resources={
            "engineer_hours": 6,
            "infra_capacity": 1,
            "budget": 500,
        },
    ),
}