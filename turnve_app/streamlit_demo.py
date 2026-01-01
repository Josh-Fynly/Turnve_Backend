import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf import FPDF  # Requires: pip install fpdf
from PIL import Image  # Requires: pip install Pillow

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

ALL_INDUSTRIES = [
    "Technology & ICT", "Financial Services", "Retail & E-commerce", "Manufacturing",
    "Real Estate", "Media & Entertainment", "Energy & Utilities", "Healthcare"
]

# Config for Locking/Unlocking
INDUSTRY_STATUS = {
    "Technology & ICT": {"locked": False, "freemium": True},
    "Energy & Utilities": {"locked": False, "freemium": True},
    "Financial Services": {"locked": True, "freemium": False},
    "Retail & E-commerce": {"locked": True, "freemium": False},
    "Manufacturing": {"locked": True, "freemium": False},
    "Real Estate": {"locked": True, "freemium": False},
    "Media & Entertainment": {"locked": True, "freemium": False},
    "Healthcare": {"locked": True, "freemium": False},
}

# -----------------------------
# CORE SIMULATION DATA
# -----------------------------
ACTIVE_INDUSTRY_DATA = {
    "Technology & ICT": {
        "roles": {
            "Product Associate": {
                "description": "Bridge the gap between business, design, and engineering to launch products.",
                "project": {
                    "title": "Product Feature Launch Simulation",
                    "goal": "Launch a new 'Dark Mode' feature for the mobile app based on user demand.",
                    "tasks": [
                        "Analyze user feedback and feature request",
                        "Define success metrics (KPIs)",
                        "Craft a product requirement summary",
                        "Align with stakeholders"
                    ]
                }
            },
            "Software Engineer": {
                "description": "Design, develop, and test software systems to solve technical problems.",
                "project": {
                    "title": "Full Stack Feature Implementation",
                    "goal": "Build and deploy a scalable User Authentication System.",
                    "tasks": [
                        "Design Database Schema",
                        "Implement API Endpoints",
                        "Build Frontend Component",
                        "Write Unit Tests"
                    ]
                }
            }
        }
    },
    "Energy & Utilities": {
        "roles": {
            "Petroleum Engineer": {
                "description": "Design and develop methods for extracting oil and gas from deposits.",
                "project": {
                    "title": "Oil Field Production Optimization Simulation",
                    "goal": "Increase the output of an aging oil field while maintaining safety standards.",
                    "tasks": [
                        "Analyze well performance data",
                        "Identify production bottlenecks",
                        "Recommend optimization techniques",
                        "Prepare technical report"
                    ]
                }
            },
            "Energy Data Analyst": {
                "description": "Interpret data to help energy companies make better business decisions.",
                "project": {
                    "title": "Energy Consumption Analysis Simulation",
                    "goal": "Reduce operational costs by analyzing grid consumption patterns.",
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

# -----------------------------
# LEARNING RESOURCES (AI COACH)
# -----------------------------
LEARNING_RESOURCES = {
    "Product Associate": [
        ("Product Management Tutorial for Beginners (YouTube)", "https://www.youtube.com/watch?v=kbs-QwjLnEg "),
        ("What is Product Management? (YouTube)", "https://www.youtube.com/watch?v=3KaqaF8YciU "),
    ],
    "Software Engineer": [
        ("Beginner Guide to Software Engineering (YouTube)", "https://www.youtube.com/watch?v=nF65aNTc4Mk "),
        ("Introduction to Software Engineering (YouTube)", "https://www.youtube.com/watch?v=IHx9ImEMuzQ "),
    ],
    "Petroleum Engineer": [
        ("Applied Petroleum Engineering Lessons (YouTube)", "https://www.youtube.com/watch?v=Zypkj33Zv9E "),
        ("Types of Petroleum Engineers (YouTube)", "https://www.youtube.com/watch?v=eAUGSZg3jXA "),
    ]
}

# -----------------------------
# SESSION STATE MANAGEMENT
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
# HELPER FUNCTIONS
# -----------------------------
def reset_simulation():
    st.session_state.step = "industry"
    st.session_state.industry = None
    st.session_state.role = None
    st.session_state.completed_tasks = []

def generate_pdf_portfolio(industry, role, project, tasks):
    pdf = FPDF()
    pdf.add_page()
    
    # Add logo at the top center
    # Make sure you have a file named 'turnve_logo.jpg' in your project directory
    try:
        # Add logo at the top center
        pdf.image('turnve_logo.jpg', x=pdf.w/2 - 30, y=10, w=60)  # Adjust width as needed
        pdf.ln(40)  # Add space after logo
    except Exception as e:
        # If logo file is not found, use text instead
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 15, "Turnve", ln=True, align='C')
        pdf.ln(10)
    
    # Continue with existing content
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Career Simulation Portfolio", ln=True, align='C')
    pdf.ln(10)
    
    # Candidate Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Industry:", 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, industry, 1)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Role:", 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, role, 1)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Date:", 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, datetime.now().strftime("%Y-%m-%d"), 1)
    pdf.ln(10)
    
    # Project Details
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Project: {project['title']}", ln=True)
    
    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, f"Goal: {project['goal']}")
    pdf.ln(5)
    
    # Completed Tasks
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Competencies Demonstrated & Tasks Completed:", ln=True)
    pdf.set_font("Arial", '', 11)
    
    for task in tasks:
        pdf.cell(0, 8, f"- {task} [VERIFIED]", ln=True)
        
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Generated by Turnve AI Coach. This document serves as a simulation-based proof of experience.", ln=True, align='C')

    return pdf.output(dest="S").encode("latin-1")

# -----------------------------
# APP UI & FLOW
# -----------------------------

st.title("Turnve – Career Simulation Platform")
st.markdown("### Train. Simulate. Build proof of experience.")

# ==========================================
# PHASE 1: INDUSTRY SELECTION (4x2 GRID)
# ==========================================
if st.session_state.step == "industry":
    st.info("Select an industry to begin your simulation.")
    
    rows = [ALL_INDUSTRIES[i:i + 4] for i in range(0, len(ALL_INDUSTRIES), 4)]

    for row in rows:
        cols = st.columns(4)
        for idx, industry_name in enumerate(row):
            config = INDUSTRY_STATUS.get(industry_name)
            
            with cols[idx]:
                container = st.container(border=True)
                container.markdown(f"**{industry_name}**")
                
                if config["locked"]:
                    container.caption(" Premium Access Only")
                    container.button("Unlock", key=f"lock_{industry_name}", disabled=True)
                else:
                    container.caption("✨ Freemium Access")
                    if container.button("Enter Simulation", key=f"btn_{industry_name}"):
                        st.session_state.industry = industry_name
                        st.session_state.step = "role"
                        st.rerun()

# ==========================================
# PHASE 2: ROLE SELECTION
# ==========================================
elif st.session_state.step == "role":
    st.button("← Choose Different Industry", on_click=reset_simulation)
    
    st.divider()
    st.subheader(f"Available Roles in {st.session_state.industry}")
    
    roles_data = ACTIVE_INDUSTRY_DATA[st.session_state.industry]["roles"]
    
    for role_name, role_info in roles_data.items():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {role_name}")
                st.write(role_info["description"])
                st.info(f"**Project:** {role_info['project']['title']}")
            with c2:
                st.write("") # Spacer
                st.write("")
                if st.button("Start Career Path", key=f"start_{role_name}", use_container_width=True):
                    st.session_state.role = role_name
                    st.session_state.step = "project"
                    st.rerun()

# ==========================================
# PHASE 3: PROJECT SIMULATION
# ==========================================
elif st.session_state.step == "project":
    role_data = ACTIVE_INDUSTRY_DATA[st.session_state.industry]["roles"][st.session_state.role]
    current_project = role_data["project"]
    
    # --- Sidebar: AI Coach ---
    with st.sidebar:
        st.header(" AI Coach")
        st.success(f"Role: **{st.session_state.role}**")
        
        st.markdown("###  Recommended Learning")
        st.caption("New to this role? Watch these tutorials before starting tasks:")
        
        resources = LEARNING_RESOURCES.get(st.session_state.role, [])
        if resources:
            for title, link in resources:
                st.markdown(f" [{title}]({link})")
        else:
            st.warning("No specific tutorials linked for this role yet.")
            
        st.divider()
        st.markdown("**Progress Tracker**")
        progress_val = len(st.session_state.completed_tasks) / len(current_project["tasks"])
        st.progress(progress_val)
        st.caption(f"{int(progress_val * 100)}% Completed")

    # --- Main Project Area ---
    st.button("← Back to Roles", on_click=lambda: st.session_state.update(step="role", completed_tasks=[]))
    st.divider()
    
    st.subheader(f"Project: {current_project['title']}")
    st.markdown(f"**Goal:** *{current_project['goal']}*")
    
    st.markdown("###  Execution Tasks")
    
    for index, task in enumerate(current_project["tasks"]):
        # Logic to ensure sequential completion (optional, but good for simulation feel)
        # To force order: if index > 0 and current_project["tasks"][index-1] not in st.session_state.completed_tasks: continue
        
        is_done = task in st.session_state.completed_tasks
        
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            
            with c1:
                if is_done:
                    st.markdown(f"✅ ~~{task}~~")
                else:
                    st.markdown(f"**{index + 1}. {task}**")
                    st.caption("Pending execution...")
            
            with c2:
                if not is_done:
                    if st.button("Execute", key=f"task_{index}"):
                        st.session_state.completed_tasks.append(task)
                        st.rerun()
                else:
                    st.write("Completed")

    # --- Completion & Portfolio ---
    if len(st.session_state.completed_tasks) == len(current_project["tasks"]):
        st.divider()
        st.balloons()
        st.success(" MISSION ACCOMPLISHED!")
        st.markdown(
            """
            **Great job!** You have successfully completed the simulation for this role.
            Your Proof of Experience Portfolio is ready.
            """
        )
        
        pdf_file = generate_pdf_portfolio(
            st.session_state.industry,
            st.session_state.role,
            current_project,
            st.session_state.completed_tasks
        )
        
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                label=" Download Portfolio (PDF)",
                data=pdf_file,
                file_name=f"Turnve_{st.session_state.role.replace(' ', '_')}_Portfolio.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with c2:
             st.button("Start New Simulation", on_click=reset_simulation, use_container_width=True)