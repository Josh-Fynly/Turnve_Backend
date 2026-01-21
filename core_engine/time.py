from dataclasses import dataclass
from typing import List


class TimeError(Exception):
    """Raised when an invalid time operation occurs."""
    pass


@dataclass(frozen=True)
class TimeTick:
    """
    Immutable record of time advancement.
    This is evidence: why time moved and by how much.
    """
    from_time: int
    to_time: int
    reason: str


class SimulationClock:
    """
    Authoritative time controller for a Turnve simulation.

    Principles:
    - Time always moves forward
    - Time moves because of work, delays, or events
    - Every movement is recorded as evidence
    """

    def __init__(self, start_time: int = 0):
        if start_time < 0:
            raise TimeError("Simulation time cannot start below zero")

        self._current_time: int = start_time
        self._history: List[TimeTick] = []

    @property
    def now(self) -> int:
        """Current simulation time (abstract units)."""
        return self._current_time

    @property
    def history(self) -> List[TimeTick]:
        """Immutable copy of time advancement history."""
        return list(self._history)

    def advance(self, delta: int, reason: str) -> None:
        """
        Advance simulation time.

        delta: number of time units (e.g., hours, days, sprints)
        reason: human-readable explanation (required)
        """
        if delta <= 0:
            raise TimeError("Time advance must be a positive integer")

        if not reason or not reason.strip():
            raise TimeError("Time advance requires a meaningful reason")

        old_time = self._current_time
        new_time = old_time + delta

        tick = TimeTick(
            from_time=old_time,
            to_time=new_time,
            reason=reason.strip()
        )

        self._current_time = new_time
        self._history.append(tick)