import streamlit as st
import time
import random
import os
from datetime import datetime
from fpdf import FPDF  # Requires: pip install fpdf

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
# DATABASE: ALL 8 INDUSTRIES POPULATED
# -----------------------------
# NOTE: To avoid copyright issues, the "video_url" has been replaced with 
# "ai_lecture_content". The AI Coach now teaches the user directly via text.

FULL_DB = {
    "Technology & ICT": {
        "freemium": True,
        "roles": [
            {
                "title": "Product Associate",
                "description": "Bridge the gap between business, design, and engineering.",
                "project": {
                    "title": "Feature Launch Alpha",
                    "goal": "Launch 'Dark Mode' based on user metrics.",
                    "tasks": [
                        {
                            "name": "Analyze User Feedback",
                            "prompt": "Read the mock user reviews below. Summarize the top 3 pain points regarding eye strain.",
                            "ai_lecture_content": "### 🎓 Lecture: Understanding User Pain Points\n\nIn Product Management, feedback is gold. When analyzing feedback:\n1. **Categorize**: Group similar complaints (e.g., 'Too bright', 'Hurts eyes' -> Visual Comfort).\n2. **Quantify**: How many users said this? (Frequency = Priority).\n3. **Contextualize**: When does it happen? (e.g., At night).\n\n*Assignment Hint: Look for keywords like 'glare' and 'night usage' in the dataset.*",
                            "min_score": 80
                        },
                        {
                            "name": "Define Success Metrics",
                            "prompt": "List 3 KPIs that would indicate the Dark Mode launch is successful.",
                            "ai_lecture_content": "### 🎓 Lecture: Key Performance Indicators (KPIs)\n\nMetrics tell us if a feature works. Common Product KPIs:\n* **Adoption Rate**: % of users who turn the feature on.\n* **Retention**: Do they keep using the app longer?\n* **NPS (Net Promoter Score)**: Does customer satisfaction go up?\n\n*Avoid 'Vanity Metrics' like total downloads. Focus on engagement.*",
                            "min_score": 80
                        }
                    ]
                }
            },
            {
                "title": "Software Engineer",
                "description": "Build scalable software systems.",
                "project": {
                    "title": "Auth API Implementation",
                    "goal": "Secure the user login backend.",
                    "tasks": [
                        {
                            "name": "Design DB Schema",
                            "prompt": "Write the SQL 'CREATE TABLE' statement for Users (ID, Username, Hash).",
                            "ai_lecture_content": "### 🎓 Lecture: Database Design 101\n\nA **Schema** is the blueprint of your database. For a User table, you need:\n1. **Primary Key (ID)**: A unique identifier (UUID or Integer).\n2. **Constraints**: 'NOT NULL' for emails, 'UNIQUE' for usernames.\n3. **Security**: NEVER store passwords as plain text. Store the 'Hash' (encrypted string).",
                            "min_score": 80
                        }
                    ]
                }
            },
             {
                "title": "UX Designer",
                "description": "Design intuitive digital experiences.",
                "project": {
                    "title": "Mobile Navigation Redesign",
                    "goal": "Improve app flow to reduce bounce rate.",
                    "tasks": [
                        {
                            "name": "Create Wireframes",
                            "prompt": "Describe the layout of the new bottom navigation bar.",
                            "ai_lecture_content": "### 🎓 Lecture: Low-Fidelity Wireframing\n\nWireframes are the skeleton of design. Focus on layout, not colors. \n\n**The Rule of Thumb Zone**: On mobile, place key actions (like 'Home', 'Profile') in the bottom third of the screen where the thumb naturally rests.",
                            "min_score": 80
                        }
                    ]
                }
            }
        ]
    },
    "Energy & Utilities": {
        "freemium": True,
        "roles": [
            {
                "title": "Petroleum Engineer",
                "description": "Optimize extraction and analyze well performance.",
                "project": {
                    "title": "Oil Field Optimization",
                    "goal": "Increase output while maintaining safety.",
                    "tasks": [
                        {
                            "name": "Analyze Well Data",
                            "prompt": "Review the pressure data. Is the flow rate declining due to natural depletion or mechanical skin damage?",
                            "ai_lecture_content": "### 🎓 Lecture: Nodal Analysis Basics\n\nOil doesn't just flow; it is pushed by pressure. \n\n**Inflow Performance Relationship (IPR)**: This curve shows what the reservoir can deliver.\n**Tubing Performance Curve (TPR)**: This shows what the pipe can handle.\n\n*Intersection Point = Production Rate.* If pressure drops but flow drops faster, check for 'Skin Damage' (blockage near the wellbore).",
                            "min_score": 80
                        }
                    ]
                }
            },
            {
                "title": "Energy Data Analyst",
                "description": "Interpret grid data for efficiency.",
                "project": {
                    "title": "Grid Consumption Audit",
                    "goal": "Reduce waste by 15%.",
                    "tasks": [
                        {"name": "Audit Peak Load", "prompt": "Identify the hour of maximum strain on the grid.", "ai_lecture_content": "### 🎓 Lecture: Peak Load Management\n\nElectricity demand isn't constant. \n\n**Peak Load**: The highest point of demand (usually 6pm-9pm).\n**Base Load**: The minimum constant demand.\n\nEfficiency strategy: 'Peak Shaving' - shifting usage to off-hours.", "min_score": 80}
                    ]
                }
            },
             {
                "title": "Renewable Tech",
                "description": "Manage solar deployments.",
                "project": {
                    "title": "Solar Field Setup",
                    "goal": "Plan a 50-acre farm.",
                    "tasks": [
                        {"name": "Solar Irradiance Check", "prompt": "Calculate potential kWh based on sun hours.", "ai_lecture_content": "### 🎓 Lecture: Solar Irradiance\n\nNot all sunlight is equal. We measure **GHI (Global Horizontal Irradiance)**.\n\nFormula: Area (m2) x Efficiency (%) x Peak Sun Hours = Energy Output.\n*Check the latitude of the deployment site.*", "min_score": 80}
                    ]
                }
            }
        ]
    },
    "Financial Services": {
        "freemium": False,
        "roles": [
            {
                "title": "Financial Analyst",
                "description": "Assess investment performance.",
                "project": {
                    "title": "Portfolio Risk Assessment",
                    "goal": "Rebalance a $1M portfolio to minimize risk.",
                    "tasks": [
                        {"name": "Calculate Beta", "prompt": "Calculate the volatility of Tech Stock A relative to the market.", "ai_lecture_content": "### 🎓 Lecture: Understanding Beta\n\n**Beta (β)** measures volatility.\n* β = 1.0: Stock moves exactly with the market.\n* β > 1.0: High risk, high reward (Aggressive).\n* β < 1.0: Stable, low risk (Defensive).\n\nTo hedge risk, mix high beta stocks with low beta bonds.", "min_score": 80}
                    ]
                }
            },
            {
                "title": "Investment Banker",
                "description": "Manage mergers and acquisitions.",
                "project": {
                    "title": "M&A Valuation",
                    "goal": "Valuate Company X for acquisition.",
                    "tasks": [
                        {"name": "DCF Analysis", "prompt": "Perform a Discounted Cash Flow analysis.", "ai_lecture_content": "### 🎓 Lecture: DCF Basics\n\nA company is worth the present value of its future cash.\n\n**Formula**: Sum of Future Cash Flows / (1 + Discount Rate)^Years.\n*The 'Discount Rate' accounts for the risk that the money might not arrive.*", "min_score": 80}
                    ]
                }
            },
            {
                "title": "Risk Manager",
                "description": "Identify and mitigate financial risks.",
                "project": {
                    "title": "Credit Risk Modeling",
                    "goal": "Assess loan default probabilities.",
                    "tasks": [
                        {"name": "Credit Score Analysis", "prompt": "Review applicant debt-to-income ratios.", "ai_lecture_content": "### 🎓 Lecture: The 5 Cs of Credit\n\n1. **Character**: Credit history.\n2. **Capacity**: Debt-to-income ratio.\n3. **Capital**: Down payment size.\n4. **Collateral**: Asset value.\n5. **Conditions**: Interest rates.", "min_score": 80}
                    ]
                }
            }
        ]
    },
    "Retail & E-commerce": {
        "freemium": False,
        "roles": [
            {
                "title": "E-commerce Manager",
                "description": "Oversee online sales strategy.",
                "project": {
                    "title": "Holiday Sales Campaign",
                    "goal": "Launch Black Friday strategy.",
                    "tasks": [
                        {"name": "Inventory Forecasting", "prompt": "Estimate units needed for Q4.", "ai_lecture_content": "### 🎓 Lecture: Inventory Turnover\n\n**Stockout** = Lost sales. **Overstock** = Wasted cash.\n\nUse 'Historical Run Rate' + 'Seasonality Multiplier' to forecast.\nFor Black Friday, apply a 3x multiplier to standard weekend sales.", "min_score": 80}
                    ]
                }
            },
            {
                "title": "Supply Chain Coordinator",
                "description": "Manage logistics and shipping.",
                "project": {
                    "title": "Logistics Optimization",
                    "goal": "Reduce shipping times by 20%.",
                    "tasks": [
                        {"name": "Route Optimization", "prompt": "Select the optimal distribution center.", "ai_lecture_content": "### 🎓 Lecture: Last-Mile Delivery\n\nThe 'Last Mile' is the most expensive part of shipping.\n\nStrategy: **Distributed Warehousing**. Placing stock closer to population centers reduces Zone Skipping fees.", "min_score": 80}
                    ]
                }
            },
            {
                "title": "Retail Buyer",
                "description": "Select products for store shelves.",
                "project": {
                    "title": "Seasonal Collection Buy",
                    "goal": "Select best-selling items for Spring.",
                    "tasks": [
                        {"name": "Trend Analysis", "prompt": "Identify top colors for next season.", "ai_lecture_content": "### 🎓 Lecture: Merchandising Math\n\n**Sell-Through Rate**: (Units Sold / Units Received) x 100.\nIf sell-through is < 40% after 4 weeks, the product is a 'dog' (slow mover). Mark it down.", "min_score": 80}
                    ]
                }
            }
        ]
    },
    "Manufacturing": {
        "freemium": False,
        "roles": [
            {"title": "Operations Manager", "description": "Oversee production lines.", "project": {"title": "Lean Manufacturing", "tasks": [{"name": "Waste Reduction", "prompt": "Identify 7 wastes.", "ai_lecture_content": "### 🎓 Lecture: The 7 Wastes (Muda)\n1. Overproduction\n2. Waiting\n3. Transport\n4. Processing\n5. Inventory\n6. Motion\n7. Defects", "min_score": 80}]}},
            {"title": "Quality Engineer", "description": "Ensure product standards.", "project": {"title": "Six Sigma Implementation", "tasks": [{"name": "Root Cause Analysis", "prompt": "Use the 5 Whys.", "ai_lecture_content": "### 🎓 Lecture: 5 Whys\nProblem: Part is defective.\n1. Why? Machine jammed.\n2. Why? Belt broke.\n3. Why? Not maintained.\n4. Why? No schedule.\n5. Why? No manager assigned. -> **Root Cause**.", "min_score": 80}]}},
            {"title": "Production Planner", "description": "Schedule manufacturing runs.", "project": {"title": "Capacity Planning", "tasks": [{"name": "Bottleneck ID", "prompt": "Find the slowest machine.", "ai_lecture_content": "### 🎓 Lecture: Theory of Constraints\nThe output of the whole factory is determined by the slowest machine (The Bottleneck). Improve that one first.", "min_score": 80}]}}
        ]
    },
    "Real Estate": {
        "freemium": False,
        "roles": [
            {"title": "Property Manager", "description": "Manage tenant relations.", "project": {"title": "Tenant Retention", "tasks": [{"name": "Lease Renewal", "prompt": "Draft renewal terms.", "ai_lecture_content": "### 🎓 Lecture: Retention Costs\nIt costs 5x more to find a new tenant than to keep an existing one. Offer 'Renewal Incentives' (e.g., carpet cleaning) instead of rent drops.", "min_score": 80}]}},
            {"title": "Real Estate Analyst", "description": "Valuate properties.", "project": {"title": "Commercial Valuation", "tasks": [{"name": "Cap Rate Calculation", "prompt": "Calculate NOI / Price.", "ai_lecture_content": "### 🎓 Lecture: Cap Rate\n**Capitalization Rate** = Net Operating Income / Property Value.\nA high Cap Rate (8%+) means higher risk/return. A low Cap Rate (4%) means a stable, trophy asset.", "min_score": 80}]}},
            {"title": "Urban Planner", "description": "Design land use.", "project": {"title": "Zoning Simulation", "tasks": [{"name": "Site Analysis", "prompt": "Check zoning laws.", "ai_lecture_content": "### 🎓 Lecture: Zoning Codes\n**R1**: Residential Single Family.\n**C1**: Commercial.\n**M1**: Manufacturing.\nYou cannot build a factory in R1. Always check the 'Setbacks' and 'FAR' (Floor Area Ratio).", "min_score": 80}]}}
        ]
    },
    "Healthcare": {
        "freemium": False,
        "roles": [
            {"title": "Health Data Analyst", "description": "Analyze patient outcomes.", "project": {"title": "Readmission Reduction", "tasks": [{"name": "Data Cleaning", "prompt": "Remove duplicates.", "ai_lecture_content": "### 🎓 Lecture: PHI Compliance\nWhen handling health data, you must strip **PII (Personally Identifiable Information)** to comply with HIPAA. Remove Names, SSNs, and Addresses.", "min_score": 80}]}},
            {"title": "Medical Coder", "description": "Classify medical diagnoses.", "project": {"title": "ICD-10 Coding", "tasks": [{"name": "Code Assignment", "prompt": "Assign code for Hypertension.", "ai_lecture_content": "### 🎓 Lecture: ICD-10 Structure\nCharacters 1-3: Category (e.g., I10).\nCharacters 4-6: Etiology/Site.\nCharacter 7: Extension.\nAccuracy is vital for insurance reimbursement.", "min_score": 80}]}},
            {"title": "Hospital Admin", "description": "Manage facility operations.", "project": {"title": "Staff Scheduling", "tasks": [{"name": "Shift Coverage", "prompt": "Ensure ER coverage.", "ai_lecture_content": "### 🎓 Lecture: Staff-to-Patient Ratios\nSafe staffing saves lives. \nICU Ratio: 1 Nurse to 2 Patients.\nER Ratio: 1 Nurse to 4 Patients.\nOverloading nurses leads to 'Burnout' and medication errors.", "min_score": 80}]}}
        ]
    },
    "Media & Entertainment": {
        "freemium": False,
        "roles": [
            {"title": "Digital Marketer", "description": "Run ad campaigns.", "project": {"title": "Social Media Blitz", "tasks": [{"name": "Ad Targeting", "prompt": "Define audience persona.", "ai_lecture_content": "### 🎓 Lecture: Lookalike Audiences\nDon't guess. Upload your email list to Facebook. Create a **Lookalike Audience** (Top 1%) to find new people who act exactly like your best customers.", "min_score": 80}]}},
            {"title": "Content Strategist", "description": "Plan content rollouts.", "project": {"title": "Blog Calendar", "tasks": [{"name": "SEO Keyword Research", "prompt": "Find high volume keywords.", "ai_lecture_content": "### 🎓 Lecture: SEO Pillars\n1. **Volume**: How many search it?\n2. **Difficulty**: Can we rank?\n3. **Intent**: Are they looking to buy or learn?\nTarget 'Long-Tail Keywords' for easier wins.", "min_score": 80}]}},
            {"title": "Video Editor", "description": "Post-production editing.", "project": {"title": "Trailer Cut", "tasks": [{"name": "Pacing Edit", "prompt": "Cut dead air.", "ai_lecture_content": "### 🎓 Lecture: The J-Cut and L-Cut\n**J-Cut**: Audio starts before video.\n**L-Cut**: Video changes, audio continues.\nThese make dialogue scenes feel natural and professional.", "min_score": 80}]}}
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
    """Simulate time passing and earning coins"""
    st.session_state.time_spent_mins += minutes
    # 30 mins = 100 TvC
    earned = int(minutes * (COINS_PER_30_MIN / 30))
    st.session_state.wallet_tvc += earned
    st.toast(f"⏱️ {minutes} mins passed. You earned {earned} TvC!")

def unlock_industry(ind_name):
    if st.session_state.wallet_tvc >= PREMIUM_ACCESS_COST_TVC:
        st.session_state.wallet_tvc -= PREMIUM_ACCESS_COST_TVC
        st.session_state.unlocked_industries.append(ind_name)
        st.toast(f"🔓 Successfully unlocked {ind_name}!")
        time.sleep(1)
        st.rerun()
    else:
        st.error(f"Insufficient TvC! You need {PREMIUM_ACCESS_COST_TVC} TvC ($3.00 value).")

def assess_submission(submission_text):
    """Simulate AI Coach Grading"""
    if len(submission_text) < 10:
        return 0, "Submission too short. Please elaborate on your strategy."
    
    score = random.randint(75, 100) # Biased towards success for demo flow
    
    if score >= 80:
        feedback = "Excellent work. Your understanding of the core concept is solid."
    else:
        feedback = "Does not meet the 80% threshold. Review the AI Lecture and try again."
        
    return score, feedback

def generate_pdf_with_logo():
    pdf = FPDF()
    pdf.add_page()
    
    # --- LOGO INTEGRATION ---
    # Attempts to find the logo file. 
    logo_path = "turnve_logo.png" 
    if os.path.exists(logo_path):
        # Place logo in top right corner, width 30mm
        pdf.image(logo_path, x=170, y=10, w=30)
    
    # --- HEADER ---
    pdf.set_font("Arial", 'B', 24)
    # Move cursor down to not overlap with logo if it exists
    pdf.ln(10)
    pdf.cell(0, 15, "Turnve", ln=True, align='L')
    
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Proof of Experience Certification", ln=True, align='L')
    pdf.line(10, 35, 200, 35) # Horizontal line
    pdf.ln(10)
    
    # ---CANDIDATE INFO ---
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Candidate Reference: TRN-{random.randint(10000,99999)}", ln=True)
    pdf.cell(0, 8, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Certification Details", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, "Industry:", border=1)
    pdf.cell(0, 10, f" {st.session_state.industry}", border=1, ln=True)

pdf.cell(50, 10, "Role Specialization:", border=1)
pdf.cell(0, 10, f" {st.session_state.role_obj['title']}", border=1, ln=True)
pdf.cell(50, 10, "Project Completed:", border=1)
pdf.cell(0, 10, f" {st.session_state.role_obj['project']['title']}", border=1, ln=True)
pdf.ln(10)
    
# --- VERIFIED SKILLS ---
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "Verified Competencies", ln=True)

pdf.set_font("Arial", '', 11)
for task in st.session_state.completed_tasks:
    pdf.cell(
        0,
        8,
        f"[x] {task} - Assessed by AI Coach (Score: >80%)",
        ln=True
    )

pdf.cell(50, 10, "Role Specialization:", border=1)
pdf.cell(0, 10, f" {st.session_state.role_obj['title']}", border=1, ln=True)

pdf.ln(20)
pdf.set_font("Arial", 'B', 10)
pdf.set_text_color(100, 100, 100) # Gray
pdf.multi_cell(0, 5, "This document certifies that the holder has successfully completed a professional career simulation on the Turnve Platform. All tasks were graded against industry standards.", align='C')
return pdf.output(dest="S").encode("latin-1")

# -----------------------------
# 6. SIDEBAR: WALLET & NAV
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
# 7. MAIN APP UI
# -----------------------------
st.title("Turnve Career Simulation")

# =======================
# STEP 1: INDUSTRY GRID
# =======================
if st.session_state.step == "industry":
    st.subheader("Select Industry")
    st.info("Accumulate TvC coins to unlock premium industries.")

# 4x2 Grid
    industry_names = list(FULL_DB.keys()) # Get keys from the full DB
    rows = [industry_names[i:i + 4] for i in range(0, len(industry_names), 4)]
    
    for row in rows:
        cols = st.columns(4)
        for idx, ind_name in enumerate(row):
            # Check DB config
            is_freemium = FULL_DB.get(ind_name, {}).get("freemium", False)
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
                            if st.button(f"Unlock", key=f"ulk_{ind_name}"):
                                unlock_industry(ind_name)

# =======================
# STEP 2: ROLE SELECTION
# =======================
if st.session_state.step == "role":
    st.button("← Back", on_click=lambda: st.session_state.update(step="industry"))
    st.header(f"{st.session_state.industry}: Role Selection")
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
    st.error("Error: Industry data missing.")

# =======================
# STEP 3: IMMERSIVE WORKSPACE
# =======================
if st.session_state.step == "workspace":
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
        
        st.write("---")
        st.markdown("###  Certification Ready")
        st.write("Your work has been verified. Download your official Proof of Experience below.")
        
        pdf_bytes = generate_pdf_with_logo()
        st.download_button("Download Proof of Experience (PDF)", pdf_bytes, "turnve_portfolio.pdf", "application/pdf")

if st.button("Return to Dashboard"):
            for k in defaults.keys():
                del st.session_state[k]
            st.rerun()
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
    user_input = st.text_area("Analyze findings and type your solution here...", height=200, key=f"input_{current_idx}")

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
                    time.sleep(1)
                    st.rerun()
                else:
                    time.sleep(1)
                    st.rerun()
            else:
                st.error(f"Failed. Score: {score}% (Required: {current_task['min_score']}%)")
                st.write(f"Coach: {feedback}")
                st.warning("Please study the lecture notes on the right and try again.")

with col_coach:
    with st.container(border=True):
        st.markdown("###  AI Coach")
        st.info("I have prepared a lecture for this specific task. Read carefully.")

        # --- THE AI LECTURE (SAFE/ANONYMOUS) ---
        st.markdown("---")
        st.markdown(current_task['ai_lecture_content'])
        st.markdown("---")

        st.caption("You must achieve ≥80% to proceed. Do not leave this screen")