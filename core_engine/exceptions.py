"""
Core Engine Exceptions

These exceptions define failure semantics for the Turnve simulation engine.
They are intentionally framework-agnostic and side-effect free.
"""


class TurnveError(Exception):
    """
    Base class for all Turnve-related errors.
    """
    pass


# =========================
# Simulation Integrity
# =========================

class SimulationHalt(TurnveError):
    """
    Raised when the simulation must stop immediately
    to prevent invalid or unrecoverable state.
    """
    pass


class InvalidStateError(TurnveError):
    """
    Raised when session state becomes logically inconsistent.
    """
    pass


# =========================
# Decision & Work Errors
# =========================

class DecisionError(TurnveError):
    """
    Raised when a decision is invalid or cannot be applied.
    """
    pass


class UnauthorizedDecisionError(DecisionError):
    """
    Raised when a role attempts an action it is not permitted to perform.
    """
    pass


class WorkConflictError(TurnveError):
    """
    Raised when work items conflict in timing, dependency, or ownership.
    """
    pass


class ResourceAllocationError(TurnveError):
    """
    Raised when resources cannot be assigned or reallocated safely.
    """
    pass


# =========================
# Rules & Configuration
# =========================

class RuleViolationError(TurnveError):
    """
    Raised when a rule is violated during evaluation or execution.
    """
    pass


class InvalidConfigurationError(TurnveError):
    """
    Raised when industry or engine configuration is invalid.
    """
    pass