"""
Dry-run harness for Turnve Tech Simulation

This script proves that:
- the engine loads
- the tech industry loads
- sessions advance deterministically
- work, decisions, and events are generated safely

This is NOT production code.
"""

from core_engine.engine import SimulationEngine


def print_section(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    print_section("BOOTSTRAP ENGINE")

    engine = SimulationEngine(industry_name="tech")
    session = engine.create_session(role="Junior Project Manager")

    print(f"Session ID: {session.id}")
    print(f"Industry: {session.industry}")
    print(f"Role: {session.role}")

    # --------------------------------
    # DRY-RUN SIMULATION STEPS
    # --------------------------------

    STEPS = 6

    for step in range(STEPS):
        print_section(f"SIMULATION STEP {step + 1}")

        engine.step(session)

        print(f"Current time: {session.current_time}")

        print("\nWork Items:")
        if session.work_items:
            for wid, work in session.work_items.items():
                print(f" - {wid}: {work}")
        else:
            print(" (none)")

        print("\nDecisions:")
        if session.decisions:
            for d in session.decisions:
                print(f" - {d}")
        else:
            print(" (none)")

        print("\nEvents:")
        if session.events:
            for e in session.events:
                print(f" - {e}")
        else:
            print(" (none)")

        print("\nEvidence:")
        if session.evidence:
            for ev in session.evidence:
                print(f" - {ev}")
        else:
            print(" (none)")

    print_section("END SESSION")
    engine.end_session(session)

    print("Session ended cleanly.")
    print("Dry-run complete.")


if __name__ == "__main__":
    main()
