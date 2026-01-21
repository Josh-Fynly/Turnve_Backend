"""
Turnve Core Simulation Engine – Exceptions

All permanent, engine-level exception definitions live here.

Design principles:
- Explicit naming
- Stable semantics
- Human-readable intent
- No transient or UI-specific errors
"""


# -------------------------
# Base Exception
# -------------------------

class TurnveEngineError(Exception):
    """
    Base class for all Turnve engine exceptions.
    """
    pass


# -------------------------
# Session Lifecycle Errors
# -------------------------

class SessionNotStartedError(TurnveEngineError):
    """
    Raised when an operation requires an active session,
    but the session has not been started.
    """
    pass


class SessionAlreadyStartedError(TurnveEngineError):
    """
    Raised when attempting to start a session that is already active.
    """
    pass


class SessionAlreadyEndedError(TurnveEngineError):
    """
    Raised when attempting to modify a session that has ended.
    """
    pass


class EngineStateError(TurnveEngineError):
    """
    Raised when the engine enters or detects an invalid state.
    """
    pass


# -------------------------
# Time Errors
# -------------------------

class TimeError(TurnveEngineError):
    """
    Raised for invalid simulation time operations.
    """
    pass


# -------------------------
# Work Errors
# -------------------------

class WorkError(TurnveEngineError):
    """
    Raised when work violates simulation rules.
    """
    pass


class InvalidWorkTransitionError(WorkError):
    """
    Raised when a work item attempts an illegal state transition.
    """
    pass


# -------------------------
# Resource Errors
# -------------------------

class ResourceError(TurnveEngineError):
    """
    Raised when resource constraints are violated.
    """
    pass


class ResourceAllocationError(ResourceError):
    """
    Raised when required resources cannot be allocated.
    """
    pass


# -------------------------
# Decision Errors
# -------------------------

class DecisionError(TurnveEngineError):
    """
    Raised for invalid or illegal decision operations.
    """
    pass


class DecisionExpiredError(DecisionError):
    """
    Raised when attempting to make a decision past its expiry time.
    """
    pass


class DecisionAlreadyMadeError(DecisionError):
    """
    Raised when attempting to remake a decision.
    """
    pass


# -------------------------
# Event Errors
# -------------------------

class EventError(TurnveEngineError):
    """
    Raised when an event fails to execute correctly.
    """
    pass


# -------------------------
# Integrity Errors
# -------------------------

class SimulationIntegrityError(TurnveEngineError):
    """
    Raised when the simulation enters an inconsistent or corrupted state.
    """
    pass