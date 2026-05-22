
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
    CREATE TABLE IF NOT EXISTS outages (
        area TEXT UNIQUE,
        status TEXT,
        expected_fix_time TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        customer_phone TEXT UNIQUE,
        amount INTEGER,
        due_date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS new_connection_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        area TEXT,
        package TEXT,
        created_at TEXT
    )
    """)

    conn.commit()

    try:
        c.execute("""
        INSERT OR IGNORE INTO customers(name,phone,package,area)
        VALUES('Ali Khan','03001234567','Gaming Pro','DHA')
        """)

        c.execute("""
        INSERT OR IGNORE INTO outages(area,status,expected_fix_time)
        VALUES('DHA','DOWN','2 Hours')
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
• Basic Home    → 25 Mbps  → PKR 2,000/month
• Gaming Pro    → 100 Mbps → PKR 4,000/month
• Ultra Fiber   → 250 Mbps → PKR 6,500/month
• Extreme Fiber → 500 Mbps → PKR 9,000/month
"""

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=[
        "customer_type",
        "name",
        "current_package",
        "area",
        "network_status",
        "fix_time",
        "bill_info",
        "history_text",
        "plans",
        "message",
        "language"
    ],
    template="""
You are a professional ISP AI support agent for ConnectPK.

Customer: {name} ({customer_type})
Package: {current_package}
Area: {area}
Network Status: {network_status}
Fix Time: {fix_time}
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
    network_status,
    fix_time,
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
            network_status=network_status,
            fix_time=fix_time,
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

def pri_tag(p):
    cls = {
        "High":"tag-high",
        "Medium":"tag-medium",
        "Low":"tag-low"
    }.get(p, "tag-low")

    return f'<span class="tag {cls}">{p}</span>'

