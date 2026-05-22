import streamlit as st
import sqlite3
import json
import random
import datetime
import html as htmllib
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FiberISP AI Support",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS - ENHANCED DESIGN
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp { 
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 100%);
    background-attachment: fixed;
}
.main .block-container { padding: 1.5rem 2rem 4rem; max-width: 1200px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ══════ WELCOME SCREEN ══════ */
.welcome-container {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, rgba(14,165,233,0.1) 0%, rgba(59,130,246,0.05) 100%);
    border-radius: 24px;
    border: 1px solid rgba(14,165,233,0.2);
    margin: 40px 0;
    position: relative;
    overflow: hidden;
}
.welcome-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(14,165,233,0.1) 0%, transparent 70%);
    animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 0.8; }
}
.welcome-logo {
    font-size: 80px;
    margin-bottom: 20px;
    filter: drop-shadow(0 8px 24px rgba(14,165,233,0.4));
    position: relative;
    z-index: 1;
}
.welcome-title {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
    letter-spacing: -0.03em;
    position: relative;
    z-index: 1;
}
.welcome-subtitle {
    font-size: 18px;
    color: #94a3b8;
    margin-bottom: 40px;
    position: relative;
    z-index: 1;
}

/* ══════ TOP BAR ══════ */
.topbar {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 20px;
    padding: 20px 32px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 16px;
}
.topbar-icon {
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, #0ea5e9, #3b82f6);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 6px 24px rgba(14,165,233,0.4);
}
.topbar-title {
    font-size: 24px;
    font-weight: 900;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}
.topbar-sub {
    font-size: 11px;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 2px;
}
.status-pill {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80;
    padding: 8px 20px;
    border-radius: 24px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 8px;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4ade80;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px #4ade80; }
    50% { opacity: 0.3; box-shadow: none; }
}

/* ══════ ROLE CARDS ══════ */
.role-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 20px;
    padding: 40px 28px;
    cursor: pointer;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.role-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(14,165,233,0.1), transparent);
    transition: left 0.5s;
}
.role-card:hover::before {
    left: 100%;
}
.role-card:hover {
    border-color: rgba(14,165,233,0.5);
    transform: translateY(-6px);
    box-shadow: 0 16px 48px rgba(14,165,233,0.2);
}
.role-icon {
    font-size: 48px;
    margin-bottom: 16px;
    filter: drop-shadow(0 4px 16px rgba(14,165,233,0.3));
}
.role-title {
    font-size: 22px;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 10px;
}
.role-desc {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.6;
}

/* ══════ LANGUAGE CARDS ══════ */
.lang-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 20px;
    padding: 36px 28px;
    cursor: pointer;
    text-align: center;
    transition: all 0.3s;
}
.lang-card:hover {
    border-color: #0ea5e9;
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(14,165,233,0.15);
}
.lang-emoji {
    font-size: 56px;
    margin-bottom: 16px;
}
.lang-title {
    font-size: 24px;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 8px;
}
.lang-sub {
    font-size: 14px;
    color: #94a3b8;
}

/* ══════ LOGIN BOX ══════ */
.login-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 24px;
    padding: 40px 36px;
    max-width: 480px;
    margin: 0 auto;
    box-shadow: 0 8px 48px rgba(0,0,0,0.3);
}
.login-title {
    font-size: 24px;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 8px;
}
.login-sub {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 28px;
    line-height: 1.6;
}
.otp-preview {
    background: rgba(14,165,233,0.1);
    border: 2px solid rgba(14,165,233,0.3);
    border-radius: 12px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 32px;
    font-weight: 800;
    color: #0ea5e9;
    margin: 20px 0;
    text-align: center;
    letter-spacing: 0.3em;
}

/* ══════ CUSTOMER CARD ══════ */
.cust-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 24px;
}
.cust-name {
    font-size: 24px;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 16px;
}
.cust-meta {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.cust-chip {
    background: rgba(15,19,32,0.9);
    border: 1px solid rgba(14,165,233,0.15);
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 13px;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}
.cust-chip span {
    color: #f1f5f9;
    margin-left: 6px;
    font-weight: 600;
}

/* ══════ AI ASSISTANCE BANNER ══════ */
.ai-banner {
    background: linear-gradient(135deg, rgba(14,165,233,0.15) 0%, rgba(59,130,246,0.1) 100%);
    border: 2px solid rgba(14,165,233,0.3);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 20px 0;
    text-align: center;
}
.ai-banner-title {
    font-size: 18px;
    font-weight: 700;
    color: #0ea5e9;
    margin-bottom: 8px;
}
.ai-banner-sub {
    font-size: 13px;
    color: #94a3b8;
}

/* ══════ QUICK TOPICS ══════ */
.qtopic-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 16px 0;
}

