"""
Tech Work Generator

Responsible for generating realistic work items
for Tech industry projects.
"""

from typing import List
from core_engine.work import WorkItem, WorkFactory


def generate_tech_project_work(
    project_name: str,
    start_time: int,
    requires_repository: bool = True,
) -> List[WorkItem]:
    """
    Generates baseline work for a realistic tech project.
    """

    work_items: List[WorkItem] = []

    # ---- Project Planning (JPM) ----
    work_items.append(
        WorkFactory.create(
            title="Define project scope and milestones",
            description=f"Initial planning for {project_name}",
            estimated_effort=3,
            required_resources={"pm_hours": 3},
            priority=0,
            created_at=start_time,
        )
    )

    # ---- Work Canvas ----
    work_items.append(
        WorkFactory.create(
            title="Create Work Canvas",
            description="Define objectives, constraints, risks, and acceptance criteria",
            estimated_effort=2,
            required_resources={"pm_hours": 2},
            priority=0,
            created_at=start_time,
        )
    )

    # ---- Repository Setup ----
    if requires_repository:
        work_items.append(
            WorkFactory.create(
                title="Connect or create GitHub repository",
                description="Initialize repository and access control",
                estimated_effort=1,
                required_resources={"engineering_hours": 1},
                priority=1,
                created_at=start_time,
            )
        )

    # ---- Architecture ----
    work_items.append(
        WorkFactory.create(
            title="Design system architecture",
            description="Define frontend, backend, mobile, and data flow",
            estimated_effort=4,
            required_resources={"engineering_hours": 4},
            priority=1,
            created_at=start_time,
        )
    )

    # ---- Core Development ----
    work_items.extend([
        WorkFactory.create(
            title="Implement backend services",
            description="APIs, authentication, core business logic",
            estimated_effort=6,
            required_resources={"engineering_hours": 6},
            priority=2,
            created_at=start_time,
        ),
        WorkFactory.create(
            title="Implement mobile application",
            description="Mobile client implementation",
            estimated_effort=6,
            required_resources={"engineering_hours": 6},
            priority=2,
            created_at=start_time,
        ),
    ])

    # ---- Security ----
    work_items.append(
        WorkFactory.create(
            title="Security and compliance review",
            description="Encryption, secrets, compliance checks",
            estimated_effort=4,
            required_resources={"security_hours": 4},
            priority=1,
            created_at=start_time,
        )
    )

    # ---- Testing ----
    work_items.append(
        WorkFactory.create(
            title="Testing and QA",
            description="Functional, integration, and edge-case testing",
            estimated_effort=4,
            required_resources={"engineering_hours": 4},
            priority=2,
            created_at=start_time,
        )
    )

    # ---- Deployment ----
    work_items.append(
        WorkFactory.create(
            title="Deploy to production",
            description="CI/CD setup and release",
            estimated_effort=3,
            required_resources={"devops_hours": 3},
            priority=1,
            created_at=start_time,
        )
    )

    return work_items