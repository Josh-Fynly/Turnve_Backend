"""
Tech Industry – Work Generator

Responsible for generating initial and project-based work
for a tech simulation session.

This module contains NO engine logic.
"""

from typing import List, Dict


def generate_initial_work(session) -> List[Dict]:
    """
    Generates the baseline work items for a Tech simulation.

    These are high-level, role-aware work units that can later
    expand into full projects (e.g. mobile payments app).
    """

    role = session.role.lower()

    work_items: List[Dict] = []

    # -------------------------
    # Universal onboarding work
    # -------------------------

    work_items.append({
        "id": "tech_onboarding",
        "title": "Project Onboarding & Context Setup",
        "category": "foundation",
        "description": (
            "Understand the product goal, constraints, stakeholders, "
            "and success criteria."
        ),
        "required_role": None,
        "completed": False,
    })

    # -------------------------
    # Junior Project Manager
    # -------------------------

    if role in {"junior_project_manager", "project_manager"}:
        work_items.extend([
            {
                "id": "define_scope",
                "title": "Define Project Scope",
                "category": "planning",
                "description": (
                    "Translate business goals into a clear project scope, "
                    "deliverables, and exclusions."
                ),
                "required_role": "junior_project_manager",
                "completed": False,
            },
            {
                "id": "create_work_breakdown",
                "title": "Create Work Breakdown Structure",
                "category": "planning",
                "description": (
                    "Break the project into manageable components, phases, "
                    "and responsibilities."
                ),
                "required_role": "junior_project_manager",
                "completed": False,
            },
        ])

    # -------------------------
    # Software Engineering Track
    # -------------------------

    if role in {"software_engineer", "fullstack_engineer"}:
        work_items.extend([
            {
                "id": "system_design",
                "title": "System Architecture Design",
                "category": "engineering",
                "description": (
                    "Design the system architecture, services, data flow, "
                    "and integration boundaries."
                ),
                "required_role": "software_engineer",
                "completed": False,
            },
            {
                "id": "repo_setup",
                "title": "Repository Setup & Version Control",
                "category": "engineering",
                "description": (
                    "Create or connect a source code repository, define "
                    "branching strategy, and initialize the codebase."
                ),
                "required_role": "software_engineer",
                "completed": False,
                "capabilities": ["connect_repo"],
            },
        ])

    # -------------------------
    # Deployment & Delivery
    # -------------------------

    work_items.append({
        "id": "deployment_strategy",
        "title": "Deployment & Release Strategy",
        "category": "delivery",
        "description": (
            "Plan deployment environments, CI/CD pipeline, and release "
            "process."
        ),
        "required_role": None,
        "completed": False,
    })

    return work_items