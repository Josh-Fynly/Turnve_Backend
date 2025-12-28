import streamlit as st
from datetime import datetime
from fpdf import FPDF

st.set_page_config(
    page_title="Turnve – Career Simulation",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
for key in ["step", "industry", "role", "task_index", "score"]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state.step is None:
    st.session_state.step = "industry"

# -----------------------------
# DATA MODEL
# -----------------------------

SIMULATION = {
    "Technology & ICT": {
        "freemium": True,
        "roles": {
            "Product Associate": {
                "project": {
                    "title": "Product Feature Launch Simulation",
                    "tasks": [
                        {
                            "question": "Which user problem should be prioritized?",
                            "options": ["UI color", "App crashes", "New animations"],
                            "answer": "App crashes"
                        },
                        {
                            "question": "Which KPI best measures success?",
                            "options": ["Daily active users", "Bug count reduction", "Logo clicks"],
                            "answer": "Bug count reduction"
                        },
                        {
                            "question": "Which PRD section defines scope?",
                            "options": ["Goals", "Out of Scope", "Risks"],
                            "answer": "Goals"
                        },
                        {
                            "question": "Stakeholder wants speed over quality. What do you do?",
                            "options": ["Accept", "Negotiate phased rollout", "Reject request"],
                            "answer": "Negotiate phased rollout"
                        }
                    ]
                },
                "resources": [
                    ("PM Basics (YouTube)", "https://www.youtube.com/watch?v=ravLfnYuqmA")
                ]
            },
            "Software Engineer": {
                "project": {
                    "title": "Implement Dark Mode Feature",
                    "tasks": [
                        {
                            "question": "What enables dark mode toggling?",
                            "options": ["CSS variables", "Hardcoded colors", "Inline styles"],
                            "answer": "CSS variables"
                        },
                        {
                            "question": "Which React hook handles theme state?",
                            "options": ["useEffect", "useTheme", "useState"],
                            "answer": "useState"
                        },
                        {
                            "question": "What persists user theme choice?",
                            "options": ["Session memory", "LocalStorage", "Redux only"],
                            "answer": "LocalStorage"
                        }
                    ]
                },
                "resources": [
                    ("React Dark Mode Tutorial", "https://www.youtube.com/watch?v=F9UC9DY-vIU"),
                    ("CSS Variables Guide", "https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties")
                ]
            }
        }
    },
    "Energy & Utilities": {
        "freemium": True,
        "roles": {
            "Petroleum Engineer": {
                "project": {
                    "title": "Oil Field Production Optimization Simulation",
                    "tasks": [
                        {
                            "question": "Production decline suggests?",
                            "options": ["Reservoir pressure loss", "UI issue", "Network lag"],
                            "answer": "Reservoir pressure loss"
                        },
                        {
                            "question": "Main bottleneck?",
                            "options": ["Pump efficiency", "Marketing", "Weather"],
                            "answer": "Pump efficiency"
                        },
                        {
                            "question": "Best optimization method?",
                            "options": ["Gas lift", "UI redesign", "Database indexing"],
                            "answer": "Gas lift"
                        }
                    ]
                },
                "resources": [
                    ("Petroleum Engineering Intro", "https://www.youtube.com/watch?v=I7CQWgZInq4")
                ]
            }
        }
    }
}

# -----------------------------
# HELPERS
# -----------------------------
def reset():
    st.session_state.step = "industry"
    st.session_state.industry = None
    st.session_state.role = None
    st.session_state.task_index = 0
    st.session_state.score = 0

def generate_pdf(industry, role, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Turnve – Proof of Experience", ln=True)
    pdf.cell(200, 10, f"Industry: {industry}", ln=True)
    pdf.cell(200, 10, f"Role: {role}", ln=True)
    pdf.cell(200, 10, f"Score: {score}%", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# -----------------------------
# UI FLOW
# -----------------------------

st.title("Turnve – Career Simulation")

if st.session_state.step == "industry":
    st.subheader("Select Industry")
    for industry in SIMULATION:
        if st.button(industry):
            st.session_state.industry = industry
            st.session_state.step = "role"

elif st.session_state.step == "role":
    st.subheader(st.session_state.industry)
    for role in SIMULATION[st.session_state.industry]["roles"]:
        if st.button(role):
            st.session_state.role = role
            st.session_state.step = "project"
            st.session_state.task_index = 0
            st.session_state.score = 0
    st.button("Back", on_click=reset)

elif st.session_state.step == "project":
    role_data = SIMULATION[st.session_state.industry]["roles"][st.session_state.role]
    project = role_data["project"]
    task = project["tasks"][st.session_state.task_index]

    with st.sidebar:
        st.header("AI Coach")
        for title, link in role_data["resources"]:
            st.markdown(f"[{title}]({link})")

    st.subheader(project["title"])
    st.write(task["question"])

    choice = st.radio("Select answer:", task["options"])

    if st.button("Submit"):
        if choice == task["answer"]:
            st.session_state.score += int(100 / len(project["tasks"]))
            st.session_state.task_index += 1
            if st.session_state.task_index == len(project["tasks"]):
                st.success("Project Completed!")
                pdf = generate_pdf(
                    st.session_state.industry,
                    st.session_state.role,
                    st.session_state.score
                )
                st.download_button("Download Portfolio PDF", pdf, "turnve_portfolio.pdf")
                st.button("Restart", on_click=reset)
            else:
                st.info("Correct. Proceeding...")
        else:
            st.error("Incorrect. Review learning materials and retry.")