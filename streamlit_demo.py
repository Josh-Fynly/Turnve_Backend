import streamlit as st
from datetime import datetime
from fpdf import FPDF

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Turnve – Career Simulation",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================
defaults = {
    "step": "industry",
    "industry": None,
    "role": None,
    "project": None,
    "assignment_done": False,
    "score": None,
    "tvc": 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================
# INDUSTRIES & ACCESS
# =====================================================
INDUSTRIES = [
    "Technology & ICT", "Financial Services", "Retail & E-commerce", "Manufacturing",
    "Real Estate", "Media & Entertainment", "Energy & Utilities", "Healthcare"
]

INDUSTRY_ACCESS = {
    "Technology & ICT": {"freemium": True},
    "Energy & Utilities": {"freemium": True},
    "Financial Services": {"freemium": False},
    "Retail & E-commerce": {"freemium": False},
    "Manufacturing": {"freemium": False},
    "Real Estate": {"freemium": False},
    "Media & Entertainment": {"freemium": False},
    "Healthcare": {"freemium": False},
}

PAID_COST_TVC = 6  # $3 equivalent

# =====================================================
# CORE SIMULATION DATA
# =====================================================
SIMULATION = {
    "Technology & ICT": {
        "roles": {
            "Software Engineer": {
                "project": "Dark Mode Feature Implementation",
                "assignment": {
                    "title": "Implement Dark Mode",
                    "instruction": (
                        "Explain how you would implement Dark Mode in a web app.\n"
                        "Mention CSS variables, theme toggling, and persistence."
                    ),
                    "keywords": ["css", "theme", "toggle", "dark", "local storage"]
                }
            },
            "Product Associate": {
                "project": "Product Feature Launch",
                "assignment": {
                    "title": "Define Feature Success",
                    "instruction": (
                        "Describe how you would analyze feedback and define KPIs "
                        "for launching a Dark Mode feature."
                    ),
                    "keywords": ["kpi", "feedback", "adoption", "retention"]
                }
            }
        }
    },
    "Energy & Utilities": {
        "roles": {
            "Petroleum Engineer": {
                "project": "Oil Field Optimization",
                "assignment": {
                    "title": "Analyze Well Performance Data",
                    "instruction": (
                        "Explain how you would analyze well pressure, flow rate, "
                        "and decline trends to identify bottlenecks."
                    ),
                    "keywords": ["pressure", "flow", "decline", "bottleneck"]
                }
            },
            "Energy Data Analyst": {
                "project": "Consumption Optimization",
                "assignment": {
                    "title": "Identify Energy Inefficiencies",
                    "instruction": (
                        "Describe how consumption data can reveal inefficiencies "
                        "and reduce operational costs."
                    ),
                    "keywords": ["consumption", "trend", "inefficiency", "optimization"]
                }
            }
        }
    }
}

# =====================================================
# AI COACH – SCORING
# =====================================================
def score_submission(text, keywords):
    score = sum(20 for k in keywords if k in text.lower())
    return min(score, 100)

# =====================================================
# PDF PORTFOLIO
# =====================================================
def generate_portfolio():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Turnve – Proof of Experience", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Industry: {st.session_state.industry}", ln=True)
    pdf.cell(0, 8, f"Role: {st.session_state.role}", ln=True)
    pdf.cell(0, 8, f"Score: {st.session_state.score}%", ln=True)
    pdf.cell(0, 8, f"Date: {datetime.now().date()}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(
        0, 8,
        "This document certifies that the holder has completed "
        "a simulation-based project assessed by Turnve AI Coach."
    )

    return pdf.output(dest="S").encode("latin-1")

# =====================================================
# SIDEBAR – COINS
# =====================================================
with st.sidebar:
    st.header("Turnve Coins (TvC)")
    st.metric("Balance", st.session_state.tvc)

    if st.button("Simulate 30 mins learning (+100 TvC)"):
        st.session_state.tvc += 100

    if st.button("Simulate 60 mins learning (+200 TvC)"):
        st.session_state.tvc += 200

# =====================================================
# MAIN FLOW
# =====================================================
st.title("Turnve – Career Simulation Platform")
st.caption("Train. Simulate. Prove experience.")

# ---------------- INDUSTRY SELECTION ----------------
if st.session_state.step == "industry":
    st.subheader("Select Industry")

    rows = [INDUSTRIES[i:i+4] for i in range(0, 8, 4)]
    for row in rows:
        cols = st.columns(4)
        for i, industry in enumerate(row):
            access = INDUSTRY_ACCESS[industry]
            with cols[i]:
                st.markdown(f"**{industry}**")

                if access["freemium"]:
                    if st.button("Enter", key=industry):
                        st.session_state.industry = industry
                        st.session_state.step = "role"
                        st.rerun()
                else:
                    if st.session_state.tvc >= PAID_COST_TVC:
                        if st.button("Unlock (6 TvC)", key=industry):
                            st.session_state.tvc -= PAID_COST_TVC
                            st.session_state.industry = industry
                            st.session_state.step = "role"
                            st.rerun()
                    else:
                        st.caption("Locked – Earn TvC")

# ---------------- ROLE SELECTION ----------------
elif st.session_state.step == "role":
    st.button("← Back", on_click=lambda: st.session_state.update(step="industry"))

    st.subheader(f"Roles in {st.session_state.industry}")
    roles = SIMULATION.get(st.session_state.industry, {}).get("roles", {})

    for role, data in roles.items():
        with st.container(border=True):
            st.markdown(f"### {role}")
            st.write(f"Project: {data['project']}")
            if st.button("Start Simulation", key=role):
                st.session_state.role = role
                st.session_state.project = data
                st.session_state.step = "assignment"
                st.rerun()

# ---------------- ASSIGNMENT ----------------
elif st.session_state.step == "assignment":
    assignment = st.session_state.project["assignment"]

    st.subheader(assignment["title"])
    st.info(assignment["instruction"])

    submission = st.text_area("Submit your work")

    if st.button("Submit to AI Coach"):
        score = score_submission(submission, assignment["keywords"])
        st.session_state.score = score

        if score >= 80:
            st.success(f"Passed with {score}%")
            st.session_state.assignment_done = True
        else:
            st.error(f"{score}% — Minimum 80% required. Retry.")

    if st.session_state.assignment_done:
        pdf = generate_portfolio()
        st.download_button(
            "Download Portfolio (PDF)",
            pdf,
            "Turnve_Portfolio.pdf",
            "application/pdf"
        )

        if st.button("Start New Simulation"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()