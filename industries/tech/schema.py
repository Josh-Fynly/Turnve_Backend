"""
Tech Industry Schema

Defines roles, work categories, capabilities, and
canonical project templates for Tech simulations.
"""

from typing import Dict, Set, List

INDUSTRY_NAME = "tech"

# =====================================================
# Roles (parallel, first-class)
# =====================================================

TECH_ROLES: Dict[str, Dict[str, str]] = {
    "software_engineer": {
        "label": "Software Engineer",
        "description": "Builds, tests, and deploys software systems.",
    },
    "backend_engineer": {
        "label": "Backend Engineer",
        "description": "Implements server-side logic, APIs, and databases.",
    },
    "frontend_engineer": {
        "label": "Frontend Engineer",
        "description": "Builds user-facing interfaces and client logic.",
    },
    "mobile_engineer": {
        "label": "Mobile Engineer",
        "description": "Develops mobile applications for Android/iOS.",
    },
    "devops_engineer": {
        "label": "DevOps Engineer",
        "description": "Handles deployment, CI/CD, and infrastructure.",
    },
    "security_engineer": {
        "label": "Security Engineer",
        "description": "Ensures application security and compliance.",
    },
    "data_analyst": {
        "label": "Data Analyst",
        "description": "Analyzes data to generate insights and reports.",
    },
    "product_manager": {
        "label": "Product Manager",
        "description": "Defines product vision, roadmap, and priorities.",
    },
    "marketing": {
        "label": "Marketing Specialist",
        "description": "Drives product awareness, growth, and adoption.",
    },
    "ui_ux": {
        "label": "UI/UX Designer",
        "description": "Designs user interfaces and experiences.",
    },
    "operations": {
        "label": "Operations / Product Analyst",
        "description": "Ensures operational efficiency and delivery quality.",
    },
    "junior_project_manager": {
        "label": "Junior Project Manager",
        "description": "Coordinates work, reviews progress, and governs phases.",
    },
}

# =====================================================
# Work Categories (normalized → phase-aware)
# =====================================================

WORK_CATEGORIES: Dict[str, str] = {
    "discovery": "Problem understanding and requirements definition",
    "planning": "Work canvas, milestones, risks, and coordination",
    "architecture": "System and solution design",
    "frontend_development": "Client-side implementation",
    "backend_development": "Server-side implementation",
    "mobile_development": "Mobile application development",
    "database_design": "Data modeling and persistence",
    "security_compliance": "Security reviews and controls",
    "testing_qa": "Verification and quality assurance",
    "deployment": "Release and production deployment",
    "monitoring": "System health and observability",
    "documentation": "Technical and non-technical documentation",
    "delivery": "Stabilization and post-release support",
    "governance": "Reviews, approvals, and oversight",
}

# =====================================================
# Role → Capability Mapping
# (Used by rules, not enforcement)
# =====================================================

ROLE_CAPABILITIES: Dict[str, Set[str]] = {
    "junior_project_manager": {
        "planning",
        "governance",
        "documentation",
    },
    "product_manager": {
        "discovery",
        "planning",
        "documentation",
    },
    "marketing": {
        "discovery",
        "documentation",
    },
    "ui_ux": {
        "architecture",
        "frontend_development",
    },
    "frontend_engineer": {
        "frontend_development",
        "testing_qa",
    },
    "backend_engineer": {
        "backend_development",
        "database_design",
        "testing_qa",
    },
    "mobile_engineer": {
        "mobile_development",
        "testing_qa",
    },
    "software_engineer": {
        "frontend_development",
        "backend_development",
        "testing_qa",
    },
    "devops_engineer": {
        "deployment",
        "monitoring",
    },
    "security_engineer": {
        "security_compliance",
    },
    "data_analyst": {
        "discovery",
        "documentation",
    },
    "operations": {
        "monitoring",
        "delivery",
    },
}

# =====================================================
# Canonical Project Templates (simulation seeds)
# =====================================================

PROJECT_TEMPLATES: List[str] = [
    "Build a mobile payments app",
    "Build a SaaS web platform",
    "Build an API service",
    "Migrate a legacy system",
    "Scale an existing product",
]