/* ══════ SECTION HEADERS ══════ */
.sec-hdr {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin: 24px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(14,165,233,0.1);
}

/* ══════ STREAMLIT OVERRIDES ══════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #0f172a !important;
    border: 1px solid rgba(14,165,233,0.2) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.15) !important;
}
label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(14,165,233,0.3) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0f172a;
    border-bottom: 1px solid rgba(14,165,233,0.15);
    gap: 0;
    border-radius: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-bottom: 3px solid transparent !important;
    padding: 14px 24px !important;
}
.stTabs [aria-selected="true"] {
    color: #0ea5e9 !important;
    border-bottom-color: #0ea5e9 !important;
    background: transparent !important;
}

/* ══════ CHAT STYLING ══════ */
div[data-testid="stChatMessageContent"] {
    background: transparent !important;
}
div[data-testid="stChatMessage"] {
    padding: 12px 0 !important;
}

/* ══════ METRIC CARDS ══════ */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.metric-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.15);
    border-radius: 16px;
    padding: 20px 24px;
    transition: border-color 0.2s;
}
.metric-card:hover {
    border-color: rgba(14,165,233,0.3);
}
.metric-num {
    font-size: 32px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.03em;
}
.metric-lbl {
    font-size: 11px;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 6px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.metric-num.red { color: #f87171; }
.metric-num.yellow { color: #fbbf24; }
.metric-num.green { color: #4ade80; }
.metric-num.blue { color: #0ea5e9; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def get_db():
    conn = sqlite3.connect("fifiber_system.db", check_same_thread=False)
    c = conn.cursor()
    
    # Create tables
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        package TEXT,
        area TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT,
        customer_phone TEXT,
        issue TEXT,
        priority TEXT,
        sentiment TEXT,
        technician TEXT,
        status TEXT,
        created_at TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS outages (
        area TEXT UNIQUE,
        status TEXT,
        expected_fix_time TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS bills (
        customer_phone TEXT UNIQUE,
        amount INTEGER,
        due_date TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS new_connection_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        area TEXT,
        package TEXT,
        created_at TEXT
    )""")
    
    conn.commit()
    
    # Insert pre-registered customer: Affan
    try:
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                  ("Affan", "03146532146", "Gaming Pro 100Mbps", "Peshawar - University Town"))
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES(?,?,?)",
                  ("03146532146", 4000, "2026-06-15"))
        conn.commit()
    except:
        pass
    
    return conn

conn = get_db()
def db():
    return conn.cursor()

# ═══════════════════════════════════════════════════════════════
# PAKISTAN LOCATIONS
# ═══════════════════════════════════════════════════════════════
PAKISTAN_LOCATIONS = [
    # Peshawar
    "Peshawar - University Town", "Peshawar - Hayatabad", "Peshawar - Saddar",
    "Peshawar - Board Bazaar", "Peshawar - Gulbahar", "Peshawar - Tehkal",
    # Islamabad
    "Islamabad - F-6", "Islamabad - F-7", "Islamabad - F-8", "Islamabad - F-10",
    "Islamabad - G-6", "Islamabad - G-7", "Islamabad - G-8", "Islamabad - G-9",
    "Islamabad - Blue Area", "Islamabad - I-8", "Islamabad - I-9", "Islamabad - I-10",
    # Rawalpindi
    "Rawalpindi - Satellite Town", "Rawalpindi - Bahria Town", "Rawalpindi - Saddar",
    "Rawalpindi - Commercial Market", "Rawalpindi - PWD", "Rawalpindi - Chaklala",
    # Lahore
    "Lahore - DHA", "Lahore - Gulberg", "Lahore - Model Town", "Lahore - Johar Town",
    "Lahore - Cantt", "Lahore - Faisal Town", "Lahore - Iqbal Town", "Lahore - Garden Town",
    "Lahore - Bahria Town", "Lahore - Township", "Lahore - Allama Iqbal Town",
    # Karachi
    "Karachi - DHA", "Karachi - Clifton", "Karachi - Gulshan", "Karachi - PECHS",
    "Karachi - Nazimabad", "Karachi - Korangi", "Karachi - North Karachi",
    "Karachi - Malir", "Karachi - Saddar", "Karachi - Gulistan-e-Johar",
    # Faisalabad
    "Faisalabad - Peoples Colony", "Faisalabad - Model Town", "Faisalabad - Madina Town",
    "Faisalabad - Susan Road", "Faisalabad - Civil Lines",
    # Multan
    "Multan - Cantt", "Multan - Gulgasht Colony", "Multan - Model Town",
    "Multan - Shah Rukn-e-Alam Colony", "Multan - Bosan Road",
    # Quetta
    "Quetta - Cantt", "Quetta - Satellite Town", "Quetta - Samungli Road",
    # Other cities
    "Sialkot", "Gujranwala", "Abbottabad", "Mardan", "Swat", "Hyderabad", "Sukkur"
]

# ═══════════════════════════════════════════════════════════════
# AI MODEL
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )

PLANS = """
• Basic Home    → 25 Mbps  → PKR 2,000/month
• Gaming Pro    → 100 Mbps → PKR 4,000/month
• Ultra Fiber   → 250 Mbps → PKR 6,500/month
• Extreme Fiber → 500 Mbps → PKR 9,000/month
"""

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["customer_type", "name", "current_package", "area",
                     "network_status", "fix_time", "bill_info", "history_text",
                     "plans", "message", "language", "first_message"],
    template="""
You are a professional ISP AI support agent for FiberISP, a Pakistani internet provider.

Customer: {name} ({customer_type})
Package: {current_package}
Area: {area}
Network Status: {network_status} | Fix Time: {fix_time}
Bill: {bill_info}
Previous Tickets: {history_text}
Available Plans: {plans}

Current Message: {message}
Is First Message: {first_message}

LANGUAGE RULE:
- Customer selected: {language}
- If {language} is "Urdu", reply ENTIRELY in Urdu script (اردو)
- If {language} is "English", reply ENTIRELY in English
- Never mix languages

GREETING RULE:
- If {first_message} is "yes", start with a warm greeting in {language}
- If {first_message} is "no", DO NOT greet - just respond to the issue

Tasks:
1. Detect sentiment: Positive/Neutral/Frustrated/Angry
2. Assign priority: High/Medium/Low
3. Determine category from message
4. Recommend technician if hardware issue: yes/no
5. Mention outage only if status is DOWN
6. Be empathetic, professional, concise (2-4 sentences)

Return ONLY valid JSON (no markdown):
{{"category":"","priority":"","sentiment":"","technician_required":"yes or no","reply":""}}
"""
)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def gen_ticket_id():
    return f"FIB-{datetime.datetime.now().year}-{random.randint(1000, 9999)}"

def gen_tech():
    return f"TECH-{random.randint(100, 999)}"

def process_ticket(llm, phone, customer_type, name, current_package,
                   area, network_status, fix_time, bill_info,
                   history_text, message, language="English", first_message=False):
    try:
        prompt_text = PROMPT_TEMPLATE.format(
            customer_type=customer_type,
            name=name,
            current_package=current_package,
            area=area,
            network_status=network_status,
            fix_time=fix_time,
            bill_info=bill_info,
            history_text=history_text,
            plans=PLANS,
            message=message,
            language=language,
            first_message="yes" if first_message else "no"
        )
        
        response = llm.invoke(prompt_text)
        raw = response.content.strip().replace("```json", "").replace("```", "").strip()
        
        import re
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        result = json.loads(m.group(0) if m else raw)
        
        ticket_id = gen_ticket_id()
        technician = gen_tech() if result.get("technician_required", "").lower() == "yes" else "Not Assigned"
        
        c = db()
        c.execute("INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)", (
            ticket_id,
            phone,
            result.get("category", "General"),
            result.get("priority", "Medium"),
            result.get("sentiment", "Neutral"),
            technician,
            "Open",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        
        result["ticket_id"] = ticket_id
        result["technician"] = technician
        return result, None
    except Exception as e:
        return None, str(e)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════
defaults = {
    "screen": "welcome",
    "phone": "",
    "otp": None,
    "customer": None,
    "customer_type": "",
    "bill_info": "",
    "network_status": "ACTIVE",
    "fix_time": "N/A",
    "history_text": "",
    "chat": [],
    "lang": "",
    "api_key": "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",
    "first_message_sent": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
# TOP BAR
# ═══════════════════════════════════════════════════════════════
if st.session_state.screen != "welcome":
    st.markdown("""
    <div class="topbar">
      <div class="topbar-brand">
        <div class="topbar-icon">🌐</div>
        <div>
          <div class="topbar-title">FiberISP</div>
          <div class="topbar-sub">AI-POWERED SUPPORT SYSTEM</div>
        </div>
      </div>
      <div class="status-pill"><div class="status-dot"></div> ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════════════╗
# ║ SCREEN: WELCOME                                               ║
# ╚═══════════════════════════════════════════════════════════════╝
if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-logo">🌐</div>
        <div class="welcome-title">Welcome to FiberISP</div>
        <div class="welcome-subtitle">Experience lightning-fast fiber internet with AI-powered support</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 40px 0 20px;'><span style='font-size:16px; color:#94a3b8;'>Are you a new or existing customer?</span></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_exist, col_new = st.columns(2, gap="large")
        
        with col_exist:
            st.markdown("""
            <div class="role-card">
              <div class="role-icon">👤</div>
              <div class="role-title">Existing Customer</div>
              <div class="role-desc">Login to access your dashboard and get support</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Login", key="btn_existing", use_container_width=True):
                st.session_state.screen = "lang_select"
                st.session_state.customer_type = "existing"
                st.rerun()
        
        with col_new:
            st.markdown("""
            <div class="role-card">
              <div class="role-icon">🆕</div>
              <div class="role-title">New Customer</div>
              <div class="role-desc">Register to get started with FiberISP</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Register", key="btn_new", use_container_width=True):
                st.session_state.screen = "lang_select"
                st.session_state.customer_type = "new"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Admin button centered below
        col_a, col_b, col_c = st.columns([2, 1, 2])
        with col_b:
            if st.button("🛠️ Admin", key="btn_admin_welcome"):
                st.session_state.screen = "admin_login"
                st.rerun()

# ╔═══════════════════════════════════════════════════════════════╗
# ║ SCREEN: LANGUAGE SELECTION                                    ║
# ╚═══════════════════════════════════════════════════════════════╝
elif st.session_state.screen == "lang_select":
    st.markdown("""
    <div style='text-align:center; margin: 40px 0 28px;'>
      <div style='font-size:32px; font-weight:900; color:#f1f5f9; margin-bottom:12px;'>🌍 Choose Your Language</div>
      <div style='font-size:16px; color:#94a3b8;'>آپ کی پسندیدہ زبان منتخب کریں / Select your preferred language</div>
    </div>
    """, unsafe_allow_html=True)
    
    _, lcol, rcol, _ = st.columns([1, 2, 2, 1])
    
    with lcol:
        st.markdown("""
        <div class="lang-card">
          <div class="lang-emoji">🇬🇧</div>
          <div class="lang-title">English</div>
          <div class="lang-sub">Continue in English</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select English", key="lang_en", use_container_width=True):
            st.session_state.lang = "English"
            if st.session_state.customer_type == "new":
                st.session_state.screen = "new_customer_register"
            else:
                st.session_state.screen = "customer_login"
            st.rerun()
    
    with rcol:
        st.markdown("""
        <div class="lang-card">
          <div class="lang-emoji">🇵🇰</div>
          <div class="lang-title">اردو</div>
          <div class="lang-sub">اردو میں جاری رکھیں</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اردو منتخب کریں", key="lang_ur", use_container_width=True):
            st.session_state.lang = "Urdu"
            if st.session_state.customer_type == "new":
                st.session_state.screen = "new_customer_register"
            else:
                st.session_state.screen = "customer_login"
            st.rerun()

# ╔═══════════════════════════════════════════════════════════════╗
# ║ SCREEN: CUSTOMER LOGIN (PHONE + OTP)                          ║
# ╚═══════════════════════════════════════════════════════════════╝
elif st.session_state.screen == "customer_login":
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="login-box">
          <div class="login-title">📱 Customer Login</div>
          <div class="login-sub">Enter your registered phone number to receive an OTP</div>
        </div>
        """, unsafe_allow_html=True)
        
        phone = st.text_input("Phone Number", placeholder="03001234567", key="phone_input")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Send OTP →", key="send_otp"):
                if phone.strip():
                    # Check if customer exists
                    c = db()
                    c.execute("SELECT name FROM customers WHERE phone=?", (phone.strip(),))
                    cust = c.fetchone()
                    
                    if cust:
                        otp = random.randint(1000, 9999)
                        st.session_state.phone = phone.strip()
                        st.session_state.otp = otp
                        st.session_state.screen = "otp_verify"
                        st.rerun()
                    else:
                        st.error("Phone number not registered. Please register as a new customer.")
                else:
                    st.error("Please enter a phone number.")
        
        with c2:
            if st.button("← Back", key="back_login"):
                st.session_state.screen = "welcome"
                st.rerun()

# ╔═══════════════════════════════════════════════════════════════╗
# ║ SCREEN: OTP VERIFICATION                                      ║
# ╚═══════════════════════════════════════════════════════════════╝
elif st.session_state.screen == "otp_verify":
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown(f"""
        <div class="login-box">
          <div class="login-title">🔐 OTP Verification</div>
          <div class="login-sub">Enter the 4-digit OTP sent to<br><strong style="color:#f1f5f9;">{st.session_state.phone}</strong></div>
          <div class="otp-preview">{st.session_state.otp}</div>
        </div>
        """, unsafe_allow_html=True)
        
        entered = st.text_input("Enter OTP", placeholder="Enter 4-digit code", key="otp_input")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Verify & Login →", key="verify_otp"):
                if entered.strip() == str(st.session_state.otp):
                    phone = st.session_state.phone
                    c = db()
                    
                    # Load customer data
                    c.execute("SELECT name, package, area FROM customers WHERE phone=?", (phone,))
                    c
