import json
from pathlib import Path
from typing import Dict, Any, Tuple

BASE_PATH = Path(__file__).parent.parent / "data" / "scenarios"


def load_simulation(simulation_id: str) -> Dict[str, Any]:
    """
    Load a simulation scenario by ID.
    """
    file_path = BASE_PATH / f"{simulation_id}.json"

    if not file_path.exists():
        raise ValueError("Simulation scenario not found")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def initialize_state(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initialize simulation state from scenario.
    """
    return scenario.get("initial_state", {}).copy()


def apply_action(
    simulation_id: str,
    state: Dict[str, Any],
    action_id: str,
    choice: str,
) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
    """
    Stateless action application.
    Frontend sends state, backend returns updated state.
    """
    scenario = load_simulation(simulation_id)

    actions = scenario.get("actions", {})
    if action_id not in actions:
        raise ValueError("Invalid action")

    action = actions[action_id]
    choices = action.get("choices", {})
    if choice not in choices:
        raise ValueError("Invalid choice")

    outcome = choices[choice]

    new_state = state.copy()
    for key, delta in outcome.get("effects", {}).items():
        new_state[key] = round(new_state.get(key, 0) + delta, 2)

    feedback = outcome.get("feedback", "")

    log = {
        "action_id": action_id,
        "choice": choice,
        "effects": outcome.get("effects", {}),
    }

    return new_state, feedback, log


def generate_score(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a simple performance score.
    """
    score = {
        "execution": max(0, min(1, 1 - abs(state.get("deadline_days", 0)) / 10)),
        "risk_management": max(0, 1 - state.get("risk", 0)),
        "stakeholder_management": state.get("stakeholder_trust", 0),
    }

    score["overall"] = round(sum(score.values()) / len(score), 2)
    return score


def generate_coach_summary(state: Dict[str, Any], score: Dict[str, Any]) -> str:
    """
    Generate human-readable coaching feedback.
    """
    insights = []

    risk = state.get("risk", 0)
    trust = state.get("stakeholder_trust", 0)

    if risk > 0.6:
        insights.append("Your decisions significantly increased delivery risk.")
    elif risk < 0.3:
        insights.append("You proactively reduced risk, a strong junior-to-mid PM signal.")

    if trust < 0.4:
        insights.append("Stakeholder trust declined, which may slow future execution.")
    elif trust > 0.7:
        insights.append("You strengthened stakeholder confidence under pressure.")

    return (
        f"Overall performance score: {score.get('overall', 0)}. "
        + " ".join(insights)
    )