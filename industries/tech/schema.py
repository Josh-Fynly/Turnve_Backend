"""
Tech Industry Schema

Defines roles, work categories, and project types
for the Tech industry vertical.
"""

from typing import Set, Dict, List


INDUSTRY_NAME = "tech"


# ---- Roles ----

ROLES: Set[str] = {
    "Junior Project Manager",
    "Software Engineer",
    "Mobile Engineer",
    "Backend Engineer",
    "Frontend Engineer",
    "DevOps Engineer",
    "Security Engineer",
    "Designer",
}


# ---- Work Categories ----

WORK_CATEGORIES: Set[str] = {
    "product_planning",
    "project_management",
    "ui_ux",
    "frontend_development",
    "backend_development",
    "mobile_development",
    "database_design",
    "security_compliance",
    "testing_qa",
    "deployment",
    "monitoring",
    "documentation",
}


# ---- Role → Allowed Work Mapping ----

ROLE_CAPABILITIES: Dict[str, Set[str]] = {
    "Junior Project Manager": {
        "product_planning",
        "project_management",
        "documentation",
    },
    "Designer": {
        "ui_ux",
    },
    "Frontend Engineer": {
        "frontend_development",
        "testing_qa",
    },
    "Backend Engineer": {
        "backend_development",
        "database_design",
        "testing_qa",
    },
    "Mobile Engineer": {
        "mobile_development",
        "testing_qa",
    },
    "DevOps Engineer": {
        "deployment",
        "monitoring",
    },
    "Security Engineer": {
        "security_compliance",
    },
}


# ---- Canonical Project Types ----

PROJECT_TEMPLATES: List[str] = [
    "Build a mobile payments app",
    "Build a SaaS web platform",
    "Build an API service",
    "Migrate legacy system",
    "Scale an existing product",
]