def render_chat(chat_list):
    for msg in chat_list:

        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["text"])

        elif msg["role"] == "ai":
            with st.chat_message("assistant", avatar="🌐"):

                if "error" in msg:
                    st.error(msg["error"])

                else:
                    r = msg["result"]

                    st.write(r.get("reply", ""))

                    st.caption(
                        f"🎫 {r.get('ticket_id','')}  ·  🔧 {r.get('technician','Not Assigned')}"
                    )

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
defaults = {
    "screen": "role",
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
    "api_key": "YOUR_GROQ_API_KEY"
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

    <div class="status-pill">
        <div class="status-dot"></div>
        SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
# ROLE SCREEN
# ════════════════════════════════════════
if st.session_state.screen == "role":

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">👤</div>
            <div class="role-title">Customer</div>
            <div class="role-desc">
                Get support for internet issues, billing and plans.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Login as Customer"):
            st.session_state.screen = "customer_login"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🛠️</div>
            <div class="role-title">Admin</div>
            <div class="role-desc">
                Manage customers, outages and tickets.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Login as Admin"):
            st.session_state.screen = "admin_login"
            st.rerun()

# ════════════════════════════════════════
# CUSTOMER LOGIN
# ════════════════════════════════════════
elif st.session_state.screen == "customer_login":

    _, col, _ = st.columns([1,2,1])

    with col:

        st.markdown("""
        <div class="login-box">
            <div class="login-title">📱 Customer Login</div>
            <div class="login-sub">
                Enter your phone number
            </div>
        </div>
        """, unsafe_allow_html=True)

        phone = st.text_input(
            "Phone Number",
            placeholder="03001234567"
        )

        if st.button("Send OTP"):

            if phone.strip():

                otp = random.randint(1000, 9999)

                st.session_state.phone = phone
                st.session_state.otp = otp
                st.session_state.screen = "otp"

                st.rerun()

            else:
                st.error("Enter phone number")

        if st.button("Back"):
            st.session_state.screen = "role"
            st.rerun()

# ════════════════════════════════════════
# OTP
# ════════════════════════════════════════
elif st.session_state.screen == "otp":

    _, col, _ = st.columns([1,2,1])

    with col:

        st.markdown(f"""
        <div class="login-box">
            <div class="login-title">🔐 OTP Verification</div>
            <h2>{st.session_state.otp}</h2>
        </div>
        """, unsafe_allow_html=True)

        entered = st.text_input("Enter OTP")

        if st.button("Verify"):

            if entered == str(st.session_state.otp):

                phone = st.session_state.phone

                c = db()

                c.execute("""
                SELECT name,package,area
                FROM customers
                WHERE phone=?
                """, (phone,))

                cust = c.fetchone()

                if cust:

                    st.session_state.customer = {
                        "name": cust[0],
                        "package": cust[1],
                        "area": cust[2]
                    }

                    st.session_state.customer_type = "Existing Customer"

                else:
                    st.session_state.customer = None
                    st.session_state.customer_type = "New Customer"

                st.session_state.screen = "lang_select"

                st.rerun()

            else:
                st.error("Invalid OTP")

# ════════════════════════════════════════
# LANGUAGE SELECT
# ════════════════════════════════════════
elif st.session_state.screen == "lang_select":

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="lang-card">
            <h1>🇬🇧</h1>
            <h2>English</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button("English"):

            st.session_state.lang = "English"

            if st.session_state.customer is None:
                st.session_state.screen = "new_customer"
            else:
                st.session_state.screen = "customer"

            st.rerun()

    with c2:

        st.markdown("""
        <div class="lang-card">
            <h1>🇵🇰</h1>
            <h2>اردو</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button("اردو"):

            st.session_state.lang = "Urdu"

            if st.session_state.customer is None:
                st.session_state.screen = "new_customer"
            else:
                st.session_state.screen = "customer"

            st.rerun()

# ════════════════════════════════════════
# NEW CUSTOMER
# ════════════════════════════════════════
elif st.session_state.screen == "new_customer":

    st.markdown("""
    <div class="login-box">
        <div class="login-title">🆕 New Customer</div>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Full Name")

    area = st.selectbox(
        "Area",
        ["DHA","Gulshan","Clifton","Nazimabad","Korangi"]
    )

    if st.button("Register"):

        if name.strip():

            c = db()

            c.execute("""
            INSERT OR IGNORE INTO customers(name,phone,package,area)
            VALUES(?,?,?,?)
            """, (
                name,
                st.session_state.phone,
                "No Package",
                area
            ))

            conn.commit()

            st.session_state.customer = {
                "name": name,
                "package": "No Package",
                "area": area
            }

            st.session_state.screen = "customer"

            st.rerun()

# ════════════════════════════════════════
# CUSTOMER PORTAL
# ════════════════════════════════════════
elif st.session_state.screen == "customer":

    cust = st.session_state.customer
    phone = st.session_state.phone
    lang = st.session_state.lang

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

    tab1, tab2, tab3 = st.tabs([
        "💬 Support",
        "💳 Bill",
        "📶 Plans"
    ])

    # SUPPORT TAB
    with tab1:

        st.markdown("""
        <div class="sec-hdr">
            Quick Topics
        </div>
        """, unsafe_allow_html=True)

        topics = [
            "Slow internet speed",
            "WiFi not working",
            "No internet connection",
            "Weak signals",
            "Need technician"
        ]

        cols = st.columns(5)

        for i, topic in enumerate(topics):

            with cols[i]:

                if st.button(topic, key=f"topic_{i}"):

                    st.session_state.chat.append({
                        "role": "user",
                        "text": topic
                    })

                    with st.spinner("AI is analyzing..."):

                        result, err = process_ticket(
                            llm,
                            phone,
                            st.session_state.customer_type,
                            cust["name"],
                            cust["package"],
                            cust["area"],
                            st.session_state.network_status,
                            st.session_state.fix_time,
                            st.session_state.bill_info,
                            st.session_state.history_text,
                            topic,
                            lang
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

        st.markdown("""
        <div class="sec-hdr">
            Conversation
        </div>
        """, unsafe_allow_html=True)

        render_chat(st.session_state.chat)

        user_msg = st.chat_input("Type your issue...")

        if user_msg:

            st.session_state.chat.append({
                "role": "user",
                "text": user_msg
            })

            with st.spinner("Thinking..."):

                result, err = process_ticket(
                    llm,
                    phone,
                    st.session_state.customer_type,
                    cust["name"],
                    cust["package"],
                    cust["area"],
                    st.session_state.network_status,
                    st.session_state.fix_time,
                    st.session_state.bill_info,
                    st.session_state.history_text,
                    user_msg,
                    lang
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

    # PLAN TAB
    with tab3:

        plans = [
            ("Basic Home","25 Mbps","PKR 2,000"),
            ("Gaming Pro","100 Mbps","PKR 4,000"),
            ("Ultra Fiber","250 Mbps","PKR 6,500"),
            ("Extreme Fiber","500 Mbps","PKR 9,000"),
        ]

        cols = st.columns(4)

        for i, (name, speed, price) in enumerate(plans):

            with cols[i]:

                st.markdown(f"""
                <div class="plan-card">
                    <div class="plan-name">{name}</div>
                    <div class="plan-speed">{speed}</div>
                    <div class="plan-price">{price}</div>
                </div>
                """, unsafe_allow_html=True)

                st.button("Choose", key=f"choose_{i}")

# ════════════════════════════════════════
# ADMIN LOGIN
# ════════════════════════════════════════
elif st.session_state.screen == "admin_login":

    st.markdown("""
    <div class="login-box">
        <div class="login-title">🔐 Admin Login</div>
    </div>
    """, unsafe_allow_html=True)

    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        if pwd == "admin123":

            st.session_state.screen = "admin"
            st.rerun()

        else:
            st.error("Wrong password")

# ════════════════════════════════════════
# ADMIN DASHBOARD
# ════════════════════════════════════════
elif st.session_state.screen == "admin":

    c = db()

    c.execute("SELECT COUNT(*) FROM customers")
    total_customers = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = c.fetchone()[0]

    c.execute("""
    SELECT COUNT(*)
    FROM tickets
    WHERE status='Open'
    """)
    open_tickets = c.fetchone()[0]

    c.execute("""
    SELECT COUNT(*)
    FROM tickets
    WHERE priority='High'
    """)
    high_priority = c.fetchone()[0]

    st.markdown(f"""
    <div class="metric-grid">

        <div class="metric-card">
            <div class="metric-num">{total_customers}</div>
            <div class="metric-lbl">Customers</div>
        </div>

        <div class="metric-card">
            <div class="metric-num">{total_tickets}</div>
            <div class="metric-lbl">Tickets</div>
        </div>

        <div class="metric-card">
            <div class="metric-num">{open_tickets}</div>
            <div class="metric-lbl">Open</div>
        </div>

        <div class="metric-card">
            <div class="metric-num">{high_priority}</div>
            <div class="metric-lbl">High Priority</div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([
        "🎫 Tickets",
        "👥 Customers"
    ])

    with tab1:

        c.execute("""
        SELECT *
        FROM tickets
        ORDER BY created_at DESC
        """)

        rows = c.fetchall()

        for row in rows:

            tid, phone, issue, priority, sentiment, tech, status, created = row

            st.markdown(f"""
            <div class="ticket-card">

                <div class="ticket-id">
                    {tid}
                </div>

                <div class="ticket-issue">
                    {issue}
                </div>

                {pri_tag(priority)}

                <div style="margin-top:10px;color:#94a3b8;font-size:12px;">
                    {phone} · {created}
                </div>

            </div>
            """, unsafe_allow_html=True)

    with tab2:

        c.execute("""
        SELECT name,phone,package,area
        FROM customers
        """)

        rows = c.fetchall()

        if rows:

            import pandas as pd

            df = pd.DataFrame(
                rows,
                columns=["Name","Phone","Package","Area"]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    if st.button("Logout"):

        st.session_state.screen = "role"

        st.rerun()
````

