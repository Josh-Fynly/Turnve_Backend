import streamlit as st
import time
import random
import os
from datetime import datetime
from fpdf import FPDF

# -----------------------------
# CONFIG & PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Turnve – Career Simulation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# BRANDING
# -----------------------------
LOGO_PATH = "assets/turnve_logo.jpg"

# -----------------------------
# TURNVE ECONOMY CONFIG
# -----------------------------
TVC_EXCHANGE_RATE = 0.5  # 1 TvC = $0.5
COINS_PER_30_MIN = 100   # 30 mins = 100 TvC
PREMIUM_ACCESS_COST_USD = 3.00
PREMIUM_ACCESS_COST_TVC = int(PREMIUM_ACCESS_COST_USD / TVC_EXCHANGE_RATE)

# -----------------------------
# DATABASE: INDUSTRIES, ROLES, PROJECTS
# -----------------------------
INDUSTRIES_LIST = [
    "Technology & ICT", "Financial Services", "Retail & E-commerce", "Manufacturing",
    "Real Estate", "Media & Entertainment", "Energy & Utilities", "Healthcare"
]

INDUSTRY_CONFIG = {
    "Technology & ICT": {"freemium": True},
    "Energy & Utilities": {"freemium": True},
    "Financial Services": {"freemium": False},
    "Retail & E-commerce": {"freemium": False},
    "Manufacturing": {"freemium": False},
    "Real Estate": {"freemium": False},
    "Media & Entertainment": {"freemium": False},
    "Healthcare": {"freemium": False},
}

FULL_DB = {
    "Energy & Utilities": {
        "roles": [
            {
                "title": "Petroleum Engineer",
                "description": "Optimize extraction and analyze well performance.",
                "project": {
                    "title": "Oil Field Production Optimization",
                    "goal": "Analyze data to increase output while maintaining safety.",
                    "tasks": [
                        {
                            "name": "Analyze well performance data",
                            "prompt": "Review the provided pressure and flow rate datasets. Identify anomalies indicating blockage.",
                            "video_url": "https://www.youtube.com/watch?v=I7CQWgZInq4",
                            "resource_site": "Coursera (Energy Track)",
                            "min_score": 80
                        },
                        {
                            "name": "Identify production bottlenecks",
                            "prompt": "Based on your analysis, list the top 3 choke points in the pipeline infrastructure.",
                            "video_url": "https://www.youtube.com/watch?v=ZzjM1R5jR1k",
                            "resource_site": "Udemy (Oil & Gas)",
                            "min_score": 80
                        },
                        {
                            "name": "Recommend Optimization Techniques",
                            "prompt": "Propose an intervention strategy (e.g., Acidizing, Hydraulic Fracturing) for Well #4.",
                            "video_url": "https://www.youtube.com/watch?v=eAUGSZg3jXA",
                            "resource_site": "DigitalDefynd",
                            "min_score": 80
                        }
                    ]
                }
            }
        ]
    },
    "Technology & ICT": {
        "roles": [
            {
                "title": "Product Associate",
                "description": "Manage feature lifecycles and user requirements.",
                "project": {
                    "title": "Product Feature Launch Simulation",
                    "goal": "Launch 'Dark Mode' for the app.",
                    "tasks": [
                        {
                            "name": "Analyze user feedback",
                            "prompt": "Summarize the top 3 user complaints regarding eye strain.",
                            "video_url": "https://www.youtube.com/watch?v=ravLfnYuqmA",
                            "resource_site": "Coursera",
                            "min_score": 80
                        },
                        {
                            "name": "Define Success Metrics (KPIs)",
                            "prompt": "What 3 metrics will indicate this launch is successful?",
                            "video_url": "https://www.youtube.com/watch?v=3KaqaF8YciU",
                            "resource_site": "Udemy",
                            "min_score": 80
                        }
                    ]
                }
            }
        ]
    }
}

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
defaults = {
    "step": "industry",
    "wallet_tvc": 0,
    "time_spent_mins": 0,
    "unlocked_industries": [],
    "industry": None,
    "role_obj": None,
    "completed_tasks": [],
    "current_task_index": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def add_time(minutes):
    earned = int(minutes * (COINS_PER_30_MIN / 30))
    st.session_state.time_spent_mins += minutes
    st.session_state.wallet_tvc += earned
    st.toast(f"{minutes} mins simulated. +{earned} TvC")

def assess_submission(text):
    if len(text) < 10:
        return 0, "Submission too short."
    score = random.randint(65, 100)
    feedback = "Excellent work." if score >= 80 else "Below pass threshold."
    return score, feedback

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, w=50)
        pdf.ln(35)
    else:
        pdf.ln(20)

    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, "Turnve Proof of Experience", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Candidate ID: TRN-{random.randint(1000,9999)}", ln=True)
    pdf.cell(0, 10, f"Role: {st.session_state.role_obj['title']}", ln=True)
    pdf.cell(0, 10, f"Industry: {st.session_state.industry}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Verified Skills & Projects", ln=True)
    pdf.set_font("Arial", '', 12)

    for task in st.session_state.completed_tasks:
        pdf.cell(0, 10, f"- {task} [Passed]", ln=True)

    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Certified by Turnve AI Coach", ln=True, align='C')

    return pdf.output(dest="S").encode("latin-1")

# -----------------------------
# UI HEADER
# -----------------------------
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=180)

st.title("Turnve Career Simulation")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.metric("TvC Coins", st.session_state.wallet_tvc)
    st.metric("Est. Value ($)", st.session_state.wallet_tvc * TVC_EXCHANGE_RATE)
    if st.button("Simulate 30 Mins"):
        add_time(30)

# -----------------------------
# MAIN FLOW
# -----------------------------
if st.session_state.step == "industry":
    for ind in INDUSTRIES_LIST:
        if st.button(ind):
            st.session_state.industry = ind
            st.session_state.step = "role"
            st.rerun()

elif st.session_state.step == "role":
    roles = FULL_DB.get(st.session_state.industry, {}).get("roles", [])
    for role in roles:
        if st.button(role["title"]):
            st.session_state.role_obj = role
            st.session_state.step = "workspace"
            st.session_state.completed_tasks = []
            st.session_state.current_task_index = 0
            st.rerun()

elif st.session_state.step == "workspace":
    role = st.session_state.role_obj
    tasks = role["project"]["tasks"]
    idx = st.session_state.current_task_index

    if idx == len(tasks):
        st.success("Simulation complete")
        st.download_button(
            "Download Certificate",
            generate_pdf(),
            "turnve_certificate.pdf",
            "application/pdf"
        )
        st.stop()

    task = tasks[idx]
    st.subheader(task["name"])
    response = st.text_area("Your submission")

    if st.button("Submit"):
        score, feedback = assess_submission(response)
        if score >= task["min_score"]:
            st.session_state.completed_tasks.append(task["name"])
            st.session_state.current_task_index += 1
            st.success(f"Passed ({score}%)")
            st.rerun()
        else:
            st.error(f"Failed ({score}%)")
            st.write(feedback)