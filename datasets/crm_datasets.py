"""
Synthetic B2B SaaS CRM Dataset Generator

Generates realistic CRM data for analytics simulation.

Entities:
- companies
- users
- subscriptions
- activity logs

Designed for:
- SQL analysis
- cohort analysis
- churn modeling
- KPI dashboards
"""

import random
from dataclasses import dataclass, asdict
from typing import List, Dict


# -------------------------
# Data Models
# -------------------------

@dataclass
class Company:
    company_id: int
    name: str
    industry: str
    employees: int
    region: str


@dataclass
class Subscription:
    company_id: int
    plan: str
    monthly_price: float
    start_month: int
    active: bool


@dataclass
class Activity:
    company_id: int
    month: int
    logins: int
    feature_usage: int


# -------------------------
# Constants
# -------------------------

INDUSTRIES = [
    "Fintech",
    "Healthcare",
    "E-commerce",
    "Education",
    "Logistics",
]

REGIONS = [
    "North America",
    "Europe",
    "Africa",
    "Asia",
]

PLANS = {
    "Starter": 49,
    "Growth": 129,
    "Enterprise": 399,
}


# -------------------------
# Dataset Generator
# -------------------------

class CRMDataset:
    """
    Generates synthetic SaaS CRM data.
    """

    def __init__(self, seed: int = 42):
        self.random = random.Random(seed)

    # -------------------------
    # Companies
    # -------------------------

    def generate_companies(self, n: int = 100) -> List[Company]:
        companies = []

        for i in range(1, n + 1):
            company = Company(
                company_id=i,
                name=f"Company_{i}",
                industry=self.random.choice(INDUSTRIES),
                employees=self.random.randint(5, 500),
                region=self.random.choice(REGIONS),
            )
            companies.append(company)

        return companies

    # -------------------------
    # Subscriptions
    # -------------------------

    def generate_subscriptions(
        self, companies: List[Company]
    ) -> List[Subscription]:

        subscriptions = []

        for company in companies:
            plan = self.random.choices(
                population=list(PLANS.keys()),
                weights=[0.5, 0.35, 0.15],
            )[0]

            churn_probability = 0.1 if plan == "Enterprise" else 0.25

            active = self.random.random() > churn_probability

            subscription = Subscription(
                company_id=company.company_id,
                plan=plan,
                monthly_price=PLANS[plan],
                start_month=self.random.randint(1, 6),
                active=active,
            )

            subscriptions.append(subscription)

        return subscriptions

    # -------------------------
    # Activity Logs
    # -------------------------

    def generate_activity(
        self,
        subscriptions: List[Subscription],
        months: int = 12,
    ) -> List[Activity]:

        activity_logs = []

        for sub in subscriptions:
            base_usage = {
                "Starter": 50,
                "Growth": 150,
                "Enterprise": 400,
            }[sub.plan]

            for month in range(1, months + 1):

                if not sub.active and month > 6:
                    continue  # churned users stop activity

                activity = Activity(
                    company_id=sub.company_id,
                    month=month,
                    logins=int(
                        self.random.gauss(base_usage * 0.6, 10)
                    ),
                    feature_usage=int(
                        self.random.gauss(base_usage, 25)
                    ),
                )

                activity_logs.append(activity)

        return activity_logs

    # -------------------------
    # Full Dataset
    # -------------------------

    def generate_full_dataset(self, n_companies: int = 100) -> Dict:

        companies = self.generate_companies(n_companies)
        subscriptions = self.generate_subscriptions(companies)
        activity = self.generate_activity(subscriptions)

        return {
            "companies": [asdict(c) for c in companies],
            "subscriptions": [asdict(s) for s in subscriptions],
            "activity": [asdict(a) for a in activity],
        }


# -------------------------
# Convenience Function
# -------------------------

def load_crm_dataset(seed: int = 42, n_companies: int = 100) -> Dict:
    """
    Public entry point used by simulation.
    """

    generator = CRMDataset(seed=seed)
    return generator.generate_full_dataset(n_companies)
