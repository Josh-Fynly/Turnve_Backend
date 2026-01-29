"""
Turnve Tech Simulation Dry-Run Harness

This script runs a deterministic simulation loop
and prints state transitions for manual validation.

NO engine mutation.
NO test framework.
NO deployment dependency.
"""

from core_engine.engine import SimulationEngine
from core_engine.exceptions import SimulationHalt


def print_divider():
    print("\n" + "-" * 80 + "\n")


def summarize_session(session):
    print(f"⏱  Time: {session.current_time}")
    print(f"📦 Work items ({len(session.work_items)}):")

    for wid, work in session.work_items.items():
        title = work.get("title", "UNKNOWN")
        completed = work.get("completed", False)
        status = "✅" if completed else "⏳"
        print(f"   {status} {title}")

    print(f"\n🧠 Decisions taken ({len(session.decisions)}):")
    for d in session.decisions[-3:]:
        print(f"   • {d.get('title')} @ t={d.get('time')}")

    print(f"\n⚡ Events fired ({len(session.events)}):")
    for e in session.events[-3:]:
        print(f"   • {e.get('description')} @ t={e.get('time')}")

    print(f"\n🧾 Evidence count: {len(session.evidence)}")


def main():
    engine = SimulationEngine("tech")
    session = engine.create_session(role="developer")

    MAX_STEPS = 12

    print_divider()
    print("🚀 Starting Tech Simulation Dry-Run")
    print_divider()

    try:
        for step in range(MAX_STEPS):
            print(f"▶️  STEP {step + 1}")

            engine.step(session)
            summarize_session(session)

            print_divider()

            # Optional early exit if no new work appears
            if not session.work_items:
                print("⚠️  No work remaining. Ending simulation.")
                break

    except SimulationHalt as halt:
        print(f"🛑 Simulation halted: {halt}")

    finally:
        engine.end_session(session)
        print("✅ Simulation ended cleanly.")


if __name__ == "__main__":
    main()