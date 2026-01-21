from dataclasses import dataclass
from typing import List


class TimeError(Exception):
    pass


@dataclass(frozen=True)
class TimeTick:
    """
    Immutable record of time advancement.
    Used for replay, audit, and evidence.
    """
    from_time: int
    to_time: int
    reason: str


class SimulationClock:
    """
    Authoritative time controller for a simulation session.

    Rules:
    - Time only moves forward
    - Time advances due to actions or system events
    - Time advancement is recorded, not guessed
    """

    def __init__(self, start_time: int = 0):
        if start_time < 0:
            raise TimeError("Simulation time cannot start below zero")

        self._current_time: int = start_time
        self._history: List[TimeTick] = []

    @property
    def now(self) -> int:
        return self._current_time

    @property
    def history(self) -> List[TimeTick]:
        return list(self._history)

    def advance(self, delta: int, reason: str) -> None:
        """
        Advance simulation time.

        delta: number of time units to move forward
        reason: human-readable explanation (e.g. 'code review delay')
        """
        if delta <= 0:
            raise TimeError("Time advance must be a positive integer")

        if not reason:
            raise TimeError("Time advance requires a reason")

        old_time = self._current_time
        new_time = old_time + delta

        tick = TimeTick(
            from_time=old_time,
            to_time=new_time,
            reason=reason
        )

        self._current_time = new_time
        self._history.append(tick)