"""
Turnve Tech Simulation – Dry Run Harness

Purpose:
- Validate engine ↔ session ↔ industry integration
- Observe deterministic simulation progression
- Catch silent stalls, duplication, or runaway generation

This file MUST NOT mutate core logic.
It is read-only orchestration + logging.
"""

from core_engine.engine import SimulationEngine
from core_engine.exceptions import SimulationHalt


def print_step_header(step: int, time: int):
    print("\n" + "=" * 60)
    print(f"STEP {step} | SIMULATION TIME: {time}")
    print("=" * 60)


def print_work(session):
    print("\nWork Items:")
    if not session.work_items:
        print("  (none)")
        return

    for wid, work in session.work_items.items():
        status = work.get("status", "unknown")
        print(f"  - {work.get('title', wid)} [{status}]")


def print_decisions(session, last_time):
    decisions = [
        d for d in session.decisions if d.get("time") == last_time
    ]

    print("\nDecisions:")
    if not decisions:
        print("  (none)")
        return

    for d in decisions:
        print(f"  - {d.get('title')}")


def print_events(session, last_time):
    events = [
        e for e in session.events if e.get("time") == last_time
    ]

    print("\nEvents:")
    if not events:
        print("  (none)")
        return

    for e in events:
        print(f"  - {e.get('event_type')}: {e.get('description')}")


def run_simulation(max_steps: int = 15):
    print("\n🚀 Starting Turnve Tech Simulation Dry Run")

    engine = SimulationEngine("tech")
    session = engine.create_session(role="developer")

    try:
        for step in range(1, max_steps + 1):
            print_step_header(step, session.current_time)

            engine.step(session)

            print_work(session)
            print_decisions(session, session.current_time - 1)
            print_events(session, session.current_time - 1)

            if not session.is_active():
                print("\n🛑 Session ended by engine.")
                break

    except SimulationHalt as e:
        print("\n❗ Simulation halted:", str(e))

    print("\n✅ Dry run completed.")
    print(f"Final simulation time: {session.current_time}")
    print(f"Total work items: {len(session.work_items)}")
    print(f"Total decisions: {len(session.decisions)}")
    print(f"Total events: {len(session.events)}")
    print(f"Total evidence records: {len(session.evidence)}")


if __name__ == "__main__":
    run_simulation()
