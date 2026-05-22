import streamlit as st
import sqlite3
import json
import random
import datetime

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ISP AI Support",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}
.stApp {
    background: #0d0e11;
}
.main .block-container {
    padding: 2rem 2rem 4rem;
    max-width: 1100px;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top bar ── */
.topbar {
    background: linear-gradient(135deg, #0f1117 0%, #141821 100%);
    border: 1px solid #1e2533;
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-left: 4px solid #3b82f6;
}
.topbar-brand { display: flex; align-items: center; gap: 14px; }
.topbar-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.topbar-title { font-size: 22px; font-weight: 700; color: #f1f5f9; }
.topbar-sub { font-size: 12px; color: #64748b; font-family: 'JetBrains Mono', monospace; letter-spacing: .05em; }
.status-pill {
    background: rgba(34, 197, 94, .12);
    border: 1px solid rgba(34, 197, 94, .3);
    color: #22c55e;
    padding: 6px 14px; border-radius: 20px;
    font-size: 12px; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 6px;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #22c55e;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

/* ── Role cards ── */
.role-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 8px; }
.role-card {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 14px;
    padding: 28px 24px;
    cursor: pointer;
    transition: all .2s;
    text-align: center;
}
.role-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
.role-card.selected { border-color: #3b82f6; background: rgba(59, 130, 246, .08); }
.role-icon { font-size: 36px; margin-bottom: 12px; }
.role-title { font-size: 18px; font-weight: 700; color: #f1f5f9; margin-bottom: 6px; }
.role-desc { font-size: 13px; color: #64748b; }

/* ── Metric cards ── */
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }
.metric-card {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 12px;
    padding: 18px 20px;
}
.metric-num { font-size: 28px; font-weight: 700; color: #f1f5f9; }
.metric-lbl { font-size: 12px; color: #64748b; font-family: 'JetBrains Mono', monospace; margin-top: 4px; letter-spacing: .04em; }
.metric-num.red { color: #ef4444; }
.metric-num.yellow { color: #f59e0b; }
.metric-num.green { color: #22c55e; }
.metric-num.blue { color: #3b82f6; }

/* ── Section header ── */
.sec-hdr {
    font-size: 13px; font-weight: 600; color: #64748b;
    letter-spacing: .07em; text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin: 24px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2533;
}

/* ── Ticket card ── */
.ticket-card {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    border-left: 3px solid #3b82f6;
}
.ticket-card.high { border-left-color: #ef4444; }
.ticket-card.medium { border-left-color: #f59e0b; }
.ticket-card.low { border-left-color: #22c55e; }
.ticket-card.resolved { border-left-color: #475569; opacity: .7; }

.ticket-hdr { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.ticket-id { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #94a3b8; }
.ticket-status { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
.s-open { background: rgba(59,130,246,.15); color: #60a5fa; }
.s-resolved { background: rgba(71,85,105,.15); color: #94a3b8; }

.ticket-issue { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 6px; }
.ticket-meta { display: flex; gap: 10px; flex-wrap: wrap; }
.tag {
    font-size: 11px; font-weight: 600; padding: 3px 10px;
    border-radius: 20px; font-family: 'JetBrains Mono', monospace;
}
.tag-high { background: rgba(239,68,68,.12); color: #ef4444; }
.tag-medium { background: rgba(245,158,11,.12); color: #f59e0b; }
.tag-low { background: rgba(34,197,94,.12); color: #22c55e; }
.tag-tech { background: rgba(59,130,246,.12); color: #60a5fa; }
.tag-cat { background: rgba(139,92,246,.12); color: #a78bfa; }
.tag-sent { background: rgba(100,116,139,.12); color: #94a3b8; }

/* ── Chat ── */
.chat-msg-user {
    display: flex; justify-content: flex-end; margin-bottom: 14px;
}
.chat-msg-ai {
    display: flex; justify-content: flex-start; margin-bottom: 14px;
}
.bubble-user {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: #fff;
    padding: 12px 16px; border-radius: 18px 18px 4px 18px;
    max-width: 72%; font-size: 14px; line-height: 1.5;
}
.bubble-ai {
    background: #141821;
    border: 1px solid #1e2533;
    color: #e2e8f0;
    padding: 14px 18px; border-radius: 4px 18px 18px 18px;
    max-width: 80%; font-size: 14px; line-height: 1.6;
}
.ai-label {
    font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace;
    margin-bottom: 6px; display: flex; align-items: center; gap: 6px;
}
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #3b82f6; }

/* ── Ticket result box ── */
.result-box {
    background: #080c12;
    border: 1px solid #1e2533;
    border-radius: 12px;
    padding: 16px 18px;
    margin-top: 12px;
}
.result-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.result-reply {
    background: rgba(59,130,246,.06);
    border: 1px solid rgba(59,130,246,.2);
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 13px; color: #cbd5e1; line-height: 1.6;
}
.result-reply-lbl {
    font-size: 10px; color: #3b82f6; font-family: 'JetBrains Mono', monospace;
    letter-spacing: .06em; text-transform: uppercase; margin-bottom: 6px;
}
.ticket-id-big {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px; color: #f59e0b;
    background: rgba(245,158,11,.1);
    border: 1px solid rgba(245,158,11,.25);
    padding: 4px 12px; border-radius: 6px;
    display: inline-block; margin-bottom: 10px;
}
.tech-assign {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; color: #60a5fa;
    background: rgba(59,130,246,.08);
    border: 1px solid rgba(59,130,246,.2);
    padding: 4px 12px; border-radius: 6px;
    display: inline-block; margin-left: 8px;
}

/* ── Login form ── */
.login-box {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 16px;
    padding: 32px 28px;
    max-width: 420px;
    margin: 0 auto;
}
.login-title { font-size: 20px; font-weight: 700; color: #f1f5f9; margin-bottom: 6px; }
.login-sub { font-size: 13px; color: #64748b; margin-bottom: 24px; }
.otp-preview {
    background: rgba(34,197,94,.08);
    border: 1px solid rgba(34,197,94,.25);
    border-radius: 8px;
    padding: 12px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px; color: #22c55e;
    margin-bottom: 16px;
    text-align: center;
    letter-spacing: .1em;
}

/* ── Streamlit component overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #0f1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,.2) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all .2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,.3) !important;
}
.stButton > button[kind="secondary"] {
    background: #1e2533 !important;
    color: #94a3b8 !important;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #1e2533;
    border-radius: 12px;
    overflow: hidden;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0f1117;
    border-bottom: 1px solid #1e2533;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: .04em !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom-color: #3b82f6 !important;
    background: transparent !important;
}
.stAlert { border-radius: 10px !important; }

/* ── Customer info card ── */
.cust-card {
    background: linear-gradient(135deg, #0f1421 0%, #0f1117 100%);
    border: 1px solid #1e2533;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 20px;
}
.cust-name { font-size: 20px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }
.cust-meta { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 10px; }
.cust-chip {
    background: rgba(30,37,51,.8);
    border: 1px solid #263146;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px; color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}
.cust-chip span { color: #e2e8f0; margin-left: 4px; }
.outage-warn {
    background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,.25);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px; color: #fca5a5;
    margin-top: 10px;
    display: flex; align-items: center; gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────
@st.cache_resource
def get_db():
    conn = sqlite3.connect("isp_system.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT UNIQUE, package TEXT, area TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT, customer_phone TEXT, issue TEXT,
        priority TEXT, sentiment TEXT, technician TEXT,
        status TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS outages (
        area TEXT UNIQUE, status TEXT, expected_fix_time TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS bills (
        customer_phone TEXT UNIQUE, amount INTEGER, due_date TEXT)""")
    conn.commit()

    # Seed data
    try:
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES('Ali Khan','03001234567','Gaming Pro','DHA')")
        c.execute("INSERT OR IGNORE INTO outages(area,status,expected_fix_time) VALUES('DHA','DOWN','2 Hours')")
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES('03001234567',5400,'2026-05-30')")
        conn.commit()
    except:
        pass
    return conn

conn = get_db()

def db():
    return conn.cursor()

# ─────────────────────────────────────────
# AI MODEL
# ─────────────────────────────────────────
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
    input_variables=["customer_type","name","current_package","area",
                     "network_status","fix_time","bill_info","history_text","plans","message"],
    template="""
You are a professional ISP AI support agent for a Pakistani internet provider.

Customer: {name} ({customer_type})
Package: {current_package}
Area: {area}
Network Status: {network_status} | Fix Time: {fix_time}
Bill: {bill_info}
History: {history_text}
Available Plans: {plans}

Message: {message}

Rules:
- Detect sentiment
- Assign priority (High/Medium/Low)
- Recommend technician if needed
- Mention outage if area is DOWN
- Support both Urdu and English
- Be empathetic and professional
- Keep reply concise (2-4 sentences)

Return ONLY valid JSON, no markdown:
{{"category":"","priority":"","sentiment":"","technician_required":"","reply":""}}
"""
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def gen_ticket_id():
    return f"ISP-{datetime.datetime.now().year}-{random.randint(1000,9999)}"

def gen_tech():
    return f"TECH-{random.randint(100,999)}"

def process_ticket(llm, phone, customer_type, name, current_package,
                   area, network_status, fix_time, bill_info, history_text, message):
    try:
        prompt_text = PROMPT_TEMPLATE.format(
            customer_type=customer_type, name=name,
            current_package=current_package, area=area,
            network_status=network_status, fix_time=fix_time,
            bill_info=bill_info, history_text=history_text,
            plans=PLANS, message=message
        )
        response = llm.invoke(prompt_text)
        raw = response.content.strip().replace("```json","").replace("```","").strip()
        import re
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        result = json.loads(m.group(0) if m else raw)

        ticket_id = gen_ticket_id()
        technician = gen_tech() if result.get("technician_required","").lower() == "yes" else "Not Assigned"

        c = db()
        c.execute("INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)", (
            ticket_id, phone,
            result.get("category","General"),
            result.get("priority","Medium"),
            result.get("sentiment","Neutral"),
            technician, "Open",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        result["ticket_id"] = ticket_id
        result["technician"] = technician
        return result, None
    except Exception as e:
        return None, str(e)

def pri_tag(p):
    cls = {"High":"tag-high","Medium":"tag-medium","Low":"tag-low"}.get(p,"tag-low")
    return f'<span class="tag {cls}">{p}</span>'

def sent_tag(s):
    return f'<span class="tag tag-sent">{s}</span>'

def cat_tag(c):
    return f'<span class="tag tag-cat">{c}</span>'

def tech_tag(t):
    if t == "Not Assigned":
        return f'<span class="tag tag-sent">{t}</span>'
    return f'<span class="tag tag-tech">🔧 {t}</span>'

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
defaults = {
    "screen": "role",        # role | customer_login | otp | customer | admin_login | admin
    "phone": "",
    "otp": None,
    "customer": None,
    "customer_type": "",
    "bill_info": "",
    "network_status": "ACTIVE",
    "fix_time": "N/A",
    "history_text": "",
    "chat": [],
    "api_key": "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",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-icon">🌐</div>
    <div>
      <div class="topbar-title">ConnectPK ISP</div>
      <div class="topbar-sub">AI CUSTOMER SUPPORT SYSTEM</div>
    </div>
  </div>
  <div class="status-pill"><div class="status-dot"></div> SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# SCREEN: ROLE SELECTION
# ═══════════════════════════════════════════════
if st.session_state.screen == "role":
    st.markdown("<div style='text-align:center;margin-bottom:8px;'><span style='font-size:14px;color:#64748b;'>Select your role to continue</span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="role-card">
          <div class="role-icon">👤</div>
          <div class="role-title">Customer</div>
          <div class="role-desc">Get AI-powered support for your internet issues, billing, and upgrades</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Login as Customer", key="btn_cust"):
            st.session_state.screen = "customer_login"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="role-card">
          <div class="role-icon">🛠️</div>
          <div class="role-title">Admin</div>
          <div class="role-desc">Manage customers, tickets, outages, and resolve support requests</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Login as Admin", key="btn_admin"):
            st.session_state.screen = "admin_login"
            st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: CUSTOMER PHONE LOGIN
# ═══════════════════════════════════════════════
elif st.session_state.screen == "customer_login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="login-box">
          <div class="login-title">📱 Customer Login</div>
          <div class="login-sub">Enter your registered phone number to receive an OTP</div>
        </div>""", unsafe_allow_html=True)
        phone = st.text_input("Phone Number", placeholder="03001234567", key="phone_input")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Send OTP →", key="send_otp"):
                if phone.strip():
                    otp = random.randint(1000, 9999)
                    st.session_state.phone = phone.strip()
                    st.session_state.otp = otp
                    st.session_state.screen = "otp"
                    st.rerun()
                else:
                    st.error("Please enter a phone number.")
        with c2:
            if st.button("← Back", key="back_role"):
                st.session_state.screen = "role"
                st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: OTP VERIFICATION
# ═══════════════════════════════════════════════
elif st.session_state.screen == "otp":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown(f"""
        <div class="login-box">
          <div class="login-title">🔐 OTP Verification</div>
          <div class="login-sub">A one-time password has been sent to {st.session_state.phone}</div>
          <div class="otp-preview">OTP: {st.session_state.otp}</div>
        </div>""", unsafe_allow_html=True)
        entered = st.text_input("Enter OTP", placeholder="Enter 4-digit OTP", key="otp_input")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Verify & Login →", key="verify_otp"):
                if entered.strip() == str(st.session_state.otp):
                    phone = st.session_state.phone
                    c = db()
                    c.execute("SELECT name,package,area FROM customers WHERE phone=?", (phone,))
                    cust = c.fetchone()

                    if cust:
                        st.session_state.customer = {"name": cust[0], "package": cust[1], "area": cust[2]}
                        st.session_state.customer_type = "Existing Customer"
                        area = cust[2]
                    else:
                        st.session_state.customer = None
                        st.session_state.customer_type = "New Customer"
                        area = ""

                    # Bill
                    c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,))
                    bill = c.fetchone()
                    st.session_state.bill_info = f"PKR {bill[0]}, Due: {bill[1]}" if bill else "No billing record"

                    # Outage
                    if area:
                        c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (area,))
                        out = c.fetchone()
                        if out:
                            st.session_state.network_status = out[0]
                            st.session_state.fix_time = out[1]

                    # History
                    c.execute("SELECT issue FROM tickets WHERE customer_phone=?", (phone,))
                    rows = c.fetchall()
                    st.session_state.history_text = "\n".join([f"- {r[0]}" for r in rows]) if rows else "No previous tickets."

                    st.session_state.screen = "new_customer" if not cust else "customer"
                    st.session_state.chat = []
                    st.rerun()
                else:
                    st.error("Invalid OTP. Please try again.")
        with c2:
            if st.button("← Back", key="back_login"):
                st.session_state.screen = "customer_login"
                st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: NEW CUSTOMER REGISTRATION
# ═══════════════════════════════════════════════
elif st.session_state.screen == "new_customer":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="login-box">
          <div class="login-title">🆕 New Customer Registration</div>
          <div class="login-sub">Complete your profile to get started</div>
        </div>""", unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="Ali Khan")
        area = st.selectbox("Your Area", ["DHA","Gulshan","PECHS","Clifton","Nazimabad","Korangi","North Karachi","Malir","Other"])
        if st.button("Register & Continue →", key="register"):
            if name.strip():
                phone = st.session_state.phone
                c = db()
                c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                          (name.strip(), phone, "No Package", area))
                conn.commit()
                # Outage check
                c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (area,))
                out = c.fetchone()
                if out:
                    st.session_state.network_status = out[0]
                    st.session_state.fix_time = out[1]
                st.session_state.customer = {"name": name.strip(), "package": "No Package", "area": area}
                st.session_state.screen = "customer"
                st.rerun()
            else:
                st.error("Please enter your name.")

# ═══════════════════════════════════════════════
# SCREEN: CUSTOMER CHAT
# ═══════════════════════════════════════════════
elif st.session_state.screen == "customer":
    cust = st.session_state.customer
    phone = st.session_state.phone
    llm = get_llm(st.session_state.api_key)

    # Customer card
    outage_html = ""
    if st.session_state.network_status == "DOWN":
        outage_html = f'<div class="outage-warn">⚠️ <b>Network Outage in {cust["area"]}</b> — Expected fix: {st.session_state.fix_time}</div>'

    st.markdown(f"""
    <div class="cust-card">
      <div class="cust-name">👋 Welcome back, {cust["name"]}</div>
      <div class="cust-meta">
        <div class="cust-chip">📱 <span>{phone}</span></div>
        <div class="cust-chip">📦 <span>{cust["package"]}</span></div>
        <div class="cust-chip">📍 <span>{cust["area"]}</span></div>
        <div class="cust-chip">💳 <span>{st.session_state.bill_info}</span></div>
      </div>
      {outage_html}
    </div>
    """, unsafe_allow_html=True)

    # Logout
    if st.button("Logout", key="logout_cust"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

    # Quick suggestions
    st.markdown("<div class='sec-hdr'>Quick Topics</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    suggestions = ["🐌 Slow internet", "💳 Check my bill", "⬆️ Upgrade plan", "📡 WiFi issue"]
    for i, s in enumerate(suggestions):
        with cols[i]:
            if st.button(s, key=f"sug_{i}"):
                st.session_state.chat.append({"role": "user", "text": s.split(" ", 1)[1]})
                with st.spinner("AI is analyzing…"):
                    result, err = process_ticket(
                        llm, phone,
                        st.session_state.customer_type,
                        cust["name"], cust["package"], cust["area"],
                        st.session_state.network_status, st.session_state.fix_time,
                        st.session_state.bill_info, st.session_state.history_text,
                        s.split(" ", 1)[1]
                    )
                if result:
                    st.session_state.chat.append({"role": "ai", "result": result})
                else:
                    st.session_state.chat.append({"role": "ai", "error": err})
                st.rerun()

    # Chat history
    st.markdown("<div class='sec-hdr'>Conversation</div>", unsafe_allow_html=True)

    if not st.session_state.chat:
        st.markdown("""
        <div style='text-align:center;padding:32px;color:#475569;'>
          <div style='font-size:32px;margin-bottom:8px;'>💬</div>
          <div style='font-size:14px;'>Ask anything about your internet service</div>
        </div>""", unsafe_allow_html=True)

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-msg-user">
              <div class="bubble-user">{msg["text"]}</div>
            </div>""", unsafe_allow_html=True)
        elif msg["role"] == "ai":
            if "error" in msg:
                st.error(f"Error: {msg['error']}")
            else:
                r = msg["result"]
                tech_html = f'<span class="tech-assign">🔧 {r["technician"]}</span>' if r["technician"] != "Not Assigned" else ""
                st.markdown(f"""
                <div class="chat-msg-ai">
                  <div class="bubble-ai">
                    <div class="ai-label"><div class="ai-dot"></div> ISP AI Support Agent</div>
                    <div class="result-box">
                      <div style="margin-bottom:10px;">
                        <span class="ticket-id-big">🎫 {r["ticket_id"]}</span>
                        {tech_html}
                      </div>
                      <div class="result-row">
                        {cat_tag(r.get("category","General"))}
                        {pri_tag(r.get("priority","Medium"))}
                        {sent_tag(r.get("sentiment","Neutral"))}
                      </div>
                      <div class="result-reply">
                        <div class="result-reply-lbl">AI Response</div>
                        {r.get("reply","")}
                      </div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_msg = st.text_input("Your Message", placeholder="Type your issue here… (English or Urdu)", label_visibility="collapsed")
        submitted = st.form_submit_button("Send Message →")
        if submitted and user_msg.strip():
            st.session_state.chat.append({"role": "user", "text": user_msg.strip()})
            with st.spinner("AI is analyzing your issue…"):
                result, err = process_ticket(
                    llm, phone,
                    st.session_state.customer_type,
                    cust["name"], cust["package"], cust["area"],
                    st.session_state.network_status, st.session_state.fix_time,
                    st.session_state.bill_info, st.session_state.history_text,
                    user_msg.strip()
                )
            if result:
                st.session_state.chat.append({"role": "ai", "result": result})
            else:
                st.session_state.chat.append({"role": "ai", "error": err})
            st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: ADMIN LOGIN
# ═══════════════════════════════════════════════
elif st.session_state.screen == "admin_login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="login-box">
          <div class="login-title">🔐 Admin Access</div>
          <div class="login-sub">Enter your admin credentials to access the dashboard</div>
        </div>""", unsafe_allow_html=True)
        pwd = st.text_input("Admin Password", type="password", placeholder="Enter password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login →", key="admin_go"):
                if pwd == "admin123":
                    st.session_state.screen = "admin"
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        with c2:
            if st.button("← Back", key="back_admin"):
                st.session_state.screen = "role"
                st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: ADMIN DASHBOARD
# ═══════════════════════════════════════════════
elif st.session_state.screen == "admin":
    c = db()

    # Metrics
    c.execute("SELECT COUNT(*) FROM customers"); total_cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets"); total_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'"); open_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE priority='High' AND status='Open'"); high_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM outages WHERE status='DOWN'"); outages = c.fetchone()[0]

    col_logout, _ = st.columns([1, 5])
    with col_logout:
        if st.button("← Logout", key="admin_logout"):
            st.session_state.screen = "role"
            st.rerun()

    st.markdown("""
    <div class="metric-grid">
      <div class="metric-card"><div class="metric-num blue">{tc}</div><div class="metric-lbl">Total Customers</div></div>
      <div class="metric-card"><div class="metric-num">{tt}</div><div class="metric-lbl">Total Tickets</div></div>
      <div class="metric-card"><div class="metric-num yellow">{ot}</div><div class="metric-lbl">Open Tickets</div></div>
      <div class="metric-card"><div class="metric-num red">{ht}</div><div class="metric-lbl">High Priority Open</div></div>
    </div>
    """.format(tc=total_cust, tt=total_tick, ot=open_tick, ht=high_tick), unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎫  Tickets", "👥  Customers", "📡  Outages", "⚙️  Manage"])

    with tab1:
        st.markdown("<div class='sec-hdr'>All Tickets</div>", unsafe_allow_html=True)
        c.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        rows = c.fetchall()
        if rows:
            for row in rows:
                tid, tphone, issue, priority, sentiment, tech, status, created = row
                card_cls = "resolved" if status == "Resolved" else priority.lower()
                st.markdown(f"""
                <div class="ticket-card {card_cls}">
                  <div class="ticket-hdr">
                    <div style="display:flex;align-items:center;gap:10px;">
                      <span class="ticket-id">{tid}</span>
                      <span class="ticket-id">📱 {tphone}</span>
                    </div>
                    <span class="ticket-status {'s-resolved' if status=='Resolved' else 's-open'}">{status}</span>
                  </div>
                  <div class="ticket-issue">{issue}</div>
                  <div class="ticket-meta">
                    {pri_tag(priority)}
                    {cat_tag(issue)}
                    {sent_tag(sentiment)}
                    {tech_tag(tech)}
                    <span class="tag tag-sent">🕐 {created}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No tickets found.")

    with tab2:
        st.markdown("<div class='sec-hdr'>Registered Customers</div>", unsafe_allow_html=True)
        c.execute("SELECT name,phone,package,area FROM customers")
        rows = c.fetchall()
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=["Name","Phone","Package","Area"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No customers found.")

    with tab3:
        st.markdown("<div class='sec-hdr'>Network Outages</div>", unsafe_allow_html=True)
        c.execute("SELECT * FROM outages")
        rows = c.fetchall()
        if rows:
            for row in rows:
                area_n, status_n, fix_n = row
                color = "#ef4444" if status_n == "DOWN" else "#22c55e"
                st.markdown(f"""
                <div style="background:#0f1117;border:1px solid #1e2533;border-radius:10px;padding:14px 18px;margin-bottom:8px;border-left:3px solid {color};">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <div style="font-size:15px;font-weight:700;color:#f1f5f9;">📍 {area_n}</div>
                      <div style="font-size:12px;color:#64748b;margin-top:4px;font-family:monospace;">Expected fix: {fix_n}</div>
                    </div>
                    <span style="background:{'rgba(239,68,68,.12)' if status_n=='DOWN' else 'rgba(34,197,94,.12)'};color:{color};padding:5px 14px;border-radius:20px;font-size:12px;font-weight:700;">{status_n}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No outages recorded.")

        # Add outage
        st.markdown("<div class='sec-hdr'>Add / Update Outage</div>", unsafe_allow_html=True)
        with st.form("add_outage"):
            oa = st.text_input("Area", placeholder="e.g. Gulshan")
            os = st.selectbox("Status", ["DOWN","ACTIVE"])
            of = st.text_input("Expected Fix Time", placeholder="e.g. 3 Hours")
            if st.form_submit_button("Save Outage"):
                db().execute("INSERT OR REPLACE INTO outages(area,status,expected_fix_time) VALUES(?,?,?)", (oa,os,of))
                conn.commit()
                st.success(f"Outage for {oa} saved.")
                st.rerun()

    with tab4:
        st.markdown("<div class='sec-hdr'>Resolve Ticket</div>", unsafe_allow_html=True)
        with st.form("resolve_form"):
            tid_input = st.text_input("Ticket ID", placeholder="ISP-2026-XXXX")
            if st.form_submit_button("Mark as Resolved ✓"):
                db().execute("UPDATE tickets SET status='Resolved' WHERE ticket_id=?", (tid_input,))
                conn.commit()
                st.success(f"Ticket {tid_input} resolved.")
                st.rerun()

        st.markdown("<div class='sec-hdr'>API Key</div>", unsafe_allow_html=True)
        new_key = st.text_input("Groq API Key", value=st.session_state.api_key, type="password")
        if st.button("Update API Key"):
            st.session_state.api_key = new_key
            st.success("API key updated.")
