"""
Turnve Core Simulation Engine – Engine

The Engine is the orchestrator of a simulation run.
It is industry-agnostic and owns no domain logic.

Responsibilities:
- Create and manage sessions
- Load industry modules
- Generate work
- Advance time
- Apply rules
- Trigger events
- Record evidence

Design guarantees:
- Deterministic
- Auditable
- Extensible
- No AI, no UI, no industry coupling
"""

from typing import Any, Dict, Optional
import importlib

from .session import Session
from .exceptions import EngineStateError


class Engine:
    """
    The Engine coordinates a simulation session with an industry module.
    """

    def __init__(self, industry_key: str):
        """
        :param industry_key: e.g. "tech"
        """
        self.industry_key = industry_key
        self.industry = self._load_industry(industry_key)

        self.session: Optional[Session] = None
        self._initialized: bool = False

    # -------------------------
    # Industry loading
    # -------------------------

    def _load_industry(self, industry_key: str):
        """
        Dynamically loads an industry package.

        Expected structure:
        industries.<industry_key>.schema
        industries.<industry_key>.work_generator
        industries.<industry_key>.rules
        industries.<industry_key>.events
        """
        try:
            base = f"industries.{industry_key}"

            return {
                "schema": importlib.import_module(f"{base}.schema"),
                "work_generator": importlib.import_module(f"{base}.work_generator"),
                "rules": importlib.import_module(f"{base}.rules"),
                "events": importlib.import_module(f"{base}.events"),
            }
        except ModuleNotFoundError as exc:
            raise EngineStateError(
                f"Industry '{industry_key}' is not properly configured"
            ) from exc

    # -------------------------
    # Session lifecycle
    # -------------------------

    def create_session(
        self,
        industry: str,
        role: str,
        actors: Optional[list[str]] = None,
    ) -> Session:
        if self.session:
            raise EngineStateError("Engine already has an active session")

        self.session = Session(
            industry=industry,
            role=role,
            actors=actors,
        )
        return self.session

    def start(self) -> None:
        if not self.session:
            raise EngineStateError("No session to start")

        self.session.start()
        self._initialize_industry()
        self._initialized = True

    def end(self) -> None:
        if not self.session or not self.session.is_active():
            raise EngineStateError("No active session to end")

        self.session.end()

    # -------------------------
    # Initialization
    # -------------------------

    def _initialize_industry(self) -> None:
        """
        Industry bootstrapping:
        - Validate schema
        - Generate initial work
        """
        schema = self.industry["schema"]
        generator = self.industry["work_generator"]

        # Optional schema validation hook
        if hasattr(schema, "validate"):
            schema.validate()

        # Initial work generation
        if hasattr(generator, "generate_initial_work"):
            work_items = generator.generate_initial_work(self.session)

            for work in work_items:
                self.session.register_work(work["id"], work)

    # -------------------------
    # Simulation step
    # -------------------------

    def tick(self, time_delta: int = 1) -> None:
        """
        Advances the simulation by one step.
        """
        if not self.session or not self.session.is_active():
            raise EngineStateError("Session is not active")

        if not self._initialized:
            raise EngineStateError("Engine not initialized")

        # Advance time
        self.session.advance_time(time_delta)

        # Apply industry rules
        rules = self.industry["rules"]
        if hasattr(rules, "apply"):
            rules.apply(self.session)

        # Trigger events
        events = self.industry["events"]
        if hasattr(events, "check_and_trigger"):
            triggered = events.check_and_trigger(self.session)

            for event in triggered or []:
                self.session.trigger_event(event)

    # -------------------------
    # Snapshot
    # -------------------------

    def snapshot(self) -> Dict[str, Any]:
        if not self.session:
            raise EngineStateError("No session to snapshot")

        return self.session.snapshot()