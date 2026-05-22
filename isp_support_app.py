````python
import streamlit as st
import sqlite3
import json
import random
import datetime
import html as htmllib
import re

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
ENHANCED_CSS = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #07090f !important;
    color: white;
    font-family: Arial, sans-serif;
}

.block-container {
    max-width: 1200px !important;
    padding-top: 2rem;
}

.topbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:18px 24px;
    background:#0b0e18;
    border:1px solid rgba(255,255,255,.06);
    border-radius:16px;
    margin-bottom:24px;
}

.topbar-brand {
    display:flex;
    align-items:center;
    gap:14px;
}

.topbar-icon {
    width:48px;
    height:48px;
    border-radius:12px;
    background:linear-gradient(135deg,#0ea5e9,#14b8a6);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
}

.topbar-title {
    font-size:20px;
    font-weight:700;
    color:#f0f6ff;
}

.topbar-sub {
    font-size:11px;
    color:#64748b;
    letter-spacing:.08em;
}

.status-pill {
    background:rgba(34,197,94,.1);
    color:#4ade80;
    border:1px solid rgba(34,197,94,.25);
    padding:8px 14px;
    border-radius:30px;
    font-size:12px;
    display:flex;
    align-items:center;
    gap:8px;
}

.status-dot {
    width:8px;
    height:8px;
    border-radius:50%;
    background:#4ade80;
}

.role-card,
.login-box,
.cust-card,
.plan-card,
.ticket-card,
.nc-card,
.bill-card,
.metric-card,
.lang-card {
    background:#0b0e18;
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:20px;
    margin-bottom:20px;
}

.role-card {
    text-align:center;
    min-height:240px;
}

.role-icon {
    font-size:52px;
    margin-bottom:14px;
}

.role-title {
    font-size:24px;
    font-weight:700;
    margin-bottom:10px;
}

.role-desc {
    color:#94a3b8;
    font-size:14px;
    line-height:1.6;
}

.login-title,
.nc-title {
    font-size:24px;
    font-weight:700;
    margin-bottom:8px;
}

.login-sub,
.nc-sub {
    color:#94a3b8;
    font-size:14px;
}

.cust-name {
    font-size:24px;
    font-weight:700;
}

.cust-meta {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:14px;
}

.cust-chip {
    background:#111827;
    border:1px solid rgba(255,255,255,.06);
    padding:8px 14px;
    border-radius:30px;
    font-size:13px;
}

.outage-warn {
    margin-top:18px;
    background:rgba(239,68,68,.1);
    border:1px solid rgba(239,68,68,.25);
    color:#fca5a5;
    padding:14px;
    border-radius:12px;
}

.sec-hdr {
    font-size:12px;
    color:#64748b;
    letter-spacing:.1em;
    margin:20px 0 12px;
    text-transform:uppercase;
}

.plan-card {
    text-align:center;
}

.plan-name {
    color:#94a3b8;
    font-size:13px;
    text-transform:uppercase;
}

.plan-speed {
    font-size:28px;
    color:#38bdf8;
    font-weight:700;
    margin:10px 0;
}

.plan-price {
    font-size:20px;
    font-weight:700;
}

.bill-amount {
    font-size:48px;
    font-weight:700;
}

.metric-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:16px;
    margin-bottom:24px;
}

.metric-num {
    font-size:38px;
    font-weight:700;
}

.metric-lbl {
    color:#64748b;
    margin-top:6px;
    font-size:12px;
}

.ticket-id {
    color:#94a3b8;
    font-size:12px;
}

.ticket-issue {
    font-size:16px;
    margin:10px 0;
}

.tag {
    display:inline-block;
    margin-right:6px;
    margin-top:8px;
    padding:5px 10px;
    border-radius:20px;
    font-size:11px;
    background:#111827;
}

