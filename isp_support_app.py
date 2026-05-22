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
                st.
