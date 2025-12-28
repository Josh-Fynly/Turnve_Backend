import streamlit as st
from typing import Dict, Any

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Turnve – Career Simulation Demo",
    page_icon="🧠",
    layout="centered",
)

# =========================
# Scenario Definition
# =========================
SCENARIO = {
    "industry": "Technology & ICT",
    "role": "Product Associate",
    "initial_state": {
        "deadline_days": 10,
        "risk": 0.3,
        "stakeholder_trust": 0.6,
    },
    "actions": {
        "scope_change": {
            "label": "How do you handle a late feature request?",
            "choices": {
                "accept": {
                    "label": "Accept the request immediately",
                    "effects": {
                        "deadline_days": -4,
                        "risk": 0.2,
                        "stakeholder_trust": 0.1,
                    },
                    "feedback": "You pleased the stakeholder but increased delivery risk.",
                },
                "negotiate": {
                    "label": "Negotiate scope and timeline",
                    "effects": {
                        "deadline_days": -1,
                        "risk": -0.1,
                        "stakeholder_trust": 0.05,
                    },
                    "feedback": "You balanced delivery pressure with stakeholder alignment.",
                },
            },
        },
        "resource_tradeoff": {
            "label": "How do you reallocate team resources?",
            "choices": {
                "add_engineers": {
                    "label": "Add more engineers to speed delivery",
                    "effects": {
                        "deadline_days": 4,
                        "risk": 0.15,
                        "stakeholder_trust": -0.1,
                    },
                    "feedback": "Delivery improved, but coordination risk increased.",
                },
                "maintain_team": {
                    "label": "Keep the current team size",
                    "effects": {
                        "deadline_days": -2,
                        "risk": -0.05,
                        "stakeholder_trust": 0.05,
                    },
                    "feedback": "Stability improved, but timeline pressure increased.",
                },
            },
        },
    },
}

# =========================
# Helper Functions
# =========================
def initialize_state() -> Dict[str, Any]:
    return SCENARIO["initial_state"].copy()


def apply_action(state: Dict[str, Any], action_id: str, choice: str):
    new_state = state.copy()
    action = SCENARIO["actions"][action_id]
    outcome = action["choices"][choice]

    for key, delta in outcome["effects"].items():
        new_state[key] = round(new_state.get(key, 0) + delta, 2)

    return new_state, outcome["feedback"]


def generate_score(state: Dict[str, Any]) -> Dict[str, float]:
    score = {
        "execution": max(0, min(1, 1 - abs(state["deadline_days"]) / 10)),
        "risk_management": max(0, 1 - state["risk"]),
        "stakeholder_management": state["stakeholder_trust"],
    }
    score["overall"] = round(sum(score.values()) / len(score), 2)
    return score


def generate_coach_summary(score: Dict[str, float]) -> str:
    insights = []

    if score["risk_management"] < 0.4:
        insights.append("Your decisions increased delivery risk.")
    else:
        insights.append("You demonstrated strong risk awareness.")

    if score["stakeholder_management"] > 0.6:
        insights.append("Stakeholder trust was well managed.")
    else:
        insights.append("Stakeholder alignment needs improvement.")

    return (
        f"Overall performance score: {score['overall']}. "
        + " ".join(insights)
    )

# =========================
# Session State
# =========================
if "state" not in st.session_state:
    st.session_state.state = initialize_state()
    st.session_state.step = 1
    st.session_state.feedback = ""

# =========================
# UI
# =========================
st.title("🧠 Turnve Career Simulation")
st.caption("Technology & ICT · Product Associate")

st.markdown("### 📌 Current Project Brief")
st.info(
    "You’ve been assigned to support a product rollout under tight timelines. "
    "Your decisions will affect delivery, risk, and stakeholder trust."
)

# =========================
# Decision Flow
# =========================
if st.session_state.step <= 2:
    action_keys = list(SCENARIO["actions"].keys())
    action_id = action_keys[st.session_state.step - 1]
    action = SCENARIO["actions"][action_id]

    st.markdown(f"### 🧠 Decision {st.session_state.step}")
    choice = st.radio(
        action["label"],
        options=list(action["choices"].keys()),
        format_func=lambda x: action["choices"][x]["label"],
    )

    if st.button("Make Decision"):
        new_state, feedback = apply_action(
            st.session_state.state, action_id, choice
        )
        st.session_state.state = new_state
        st.session_state.feedback = feedback
        st.session_state.step += 1
        st.experimental_rerun()

    if st.session_state.feedback:
        st.success(st.session_state.feedback)

# =========================
# Results & Portfolio
# =========================
else:
    st.divider()
    st.markdown("### 📊 Simulation Results")

    score = generate_score(st.session_state.state)
    st.metric("Overall Score", score["overall"])

    st.markdown("### 🧑‍🏫 AI Coach Feedback")
    st.write(generate_coach_summary(score))

    st.divider()
    st.markdown("### 📁 Portfolio Proof")

    portfolio = {
        "industry": SCENARIO["industry"],
        "role": SCENARIO["role"],
        "final_state": st.session_state.state,
        "score": score,
    }

    st.download_button(
        label="Download Portfolio Proof",
        data=str(portfolio),
        file_name="turnve_portfolio.json",
        mime="application/json",
    )

    if st.button("Restart Simulation"):
        st.session_state.clear()
        st.experimental_rerun()