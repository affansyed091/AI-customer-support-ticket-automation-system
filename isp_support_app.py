import streamlit as st
import sqlite3
import json
import random
import datetime
import html as htmllib

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="FiberISP AI Support",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# CUSTOM CSS - ENHANCED DESIGN
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 100%); }
.main .block-container { padding: 1.5rem 2rem 4rem; max-width: 1400px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ══════════════════════════════════════════
   HERO HEADER
══════════════════════════════════════════ */
.hero-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 24px;
    padding: 32px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.15);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
    animation: pulse 8s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 0.8; }
}
.hero-content {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.hero-left {
    display: flex;
    align-items: center;
    gap: 24px;
}
.hero-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    box-shadow: 0 10px 40px rgba(99, 102, 241, 0.4);
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
.hero-text h1 {
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -0.03em;
}
.hero-text p {
    font-size: 14px;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.hero-badge {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    padding: 12px 24px;
    border-radius: 50px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    color: #4ade80;
}
.pulse-dot {
    width: 10px;
    height: 10px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 20px #4ade80;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.3; transform: scale(0.8); }
}

/* ══════════════════════════════════════════
   WELCOME SCREEN
══════════════════════════════════════════ */
.welcome-container {
    text-align: center;
    padding: 60px 40px;
    max-width: 900px;
    margin: 0 auto;
}
.welcome-title {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
    letter-spacing: -0.03em;
}
.welcome-subtitle {
    font-size: 18px;
    color: #94a3b8;
    margin-bottom: 60px;
    line-height: 1.6;
}
.choice-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    margin-top: 40px;
}
.choice-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 2px solid rgba(99, 102, 241, 0.15);
    border-radius: 24px;
    padding: 48px 32px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.choice-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    opacity: 0;
    transition: opacity 0.3s;
}
.choice-card:hover {
    border-color: #6366f1;
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
}
.choice-card:hover::before {
    opacity: 1;
}
.choice-icon {
    font-size: 64px;
    margin-bottom: 24px;
    filter: drop-shadow(0 8px 16px rgba(99, 102, 241, 0.3));
}
.choice-title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 12px;
}
.choice-desc {
    font-size: 15px;
    color: #94a3b8;
    line-height: 1.6;
}

/* ══════════════════════════════════════════
   MODERN FORMS
══════════════════════════════════════════ */
.form-container {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 24px;
    padding: 48px;
    max-width: 600px;
    margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.form-title {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 12px;
    text-align: center;
}
.form-subtitle {
    font-size: 15px;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 40px;
    line-height: 1.6;
}

/* ══════════════════════════════════════════
   DASHBOARD CUSTOMER INFO
══════════════════════════════════════════ */
.customer-panel {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.customer-panel::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
}
.customer-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}
.customer-name {
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.customer-chips {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 20px;
}
.info-chip {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 13px;
    color: #c7d2fe;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 8px;
}
.info-chip .label {
    color: #64748b;
}
.info-chip .value {
    color: #ffffff;
    font-weight: 600;
}

/* ══════════════════════════════════════════
   CHAT INTERFACE - ENHANCED
══════════════════════════════════════════ */
.chat-container {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 20px;
    padding: 24px;
    min-height: 500px;
    max-height: 600px;
    overflow-y: auto;
    margin-bottom: 20px;
}
.chat-container::-webkit-scrollbar {
    width: 8px;
}
.chat-container::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
}
.chat-container::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.3);
    border-radius: 4px;
}
.chat-container::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.5);
}
.chat-empty {
    text-align: center;
    padding: 80px 40px;
}
.chat-empty-icon {
    font-size: 64px;
    margin-bottom: 20px;
    opacity: 0.3;
}
.chat-empty-text {
    font-size: 18px;
    color: #64748b;
    line-height: 1.6;
}
.chat-prompt {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 2px solid rgba(99, 102, 241, 0.3);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 24px;
    text-align: center;
}
.chat-prompt-title {
    font-size: 18px;
    font-weight: 700;
    color: #a5b4fc;
    margin-bottom: 8px;
}
.chat-prompt-subtitle {
    font-size: 14px;
    color: #64748b;
}

/* Message Bubbles */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
    animation: slideInRight 0.3s ease;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 20px;
    animation: slideInLeft 0.3s ease;
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
.bubble-user {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff;
    padding: 16px 24px;
    border-radius: 24px 24px 4px 24px;
    max-width: 70%;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    font-weight: 500;
}
.bubble-ai {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #e2e8f0;
    padding: 0;
    border-radius: 4px 24px 24px 24px;
    max-width: 85%;
    font-size: 15px;
    line-height: 1.7;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}
