import streamlit as st
from datetime import datetime
from fpdf import FPDF

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Turnve – Career Simulation Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# UTILITIES
# =========================================================
def sanitize_for_pdf(text: str) -> str:
    """
    Remove unicode characters (emojis, smart quotes, etc.)
    that classic FPDF cannot encode.
    """
    if not text:
        return ""
    return text.encode("latin-1", errors="ignore").decode("latin-1")


# =========================================================
# INDUSTRIES & ACCESS CONFIG
# =========================================================
ALL_INDUSTRIES = [
    "Technology & ICT", "Financial Services", "Retail & E-commerce", "Manufacturing",
    "Real Estate", "Media & Entertainment", "Energy & Utilities", "Healthcare"
]

INDUSTRY_STATUS = {
    "Technology & ICT": {"locked": False},
    "Energy & Utilities": {"locked": False},
    "Financial Services": {"locked": True},
    "Retail & E-commerce": {"locked": True},
    "Manufacturing": {"locked": True},
    "Real Estate": {"locked": True},
    "Media & Entertainment": {"locked": True},
    "Healthcare": {"locked": True},
}

# =========================================================
# CORE SIMULATION DATA
# =========================================================
ACTIVE_INDUSTRY_DATA = {
    "Technology & ICT": {
        "roles": {
            "Product Associate": {
                "description": "Work on feature discovery, requirements, and stakeholder alignment.",
                "project": {
                    "title": "Product Feature Launch Simulation",
                    "goal": "Launch a Dark Mode feature for a web application.",
                    "tasks": [
                        "Analyze user feedback and feature request",
                        "Define success metrics (KPIs)",
                        "Craft a product requirement summary",
                        "Align with stakeholders"
                    ]
                }
            },
            "Software Engineer": {
                "description": "Build, test, and ship production-ready features.",
                "project": {
                    "title": "Dark Mode Feature Implementation",
                    "goal": "Implement Dark Mode with persistence and accessibility.",
                    "tasks": [
                        "Design theme architecture using CSS variables",
                        "Implement theme toggle logic",
                        "Persist theme selection",
                        "Validate accessibility and contrast"
                    ]
                }
            }
        }
    },
    "Energy & Utilities": {
        "roles": {
            "Petroleum Engineer": {
                "description": "Optimize oil field performance using engineering data.",
                "project": {
                    "title": "Oil Field Production Optimization Simulation",
                    "goal": "Improve output while maintaining safety and efficiency.",
                    "tasks": [
                        "Analyze well performance data",
                        "Identify production bottlenecks",
                        "Recommend optimization techniques",
                        "Prepare technical report"
                    ]
                }
            }
        }
    }
}

# =========================================================
# AI COACH RESOURCES
# =========================================================
LEARNING_RESOURCES = {
    "Product Associate": [
        ("Product Management Basics (YouTube)", "https://www.youtube.com/watch?v=3KaqaF8YciU"),
        ("Intro to Product Strategy", "https://www.coursera.org/learn/product-management")
    ],
    "Software Engineer": [
        ("CSS Variables & Theming", "https://www.youtube.com/watch?v=5f2f8d0J1Yw"),
        ("Dark Mode Best Practices", "https://web.dev/prefers-color-scheme/")
    ],
    "Petroleum Engineer": [
        ("Intro to Petroleum Engineering", "https://www.youtube.com/watch?v=Zypkj33Zv9E"),
        ("Oil Field Optimization Overview", "https://www.udemy.com/course/oil-and-gas-industry-overview/")
    ]
}

# =========================================================
# SESSION STATE
# =========================================================
if "step" not in st.session_state:
    st.session_state.step = "industry"
if "industry" not in st.session_state:
    st.session_state.industry = None
if "role" not in st.session_state:
    st.session_state.role = None
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []
if "submission" not in st.session_state:
    st.session_state.submission = ""

