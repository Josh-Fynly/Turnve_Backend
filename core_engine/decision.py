from typing import List, Dict, Any, Optional
from datetime import datetime


class DecisionOption:
    """
    Represents a single actionable option within a decision.
    """

    def __init__(
        self,
        option_id: str,
        description: str,
        resource_cost: Optional[Dict[str, int]] = None,
        consequences: Optional[List[Dict[str, Any]]] = None
    ):
        self.option_id = option_id
        self.description = description
        self.resource_cost = resource_cost or {}
        self.consequences = consequences or []


class Decision:
    """
    Represents a decision point within the simulation.
    """

    def __init__(
        self,
        decision_id: str,
        title: str,
        context: str,
        options: List[DecisionOption],
        required_role: Optional[str] = None,
        expires_at: Optional[int] = None
    ):
        self.decision_id = decision_id
        self.title = title
        self.context = context
        self.options = options
        self.required_role = required_role
        self.expires_at = expires_at

        self.made = False
        self.selected_option: Optional[DecisionOption] = None
        self.timestamp: Optional[datetime] = None

    def is_available(self, session_time: int) -> bool:
        """
        Checks whether the decision can still be made.
        """
        if self.made:
            return False
        if self.expires_at is not None and session_time > self.expires_at:
            return False
        return True

    def make(self, option_id: str, session) -> None:
        """
        Executes a decision option and applies its consequences.
        """
        if self.made:
            raise ValueError("Decision has already been made.")

        option = next(
            (opt for opt in self.options if opt.option_id == option_id),
            None
        )

        if not option:
            raise ValueError(f"Invalid decision option: {option_id}")

        # Resource validation
        for resource_name, cost in option.resource_cost.items():
            if session.resources.get(resource_name, 0) < cost:
                raise ValueError(
                    f"Insufficient resource: {resource_name}"
                )

        # Deduct resources
        for resource_name, cost in option.resource_cost.items():
            session.resources[resource_name] -= cost

        # Apply consequences
        for consequence in option.consequences:
            self._apply_consequence(consequence, session)

        self.made = True
        self.selected_option = option
        self.timestamp = datetime.utcnow()

        session.log({
            "type": "decision",
            "decision_id": self.decision_id,
            "option_id": option.option_id,
            "time": session.time
        })

    def _apply_consequence(self, consequence: Dict[str, Any], session) -> None:
        """
        Applies a single consequence to the simulation session.
        """
        action = consequence.get("action")

        if action == "add_event":
            session.events.append(consequence["event"])

        elif action == "add_work":
            session.work_items.append(consequence["work"])

        elif action == "modify_resource":
            name = consequence["resource"]
            delta = consequence.get("delta", 0)
            session.resources[name] = session.resources.get(name, 0) + delta

        elif action == "log":
            session.log(consequence.get("entry", {}))

        else:
            raise ValueError(f"Unknown consequence action: {action}")