"""
Turnve Core Simulation Engine – Exceptions

This module defines all canonical exceptions used by the core simulation engine.

Design principles:
- Engine-level only (no UI, no AI, no industry logic)
- Predictable hierarchy
- Stable contracts (do not casually rename)
"""


class SimulationError(Exception):
    """
    Base class for all simulation-related errors.
    Every exception raised by the core engine must inherit from this.
    """
    pass


# Session lifecycle errors

class SessionError(SimulationError):
    """Errors related to the lifecycle or validity of a simulation session."""
    pass


class SessionNotStartedError(SessionError):
    """Raised when an action is attempted before the session starts."""
    pass


class SessionAlreadyEndedError(SessionError):
    """Raised when an action is attempted after the session has ended."""
    pass


# Time progression errors

class TimeError(SimulationError):
    """Errors related to simulation time handling."""
    pass


class TimeRegressionError(TimeError):
    """Raised when time is forced to move backward."""
    pass


class TimeOverflowError(TimeError):
    """Raised when simulation time exceeds allowed bounds."""
    pass


# Work and task errors

class WorkError(SimulationError):
    """Errors related to work units, tasks, or deliverables."""
    pass


class WorkNotFoundError(WorkError):
    """Raised when referenced work cannot be found."""
    pass


class WorkAlreadyCompletedError(WorkError):
    """Raised when an action targets work that is already completed."""
    pass


class InvalidWorkStateError(WorkError):
    """Raised when work enters an illegal or impossible state."""
    pass


# Decision-making errors

class DecisionError(SimulationError):
    """Errors related to decisions made within the simulation."""
    pass


class InvalidDecisionError(DecisionError):
    """Raised when a decision violates simulation rules."""
    pass


class DecisionContextMissingError(DecisionError):
    """Raised when required information for a decision is missing."""
    pass


# Resource management errors

class ResourceError(SimulationError):
    """Errors related to resource allocation or consumption."""
    pass


class InsufficientResourceError(ResourceError):
    """Raised when required resources are unavailable."""
    pass


class ResourceLockedError(ResourceError):
    """Raised when a resource is locked by another actor or process."""
    pass


class ResourceOveruseError(ResourceError):
    """Raised when resource usage exceeds allowed limits."""
    pass


# Stakeholder interaction errors

class StakeholderError(SimulationError):
    """Errors related to stakeholder behavior or availability."""
    pass


class StakeholderUnavailableError(StakeholderError):
    """Raised when a stakeholder cannot act or respond."""
    pass


class StakeholderConflictError(StakeholderError):
    """Raised when stakeholder interests collide without resolution."""
    pass


# Event system errors

class EventError(SimulationError):
    """Errors related to simulation events."""
    pass


class EventTriggerError(EventError):
    """Raised when an event cannot be triggered."""
    pass


class EventResolutionError(EventError):
    """Raised when an event fails to resolve correctly."""
    pass


# Evidence and audit trail errors

class EvidenceError(SimulationError):
    """Errors related to logging or retrieving simulation evidence."""
    pass


class EvidenceIntegrityError(EvidenceError):
    """Raised when evidence is missing, corrupted, or inconsistent."""
    pass


# Engine state and configuration errors

class EngineStateError(SimulationError):
    """Errors related to invalid global engine state."""
    pass


class EngineConfigurationError(EngineStateError):
    """Raised when engine configuration is missing or invalid."""
    pass