.tag-high { color:#f87171; }
.tag-medium { color:#fbbf24; }
.tag-low { color:#4ade80; }

[data-testid="stButton"] button {
    width:100%;
    border-radius:10px !important;
    border:none !important;
    background:linear-gradient(135deg,#0ea5e9,#14b8a6) !important;
    color:white !important;
    font-weight:600 !important;
}

.stChatMessage {
    background:#0b0e18 !important;
    border:1px solid rgba(255,255,255,.06);
    border-radius:16px;
    padding:10px;
}
</style>
"""

st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────
@st.cache_resource
def get_db():
    conn = sqlite3.connect("isp_system.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        package TEXT,
        area TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT,
        customer_phone TEXT,
        issue TEXT,
        priority TEXT,
        sentiment TEXT,
        technician TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        customer_phone TEXT UNIQUE,
        amount INTEGER,
        due_date TEXT
    )
    """)

    conn.commit()

    try:
        c.execute("""
        INSERT OR IGNORE INTO customers(name,phone,package,area)
        VALUES('Ali Khan','03001234567','Gaming Pro','DHA')
        """)

        c.execute("""
        INSERT OR IGNORE INTO bills(customer_phone,amount,due_date)
        VALUES('03001234567',5400,'2026-05-30')
        """)

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
• Basic Home → 25 Mbps → PKR 2,000/month
• Gaming Pro → 100 Mbps → PKR 4,000/month
• Ultra Fiber → 250 Mbps → PKR 6,500/month
• Extreme Fiber → 500 Mbps → PKR 9,000/month
"""

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=[
        "customer_type",
        "name",
        "current_package",
        "area",
        "bill_info",
        "history_text",
        "plans",
        "message",
        "language"
    ],
    template="""
You are a professional ISP AI support agent.

Customer: {name} ({customer_type})
Package: {current_package}
Area: {area}
Bill: {bill_info}
History: {history_text}
Plans: {plans}

Message: {message}

IMPORTANT:
- Reply ONLY in {language}
- Keep response concise
- Return ONLY JSON

Format:
{{
    "category":"",
    "priority":"",
    "sentiment":"",
    "technician_required":"",
    "reply":""
}}
"""
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def gen_ticket_id():
    return f"ISP-{datetime.datetime.now().year}-{random.randint(1000,9999)}"

def gen_tech():
    return f"TECH-{random.randint(100,999)}"

def process_ticket(
    llm,
    phone,
    customer_type,
    name,
    current_package,
    area,
    bill_info,
    history_text,
    message,
    language="English"
):
    try:

        prompt_text = PROMPT_TEMPLATE.format(
            customer_type=customer_type,
            name=name,
            current_package=current_package,
            area=area,
            bill_info=bill_info,
            history_text=history_text,
            plans=PLANS,
            message=message,
            language=language
        )

        response = llm.invoke(prompt_text)

        raw = response.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\{.*\}", raw, re.DOTALL)

        if match:
            result = json.loads(match.group(0))
        else:
            result = json.loads(raw)

        ticket_id = gen_ticket_id()

        technician = (
            gen_tech()
            if result.get("technician_required", "").lower() == "yes"
            else "Not Assigned"
        )

        c = db()

        c.execute("""
        INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)
        """, (
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

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
defaults = {
    "screen": "login",
    "phone": "",
    "customer": None,
    "chat": [],
    "lang": "English",
    "api_key": "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"
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
if st.session_state.screen == "login":

    st.markdown("""
    <div class="login-box">
        <div class="login-title">📱 Customer Login</div>
    </div>
    """, unsafe_allow_html=True)

    phone = st.text_input("Phone Number")

    if st.button("Login"):

        c = db()

        c.execute("""
        SELECT name,package,area
        FROM customers
        WHERE phone=?
        """, (phone,))

        cust = c.fetchone()

        if cust:

            st.session_state.phone = phone

            st.session_state.customer = {
                "name": cust[0],
                "package": cust[1],
                "area": cust[2]
            }

            st.session_state.screen = "customer"

            st.rerun()

        else:
            st.error("Customer not found")

# ─────────────────────────────────────────
# CUSTOMER PORTAL
# ─────────────────────────────────────────
elif st.session_state.screen == "customer":

    cust = st.session_state.customer
    phone = st.session_state.phone

    llm = get_llm(st.session_state.api_key)

    st.markdown(f"""
    <div class="cust-card">
        <div class="cust-name">
            👋 Welcome, {cust["name"]}
        </div>

        <div class="cust-meta">
            <div class="cust-chip">📱 {phone}</div>
            <div class="cust-chip">📦 {cust["package"]}</div>
            <div class="cust-chip">📍 {cust["area"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):

        for k, v in defaults.items():
            st.session_state[k] = v

        st.rerun()

    tab1, tab2 = st.tabs([
        "💬 Support",
        "💳 Bill"
    ])

    # SUPPORT TAB
    with tab1:

        for msg in st.session_state.chat:

            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["text"])

            else:
                with st.chat_message("assistant", avatar="🌐"):

                    if "error" in msg:
                        st.error(msg["error"])

                    else:
                        r = msg["result"]

                        st.write(r.get("reply", ""))

                        st.caption(
                            f"🎫 {r.get('ticket_id','')} · 🔧 {r.get('technician','Not Assigned')}"
                        )

        user_msg = st.chat_input("Describe your issue...")

        if user_msg:

            st.session_state.chat.append({
                "role": "user",
                "text": user_msg
            })

            with st.spinner("AI analyzing issue..."):

                result, err = process_ticket(
                    llm,
                    phone,
                    "Existing Customer",
                    cust["name"],
                    cust["package"],
                    cust["area"],
                    "No Pending Bill",
                    "",
                    user_msg,
                    st.session_state.lang
                )

            if result:

                st.session_state.chat.append({
                    "role": "ai",
                    "result": result
                })

            else:

                st.session_state.chat.append({
                    "role": "ai",
                    "error": err
                })

            st.rerun()

    # BILL TAB
    with tab2:

        c = db()

        c.execute("""
        SELECT amount,due_date
        FROM bills
        WHERE customer_phone=?
        """, (phone,))

        row = c.fetchone()

        if row:

            amount, due = row

            st.markdown(f"""
            <div class="bill-card">
                <div>CURRENT BILL</div>

                <div class="bill-amount">
                    PKR {amount}
                </div>

                <div>Due Date: {due}</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("No bill found")
````