# =========================================================
# HELPERS
# =========================================================
def reset_simulation():
    st.session_state.step = "industry"
    st.session_state.industry = None
    st.session_state.role = None
    st.session_state.completed_tasks = []
    st.session_state.submission = ""


def generate_pdf_portfolio(industry, role, project, tasks, submission_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Turnve – Proof of Experience", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Industry: {sanitize_for_pdf(industry)}", ln=True)
    pdf.cell(0, 8, f"Role: {sanitize_for_pdf(role)}", ln=True)
    pdf.cell(0, 8, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, sanitize_for_pdf(project["title"]), ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, sanitize_for_pdf(project["goal"]))
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Tasks Completed:", ln=True)

    pdf.set_font("Arial", size=11)
    for task in tasks:
        pdf.cell(0, 7, f"- {sanitize_for_pdf(task)}", ln=True)

    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "User Submission Summary:", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, sanitize_for_pdf(submission_text))

    return pdf.output(dest="S").encode("latin-1")

# =========================================================
# UI
# =========================================================
st.title("Turnve – Career Simulation Platform")
st.caption("Train. Simulate. Prove real experience.")

# =========================================================
# STEP 1: INDUSTRY
# =========================================================
if st.session_state.step == "industry":
    st.subheader("Select Industry")

    rows = [ALL_INDUSTRIES[i:i + 4] for i in range(0, len(ALL_INDUSTRIES), 4)]

    for row in rows:
        cols = st.columns(4)
        for idx, industry in enumerate(row):
            with cols[idx]:
                box = st.container(border=True)
                box.markdown(f"**{industry}**")

                if INDUSTRY_STATUS[industry]["locked"]:
                    box.caption("🔒 Locked")
                    box.button("Premium Required", disabled=True)
                else:
                    if box.button("Enter Simulation"):
                        st.session_state.industry = industry
                        st.session_state.step = "role"
                        st.rerun()

# =========================================================
# STEP 2: ROLE
# =========================================================
elif st.session_state.step == "role":
    st.subheader(f"{st.session_state.industry} Roles")
    st.button("← Back", on_click=reset_simulation)

    roles = ACTIVE_INDUSTRY_DATA[st.session_state.industry]["roles"]
    for role, info in roles.items():
        with st.container(border=True):
            st.markdown(f"### {role}")
            st.write(info["description"])
            if st.button("Start Simulation", key=role):
                st.session_state.role = role
                st.session_state.step = "project"
                st.rerun()

# =========================================================
# STEP 3: PROJECT
# =========================================================
elif st.session_state.step == "project":
    role_data = ACTIVE_INDUSTRY_DATA[st.session_state.industry]["roles"][st.session_state.role]
    project = role_data["project"]

    with st.sidebar:
        st.header("AI Coach")
        st.write(f"Role: **{st.session_state.role}**")
        st.markdown("### Learning Resources")
        for title, link in LEARNING_RESOURCES.get(st.session_state.role, []):
            st.markdown(f"- [{title}]({link})")

    st.subheader(project["title"])
    st.write(project["goal"])

    for task in project["tasks"]:
        if task not in st.session_state.completed_tasks:
            if st.button(f"Complete: {task}"):
                st.session_state.completed_tasks.append(task)
                st.rerun()
        else:
            st.success(task)

    if len(st.session_state.completed_tasks) == len(project["tasks"]):
        st.divider()
        st.success("Project completed. Submit your explanation.")

        st.session_state.submission = st.text_area(
            "Explain how you completed the project",
            height=220
        )

        if st.button("Generate Portfolio"):
            pdf = generate_pdf_portfolio(
                st.session_state.industry,
                st.session_state.role,
                project,
                st.session_state.completed_tasks,
                st.session_state.submission
            )

            st.download_button(
                "Download Portfolio (PDF)",
                data=pdf,
                file_name="Turnve_Portfolio.pdf",
                mime="application/pdf"
            )

            st.button("Restart Simulation",on_click=reset_simulation)