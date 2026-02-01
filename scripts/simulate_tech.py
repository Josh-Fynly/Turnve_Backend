"""
Tech Industry Simulation – Dry Run Harness

This script validates that:
- The simulation engine boots
- A Tech session can be created
- Time advances deterministically
- Decisions and events are recorded
- The session ends cleanly

This is the MVP proof script.
"""

from core_engine.engine import SimulationEngine
from core_engine.exceptions import SimulationHalt


def main():
    print("\n=== TURNVE TECH SIMULATION DRY RUN ===\n")

    # ----------------------------------
    # 1. Boot engine
    # ----------------------------------
    engine = SimulationEngine(industry_name="tech")
    print("[OK] Engine initialized for industry: tech")

    # ----------------------------------
    # 2. Create session
    # ----------------------------------
    session = engine.create_session(role="junior_project_manager")
    print("[OK] Session started")
    print(f"     Role: {session.role}")
    print(f"     Time: {session.current_time}\n")

    # ----------------------------------
    # 3. Run simulation steps
    # ----------------------------------
    MAX_STEPS = 5

    try:
        for step in range(MAX_STEPS):
            print(f"--- STEP {step + 1} ---")
            engine.step(session)

            print(f"Time: {session.current_time}")
            print(f"Decisions: {len(session.decisions)}")
            print(f"Events: {len(session.events)}")
            print(f"Evidence: {len(session.evidence)}\n")

    except SimulationHalt:
        print("[HALT] Simulation halted by engine")

    # ----------------------------------
    # 4. End session
    # ----------------------------------
    engine.end_session(session)
    print("[OK] Session ended")

    # ----------------------------------
    # 5. Final snapshot
    # ----------------------------------
    snapshot = session.snapshot()

    print("\n=== FINAL SNAPSHOT ===")
    print(f"Industry: {snapshot['industry']}")
    print(f"Role: {snapshot['role']}")
    print(f"Time elapsed: {snapshot['current_time']}")
    print(f"Decisions recorded: {len(snapshot['decisions'])}")
    print(f"Events recorded: {len(snapshot['events'])}")
    print(f"Evidence records: {len(snapshot['evidence'])}")
    print("\n=== DRY RUN COMPLETE ===\n")


if __name__ == "__main__":
    main()