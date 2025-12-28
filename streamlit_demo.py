import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf import FPDF  # Requires: pip install fpdf

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Turnve – Career Simulation Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# DATA DEFINITIONS
# -----------------------------

# The 4x2 Grid Layout Definition
ALL_INDUSTRIES = [
    "Technology & ICT", "Financial Services", "Retail & E-commerce", "Manufacturing",
    "Real Estate", "Media & Entertainment", "Energy & Utilities", "Healthcare"
]

# Config for Locking/Unlocking
INDUSTRY_STATUS = {
    "Technology & ICT": {"locked": False, "freemium": True},
    "Energy & Utilities": {"locked": False, "freemium": True},  # Unlocked for demo purposes as requested
    "Financial Services": {"locked": True, "freemium": False},
    "Retail & E-commerce": {"locked": True, "freemium": False},
    "Manufacturing": {"locked": True, "freemium": False},
    "Real Estate": {"locked": True, "freemium": False},
    "Media & Entertainment": {"locked": True, "freemium": False},
    "Healthcare": {"locked": True, "freemium": False},
}

# Detailed Role Data (Only for the active industries)
ACTIVE_INDUSTRY_DATA = {
    "Technology & ICT": {
        "roles": {
            "Product Associate": {
                "description": "Define product vision and manage feature rollouts.",
                "project": {
                    "title": "Product Feature Launch Simulation",
                    "tasks": [
                        "Analyze user feedback and feature request",
                        "Define success metrics (KPIs)",
                        "Draft a product requirement summary",
                        "Align with stakeholders"
                    ]
                }
            },
            "Software Project Coordinator": {
                "description": "Manage timelines and unblock engineering teams.",
                "project": {
                    "title": "Sprint Coordination & Delivery Simulation",
                    "tasks": [
                        "Review sprint backlog",
                        "Identify delivery risks",
                        "Coordinate with engineering team",
                        "Prepare delivery status update"
                    ]
                }
            }
        }
    },
    "Energy & Utilities": {
        "roles": {
            "Petroleum Engineer": {
                "description": "Optimize oil and gas production methods.",
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
            "Energy Data Analyst": {
                "description": "Analyze consumption patterns for efficiency.",
                "project": {
                    "title": "Energy Consumption Analysis Simulation",
                    "tasks": [
                        "Analyze consumption data",
                        "Identify inefficiencies",
                        "Propose optimization strategy"
                    ]
                }
            }
        }
    }
}

# AI Coach Learning Resources (Updated with working links)
LEARNING_RESOURCES = {
    "Product Associate": [
        ("Intro to Product Management (YouTube)", "https://www.youtube.com/watch?v=ravLfnYuqmA"),
        ("Product Management Fundamentals (Coursera)", "https://www.coursera.org/learn/product-management-fundamentals"),
    ],
    "Petroleum Engineer": [
        ("Introduction to Petroleum Engineering (YouTube)", "https://www.youtube.com/watch?v=I7CQWgZInq4"),
        ("Oil & Gas Industry Overview (Udemy)", "https://www.udemy.com/course/oil-and-gas-industry-overview/"),
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

def generate_pdf_portfolio(industry, role, project, tasks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Turnve - Proof of Experience Portfolio", ln=1, align='C')
    pdf.ln(10)
    
    # Details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    pdf.cell(200, 10, txt=f"Industry: {industry}", ln=1)
    pdf.cell(200, 10, txt=f"Role: {role}", ln=1)
    pdf.ln(10)
    
    # Project
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Project: {project['title']}", ln=1)
    pdf.ln(5)
    
    # Tasks
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Completed Tasks & Competencies:", ln=1)
    for task in tasks:
        pdf.cell(200, 10, txt=f"- {task} (Verified)", ln=1)
        
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="This document serves as simulation-based proof of experience.", ln=1, align='C')

    return pdf.output(dest="S").encode("latin-1")

# -----------------------------
# APP FLOW
# -----------------------------

st.title("Turnve – Career Simulation Platform")
st.markdown("**Train. Simulate. Build proof of experience.**")

# -------- STEP 1: INDUSTRY SELECTION (4x2 Grid) --------
if st.session_state.step == "industry":
    st.subheader("Select Industry")
    st.info("Choose a Freemium industry to start your career simulation.")

    # Create rows for the 4x2 grid
    rows = [ALL_INDUSTRIES[i:i + 4] for i in range(0, len(ALL_INDUSTRIES), 4)]

    for row in rows:
        cols = st.columns(4)
        for idx, industry_name in enumerate(row):
            config = INDUSTRY_STATUS.get(industry_name)
            
            with cols[idx]:
                container = st.container(border=True)
                container.markdown(f"**{industry_name}**")
                
                if config["locked"]:
                    container.caption("🔒 Premium")
                    container.button("Unlock Access", key=f"btn_{industry_name}", disabled=True)
                else:
                    container.caption("✨ Freemium")
                    if container.button("Enter Simulation", key=f"btn_{industry_name}"):
                        st.session_state.industry = industry_name
                        st.session_state.step = "role"
                        st.rerun()

# -------- STEP 2: ROLE SELECTION --------
elif st.session_state.step == "role":
    st.subheader(f"Industry: {st.session_state.industry}")
    st.markdown("### Select a Role to Simulate")
    
    # Get roles for the selected active industry
    roles_data = ACTIVE_INDUSTRY_DATA[st.session_state.industry]["roles"]
    
    for role_name, role_info in roles_data.items():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"#### {role_name}")
            c1.write(role_info["description"])
            if c2.button("Start Career", key=role_name):
                st.session_state.role = role_name
                st.session_state.step = "project"
                st.rerun()

    st.button("← Back to Industries", on_click=reset_simulation)

# -------- STEP 3: PROJECT SIMULATION --------
elif st.session_state.step == "project":
    role_data = ACTIVE_INDUSTRY_DATA[st.session_state.industry]["roles"][st.session_state.role]
    current_project = role_data["project"]

    # Sidebar: AI Coach
    with st.sidebar:
        st.header("🤖 AI Coach")
        st.info(f"You are currently simulating the role of a **{st.session_state.role}**.")
        
        st.markdown("### Recommended Learning")
        st.write("Before you proceed, review these materials to master the concepts:")
        
        resources = LEARNING_RESOURCES.get(st.session_state.role, [])
        if resources:
            for title, link in resources:
                st.markdown(f"📚 [{title}]({link})")
        else:
            st.write("No specific resources tagged for this role yet.")
            
        st.divider()
        st.caption("Need help? The AI Coach monitors your progress.")

    # Main Area
    st.subheader(f"Project: {current_project['title']}")
    
    # Progress Bar
    progress = len(st.session_state.completed_tasks) / len(current_project["tasks"])
    st.progress(progress, text=f"Project Progress: {int(progress * 100)}%")

    st.markdown("### 📋 Pending Tasks")
    
    # Task List
    for task in current_project["tasks"]:
        is_completed = task in st.session_state.completed_tasks
        
        if is_completed:
            st.success(f"✅ {task}")
        else:
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{task}**")
            if c2.button("Complete Task", key=task):
                st.session_state.completed_tasks.append(task)
                st.rerun()

    # Completion Logic
    if len(st.session_state.completed_tasks) == len(current_project["tasks"]):
        st.balloons()
        st.success("🎉 Project Completed Successfully!")
        st.markdown("You have demonstrated the core competencies for this role.")

        # Generate PDF
        pdf_data = generate_pdf_portfolio(
            st.session_state.industry,
            st.session_state.role,
            current_project,
            st.session_state.completed_tasks
        )
        
        st.download_button(
            label="📄 Download Portfolio (PDF)",
            data=pdf_data,
            file_name="Turnve_Portfolio.pdf",
            mime="application/pdf"
        )
        
        st.button("Simulation Completed - Restart", on_click=reset_simulation)
