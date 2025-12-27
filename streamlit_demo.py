import streamlit as st
from app.services.simulation_engine import (
    load_simulation,
    apply_action,
    generate_score,
    generate_coach_summary,
)

SIMULATION_ID = "technology_product_associate"

st.set_page_config(
    page_title="Turnve Demo",
    layout="centered"
)

st.title("Turnve Career Simulation")
st.write("Work on real projects. Learn by doing.")

# Initialize session
if "scenario" not in st.session_state:
    st.session_state.scenario = load_simulation(SIMULATION_ID)
    st.session_state.state = st.session_state.scenario["initial_state"].copy()
    st.session_state.completed = False

scenario = st.session_state.scenario
state = st.session_state.state

# Project brief
st.subheader("Project Brief")
st.write(scenario["context"]["summary"])

# Task
if not st.session_state.completed:
    st.subheader("Your Task")

    for action_id, action in scenario["actions"].items():
        st.write(action["prompt"])

        for choice_id, choice in action["choices"].items():
            if st.button(choice["label"]):
                new_state, feedback, _ = apply_action(
                    SIMULATION_ID,
                    state,
                    action_id,
                    choice_id
                )

                st.session_state.state = new_state
                st.session_state.feedback = feedback
                st.session_state.completed = True
                st.rerun()

# Feedback
if st.session_state.completed:
    st.subheader("AI Coach Feedback")
    st.success(st.session_state.feedback)

    score = generate_score(st.session_state.state)
    summary = generate_coach_summary(st.session_state.state, score)

    st.write(summary)
    st.json(score)
