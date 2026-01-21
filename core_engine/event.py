from dataclasses import dataclass
from typing import Callable, Any
import uuid


class EventError(Exception):
    pass


@dataclass
class Event:
    """
    Represents a state-changing occurrence in the simulation.

    Events are:
    - Triggered by time, decisions, or system conditions
    - Not user submissions
    - Logged as evidence
    """
    id: str
    name: str
    description: str
    trigger_time: int
    handler: Callable[[Any], None]

    def trigger(self, session) -> None:
        """
        Apply the event's effect to the simulation session.
        """
        if session.time.now < self.trigger_time:
            raise EventError("Event triggered before its scheduled time")

        # Apply effect
        self.handler(session)

        # Record evidence
        session.log({
            "type": "event",
            "event_id": self.id,
            "name": self.name,
            "description": self.description,
            "time": session.time.now
        })


class EventFactory:
    """
    Creates events in a controlled, auditable way.
    """

    @staticmethod
    def create(
        name: str,
        description: str,
        trigger_time: int,
        handler: Callable[[Any], None]
    ) -> Event:

        if trigger_time < 0:
            raise EventError("Event trigger time cannot be negative")

        return Event(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            trigger_time=trigger_time,
            handler=handler
        )