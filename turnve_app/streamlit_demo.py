import streamlit as st
import time
import random
from datetime import datetime
from fpdf import FPDF
from PIL import Image  # Requires: pip install Pillow

# -----------------------------
# CONFIG & PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Turnve – Career Simulation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# TURNVE ECONOMY CONFIG
# -----------------------------
TVC_EXCHANGE_RATE = 0.5  # 1 TvC = $0.5
COINS_PER_30_MIN = 100   # 30 mins = 100 TvC
PREMIUM_ACCESS_COST_USD = 3.00
PREMIUM_ACCESS_COST_TVC = int(PREMIUM_ACCESS_COST_USD / TVC_EXCHANGE_RATE) # 6 TvC

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

# Expanded Data Structure with Embedded Learning
# Note: For demo brevity, I've fully populated the Freemium ones. 
# In a full app, all would be populated.
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
                            "video_url": "https://www.youtube.com/watch?v=I7CQWgZInq4 ", # Intro to Petroleum Engineering
                            "resource_site": "Coursera (Energy Track)",
                            "min_score": 80
                        },
                        {
                            "name": "Identify production bottlenecks",
                            "prompt": "Based on your analysis, list the top 3 choke points in the pipeline infrastructure.",
                            "video_url": "https://www.youtube.com/watch?v=ZzjM1R5jR1k ", 
                            "resource_site": "Udemy (Oil & Gas)",
                            "min_score": 80
                        },
                        {
                            "name": "Recommend Optimization Techniques",
                            "prompt": "Propose an intervention strategy (e.g., Acidizing, Hydraulic Fracturing) for Well #4.",
                            "video_url": "https://www.youtube.com/watch?v=eAUGSZg3jXA ",
                            "resource_site": "DigitalDefynd",
                            "min_score": 80
                        }
                    ]
                }
            },
            {
                "title": "Energy Data Analyst",
                "description": "Interpret grid data to improve efficiency.",
                "project": {
                    "title": "Grid Consumption Analysis",
                    "goal": "Reduce waste by 15% through data analysis.",
                    "tasks": [
                        {"name": "Audit Grid Load", "prompt": "Identify peak load times.", "video_url": "https://www.youtube.com/watch?v=f7G870W_2TQ ", "resource_site": "Khan Academy", "min_score": 80},
                        {"name": "Forecast Demand", "prompt": "Create a 7-day demand forecast.", "video_url": "https://www.youtube.com/watch?v=f7G870W_2TQ ", "resource_site": "Coursera", "min_score": 80},
                    ]
                }
            },
            {
                "title": "Renewable Systems Tech",
                "description": "Manage solar and wind farm deployments.",
                "project": {
                    "title": "Solar Field Deployment",
                    "goal": "Plan the layout for a 50-acre solar farm.",
                    "tasks": [
                        {"name": "Site Feasibility Study", "prompt": "Assess soil and sun hours.", "video_url": "https://www.youtube.com/watch?v=xKxrkht7CpY ", "resource_site": "Mindluster", "min_score": 80},
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
                            "video_url": "https://www.youtube.com/watch?v=ravLfnYuqmA ",
                            "resource_site": "Coursera",
                            "min_score": 80
                        },
                        {
                            "name": "Define Success Metrics (KPIs)",
                            "prompt": "What 3 metrics will indicate this launch is successful?",
                            "video_url": "https://www.youtube.com/watch?v=3KaqaF8YciU ",
                            "resource_site": "Udemy",
                            "min_score": 80
                        }
                    ]
                }
            },
            {
                "title": "Software Engineer",
                "description": "Build scalable software solutions.",
                "project": {
                    "title": "Auth System Implementation",
                    "goal": "Build a secure login API.",
                    "tasks": [
                        {"name": "Design DB Schema", "prompt": "Submit the SQL for the User table.", "video_url": "https://www.youtube.com/watch?v=nF65aNTc4Mk ", "resource_site": "YouTube/FreeCodeCamp", "min_score": 80},
                        {"name": "Write Unit Tests", "prompt": "Write a test case for invalid password entry.", "video_url": "https://www.youtube.com/watch?v=IHx9ImEMuzQ ", "resource_site": "Khan Academy", "min_score": 80}
                    ]
                }
            },
            {
                "title": "UX Designer",
                "description": "Design intuitive user interfaces.",
                "project": {
                    "title": "Mobile App Redesign",
                    "goal": "Improve navigation flow.",
                    "tasks": [
                        {"name": "Wireframing", "prompt": "Create a low-fidelity wireframe.", "video_url": "https://www.youtube.com/watch?v=c9Wg6Cb_YlU ", "resource_site": "DigitalDefynd", "min_score": 80},
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
    "role_obj": None, # Holds the full role object
    "completed_tasks": [], # List of task names
    "current_task_index": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def add_time(minutes):
    """Simulate time passing and earning coins"""
    st.session_state.time_spent_mins += minutes
    # 30 mins = 100 TvC -> 1 min = 3.33 TvC
    earned = int(minutes * (COINS_PER_30_MIN / 30))
    st.session_state.wallet_tvc += earned
    st.toast(f"⏱️ {minutes} mins passed. You earned {earned} TvC!")

def unlock_industry(ind_name):
    if st.session_state.wallet_tvc >= PREMIUM_ACCESS_COST_TVC:
        st.session_state.wallet_tvc -= PREMIUM_ACCESS_COST_TVC
        st.session_state.unlocked_industries.append(ind_name)
        st.toast(f" Successfully unlocked {ind_name}!")
        st.rerun()
    else:
        st.error(f"Insufficient TvC! You need {PREMIUM_ACCESS_COST_TVC} TvC ($3.00 value).")

def assess_submission(submission_text):
    """Simulate AI Coach Grading"""
    if len(submission_text) < 10:
        return 0, "Submission too short. Please elaborate."
    
    # Mock grading logic: Random score between 60 and 100 for demo
    score = random.randint(65, 100) 
    
    if score >= 80:
        feedback = "Excellent work. Your approach aligns with industry standards."
    else:
        feedback = "Does not meet the 80% threshold. Review the learning material and try again."
        
    return score, feedback

def generate_pdf():
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
        pdf.cell(0, 15, "Turnve Proof of Experience", ln=True, align='C')
        pdf.ln(10)
    
    # Continue with existing content
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
        pdf.cell(0, 10, f"- {task} [Passed Assessment]", ln=True)
        
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Certified by Turnve AI Coach", ln=True, align='C')
    
    return pdf.output(dest="S").encode("latin-1")

# -----------------------------
# SIDEBAR: WALLET & NAV
# -----------------------------
with st.sidebar:
    st.title("Turnve Wallet")
    
    c1, c2 = st.columns(2)
    c1.metric("TvC Coins", f"{st.session_state.wallet_tvc}")
    c2.metric("Est. Value", f"${st.session_state.wallet_tvc * TVC_EXCHANGE_RATE:.2f}")
    
    st.caption(f"Rate: {COINS_PER_30_MIN} TvC / 30 mins")
    
    st.divider()
    
    # Simulation Tool for Demo Users
    st.subheader("Dev Tools (Simulation)")
    if st.button("Simulate 30 Mins Work"):
        add_time(30)
    if st.button("Simulate 60 Mins Work"):
        add_time(60)

    st.divider()
    if st.button("Reset Demo"):
        for k in defaults.keys():
            del st.session_state[k]
        st.rerun()

# -----------------------------
# MAIN APP
# -----------------------------
st.title("Turnve Career Simulation")

# =======================
# STEP 1: INDUSTRY GRID
# =======================
if st.session_state.step == "industry":
    st.subheader("Select Industry")
    
    # 4x2 Grid
    rows = [INDUSTRIES_LIST[i:i + 4] for i in range(0, len(INDUSTRIES_LIST), 4)]
    
    for row in rows:
        cols = st.columns(4)
        for idx, ind_name in enumerate(row):
            is_freemium = INDUSTRY_CONFIG.get(ind_name, {}).get("freemium", False)
            is_unlocked = ind_name in st.session_state.unlocked_industries
            
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"#### {ind_name}")
                    
                    if is_freemium or is_unlocked:
                        st.caption("✅ Available")
                        if st.button("Enter", key=f"ent_{ind_name}"):
                            st.session_state.industry = ind_name
                            st.session_state.step = "role"
                            st.rerun()
                    else:
                        st.caption(f" Locked ({PREMIUM_ACCESS_COST_TVC} TvC)")
                        if st.button(f"Unlock (${PREMIUM_ACCESS_COST_USD})", key=f"ulk_{ind_name}"):
                            unlock_industry(ind_name)

# =======================
# STEP 2: ROLE SELECTION
# =======================
elif st.session_state.step == "role":
    st.button("← Back", on_click=lambda: st.session_state.update(step="industry"))
    st.header(f"{st.session_state.industry}: Role Selection")
    
    # Check if we have data for this industry (for demo purposes)
    if st.session_state.industry in FULL_DB:
        roles = FULL_DB[st.session_state.industry]["roles"]
        
        for role in roles:
            with st.container(border=True):
                c1, c2 = st.columns([4,1])
                with c1:
                    st.subheader(role["title"])
                    st.write(role["description"])
                    st.info(f"Project: {role['project']['title']}")
                with c2:
                    st.write("")
                    if st.button("Start Path", key=f"start_{role['title']}"):
                        st.session_state.role_obj = role
                        st.session_state.step = "workspace"
                        st.session_state.current_task_index = 0
                        st.session_state.completed_tasks = []
                        st.rerun()
    else:
        st.warning("Simulation content for this industry is coming soon (Demo limitation). Try Technology or Energy.")

# =======================
# STEP 3: IMMERSIVE WORKSPACE
# =======================
elif st.session_state.step == "workspace":
    role = st.session_state.role_obj
    tasks = role['project']['tasks']
    current_idx = st.session_state.current_task_index
    
    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader(f"Project: {role['project']['title']}")
    with c2:
        if st.button("Exit Simulation"):
            st.session_state.step = "role"
            st.rerun()
            
    # Progress Bar
    prog = len(st.session_state.completed_tasks) / len(tasks)
    st.progress(prog, text=f"Completion: {int(prog*100)}%")

    # If all tasks done
    if len(st.session_state.completed_tasks) == len(tasks):
        st.success(" Simulation Complete!")
        st.balloons()
        pdf_bytes = generate_pdf()
        st.download_button("Download Proof of Experience (PDF)", pdf_bytes, "turnve_portfolio.pdf", "application/pdf")
        st.stop()

    # Current Active Task
    current_task = tasks[current_idx]
    
    st.divider()
    
    # LAYOUT: LEFT (Work) | RIGHT (AI Coach)
    col_work, col_coach = st.columns([1.5, 1])
    
    with col_work:
        st.markdown(f"###  Task {current_idx + 1}: {current_task['name']}")
        st.write(current_task['prompt'])
        
        st.markdown("#### Your Workspace")
        user_input = st.text_area("Analyze findings and type your solution here...", height=200)
        
        if st.button("Submit to AI Coach"):
            with st.spinner("AI Coach is grading your submission..."):
                time.sleep(1.5) # Simulate processing
                score, feedback = assess_submission(user_input)
                
                if score >= current_task['min_score']:
                    st.success(f"Passed! Score: {score}%")
                    st.write(f"Coach: {feedback}")
                    st.session_state.completed_tasks.append(current_task['name'])
                    if current_idx + 1 < len(tasks):
                        st.session_state.current_task_index += 1
                        st.button("Next Task →") # Rerun trigger
                    else:
                        st.rerun()
                else:
                    st.error(f"Failed. Score: {score}% (Required: {current_task['min_score']}%)")
                    st.write(f"Coach: {feedback}")
                    st.warning("Please review the learning material on the right and try again.")

    with col_coach:
        st.container(border=True).markdown("###  AI Coach Hub")
        st.info("I am here to guide you. Watch this quick course to understand the task.")
        
        # Embedded Learning
        st.video(current_task['video_url'])
        
        st.markdown(f"**Source:** {current_task['resource_site']}")
        st.caption("You must achieve ≥80% to proceed. Do not leave this screen.")