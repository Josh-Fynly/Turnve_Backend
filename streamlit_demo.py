import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Turnve – Career Simulation Demo",
    layout="wide",
)

# -----------------------------
# Session state initialization
# -----------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 0

if "industry" not in st.session_state:
    st.session_state.industry = None

if "role" not in st.session_state:
    st.session_state.role = None

if "learning_done" not in st.session_state:
    st.session_state.learning_done = False

if "submission" not in st.session_state:
    st.session_state.submission = None

if "score" not in st.session_state:
    st.session_state.score = None


# -----------------------------
# Helpers
# -----------------------------
def go_to(stage: int):
    st.session_state.stage = stage


# -----------------------------
# UI STAGES
# -----------------------------

# STAGE 0 — Industry Selection
if st.session_state.stage == 0:
    st.title("Select Industry")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Technology & ICT"):
            st.session_state.industry = "Technology & ICT"
            go_to(1)

    with col2:
        st.button("Financial Services 🔒", disabled=True)

    with col3:
        st.button("Retail & E-commerce 🔒", disabled=True)

    with col4:
        st.button("Manufacturing 🔒", disabled=True)

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.button("Real Estate 🔒", disabled=True)

    with col6:
        st.button("Media & Entertainment 🔒", disabled=True)

    with col7:
        st.button("Energy & Utilities 🔒", disabled=True)

    with col8:
        st.button("Healthcare 🔒", disabled=True)


# STAGE 1 — Role Selection
elif st.session_state.stage == 1:
    st.header("Technology & ICT — Select Role")

    roles = [
        "Product Associate",
        "Software Project Coordinator",
        "Technical Program Assistant",
        "QA & Delivery Analyst",
    ]

    for role in roles:
        if st.button(role):
            st.session_state.role = role
            go_to(2)

    st.button("← Back", on_click=lambda: go_to(0))


# STAGE 2 — Role Overview + AI Coach Intro
elif st.session_state.stage == 2:
    st.header(st.session_state.role)

    st.subheader("Role Overview")
    st.write(
        "This role is designed for individuals with little or no prior experience. "
        "You will learn by doing real-world projects under guided supervision."
    )

    st.subheader("AI Coach")
    st.info(
        "I’ll guide you through this project step by step. "
        "If you’re new, I’ll recommend learning resources when needed."
    )

    if st.button("Proceed to Project"):
        go_to(3)

    st.button("← Back", on_click=lambda: go_to(1))


# STAGE 3 — Project Brief
elif st.session_state.stage == 3:
    st.header("New Project Assignment")

    st.markdown(
        """
        **Stakeholder Message**

        > You’ve been assigned a project to support a product feature rollout.
        >
        > **Goal:** Prepare a short execution plan for launch coordination  
        > **Timeline:** 7 days  
        > **Deliverables:** Written plan + risk considerations
        """
    )

    if st.button("Start Working"):
        go_to(4)

    st.button("← Back", on_click=lambda: go_to(2))


# STAGE 4 — Learning Trigger
elif st.session_state.stage == 4:
    st.header("AI Coach Recommendation")

    st.warning(
        "If this is your first time in this role, learning the basics first will help."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Continue Anyway"):
            go_to(5)

    with col2:
        if st.button("Learn First (Recommended)"):
            go_to(4_1)


# STAGE 4.1 — Learning Resources
elif st.session_state.stage == 4_1:
    st.header("Learning Resources")

    st.write("Recommended free resources:")

    st.markdown(
        """
        - 🎥 [YouTube – Product & Project Fundamentals](https://www.youtube.com)
        - 📘 [Coursera – Project Management Basics](https://www.coursera.org)
        - 📗 [Khan Academy – Planning & Execution](https://www.khanacademy.org)
        - 🎓 [Udemy – Entry-Level PM Skills](https://www.udemy.com)
        """
    )

    if st.button("Return to Project"):
        st.session_state.learning_done = True
        go_to(5)


# STAGE 5 — Hands-on Work
elif st.session_state.stage == 5:
    st.header("Work on Your Project")

    st.write("Complete the task below:")

    plan = st.text_area(
        "Describe your execution approach:",
        placeholder="Explain how you would approach this project..."
    )

    if st.button("Submit Work"):
        st.session_state.submission = plan
        st.session_state.score = {
            "Execution": 82,
            "Communication": 76,
            "Problem Solving": 80,
        }
        go_to(6)

    st.button("← Back", on_click=lambda: go_to(3))


# STAGE 6 — AI Coach Feedback
elif st.session_state.stage == 6:
    st.header("AI Coach Feedback")

    st.success("Good effort! Here’s how you performed:")

    for skill, value in st.session_state.score.items():
        st.write(f"**{skill}:** {value}%")

    st.info(
        "Strengths: Clear execution thinking.\n\n"
        "Areas to improve: More risk mitigation detail."
    )

    if st.button("Generate Portfolio"):
        go_to(7)


# STAGE 7 — Portfolio Output
elif st.session_state.stage == 7:
    st.header("Your Turnve Portfolio")

    st.markdown(
        f"""
        **Industry:** {st.session_state.industry}  
        **Role:** {st.session_state.role}  

        **Completed Project:** Product Launch Coordination  
        **Skills Validated:** Execution, Communication, Problem Solving
        """
    )

    st.success("Portfolio ready for employers.")

    st.button("Download Portfolio (PDF)")
    st.button("Share with Employers")

    st.button("Restart Demo", on_click=lambda: go_to(0)