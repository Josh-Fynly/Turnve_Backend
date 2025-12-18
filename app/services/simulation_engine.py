import json
from pathlib import Path
from typing import Dict, Any, Tuple


BASE_PATH = Path(__file__).parent.parent / "data" / "scenarios"
SIMULATION_PATH = Path(__file__).parent.parent / "data" / "scenarios"


def load_scenario(industry: str, role: str) -> Dict[str, Any]:
    filename = f"{industry}_{role}.json"
    path = BASE_PATH / filename

    if not path.exists():
        raise ValueError("Scenario not found")

    with open(path, "r") as f:
        scenario = json.load(f)

    return scenario


def load_simulation(simulation_id: str) -> Dict[str, Any]:
    """
    Load a simulation by unique simulation ID.
    Used for demo, API exposure, and future expansion.
    """
    file_path = SIMULATION_PATH / f"{simulation_id}.json"

    if not file_path.exists():
        raise ValueError("Simulation scenario not found")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_action(
    state: Dict[str, Any],
    action_id: str,
    choice: str,
) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
    new_state = state.copy()

    # Existing demo logic preserved
    scenario = load_scenario("financial", "product_manager")
    action = scenario["actions"][action_id]
    outcome = action["choices"][choice]

    for key, delta in outcome["effects"].items():
        new_state[key] = round(new_state.get(key, 0) + delta, 2)

    feedback = outcome["feedback"]

    return new_state, feedback, {
        "action_id": action_id,
        "choice": choice,
        "effects": outcome["effects"],
    }


def generate_score(state: Dict[str, Any]) -> Dict[str, Any]:
    score = {
        "execution": max(0, min(1, 1 - abs(state["deadline_days"]) / 10)),
        "risk_management": max(0, 1 - state["risk"]),
        "stakeholder_management": state["stakeholder_trust"],
    }
    score["overall"] = round(sum(score.values()) / len(score), 2)
    return score


def generate_coach_summary(state: Dict[str, Any], score: Dict[str, Any]) -> str:
    risk = state.get("risk", 0)
    trust = state.get("stakeholder_trust", 0)
    deadline = state.get("deadline_days", 0)
    overall = score.get("overall", 0)

    insights = []

    # Risk analysis
    if risk > 0.6:
        insights.append(
            "Your decisions significantly increased delivery risk. In real-world PM roles, this often leads to firefighting later."
        )
    elif risk < 0.3:
        insights.append(
            "You proactively reduced risk, which is a strong signal of senior-level product judgment."
        )

    # Stakeholder trust analysis
    if trust < 0.4:
        insights.append(
            "Stakeholder trust declined. This can limit influence and slow execution in future phases."
        )
    elif trust > 0.7:
        insights.append(
            "You strengthened stakeholder confidence — a critical advantage when navigating uncertainty."
        )

    # Deadline pressure
    if deadline < 0:
        insights.append(
            "You traded timeline certainty for quality. This is often the right call in regulated environments."
        )
    elif deadline > 10:
        insights.append(
            "You preserved schedule flexibility, giving the team room to adapt."
        )

    # Final synthesis
    summary = (
        f"Overall performance score: {overall}. "
        + " ".join(insights)
        + " Focus on balancing speed, trust, and risk as pressure increases."
    )

    return summary