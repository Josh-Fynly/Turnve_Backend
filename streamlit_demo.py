import streamlit as st
from copy import deepcopy

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="TURNVE – Career Simulation Demo",
    page_icon="🧠",
    layout="centered",
)

st.title("TURNVE – Career Simulation")
st.caption("Learn by doing real work, not watching slides.")

# -------------------------------------------------
# SESSION STATE INITIALIZATION (CRITICAL)
# -------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "simulation_id" not in st.session_state:
    st.session_state.simulation_id = None

if "state" not in st.session_state:
    st.session_state.state = None

if "history" not in st.session_state:
    st.session_state.history = []

if "feedback" not in st.session_state:
    st.session_state.feedback = None

# -------------------------------------------------
# MOCK SCENARIO (LOCAL DEMO SAFE)
# -------------------------------------------------
SCENARIO = {
    "id": "technology_product_associate",
    "title": "Feature Delivery Under Pressure",
    "initial_state": {
        "deadline_days": 14,
        "risk": 0.3,
        "stakeholder_trust": 0.6,
    },
    "actions": {
        "delivery_decision": {
            "prompt": "The engineering team requests more time to ensure quality. What do you do?",
            "choices": {
                "accept_immediately": {
                    "label": "Accept the request immediately",
                    "effects": {"deadline_days": -3, "risk": -0.1, "stakeholder_trust": 0.1},
                    "feedback": "Quality improves, but leadership is concerned about delays."
                },
                "add_engineers": {
                    "label": "Add more engineers to speed delivery",
                    "effects": {"deadline_days": 1, "risk": 0.15, "stakeholder_trust": -0.05},
                    "feedback": "Delivery is faster, but coordination risk increases."
                }
            }
        }
    }
}

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def initialize_simulation():
    st.session_state.simulation_id = SCENARIO["id"]
    st.session_state.state = deepcopy(SCENARIO["initial_state"])
    st.session_state.history = []
    st.session_state.feedback = None
    st.session_state.step = 1


def restart_simulation():
    st.session_state.clear()
    st.experimental_rerun()


def apply_action(action_id, choice_key):
    if st.session_state.state is None:
        st.warning("Simulation not started.")
        return

    action = SCENARIO["actions"][action_id]
    outcome = action["choices"][choice_key]

    new_state = deepcopy(st.session_state.state)
    for key, delta in outcome["effects"].items():
        new_state[key] = round(new_state.get(key, 0) + delta, 2)

    st.session_state.state = new_state
    st.session_state.feedback = outcome["feedback"]
    st.session_state.history.append(
        {"action": action_id, "choice": choice_key}
    )


# -------------------------------------------------
# STEP 0 – DASHBOARD
# -------------------------------------------------
if st.session_state.step == 0:
    st.subheader("Dashboard")

    st.info("This feels like work — not a course.")

    if st.button("▶ Start Solo Simulation"):
        initialize_simulation()

# -------------------------------------------------
# STEP 1 – PROJECT BRIEF
# -------------------------------------------------
elif st.session_state.step == 1:
    st.subheader("📩 Project Brief")

    st.markdown(
        """
        **You’ve been assigned a project by a stakeholder.**

        **Goal:** Deliver a new feature without harming trust or quality  
        **Timeline:** 2 weeks  
        **Context:** Users are waiting, leadership wants speed
        """
    )

    if st.button("Continue"):
        st.session_state.step = 2

# -------------------------------------------------
# STEP 2 – DECISION MAKING
# -------------------------------------------------
elif st.session_state.step == 2:
    action = SCENARIO["actions"]["delivery_decision"]

    st.subheader("🧩 Decision Point")
    st.write(action["prompt"])

    for choice_key, choice in action["choices"].items():
        if st.button(choice["label"], key=choice_key):
            apply_action("delivery_decision", choice_key)

    if st.session_state.feedback:
        st.success(st.session_state.feedback)
        st.session_state.step = 3

# -------------------------------------------------
# STEP 3 – AI COACH FEEDBACK
# -------------------------------------------------
elif st.session_state.step == 3:
    st.subheader("🤖 AI Coach Feedback")

    state = st.session_state.state

    st.write("### Performance Snapshot")
    st.metric("Deadline Days", state["deadline_days"])
    st.metric("Risk Level", state["risk"])
    st.metric("Stakeholder Trust", state["stakeholder_trust"])

    st.info(
        "You balanced trade-offs under pressure. "
        "Strong PMs understand that speed, risk, and trust move together."
    )

    if st.button("Finish Simulation"):
        st.session_state.step = 4

# -------------------------------------------------
# STEP 4 – PORTFOLIO PROOF
# -------------------------------------------------
elif st.session_state.step == 4:
    st.subheader("📁 Portfolio Proof")

    st.success("Simulation Completed!")

    st.markdown(
        """
        **Project:** Feature Delivery Under Pressure  
        **Role:** Product Associate  
        **Skills Validated:**  
        - Decision Making  
        - Risk Awareness  
        - Stakeholder Management
        """
    )

    st.caption("This project can now appear on your portfolio.")

    if st.button("🔁 Restart Simulation"):
        restart_simulation()