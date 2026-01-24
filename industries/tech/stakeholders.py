"""
Tech Industry Stakeholders

Defines all human and non-human stakeholders involved in
a Tech industry simulation.

Stakeholders:
- Do NOT execute work directly
- Influence priorities, constraints, risk, and events
- Generate pressure, feedback, and accountability
"""

from dataclasses import dataclass
from typing import Optional, List


# -------------------------
# Base Stakeholder
# -------------------------

@dataclass
class Stakeholder:
    """
    Base stakeholder definition.
    """
    id: str
    name: str
    role: str
    influence_level: int  # 1 (low) → 5 (critical)
    expectations: Optional[List[str]] = None


# -------------------------
# Internal Stakeholders
# -------------------------

def founder() -> Stakeholder:
    return Stakeholder(
        id="founder",
        name="Company Founder",
        role="Founder",
        influence_level=5,
        expectations=[
            "Product viability",
            "Speed to market",
            "Cost control",
        ],
    )


def junior_project_manager() -> Stakeholder:
    return Stakeholder(
        id="jpm",
        name="Junior Project Manager",
        role="Junior Project Manager",
        influence_level=3,
        expectations=[
            "Clear requirements",
            "On-time delivery",
            "Minimal rework",
        ],
    )


def engineering_team() -> Stakeholder:
    return Stakeholder(
        id="engineering",
        name="Engineering Team",
        role="Engineers",
        influence_level=4,
        expectations=[
            "Clear scope",
            "Stable requirements",
            "Adequate resources",
        ],
    )


def product_designer() -> Stakeholder:
    return Stakeholder(
        id="designer",
        name="Product Designer",
        role="Designer",
        influence_level=3,
        expectations=[
            "User-centered design",
            "Design consistency",
        ],
    )


# -------------------------
# External Stakeholders
# -------------------------

def client_or_users() -> Stakeholder:
    return Stakeholder(
        id="users",
        name="End Users / Client",
        role="Customer",
        influence_level=5,
        expectations=[
            "Reliability",
            "Ease of use",
            "Security",
        ],
    )


def regulator() -> Stakeholder:
    return Stakeholder(
        id="regulator",
        name="Regulatory Authority",
        role="Regulator",
        influence_level=4,
        expectations=[
            "Compliance",
            "Data protection",
            "Financial regulations",
        ],
    )


def investor() -> Stakeholder:
    return Stakeholder(
        id="investor",
        name="Investor",
        role="Investor",
        influence_level=4,
        expectations=[
            "Growth metrics",
            "Risk management",
            "Scalability",
        ],
    )


# -------------------------
# Factory
# -------------------------

def default_tech_stakeholders() -> List[Stakeholder]:
    """
    Returns the default stakeholder set for a Tech simulation.
    """
    return [
        founder(),
        junior_project_manager(),
        engineering_team(),
        product_designer(),
        client_or_users(),
        regulator(),
        investor(),
    ]