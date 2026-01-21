from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


class DecisionError(Exception):
    """Permanent decision system error."""
    pass


@dataclass(frozen=True)
class DecisionOption:
    """
    A single actionable option within a decision.
    """
    option_id: str
    description: str
    resource_cost: Dict[str, int]
    consequences: List[Dict[str, Any]]


class Decision:
    """
    Represents a decision point within the simulation.

    Decisions:
    - Consume time
    - Consume resources
    - Trigger consequences
    - Are logged as evidence
    """

    def __init__(
        self,
        decision_id: str,
        title: str,
        context: str,
        options: List[DecisionOption],
        required_role: Optional[str] = None,
        expires_at: Optional[int] = None,
        time_cost: int = 1
    ):
        self.decision_id = decision_id
        self.title = title
        self.context = context
        self.options = options
        self.required_role = required_role
        self.expires_at = expires_at
        self.time_cost = time_cost

        self.made = False
        self.selected_option: Optional[DecisionOption] = None
        self.made_at: Optional[int] = None
        self.logged_at: Optional[datetime] = None

    def is_available(self, session_time: int) -> bool:
        if self.made:
            return False
        if self.expires_at is not None and session_time > self.expires_at:
            return False
        return True

    def make(self, option_id: str, session) -> None:
        if self.made:
            raise DecisionError("Decision already made")

        if not self.is_available(session.time.now):
            raise DecisionError("Decision expired")

        option = next(
            (opt for opt in self.options if opt.option_id == option_id),
            None
        )

        if not option:
            raise DecisionError(f"Invalid decision option: {option_id}")

        # Allocate resources via ResourcePool
        if option.resource_cost:
            session.resources.allocate(option.resource_cost)

        # Advance time
        session.time.advance(
            self.time_cost,
            reason=f"Decision taken: {self.title}"
        )

        # Apply consequences (controlled)
        for consequence in option.consequences:
            self._apply_consequence(consequence, session)

        self.made = True
        self.selected_option = option
        self.made_at = session.time.now
        self.logged_at = datetime.utcnow()

        session.log({
            "type": "decision",
            "decision_id": self.decision_id,
            "option_id": option.option_id,
            "time": self.made_at,
            "title": self.title
        })

    def _apply_consequence(self, consequence: Dict[str, Any], session) -> None:
        action = consequence.get("action")

        if action == "add_event":
            session.events.append(consequence["event"])

        elif action == "add_work":
            session.work_items.append(consequence["work"])

        elif action == "log":
            session.log(consequence.get("entry", {}))

        else:
            raise DecisionError(
                f"Unsupported consequence action: {action}"
            )