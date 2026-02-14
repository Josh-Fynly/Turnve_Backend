"""
Phase 1 — Foundations of B2B SaaS CRM Analytics

Dataset-powered analytics tasks.
"""

from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict


# -------------------------
# Task Model
# -------------------------

@dataclass
class PhaseTask:
    id: str
    title: str
    description: str


# -------------------------
# Helpers
# -------------------------

def _get_dataset(session) -> Dict:
    dataset = session.flags.get("dataset")

    if not dataset:
        raise RuntimeError("CRM dataset not loaded in session")

    return dataset


# -------------------------
# Analytics Functions
# -------------------------

def compute_customer_summary(session) -> Dict:
    dataset = _get_dataset(session)

    companies = dataset["companies"]
    subscriptions = dataset["subscriptions"]

    total_companies = len(companies)

    active = sum(1 for s in subscriptions if s["active"])
    churned = total_companies - active

    churn_rate = churned / total_companies if total_companies else 0

    return {
        "total_companies": total_companies,
        "active_companies": active,
        "churned_companies": churned,
        "churn_rate": round(churn_rate, 3),
    }


def compute_revenue_by_plan(session) -> Dict:
    dataset = _get_dataset(session)

    revenue = defaultdict(float)

    for sub in dataset["subscriptions"]:
        if sub["active"]:
            revenue[sub["plan"]] += sub["monthly_price"]

    return dict(revenue)


def compute_usage_trends(session) -> Dict:
    dataset = _get_dataset(session)

    monthly_usage = defaultdict(int)

    for act in dataset["activity"]:
        monthly_usage[act["month"]] += act["feature_usage"]

    return dict(sorted(monthly_usage.items()))


# -------------------------
# Tasks
# -------------------------

def get_tasks() -> List[PhaseTask]:
    return [
        PhaseTask(
            id="p1_customer_summary",
            title="Analyze customer base",
            description=(
                "Compute total companies, active subscriptions, "
                "and churn rate from the CRM dataset."
            ),
        ),
        PhaseTask(
            id="p1_revenue_analysis",
            title="Analyze revenue by plan",
            description=(
                "Calculate total monthly revenue grouped by subscription plan."
            ),
        ),
        PhaseTask(
            id="p1_usage_trends",
            title="Analyze product usage trends",
            description=(
                "Aggregate feature usage per month to identify trends."
            ),
        ),
    ]


# -------------------------
# Evaluation
# -------------------------

def evaluate_task(session, task_id: str) -> Dict:
    """
    Executes analytics task and records completion.
    """

    completed = session.flags.setdefault(
        "phase1_completed_tasks",
        set(),
    )

    if task_id == "p1_customer_summary":
        result = compute_customer_summary(session)

    elif task_id == "p1_revenue_analysis":
        result = compute_revenue_by_plan(session)

    elif task_id == "p1_usage_trends":
        result = compute_usage_trends(session)

    else:
        raise ValueError(f"Unknown Phase 1 task: {task_id}")

    completed.add(task_id)

    return result


# -------------------------
# Completion Check
# -------------------------

def is_complete(session) -> bool:
    completed = session.flags.get("phase1_completed_tasks", set())

    return len(completed) >= len(get_tasks())


# -------------------------
# Portfolio Artifact
# -------------------------

def build_portfolio_artifact(session) -> Dict:
    """
    Generates a structured analytics report.
    """

    return {
        "title": "B2B SaaS CRM Analytics Report",
        "customer_summary": compute_customer_summary(session),
        "revenue_analysis": compute_revenue_by_plan(session),
        "usage_trends": compute_usage_trends(session),
        "skills_demonstrated": [
            "Data aggregation",
            "KPI analysis",
            "Business insight generation",
        ],
    }