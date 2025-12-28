import streamlit as st
from datetime import datetime
from io import BytesIO

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Turnve – Career Simulation Demo",
    layout="wide"
)

# -----------------------------
# DATA DEFINITIONS
# -----------------------------

INDUSTRIES = {
    "Technology & ICT": {
        "freemium": True,
        "roles": {
            "Product Associate": {
                "project": {
                    "title": "Product Feature Launch Simulation",
                    "tasks": [
                        "Analyze user feedback and feature request",
                        "Define success metrics",
                        "Draft a product requirement summary",
                        "Align with stakeholders"
                    ]
                }
            },
            "Software Project Coordinator": {
                "project": {
                    "title": "Sprint Coordination & Delivery Simulation",
                    "tasks": [
                        "Review sprint backlog",
                        "Identify delivery risks",
                        "Coordinate with engineering team",
                        "Prepare delivery status update"
                    ]
                }
            },
            "Technical Program Assistant": {
                "project": {
                    "title": "Cross-Team Program Tracking Simulation",
                    "tasks": [
                        "Track milestones across teams",
                        "Resolve dependency conflicts",
                        "Prepare executive progress report"
                    ]
                }
            },
            "QA & Delivery Analyst": {
                "project": {
                    "title": "Release Quality Assurance Simulation",
                    "tasks": [
                        "Review test cases",
                        "Identify release blockers",
                        "Approve or delay product release"
                    ]
                }
            }
        }
    },
    "Energy & Utilities": {
        "freemium": True,
        "roles": {
            "Energy Data Analyst": {
                "project": {
                    "title": "Energy Consumption Analysis Simulation",
                    "tasks": [
                        "Analyze consumption data",
                        "Identify inefficiencies",
                        "Propose optimization strategy"
                    ]
                }
            },
            "Power Systems Technician": {
                "project": {
                    "title": "Grid Stability Monitoring Simulation",
                    "tasks": [
                        "Assess system load",
                        "Detect fault risks",
                        "Recommend maintenance actions"
                    ]
                }
            },
            "Renewable Energy Project Assistant": {
                "project": {
                    "title": "Solar Deployment Planning Simulation",
                    "tasks": [
                        "Review site feasibility",
                        "Estimate deployment timeline",
                        "Prepare stakeholder update"
                    ]
                }
            },
            "Petroleum Engineer": {
                "project": {
                    "title": "Oil Field Production Optimization Simulation",
                    "tasks": [
                        "Analyze well performance data",
                        "Identify production bottlenecks",
                        "Recommend optimization techniques",
                        "Prepare technical report"
                    ]
                }
            },
            "Operations Analyst": {
                "project": {
                    "title": "Operational Efficiency Improvement Simulation",
                    "tasks": [
                        "Audit operational workflow",
                        "Identify cost leakages",
                        "Recommend efficiency improvements"
                    ]
                }
            }
        }
    }
}

LEARNING_RESOURCES = {
    "Product Associate": [
        ("Intro to Product Management", "https://www.youtube.com/watch?v=7zLXaJt0b9k")
    ],
    "Petroleum Engineer": [
        ("Intro to Petroleum Engineering", "https://www.youtube.com/watch?v=ZzjM1R5jR1k")
    ]
}

# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = "industry"

if "industry" not in st.session_state:
    st.session_state.industry = None

if "role" not in st.session_state:
    st.session_state.role = None

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []

# -----------------------------
# UI HELPERS
# -----------------------------

def reset_simulation():
    st.session_state.step = "industry"
    st.session_state.industry = None
    st.session_state.role = None
    st.session_state.completed_tasks = []

def generate_portfolio():
    buffer = BytesIO()
    content = f"""
TURNVE PROJECT PORTFOLIO

Industry: {st.session_state.industry}
Role: {st.session_state.role}

Project Completed:
- {current_project['title']}

Tasks:
""" + "\n".join(f"- {t}" for t in current_project["tasks"])

    buffer.write(content.encode("utf-8"))
    buffer.seek(0)
    return buffer

# -----------------------------
# APP FLOW
# -----------------------------

st.title("Turnve – Career Simulation Platform")
st.caption("Train. Simulate. Build proof of experience.")

# -------- INDUSTRY SELECTION --------
if st.session_state.step == "industry":
    st.subheader("Select Industry")

    cols = st.columns(2)
    industry_list = list(INDUSTRIES.keys())

    for idx, industry in enumerate(industry_list):
        with cols[idx % 2]:
            if st.button(industry, use_container_width=True):
                st.session_state.industry = industry
                st.session_state.step = "role"

# -------- ROLE SELECTION --------
elif st.session_state.step == "role":
    st.subheader(f"Industry: {st.session_state.industry}")
    st.markdown("### Select Role")

    roles = INDUSTRIES[st.session_state.industry]["roles"]

    for role in roles:
        if st.button(role, use_container_width=True):
            st.session_state.role = role
            st.session_state.step = "project"

    st.button("Restart Simulation", on_click=reset_simulation)

# -------- PROJECT SIMULATION --------
elif st.session_state.step == "project":
    role_data = INDUSTRIES[st.session_state.industry]["roles"][st.session_state.role]
    current_project = role_data["project"]

    st.subheader(current_project["title"])
    st.markdown("### Project Tasks")

    for task in current_project["tasks"]:
        if task not in st.session_state.completed_tasks:
            if st.button(f"Complete: {task}", key=task):
                st.session_state.completed_tasks.append(task)

    # Learning Assist
    if st.session_state.role in LEARNING_RESOURCES:
        st.markdown("### AI Coach – Learning Support")
        for title, link in LEARNING_RESOURCES[st.session_state.role]:
            st.markdown(f"- [{title}]({link})")

    # Completion
    if len(st.session_state.completed_tasks) == len(current_project["tasks"]):
        st.success("Project Completed Successfully!")
        st.metric("Project Score", "92%")

        pdf = generate_portfolio()
        st.download_button(
            "Download Portfolio (PDF)",
            data=pdf,
            file_name="turnve_portfolio.txt",
            mime="text/plain"
        )

        st.button(
            "Share with Employers",
            on_click=lambda: st.info("Sharable link generated (demo)")
        )

    st.button("Restart Simulation", on_click=reset_simulation)