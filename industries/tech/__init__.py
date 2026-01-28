
"""
Tech industry integration layer.
"""

from .work_generator import generate_tech_work


def generate_initial_work(session):
    """
    Called once by the engine at session start.
    Registers all possible Tech work into the session.
    """

    work_items = generate_tech_work(session)

    for work in work_items:
        session.register_work(
            work_id=work.id,
            payload={
                "id": work.id,
                "title": work.title,
                "description": work.description,
                "estimated_effort": work.estimated_effort,
                "required_resources": work.required_resources,
                "priority": work.priority,
                "created_at": work.created_at,
                "status": work.status,
            }
        )