.ai-header {
    background: rgba(99, 102, 241, 0.1);
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.15);
}
.ai-avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}
.ai-name {
    font-size: 13px;
    font-weight: 700;
    color: #a5b4fc;
    font-family: 'JetBrains Mono', monospace;
}
.ai-content {
    padding: 20px 24px;
}
.ai-content p {
    margin-bottom: 12px;
    color: #cbd5e1;
}
.ai-content p:last-child {
    margin-bottom: 0;
}

/* Ticket Badge in AI Response */
.ticket-badge-inline {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.3);
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: #fbbf24;
    margin-top: 12px;
}
.tech-badge-inline {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: #a5b4fc;
    margin-top: 12px;
    margin-left: 8px;
}

/* ══════════════════════════════════════════
   QUICK TOPICS
══════════════════════════════════════════ */
.topics-container {
    margin-bottom: 24px;
}
.topics-label {
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 16px;
    font-family: 'JetBrains Mono', monospace;
}
.topics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
}
.topic-btn {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #94a3b8;
    padding: 14px 20px;
    border-radius: 16px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 10px;
}
.topic-btn:hover {
    border-color: #6366f1;
    background: rgba(99, 102, 241, 0.1);
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
}

/* ══════════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════════ */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.metric-box {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 20px;
    padding: 28px 24px;
    text-align: center;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    opacity: 0;
    transition: opacity 0.3s;
}
.metric-box:hover {
    border-color: #6366f1;
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
}
.metric-box:hover::before {
    opacity: 1;
}
.metric-value {
    font-size: 40px;
    font-weight: 900;
    margin-bottom: 8px;
    letter-spacing: -0.03em;
}
.metric-label {
    font-size: 12px;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.metric-value.blue { color: #6366f1; }
.metric-value.green { color: #4ade80; }
.metric-value.yellow { color: #fbbf24; }
.metric-value.red { color: #f87171; }

/* ══════════════════════════════════════════
   STREAMLIT OVERRIDES
══════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > div:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}
label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
    margin-bottom: 8px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 32px !important;
    transition: all 0.3s !important;
    width: 100% !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.8) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #6366f1 !important;
    color: #ffffff !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 16px;
    padding: 8px;
    gap: 8px;
    border: 1px solid rgba(99, 102, 241, 0.15);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
}
div[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 16px !important;
}
div[data-testid="stChatInput"] input {
    background: transparent !important;
    color: #e2e8f0 !important;
}

/* Admin Section */
.admin-section {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 24px;
}
.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.15);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# DATABASE WITH PRE-REGISTERED CUSTOMER
# ─────────────────────────────────────────
@st.cache_resource
def get_db():
    conn = sqlite3.connect("fiberisp_system.db", check_same_thread=False)
    c = conn.cursor()
    
    # Create tables
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, 
        phone TEXT UNIQUE, 
        package TEXT, 
        area TEXT,
        registered_at TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY, 
        customer_phone TEXT, 
        issue TEXT,
        priority TEXT, 
        sentiment TEXT, 
        technician TEXT,
        status TEXT, 
        created_at TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS bills (
        customer_phone TEXT UNIQUE, 
        amount INTEGER, 
        due_date TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS outages (
        area TEXT UNIQUE, 
        status TEXT, 
        expected_fix_time TEXT
    )""")
    
    conn.commit()
    
    # Insert pre-registered customer: Affan
    try:
        c.execute("""INSERT OR IGNORE INTO customers(name, phone, package, area, registered_at) 
                     VALUES('Affan', '03146532146', 'Gaming Pro', 'Peshawar', ?)""",
                  (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
        c.execute("""INSERT OR IGNORE INTO bills(customer_phone, amount, due_date) 
                     VALUES('03146532146', 4000, '2026-06-15')""")
        conn.commit()
    except:
        pass
    
    return conn

conn = get_db()
def db(): 
    return conn.cursor()

# ─────────────────────────────────────────
# AI MODEL WITH ENHANCED CAPABILITIES
# ─────────────────────────────────────────
@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        temperature=0.4
    )

PLANS = """
• Basic Home    → 25 Mbps  → PKR 2,000/month
• Gaming Pro    → 100 Mbps → PKR 4,000/month  
• Ultra Fiber   → 250 Mbps → PKR 6,500/month
• Extreme Fiber → 500 Mbps → PKR 9,000/month
"""

PAKISTAN_CITIES = [
    "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad",
    "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala",
    "Hyderabad", "Abbottabad", "Mardan", "Sargodha", "Bahawalpur",
    "Sukkur", "Larkana", "Sheikhupura", "Jhang", "Rahim Yar Khan",
    "Gujrat", "Kasur", "Dera Ghazi Khan", "Sahiwal", "Nawabshah",
    "Mingora", "Okara", "Mirpur", "Chiniot", "Sadiqabad"
]

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["customer_type", "name", "phone", "current_package", "area",
                     "bill_info", "history_text", "plans", "message", "action_type"],
    template="""
You are FiberISP AI Assistant, a professional and friendly support agent for FiberISP, Pakistan's leading internet service provider.

CUSTOMER PROFILE:
- Name: {name}
- Phone: {phone}
- Type: {customer_type}
- Current Package: {current_package}
- Area: {area}
- Billing: {bill_info}
- Support History: {history_text}

ACTION TYPE: {action_type}
- If "GREETING": Greet ONCE warmly and ask how you can help
- If "SUPPORT": Handle support request professionally
- If "UPDATE_NAME": Confirm name change and provide new name
- If "SHOW_RECORDS": Display customer information in a structured format

AVAILABLE PLANS:
{plans}

CUSTOMER MESSAGE: {message}

IMPORTANT RULES:
1. Be professional, empathetic, and concise
2. Detect sentiment accurately (Positive/Neutral/Frustrated/Angry)
3. Assign correct priority (High/Medium/Low) based on urgency
4. Recommend technician for hardware/physical issues
5. For name changes: extract new name and confirm the change
6. When showing records: format them clearly with proper structure
7. Keep responses 2-4 sentences unless showing records/detailed info
8. Use emojis sparingly and professionally
9. Always be helpful and solution-oriented

CAPABILITIES:
- Handle complaints, queries, and requests
- Update customer name
- Show billing, package, and support history
- Process upgrade/downgrade requests
- Schedule technician visits
- Explain plans and pricing

Return ONLY valid JSON (no markdown):
{{
    "category": "Support Issue Category",
    "priority": "High/Medium/Low",
    "sentiment": "Positive/Neutral/Frustrated/Angry",
    "technician_required": "yes or no",
    "reply": "Your professional response",
    "action": "none or update_name or show_records",
    "new_data": {{}}
}}
"""
)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def gen_ticket_id(): 
    return f"FIBER-{datetime.datetime.now().year}-{random.randint(10000,99999)}"

def gen_tech(): 
    return f"TECH-{random.randint(1000,9999)}"

def process_message(llm, phone, customer_type, name, current_package, area,
                   bill_info, history_text, message, action_type="SUPPORT"):
    """Process customer message and generate AI response with actions"""
    try:
        prompt_text = PROMPT_TEMPLATE.format(
            customer_type=customer_type, 
            name=name, 
            phone=phone,
            current_package=current_package, 
            area=area,
            bill_info=bill_info, 
            history_text=history_text,
            plans=PLANS, 
            message=message,
            action_type=action_type
        )
        
        response = llm.invoke(prompt_text)
        raw = response.content.strip()
        
        # Clean JSON response
        import re
        raw = raw.replace("```json", "").replace("```", "").strip()
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        result = json.loads(m.group(0) if m else raw)
        
        # Create ticket for support issues
        if action_type == "SUPPORT":
            ticket_id = gen_ticket_id()
            technician = gen_tech() if result.get("technician_required", "").lower() == "yes" else "Not Assigned"
            
            c = db()
            c.execute("""INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)""", (
                ticket_id, 
                phone,
                result.get("category", "General Support"),
                result.get("priority", "Medium"),
                result.get("sentiment", "Neutral"),
                technician, 
                "Open",
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            
            result["ticket_id"] = ticket_id
            result["technician"] = technician
        
        # Handle name update action
        if result.get("action") == "update_name" and "new_data" in result:
            new_name = result["new_data"].get("name")
            if new_name:
                c = db()
                c.execute("UPDATE customers SET name=? WHERE phone=?", (new_name, phone))
                conn.commit()
                result["name_updated"] = True
        
        return result, None
        
    except Exception as e:
        return None, str(e)

# ─────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────
defaults = {
    "screen": "welcome",
    "phone": "",
    "customer": None,
    "customer_type": "",
    "bill_info": "",
    "history_text": "",
    "chat": [],
    "greeted": False,
    "api_key": "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",
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────
# HERO HEADER (SHOWN ON ALL SCREENS)
# ─────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-content">
        <div class="hero-left">
            <div class="hero-icon">🌐</div>
            <div class="hero-text">
                <h1>FiberISP</h1>
                <p>AI-Powered Customer Support</p>
            </div>
        </div>
        <div class="hero-badge">
            <div class="pulse-dot"></div>
            SYSTEM ACTIVE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# SCREEN: WELCOME (EXISTING OR NEW CUSTOMER)
# ═══════════════════════════════════════════════
if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-title">Welcome to FiberISP</div>
        <div class="welcome-subtitle">
            Experience lightning-fast internet with AI-powered support.<br>
            Select your status to continue with personalized assistance.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        choice_col1, choice_col2 = st.columns(2)
        
        with choice_col1:
            st.markdown("""
            <div class="choice-card">
                <div class="choice-icon">👤</div>
                <div class="choice-title">Existing Customer</div>
                <div class="choice-desc">Already have an account? Login with your phone number to access support</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Login", key="existing", use_container_width=True):
                st.session_state.screen = "existing_login"
                st.rerun()
        
        with choice_col2:
            st.markdown("""
            <div class="choice-card">
                <div class="choice-icon">✨</div>
                <div class="choice-title">New Customer</div>
                <div class="choice-desc">New to FiberISP? Register now and get started with premium internet service</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Register", key="new", use_container_width=True):
                st.session_state.screen = "new_register"
                st.rerun()
        
        # Admin access at bottom
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🛠️ Admin Access", key="admin_access", use_container_width=True):
            st.session_state.screen = "admin_login"
            st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: EXISTING CUSTOMER LOGIN
# ═══════════════════════════════════════════════
elif st.session_state.screen == "existing_login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="form-container">
            <div class="form-title">👤 Customer Login</div>
            <div class="form-subtitle">Enter your registered phone number to access your account</div>
        </div>
        """, unsafe_allow_html=True)
        
        phone = st.text_input("Phone Number", placeholder="03XXXXXXXXX", max_chars=11, key="login_phone")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Continue →", key="login_btn"):
                if phone.strip() and len(phone.strip()) == 11:
                    c = db()
                    c.execute("SELECT name, package, area FROM customers WHERE phone=?", (phone.strip(),))
                    cust = c.fetchone()
                    
                    if cust:
                        # Existing customer found
                        st.session_state.phone = phone.strip()
                        st.session_state.customer = {
                            "name": cust[0], 
                            "package": cust[1], 
                            "area": cust[2]
                        }
                        st.session_state.customer_type = "Existing Customer"
                        
                        # Load bill info
                        c.execute("SELECT amount, due_date FROM bills WHERE customer_phone=?", (phone.strip(),))
                        bill = c.fetchone()
                        st.session_state.bill_info = f"PKR {bill[0]:,}, Due: {bill[1]}" if bill else "No billing record"
                        
                        # Load ticket history
                        c.execute("SELECT issue FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5", (phone.strip(),))
                        tickets = c.fetchall()
                        st.session_state.history_text = "\n".join([f"• {t[0]}" for t in tickets]) if tickets else "No previous tickets"
                        
                        st.session_state.chat = []
                        st.session_state.greeted = False
                        st.session_state.screen = "customer"
                        st.rerun()
                    else:
                        st.error("❌ Phone number not found. Please register as a new customer.")
                else:
                    st.error("❌ Please enter a valid 11-digit phone number.")
        
        with col_btn2:
            if st.button("← Back", key="back_login"):
                st.session_state.screen = "welcome"
                st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: NEW CUSTOMER REGISTRATION
# ═══════════════════════════════════════════════
elif st.session_state.screen == "new_register":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="form-container">
            <div class="form-title">✨ New Customer Registration</div>
            <div class="form-subtitle">Complete your profile to get started with FiberISP</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("registration_form"):
            name = st.text_input("Full Name", placeholder="e.g., Ahmed Khan")
            phone = st.text_input("Phone Number", placeholder="03XXXXXXXXX", max_chars=11)
            area = st.selectbox("Select Your City", PAKISTAN_CITIES)
            package = st.selectbox("Choose Internet Package", [
                "Basic Home - 25 Mbps - PKR 2,000/month",
                "Gaming Pro - 100 Mbps - PKR 4,000/month",
                "Ultra Fiber - 250 Mbps - PKR 6,500/month",
                "Extreme Fiber - 500 Mbps - PKR 9,000/month"
            ])
            
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                submit = st.form_submit_button("Register →")
            with col_form2:
                if st.form_submit_button("← Back"):
                    st.session_state.screen = "welcome"
                    st.rerun()
            
            if submit:
                if name.strip() and phone.strip() and len(phone.strip()) == 11:
                    c = db()
                    # Check if phone already exists
                    c.execute("SELECT phone FROM customers WHERE phone=?", (phone.strip(),))
                    if c.fetchone():
                        st.error("❌ This phone number is already registered. Please login instead.")
                    else:
                        # Extract package name
                        package_name = package.split(" - ")[0]
                        
                        # Register new customer
                        c.execute("""INSERT INTO customers(name, phone, package, area, registered_at) 
                                     VALUES(?, ?, ?, ?, ?)""",
                                  (name.strip(), phone.strip(), package_name, area, 
                                   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        
                        # Create initial bill
                        package_prices = {"Basic Home": 2000, "Gaming Pro": 4000, "Ultra Fiber": 6500, "Extreme Fiber": 9000}
                        amount = package_prices.get(package_name, 2000)
                        due_date = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
                        c.execute("INSERT INTO bills(customer_phone, amount, due_date) VALUES(?, ?, ?)",
                                  (phone.strip(), amount, due_date))
                        conn.commit()
                        
                        # Set session state
                        st.session_state.phone = phone.strip()
                        st.session_state.customer = {"name": name.strip(), "package": package_name, "area": area}
                        st.session_state.customer_type = "New Customer"
                        st.session_state.bill_info = f"PKR {amount:,}, Due: {due_date}"
                        st.session_state.history_text = "No previous tickets"
                        st.session_state.chat = []
                        st.session_state.greeted = False
                        st.session_state.screen = "customer"
                        st.success("✅ Registration successful! Redirecting to dashboard...")
                        st.rerun()
                else:
                    st.error("❌ Please fill all fields correctly.")

# ═══════════════════════════════════════════════
# SCREEN: CUSTOMER DASHBOARD
# ═══════════════════════════════════════════════
elif st.session_state.screen == "customer":
    cust = st.session_state.customer
    phone = st.session_state.phone
    llm = get_llm(st.session_state.api_key)
    
    # Customer Info Panel
    st.markdown(f"""
    <div class="customer-panel">
        <div class="customer-header">
            <div class="customer-name">👋 Welcome, {htmllib.escape(cust["name"])}</div>
        </div>
        <div class="customer-chips">
            <div class="info-chip">
                <span class="label">📱 Phone:</span>
                <span class="value">{htmllib.escape(phone)}</span>
            </div>
            <div class="info-chip">
                <span class="label">📦 Package:</span>
                <span class="value">{htmllib.escape(cust["package"])}</span>
            </div>
            <div class="info-chip">
                <span class="label">📍 Area:</span>
                <span class="value">{htmllib.escape(cust["area"])}</span>
            </div>
            <div class="info-chip">
                <span class="label">💳 Bill:</span>
                <span class="value">{htmllib.escape(st.session_state.bill_info)}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("← Logout", key="logout"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["💬 AI Support", "📊 My Account", "📶 Upgrade"])
    
    # ── TAB 1: AI SUPPORT ──
    with tab1:
        # Auto-greet on first load
        if not st.session_state.greeted:
            st.session_state.greeted = True
            with st.spinner("AI Assistant is connecting..."):
                result, err = process_message(
                    llm, phone, st.session_state.customer_type,
                    cust["name"], cust["package"], cust["area"],
                    st.session_state.bill_info, st.session_state.history_text,
                    f"Hello, I'm {cust['name']}", "GREETING"
                )
            if result:
                st.session_state.chat.append({
                    "role": "ai", 
                    "result": result,
                    "is_greeting": True
                })
            st.rerun()
        
        # Quick Topics
        st.markdown("""
        <div class="topics-container">
            <div class="topics-label">Quick Topics - Click for instant help</div>
        </div>
        """, unsafe_allow_html=True)
        
        quick_topics = [
            ("🐌", "Slow internet speed"),
            ("📡", "WiFi not working"),
            ("⛔", "No connection"),
            ("💳", "Check my bill"),
            ("⬆️", "Upgrade plan"),
            ("🔧", "Request technician"),
            ("📋", "Ticket status"),
            ("👤", "Update my name"),
        ]
        
        cols = st.columns(4)
        for i, (icon, label) in enumerate(quick_topics):
            with cols[i % 4]:
                if st.button(f"{icon} {label}", key=f"topic_{i}", use_container_width=True):
                    st.session_state.chat.append({"role": "user", "text": label})
                    
                    with st.spinner("🤖 AI is analyzing..."):
                        action_type = "UPDATE_NAME" if "name" in label.lower() else "SUPPORT"
                        result, err = process_message(
                            llm, phone, st.session_state.customer_type,
                            cust["name"], cust["package"], cust["area"],
                            st.session_state.bill_info, st.session_state.history_text,
                            label, action_type
                        )
                    
                    if result:
                        st.session_state.chat.append({"role": "ai", "result": result})
                        # Update customer name if changed
                        if result.get("name_updated"):
                            c = db()
                            c.execute("SELECT name FROM customers WHERE phone=?", (phone,))
                            new_name = c.fetchone()[0]
                            st.session_state.customer["name"] = new_name
                    else:
                        st.session_state.chat.append({"role": "ai", "error": err})
                    
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Chat Container
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat:
                st.markdown("""
                <div class="chat-prompt">
                    <div class="chat-prompt-title">🤖 AI Assistant Ready</div>
                    <div class="chat-prompt-subtitle">Type your message below or select a quick topic above</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for msg in st.session_state.chat:
                    if msg["role"] == "user":
                        st.markdown(f"""
                        <div class="msg-user">
                            <div class="bubble-user">{htmllib.escape(msg["text"])}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif msg["role"] == "ai":
                        if "error" in msg:
                            st.error(f"⚠️ Error: {msg['error']}")
                        else:
                            r = msg["result"]
                            reply = r.get("reply", "")
                            
                            # Build ticket/tech badges
                            badges_html = ""
                            if not msg.get("is_greeting", False):
                                if "ticket_id" in r:
                                    badges_html += f'<div class="ticket-badge-inline">🎫 {htmllib.escape(r["ticket_id"])}</div>'
                                if r.get("technician") and r["technician"] != "Not Assigned":
                                    badges_html += f'<div class="tech-badge-inline">🔧 {htmllib.escape(r["technician"])}</div>'
                            
                            st.markdown(f"""
                            <div class="msg-ai">
                                <div class="bubble-ai">
                                    <div class="ai-header">
                                        <div class="ai-avatar">🤖</div>
                                        <div class="ai-name">FiberISP AI Assistant</div>
                                    </div>
                                    <div class="ai-content">
                                        <p>{htmllib.escape(reply)}</p>
                                        {badges_html}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat Input
        user_input = st.chat_input("Type your message here... (e.g., 'Change my name to Ali' or 'Show my records')")
        if user_input and user_input.strip():
            st.session_state.chat.append({"role": "user", "text": user_input.strip()})
            
            with st.spinner("🤖 AI is thinking..."):
                # Determine action type
                action_type = "SUPPORT"
                if any(word in user_input.lower() for word in ["change", "update", "name"]):
                    action_type = "UPDATE_NAME"
                elif any(word in user_input.lower() for word in ["show", "display", "records", "info", "details"]):
                    action_type = "SHOW_RECORDS"
                
                result, err = process_message(
                    llm, phone, st.session_state.customer_type,
                    cust["name"], cust["package"], cust["area"],
                    st.session_state.bill_info, st.session_state.history_text,
                    user_input.strip(), action_type
                )
            
            if result:
                st.session_state.chat.append({"role": "ai", "result": result})
                # Update customer name if changed
                if result.get("name_updated"):
                    c = db()
                    c.execute("SELECT name FROM customers WHERE phone=?", (phone,))
                    new_name = c.fetchone()[0]
                    st.session_state.customer["name"] = new_name
            else:
                st.session_state.chat.append({"role": "ai", "error": err})
            
            st.rerun()
        
        if st.session_state.chat:
            if st.button("🗑️ Clear Chat", key="clear"):
                st.session_state.chat = []
                st.session_state.greeted = False
                st.rerun()
    
    # ── TAB 2: MY ACCOUNT ──
    with tab2:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Account Overview</div>', unsafe_allow_html=True)
        
        # Billing info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid rgba(251, 191, 36, 0.3); 
                        border-radius: 16px; padding: 24px; text-align: center;">
                <div style="font-size: 12px; color: #64748b; margin-bottom: 8px; font-family: 'JetBrains Mono', monospace;">
                    CURRENT BILL
                </div>
                <div style="font-size: 36px; font-weight: 900; color: #fbbf24; margin-bottom: 8px;">
                    {st.session_state.bill_info.split(',')[0]}
                </div>
                <div style="font-size: 13px; color: #94a3b8;">
                    📅 {st.session_state.bill_info.split('Due:')[1] if 'Due:' in st.session_state.bill_info else 'N/A'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid rgba(99, 102, 241, 0.3); 
                        border-radius: 16px; padding: 24px; text-align: center;">
                <div style="font-size: 12px; color: #64748b; margin-bottom: 8px; font-family: 'JetBrains Mono', monospace;">
                    CURRENT PACKAGE
                </div>
                <div style="font-size: 24px; font-weight: 800; color: #6366f1; margin-bottom: 8px;">
                    {htmllib.escape(cust["package"])}
                </div>
                <div style="font-size: 13px; color: #94a3b8;">
                    📍 {htmllib.escape(cust["area"])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Ticket History
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎫 Recent Support Tickets</div>', unsafe_allow_html=True)
        
        c = db()
        c.execute("""SELECT ticket_id, issue, priority, status, created_at 
                     FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5""", (phone,))
        tickets = c.fetchall()
        
        if tickets:
            for ticket in tickets:
                tid, issue, priority, status, created = ticket
                priority_colors = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#4ade80"}
                priority_color = priority_colors.get(priority, "#94a3b8")
                status_color = "#4ade80" if status == "Resolved" else "#6366f1"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border-left: 3px solid {priority_color}; 
                            border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #94a3b8;">
                            {htmllib.escape(tid)}
                        </span>
                        <span style="background: rgba(99, 102, 241, 0.15); color: {status_color}; 
                                     padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700;">
                            {htmllib.escape(status)}
                        </span>
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px;">
                        {htmllib.escape(issue)}
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span style="background: rgba(248, 113, 113, 0.1); color: {priority_color}; 
                                     padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">
                            {htmllib.escape(priority)}
                        </span>
                        <span style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
                            🕐 {htmllib.escape(created)}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📋 No support tickets yet")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ── TAB 3: UPGRADE PLAN ──
    with tab3:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📶 Upgrade Your Internet Package</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #94a3b8; margin-bottom: 24px;">Current Package: <strong style="color: #6366f1;">{htmllib.escape(cust["package"])}</strong></p>', unsafe_allow_html=True)
        
        plans = [
            ("Basic Home", "25 Mbps", "PKR 2,000", "#4ade80"),
            ("Gaming Pro", "100 Mbps", "PKR 4,000", "#6366f1"),
            ("Ultra Fiber", "250 Mbps", "PKR 6,500", "#8b5cf6"),
            ("Extreme Fiber", "500 Mbps", "PKR 9,000", "#ec4899"),
        ]
        
        cols = st.columns(4)
        for i, (pname, speed, price, color) in enumerate(plans):
            with cols[i]:
                is_current = pname == cust["package"]
                border = f"border: 2px solid {color};" if is_current else f"border: 1px solid rgba(99, 102, 241, 0.15);"
                current_badge = f'<div style="font-size: 10px; color: {color}; font-weight: 700; margin-top: 8px;">✓ CURRENT</div>' if is_current else ""
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e293b, #0f172a); {border}
                            border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 20px; font-weight: 800; color: {color}; margin-bottom: 8px;">
                        {pname}
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; font-family: 'JetBrains Mono', monospace; margin-bottom: 12px;">
                        {speed}
                    </div>
                    <div style="font-size: 28px; font-weight: 900; color: #ffffff;">
                        {price}
                    </div>
                    <div style="font-size: 11px; color: #64748b;">/month</div>
                    {current_badge}
                </div>
                """, unsafe_allow_html=True)
                
                if not is_current:
                    if st.button(f"Upgrade to {pname}", key=f"upgrade_{i}"):
                        upgrade_msg = f"I want to upgrade my plan from {cust['package']} to {pname} ({speed}, {price}/month)"
                        st.session_state.chat.append({"role": "user", "text": upgrade_msg})
                        
                        with st.spinner("Processing upgrade request..."):
                            result, err = process_message(
                                llm, phone, st.session_state.customer_type,
                                cust["name"], cust["package"], cust["area"],
                                st.session_state.bill_info, st.session_state.history_text,
                                upgrade_msg, "SUPPORT"
                            )
                        
                        if result:
                            st.session_state.chat.append({"role": "ai", "result": result})
                            st.success(f"✅ Upgrade request submitted! Check AI Support tab for details.")
                        else:
                            st.error(f"❌ Error: {err}")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# SCREEN: ADMIN LOGIN
# ═══════════════════════════════════════════════
elif st.session_state.screen == "admin_login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="form-container">
            <div class="form-title">🛠️ Admin Access</div>
            <div class="form-subtitle">Enter admin credentials to access the management dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Admin Password", type="password", placeholder="Enter password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Login →", key="admin_login_btn"):
                if password == "admin123":
                    st.session_state.screen = "admin"
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
        
        with col_btn2:
            if st.button("← Back", key="back_admin"):
                st.session_state.screen = "welcome"
                st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: ADMIN DASHBOARD
# ═══════════════════════════════════════════════
elif st.session_state.screen == "admin":
    # Calculate metrics
    c = db()
    c.execute("SELECT COUNT(*) FROM customers")
    total_customers = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'")
    open_tickets = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tickets WHERE priority='High' AND status='Open'")
    high_priority = c.fetchone()[0]
    
    # Logout button
    if st.button("← Logout", key="admin_logout"):
        st.session_state.screen = "welcome"
        st.rerun()
    
    # Metrics
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-box">
            <div class="metric-value blue">{total_customers}</div>
            <div class="metric-label">Total Customers</div>
        </div>
        <div class="metric-box">
            <div class="metric-value">{total_tickets}</div>
            <div class="metric-label">Total Tickets</div>
        </div>
        <div class="metric-box">
            <div class="metric-value yellow">{open_tickets}</div>
            <div class="metric-label">Open Tickets</div>
        </div>
        <div class="metric-box">
            <div class="metric-value red">{high_priority}</div>
            <div class="metric-label">High Priority</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎫 Tickets", "👥 Customers", "📡 Outages", "⚙️ Settings"])
    
    # ── TAB 1: TICKETS ──
    with tab1:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">All Support Tickets</div>', unsafe_allow_html=True)
        
        c.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        tickets = c.fetchall()
        
        if tickets:
            for ticket in tickets:
                tid, tphone, issue, priority, sentiment, tech, status, created = ticket
                priority_colors = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#4ade80"}
                priority_color = priority_colors.get(priority, "#94a3b8")
                status_color = "#4ade80" if status == "Resolved" else "#6366f1"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border-left: 3px solid {priority_color}; 
                            border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="display: flex; gap: 12px; align-items: center;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #94a3b8;">
                                {htmllib.escape(tid)}
                            </span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #64748b;">
                                📱 {htmllib.escape(tphone)}
                            </span>
                        </div>
                        <span style="background: rgba(99, 102, 241, 0.15); color: {status_color}; 
                                     padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700;">
                            {htmllib.escape(status)}
                        </span>
                    </div>
                    <div style="font-size: 15px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px;">
                        {htmllib.escape(issue)}
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                        <span style="background: rgba(248, 113, 113, 0.1); color: {priority_color}; 
                                     padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">
                            {htmllib.escape(priority)}
                        </span>
                        <span style="background: rgba(99, 102, 241, 0.1); color: #a5b4fc; 
                                     padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">
                            {htmllib.escape(sentiment)}
                        </span>
                        <span style="background: rgba(139, 92, 246, 0.1); color: #c4b5fd; 
                                     padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">
                            🔧 {htmllib.escape(tech)}
                        </span>
                        <span style="font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
                            🕐 {htmllib.escape(created)}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📋 No tickets found")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Resolve ticket section
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Resolve Ticket</div>', unsafe_allow_html=True)
        
        with st.form("resolve_ticket"):
            ticket_id = st.text_input("Ticket ID", placeholder="FIBER-2026-XXXXX")
            if st.form_submit_button("✓ Mark as Resolved"):
                if ticket_id.strip():
                    c = db()
                    c.execute("UPDATE tickets SET status='Resolved' WHERE ticket_id=?", (ticket_id.strip(),))
                    conn.commit()
                    st.success(f"✅ Ticket {ticket_id} marked as resolved")
                    st.rerun()
                else:
                    st.error("❌ Please enter a ticket ID")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ── TAB 2: CUSTOMERS ──
    with tab2:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Registered Customers</div>', unsafe_allow_html=True)
        
        c.execute("SELECT name, phone, package, area, registered_at FROM customers ORDER BY registered_at DESC")
        customers = c.fetchall()
        
        if customers:
            import pandas as pd
            df = pd.DataFrame(customers, columns=["Name", "Phone", "Package", "Area", "Registered"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("👥 No customers found")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ── TAB 3: OUTAGES ──
    with tab3:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Network Outages</div>', unsafe_allow_html=True)
        
        c.execute("SELECT * FROM outages")
        outages = c.fetchall()
        
        if outages:
            for outage in outages:
                area, status, fix_time = outage
                status_color = "#f87171" if status == "DOWN" else "#4ade80"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border-left: 3px solid {status_color}; 
                            border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 16px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px;">
                                📍 {htmllib.escape(area)}
                            </div>
                            <div style="font-size: 12px; color: #64748b; font-family: 'JetBrains Mono', monospace;">
                                Expected Fix: {htmllib.escape(fix_time)}
                            </div>
                        </div>
                        <span style="background: {'rgba(248, 113, 113, 0.1)' if status=='DOWN' else 'rgba(74, 222, 128, 0.1)'}; 
                                     color: {status_color}; padding: 6px 16px; border-radius: 20px; 
                                     font-size: 12px; font-weight: 700;">
                            {htmllib.escape(status)}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📡 No outages recorded")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add/Update outage
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Add/Update Outage</div>', unsafe_allow_html=True)
        
        with st.form("manage_outage"):
            outage_area = st.selectbox("Area", PAKISTAN_CITIES)
            outage_status = st.selectbox("Status", ["ACTIVE", "DOWN"])
            outage_time = st.text_input("Expected Fix Time", placeholder="e.g., 2 Hours")
            
            if st.form_submit_button("Save Outage"):
                if outage_time.strip():
                    c = db()
                    c.execute("INSERT OR REPLACE INTO outages(area, status, expected_fix_time) VALUES(?, ?, ?)",
                              (outage_area, outage_status, outage_time.strip()))
                    conn.commit()
                    st.success(f"✅ Outage for {outage_area} saved")
                    st.rerun()
                else:
                    st.error("❌ Please enter fix time")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ── TAB 4: SETTINGS ──
    with tab4:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">API Configuration</div>', unsafe_allow_html=True)
        
        new_api_key = st.text_input("Groq API Key", value=st.session_state.api_key, type="password")
        if st.button("Update API Key"):
            st.session_state.api_key = new_api_key
            st.success("✅ API
