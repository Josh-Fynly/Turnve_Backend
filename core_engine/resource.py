from dataclasses import dataclass
from typing import Dict


class ResourceError(Exception):
    pass


@dataclass
class Resource:
    """
    Represents a limited capability in the simulation.

    Examples:
    - Engineer hours
    - Budget
    - Equipment
    - Server capacity
    """
    name: str
    total: int
    available: int

    def allocate(self, amount: int):
        if amount <= 0:
            raise ResourceError("Allocation amount must be positive")

        if amount > self.available:
            raise ResourceError(
                f"Not enough {self.name}. Requested {amount}, available {self.available}"
            )

        self.available -= amount

    def release(self, amount: int):
        if amount <= 0:
            raise ResourceError("Release amount must be positive")

        if self.available + amount > self.total:
            raise ResourceError(
                f"Cannot exceed total {self.name} capacity"
            )

        self.available += amount


class ResourcePool:
    """
    Holds and manages all resources for a simulation session.
    """

    def __init__(self):
        self.resources: Dict[str, Resource] = {}

    def add_resource(self, name: str, total: int):
        if name in self.resources:
            raise ResourceError(f"Resource '{name}' already exists")

        if total <= 0:
            raise ResourceError("Resource total must be positive")

        self.resources[name] = Resource(
            name=name,
            total=total,
            available=total
        )

    def allocate(self, requirements: Dict[str, int]):
        """
        Attempts to allocate multiple resources atomically.
        If one fails, none are consumed.
        """

        # Pre-check
        for name, amount in requirements.items():
            if name not in self.resources:
                raise ResourceError(f"Resource '{name}' not found")

            if amount > self.resources[name].available:
                raise ResourceError(
                    f"Insufficient {name}: required {amount}, available {self.resources[name].available}"
                )

        # Allocation
        for name, amount in requirements.items():
            self.resources[name].allocate(amount)

    def release(self, releases: Dict[str, int]):
        for name, amount in releases.items():
            if name not in self.resources:
                raise ResourceError(f"Resource '{name}' not found")

            self.resources[name].release(amount)

    def snapshot(self) -> Dict[str, int]:
        """
        Returns current availability for reporting & evidence.
        """
        return {
            name: res.available
            for name, res in self.resources.items()
        }