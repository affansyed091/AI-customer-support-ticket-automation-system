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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}
.stApp { background: #07080d; }
.main .block-container { padding: 2rem 2rem 4rem; max-width: 1140px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top bar ── */
.topbar {
    background: linear-gradient(135deg, #0b0d15 0%, #0f1320 100%);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 18px;
    padding: 18px 28px;
    margin-bottom: 28px;
    display: flex; align-items: center; justify-content: space-between;
    border-left: 4px solid #38bdf8;
    box-shadow: 0 0 40px rgba(56,189,248,0.06);
}
.topbar-brand { display: flex; align-items: center; gap: 14px; }
.topbar-icon {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 18px rgba(14,165,233,0.35);
}
.topbar-title { font-size: 21px; font-weight: 800; color: #f0f6ff; letter-spacing: -0.02em; }
.topbar-sub { font-size: 11px; color: #475569; font-family: 'JetBrains Mono', monospace; letter-spacing: .08em; margin-top: 2px; }
.status-pill {
    background: rgba(34,197,94,.1);
    border: 1px solid rgba(34,197,94,.25);
    color: #4ade80;
    padding: 6px 16px; border-radius: 20px;
    font-size: 12px; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 7px;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%; background: #4ade80;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1;box-shadow:0 0 6px #4ade80;} 50%{opacity:.3;box-shadow:none;} }

/* ── Role cards ── */
.role-card {
    background: #0b0d15;
    border: 1px solid rgba(56,189,248,.12);
    border-radius: 18px; padding: 34px 24px; cursor: pointer;
    text-align: center;
    transition: all .25s;
    position: relative; overflow: hidden;
}
.role-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,.4), transparent);
    opacity: 0; transition: opacity .3s;
}
.role-card:hover { border-color: rgba(56,189,248,.4); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(56,189,248,.08); }
.role-card:hover::before { opacity: 1; }
.role-icon { font-size: 40px; margin-bottom: 14px; filter: drop-shadow(0 4px 12px rgba(56,189,248,.3)); }
.role-title { font-size: 19px; font-weight: 700; color: #f0f6ff; margin-bottom: 8px; }
.role-desc { font-size: 13px; color: #64748b; line-height: 1.5; }

/* ── Metric cards ── */
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }
.metric-card {
    background: #0b0d15; border: 1px solid rgba(56,189,248,.1);
    border-radius: 14px; padding: 18px 20px;
    transition: border-color .2s;
}
.metric-card:hover { border-color: rgba(56,189,248,.25); }
.metric-num { font-size: 30px; font-weight: 800; color: #f0f6ff; letter-spacing: -0.03em; }
.metric-lbl { font-size: 11px; color: #475569; font-family: 'JetBrains Mono', monospace; margin-top: 4px; letter-spacing: .05em; }
.metric-num.red { color: #f87171; } .metric-num.yellow { color: #fbbf24; }
.metric-num.green { color: #4ade80; } .metric-num.blue { color: #38bdf8; }

/* ── Section header ── */
.sec-hdr {
    font-size: 11px; font-weight: 700; color: #475569;
    letter-spacing: .1em; text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin: 20px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(56,189,248,.08);
}

/* ── Ticket card ── */
.ticket-card {
    background: #0b0d15; border: 1px solid rgba(56,189,248,.1);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 10px;
    border-left: 3px solid #38bdf8;
}
.ticket-card.high { border-left-color: #f87171; }
.ticket-card.medium { border-left-color: #fbbf24; }
.ticket-card.low { border-left-color: #4ade80; }
.ticket-card.resolved { border-left-color: #334155; opacity: .65; }
.ticket-hdr { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.ticket-id { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #94a3b8; }
.ticket-status { font-size: 11px; font-weight: 700; padding: 3px 12px; border-radius: 20px; }
.s-open { background: rgba(56,189,248,.1); color: #7dd3fc; }
.s-resolved { background: rgba(51,65,85,.3); color: #94a3b8; }
.ticket-issue { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }
.ticket-meta { display: flex; gap: 8px; flex-wrap: wrap; }
.tag {
    font-size: 11px; font-weight: 600; padding: 3px 10px;
    border-radius: 20px; font-family: 'JetBrains Mono', monospace;
}
.tag-high { background: rgba(248,113,113,.1); color: #f87171; }
.tag-medium { background: rgba(251,191,36,.1); color: #fbbf24; }
.tag-low { background: rgba(74,222,128,.1); color: #4ade80; }
.tag-tech { background: rgba(56,189,248,.1); color: #7dd3fc; }
.tag-cat { background: rgba(167,139,250,.1); color: #c4b5fd; }
.tag-sent { background: rgba(100,116,139,.1); color: #94a3b8; }

/* ── Chat bubbles ── */
.chat-msg-user { display: flex; justify-content: flex-end; margin-bottom: 16px; }
.chat-msg-ai { display: flex; justify-content: flex-start; margin-bottom: 16px; }
.bubble-user {
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
    color: #fff;
    padding: 12px 18px; border-radius: 20px 20px 4px 20px;
    max-width: 70%; font-size: 14px; line-height: 1.55;
    box-shadow: 0 4px 16px rgba(14,165,233,.2);
}
.bubble-ai {
    background: #0f1320;
    border: 1px solid rgba(56,189,248,.15);
    color: #e2e8f0;
    padding: 0; border-radius: 4px 20px 20px 20px;
    max-width: 82%; font-size: 14px; line-height: 1.6;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,.3);
}
.ai-label {
    font-size: 11px; color: #475569; font-family: 'JetBrains Mono', monospace;
    padding: 10px 16px 0; display: flex; align-items: center; gap: 6px;
}
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #38bdf8; animation: blink 2s infinite; }

/* ── Result card inside bubble ── */
.result-inner { padding: 10px 16px 14px; }
.ticket-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #fbbf24;
    background: rgba(251,191,36,.08); border: 1px solid rgba(251,191,36,.2);
    padding: 4px 12px; border-radius: 6px; display: inline-block; margin-bottom: 10px;
}
.tech-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #7dd3fc;
    background: rgba(56,189,248,.08); border: 1px solid rgba(56,189,248,.2);
    padding: 4px 12px; border-radius: 6px; display: inline-block; margin-left: 8px;
}
.tag-row { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 12px; }
.reply-box {
    background: rgba(56,189,248,.04);
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 10px; padding: 12px 15px;
    font-size: 13.5px; color: #cbd5e1; line-height: 1.65;
}
.reply-lbl {
    font-size: 10px; color: #38bdf8; font-family: 'JetBrains Mono', monospace;
    letter-spacing: .08em; text-transform: uppercase; margin-bottom: 7px; font-weight: 700;
}

/* ── Quick topic buttons ── */
.qtopic-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 8px; }
.qtopic-btn {
    background: #0f1320;
    border: 1px solid rgba(56,189,248,.15);
    color: #94a3b8;
    padding: 9px 16px; border-radius: 22px;
    font-size: 13px; font-weight: 500; font-family: 'Outfit', sans-serif;
    cursor: pointer; transition: all .2s;
    display: inline-flex; align-items: center; gap: 7px;
}
.qtopic-btn:hover { border-color: #38bdf8; color: #e2e8f0; background: rgba(56,189,248,.06); }

/* ── Login box ── */
.login-box {
    background: #0b0d15;
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 18px; padding: 34px 30px;
    max-width: 440px; margin: 0 auto;
    box-shadow: 0 0 60px rgba(56,189,248,.05);
}
.login-title { font-size: 21px; font-weight: 800; color: #f0f6ff; margin-bottom: 6px; }
.login-sub { font-size: 13px; color: #64748b; margin-bottom: 24px; line-height: 1.5; }
.otp-preview {
    background: rgba(74,222,128,.07);
    border: 1px solid rgba(74,222,128,.2);
    border-radius: 10px; padding: 14px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px; font-weight: 700; color: #4ade80;
    margin-bottom: 18px; text-align: center; letter-spacing: .25em;
}

/* ── Language select ── */
.lang-card {
    background: #0b0d15;
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 18px; padding: 32px 24px;
    cursor: pointer; text-align: center; transition: all .25s;
}
.lang-card:hover { border-color: #38bdf8; transform: translateY(-3px); box-shadow: 0 12px 40px rgba(56,189,248,.1); }
.lang-emoji { font-size: 44px; margin-bottom: 12px; }
.lang-title { font-size: 20px; font-weight: 800; color: #f0f6ff; margin-bottom: 6px; }
.lang-sub { font-size: 13px; color: #64748b; }

/* ── Customer info card ── */
.cust-card {
    background: linear-gradient(135deg, #0b0f1e 0%, #0b0d15 100%);
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 16px; padding: 20px 24px; margin-bottom: 20px;
}
.cust-name { font-size: 20px; font-weight: 800; color: #f0f6ff; margin-bottom: 4px; letter-spacing: -0.01em; }
.cust-meta { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; }
.cust-chip {
    background: rgba(15,19,32,.8);
    border: 1px solid rgba(56,189,248,.12);
    border-radius: 8px; padding: 6px 13px;
    font-size: 12px; color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}
.cust-chip span { color: #e2e8f0; margin-left: 4px; }
.outage-warn {
    background: rgba(248,113,113,.07);
    border: 1px solid rgba(248,113,113,.2);
    border-radius: 10px; padding: 10px 16px;
    font-size: 13px; color: #fca5a5;
    margin-top: 12px; display: flex; align-items: center; gap: 8px;
}

/* ── New connection form ── */
.nc-card {
    background: #0b0d15;
    border: 1px solid rgba(56,189,248,.12);
    border-radius: 16px; padding: 24px 24px; margin-bottom: 14px;
}
.nc-title { font-size: 16px; font-weight: 700; color: #f0f6ff; margin-bottom: 4px; }
.nc-sub { font-size: 13px; color: #64748b; margin-bottom: 0; }
.plan-card {
    background: #0b0d15;
    border: 1px solid rgba(56,189,248,.12);
    border-radius: 14px; padding: 20px; cursor: pointer; transition: all .2s;
    text-align: center;
}
.plan-card:hover { border-color: #38bdf8; box-shadow: 0 8px 30px rgba(56,189,248,.08); }
.plan-card.selected { border-color: #38bdf8; background: rgba(56,189,248,.05); }
.plan-name { font-size: 15px; font-weight: 800; color: #f0f6ff; margin-bottom: 4px; }
.plan-speed { font-size: 12px; color: #38bdf8; font-family: 'JetBrains Mono', monospace; margin-bottom: 8px; }
.plan-price { font-size: 20px; font-weight: 800; color: #fbbf24; }
.plan-per { font-size: 11px; color: #64748b; }

/* ── Bill card ── */
.bill-card {
    background: linear-gradient(135deg, #0b0f1e, #0b0d15);
    border: 1px solid rgba(251,191,36,.2);
    border-radius: 16px; padding: 28px 24px; margin-bottom: 16px;
}
.bill-amount { font-size: 42px; font-weight: 800; color: #fbbf24; letter-spacing: -0.03em; }
.bill-currency { font-size: 18px; color: #94a3b8; margin-right: 4px; }
.bill-due { font-size: 13px; color: #64748b; margin-top: 6px; font-family: 'JetBrains Mono', monospace; }
.bill-status-ok {
    background: rgba(74,222,128,.08); border: 1px solid rgba(74,222,128,.2);
    color: #4ade80; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700;
    display: inline-block; margin-top: 14px; font-family: 'JetBrains Mono', monospace;
}
.bill-status-due {
    background: rgba(248,113,113,.08); border: 1px solid rgba(248,113,113,.2);
    color: #f87171; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700;
    display: inline-block; margin-top: 14px; font-family: 'JetBrains Mono', monospace;
}

/* ── Streamlit overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #0b0d15 !important; border: 1px solid rgba(56,189,248,.15) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.12) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: #94a3b8 !important; font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: .07em !important; text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 24px !important; transition: all .2s !important; width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(14,165,233,.3) !important;
}
.stButton > button[kind="secondary"] { background: rgba(15,19,32,.9) !important; color: #94a3b8 !important; border: 1px solid rgba(56,189,248,.15) !important; }
div[data-testid="stDataFrame"] { border: 1px solid rgba(56,189,248,.1); border-radius: 12px; overflow: hidden; }
.stTabs [data-baseweb="tab-list"] { background: #0b0d15; border-bottom: 1px solid rgba(56,189,248,.1); gap: 0; border-radius: 0; }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #64748b !important;
    font-family: 'Outfit', sans-serif !important; font-weight: 600 !important;
    font-size: 13px !important; border-bottom: 2px solid transparent !important;
    padding: 12px 22px !important;
}
.stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom-color: #38bdf8 !important; background: transparent !important; }
.stAlert { border-radius: 10px !important; }
.stForm { background: transparent !important; border: none !important; }
.stSuccess { background: rgba(74,222,128,.07) !important; border: 1px solid rgba(74,222,128,.2) !important; color: #4ade80 !important; border-radius: 10px !important; }

.empty-chat {
    text-align: center; padding: 48px 20px; color: #334155;
    border: 1px dashed rgba(56,189,248,.1); border-radius: 16px;
    margin: 8px 0 16px;
}
.empty-chat .ec-icon { font-size: 40px; margin-bottom: 10px; }
.empty-chat .ec-text { font-size: 14px; color: #475569; }
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
    c.execute("""CREATE TABLE IF NOT EXISTS new_connection_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, area TEXT, package TEXT, created_at TEXT)""")
    conn.commit()
    try:
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES('Ali Khan','03001234567','Gaming Pro','DHA')")
        c.execute("INSERT OR IGNORE INTO outages(area,status,expected_fix_time) VALUES('DHA','DOWN','2 Hours')")
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES('03001234567',5400,'2026-05-30')")
        conn.commit()
    except:
        pass
    return conn

conn = get_db()
def db(): return conn.cursor()

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
                     "network_status","fix_time","bill_info","history_text","plans","message","language"],
    template="""
You are a professional ISP AI support agent for ConnectPK, a Pakistani internet provider.

Customer: {name} ({customer_type})
Package: {current_package}
Area: {area}
Network Status: {network_status} | Fix Time: {fix_time}
Bill: {bill_info}
History: {history_text}
Available Plans: {plans}

Message: {message}

IMPORTANT LANGUAGE RULE:
- The customer has chosen to communicate in: {language}
- You MUST reply ONLY in {language}. Do not mix languages.
- If language is "Urdu", write your reply entirely in Urdu script.
- If language is "English", write your reply entirely in English.

Rules:
- Detect sentiment (Positive/Neutral/Frustrated/Angry)
- Assign priority (High/Medium/Low)
- Recommend technician if hardware issue
- Mention outage only if area is DOWN
- Be empathetic and professional
- Keep reply concise (2-4 sentences)

Return ONLY valid JSON (no markdown, no extra text):
{{"category":"","priority":"","sentiment":"","technician_required":"yes or no","reply":""}}
"""
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def gen_ticket_id(): return f"ISP-{datetime.datetime.now().year}-{random.randint(1000,9999)}"
def gen_tech(): return f"TECH-{random.randint(100,999)}"

def process_ticket(llm, phone, customer_type, name, current_package,
                   area, network_status, fix_time, bill_info, history_text, message, language="English"):
    try:
        prompt_text = PROMPT_TEMPLATE.format(
            customer_type=customer_type, name=name,
            current_package=current_package, area=area,
            network_status=network_status, fix_time=fix_time,
            bill_info=bill_info, history_text=history_text,
            plans=PLANS, message=message, language=language
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
    return f'<span class="tag {cls}">{htmllib.escape(p)}</span>'

def sent_tag(s):
    return f'<span class="tag tag-sent">{htmllib.escape(s)}</span>'

def cat_tag(c):
    return f'<span class="tag tag-cat">{htmllib.escape(c)}</span>'

def tech_tag(t):
    if t == "Not Assigned": return f'<span class="tag tag-sent">{htmllib.escape(t)}</span>'
    return f'<span class="tag tag-tech">🔧 {htmllib.escape(t)}</span>'

def render_result_bubble(r):
    tech_html = ""
    if r.get("technician","") != "Not Assigned":
        tech_html = f'<span class="tech-badge">🔧 {htmllib.escape(r["technician"])}</span>'
    # CRITICAL: escape the AI reply text to prevent HTML injection / broken rendering
    safe_reply = htmllib.escape(r.get("reply","")).replace("\n", "<br>")
    return f"""
<div class="chat-msg-ai">
  <div class="bubble-ai">
    <div class="ai-label"><div class="ai-dot"></div>ISP AI Support Agent</div>
    <div class="result-inner">
      <div style="margin-bottom:10px;">
        <span class="ticket-badge">🎫 {htmllib.escape(r.get("ticket_id",""))}</span>
        {tech_html}
      </div>
      <div class="tag-row">
        {cat_tag(r.get("category","General"))}
        {pri_tag(r.get("priority","Medium"))}
        {sent_tag(r.get("sentiment","Neutral"))}
      </div>
      <div class="reply-box">
        <div class="reply-lbl">AI Response</div>
        {safe_reply}
      </div>
    </div>
  </div>
</div>"""

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
    "lang": "",   # "English" or "Urdu"
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
      <div class="topbar-sub">AI CUSTOMER SUPPORT SYSTEM v2</div>
    </div>
  </div>
  <div class="status-pill"><div class="status-dot"></div> SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# SCREEN: ROLE SELECTION
# ═══════════════════════════════════════════════
if st.session_state.screen == "role":
    st.markdown("<div style='text-align:center;margin-bottom:20px;'><span style='font-size:14px;color:#475569;letter-spacing:.05em;'>Select your role to continue</span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="role-card">
          <div class="role-icon">👤</div>
          <div class="role-title">Customer</div>
          <div class="role-desc">Get AI-powered support for your internet issues, billing inquiries, and plan upgrades</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Login as Customer", key="btn_cust"):
            st.session_state.screen = "customer_login"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="role-card">
          <div class="role-icon">🛠️</div>
          <div class="role-title">Admin</div>
          <div class="role-desc">Manage customers, tickets, outages, and resolve support requests from the dashboard</div>
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
          <div class="login-sub">Enter your registered phone number to receive an OTP verification code</div>
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
          <div class="login-sub">Your one-time password has been sent to<br><strong style="color:#e2e8f0;">{st.session_state.phone}</strong></div>
          <div class="otp-preview">{st.session_state.otp}</div>
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

                    c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,))
                    bill = c.fetchone()
                    st.session_state.bill_info = f"PKR {bill[0]}, Due: {bill[1]}" if bill else "No billing record"

                    if area:
                        c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (area,))
                        out = c.fetchone()
                        if out:
                            st.session_state.network_status = out[0]
                            st.session_state.fix_time = out[1]

                    c.execute("SELECT issue FROM tickets WHERE customer_phone=?", (phone,))
                    rows = c.fetchall()
                    st.session_state.history_text = "\n".join([f"- {r[0]}" for r in rows]) if rows else "No previous tickets."

                    # Always go to language selection first
                    st.session_state.screen = "lang_select"
                    st.session_state.chat = []
                    st.rerun()
                else:
                    st.error("Invalid OTP. Please try again.")
        with c2:
            if st.button("← Back", key="back_login"):
                st.session_state.screen = "customer_login"
                st.rerun()

# ═══════════════════════════════════════════════
# SCREEN: LANGUAGE SELECTION
# ═══════════════════════════════════════════════
elif st.session_state.screen == "lang_select":
    st.markdown("""
    <div style='text-align:center; margin-bottom:28px;'>
      <div style='font-size:26px; font-weight:800; color:#f0f6ff; margin-bottom:8px;'>🌐 Choose Your Language</div>
      <div style='font-size:14px; color:#64748b;'>آپ کی پسندیدہ زبان منتخب کریں / Select your preferred language</div>
    </div>""", unsafe_allow_html=True)

    _, lcol, rcol, _ = st.columns([1, 2, 2, 1])
    with lcol:
        st.markdown("""
        <div class="lang-card">
          <div class="lang-emoji">🇬🇧</div>
          <div class="lang-title">English</div>
          <div class="lang-sub">Continue in English</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Select English", key="lang_en"):
            st.session_state.lang = "English"
            # Check if new or existing customer
            if st.session_state.customer is None:
                st.session_state.screen = "new_customer"
            else:
                st.session_state.screen = "customer"
            st.rerun()
    with rcol:
        st.markdown("""
        <div class="lang-card">
          <div class="lang-emoji">🇵🇰</div>
          <div class="lang-title">اردو</div>
          <div class="lang-sub">اردو میں جاری رکھیں</div>
        </div>""", unsafe_allow_html=True)
        if st.button("اردو منتخب کریں", key="lang_ur"):
            st.session_state.lang = "Urdu"
            if st.session_state.customer is None:
                st.session_state.screen = "new_customer"
            else:
                st.session_state.screen = "customer"
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
          <div class="login-sub">Complete your profile to get started with ConnectPK support</div>
        </div>""", unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="e.g. Ali Khan")
        area = st.selectbox("Your Area", ["DHA","Gulshan","PECHS","Clifton","Nazimabad","Korangi","North Karachi","Malir","Other"])
        if st.button("Register & Continue →", key="register"):
            if name.strip():
                phone = st.session_state.phone
                c = db()
                c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                          (name.strip(), phone, "No Package", area))
                conn.commit()
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
# SCREEN: CUSTOMER PORTAL (TABBED)
# ═══════════════════════════════════════════════
elif st.session_state.screen == "customer":
    cust = st.session_state.customer
    phone = st.session_state.phone
    llm = get_llm(st.session_state.api_key)
    lang = st.session_state.lang or "English"

    # Customer info card
    outage_html = ""
    if st.session_state.network_status == "DOWN":
        outage_html = f'<div class="outage-warn">⚠️ <strong>Network Outage in {htmllib.escape(cust["area"])}</strong> — Expected fix: {htmllib.escape(st.session_state.fix_time)}</div>'

    lang_flag = "🇵🇰" if lang == "Urdu" else "🇬🇧"
    st.markdown(f"""
    <div class="cust-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div class="cust-name">👋 Welcome, {htmllib.escape(cust["name"])}</div>
        <span style="font-size:12px;background:rgba(56,189,248,.08);border:1px solid rgba(56,189,248,.15);padding:4px 12px;border-radius:20px;color:#7dd3fc;font-family:'JetBrains Mono',monospace;">{lang_flag} {lang}</span>
      </div>
      <div class="cust-meta">
        <div class="cust-chip">📱 <span>{htmllib.escape(phone)}</span></div>
        <div class="cust-chip">📦 <span>{htmllib.escape(cust["package"])}</span></div>
        <div class="cust-chip">📍 <span>{htmllib.escape(cust["area"])}</span></div>
        <div class="cust-chip">💳 <span>{htmllib.escape(st.session_state.bill_info)}</span></div>
      </div>
      {outage_html}
    </div>
    """, unsafe_allow_html=True)

    col_logout, _ = st.columns([1,5])
    with col_logout:
        if st.button("← Logout", key="logout_cust"):
            for k in defaults: st.session_state[k] = defaults[k]
            st.rerun()

    # ── 4 Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs(["💬  Support Chat", "🆕  New Connection", "💳  My Bill", "📶  Upgrade Plan"])

    # ── TAB 1: SUPPORT CHAT ──
    with tab1:
        st.markdown("<div class='sec-hdr'>Quick Topics — tap to get instant help</div>", unsafe_allow_html=True)

        quick_topics = [
            ("🐌", "Slow internet speed"),
            ("📡", "WiFi not working"),
            ("⛔", "No internet connection"),
            ("💳", "Check my bill"),
            ("⬆️", "Upgrade my plan"),
            ("🔁", "Router restart help"),
            ("📶", "Weak signal"),
            ("🔧", "Request a technician"),
            ("📋", "My ticket status"),
            ("📦", "Current plan details"),
        ]

        # Render as a row of styled buttons using Streamlit columns
        cols = st.columns(5)
        for i, (icon, label) in enumerate(quick_topics):
            with cols[i % 5]:
                if st.button(f"{icon} {label}", key=f"qt_{i}"):
                    st.session_state.chat.append({"role": "user", "text": label})
                    with st.spinner("AI is analyzing…"):
                        result, err = process_ticket(
                            llm, phone, st.session_state.customer_type,
                            cust["name"], cust["package"], cust["area"],
                            st.session_state.network_status, st.session_state.fix_time,
                            st.session_state.bill_info, st.session_state.history_text,
                            label, lang
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
            <div class="empty-chat">
              <div class="ec-icon">💬</div>
              <div class="ec-text">Tap any Quick Topic above or type your issue below to get started</div>
            </div>""", unsafe_allow_html=True)

        for msg in st.session_state.chat:
            if msg["role"] == "user":
                safe_text = htmllib.escape(msg["text"])
                st.markdown(f'<div class="chat-msg-user"><div class="bubble-user">{safe_text}</div></div>', unsafe_allow_html=True)
            elif msg["role"] == "ai":
                if "error" in msg:
                    st.error(f"Error: {msg['error']}")
                else:
                    r = msg["result"]
                    st.markdown(render_result_bubble(r), unsafe_allow_html=True)

        # Optional text input
        st.markdown("<div class='sec-hdr'>Or type your own message</div>", unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Message", placeholder="Describe your issue…", label_visibility="collapsed")
            submitted = st.form_submit_button("Send Message →")
            if submitted and user_msg.strip():
                st.session_state.chat.append({"role": "user", "text": user_msg.strip()})
                with st.spinner("AI is analyzing your issue…"):
                    result, err = process_ticket(
                        llm, phone, st.session_state.customer_type,
                        cust["name"], cust["package"], cust["area"],
                        st.session_state.network_status, st.session_state.fix_time,
                        st.session_state.bill_info, st.session_state.history_text,
                        user_msg.strip(), lang
                    )
                if result:
                    st.session_state.chat.append({"role": "ai", "result": result})
                else:
                    st.session_state.chat.append({"role": "ai", "error": err})
                st.rerun()

        if st.session_state.chat:
            if st.button("🗑️ Clear Chat", key="clear_chat"):
                st.session_state.chat = []
                st.rerun()

    # ── TAB 2: NEW CONNECTION ──
    with tab2:
        st.markdown("""
        <div class="nc-card">
          <div class="nc-title">🆕 Request a New Internet Connection</div>
          <div class="nc-sub">Fill in the details below and our team will contact you within 24 hours to schedule installation.</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-hdr'>Choose a Plan</div>", unsafe_allow_html=True)
        plan_cols = st.columns(4)
        plans_data = [
            ("Basic Home", "25 Mbps", "PKR 2,000"),
            ("Gaming Pro", "100 Mbps", "PKR 4,000"),
            ("Ultra Fiber", "250 Mbps", "PKR 6,500"),
            ("Extreme Fiber", "500 Mbps", "PKR 9,000"),
        ]
        if "selected_plan" not in st.session_state:
            st.session_state.selected_plan = ""

        for i, (pname, speed, price) in enumerate(plans_data):
            with plan_cols[i]:
                selected_cls = "selected" if st.session_state.selected_plan == pname else ""
                st.markdown(f"""
                <div class="plan-card {selected_cls}">
                  <div class="plan-name">{pname}</div>
                  <div class="plan-speed">{speed}</div>
                  <div class="plan-price">{price}</div>
                  <div class="plan-per">/month</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Select", key=f"plan_{i}"):
                    st.session_state.selected_plan = pname
                    st.rerun()

        st.markdown("<div class='sec-hdr'>Your Details</div>", unsafe_allow_html=True)
        with st.form("new_conn_form", clear_on_submit=True):
            nc_name = st.text_input("Full Name", placeholder="e.g. Fatima Ahmed")
            nc_phone = st.text_input("Phone Number", value=phone, placeholder="03XXXXXXXXX")
            nc_area = st.selectbox("Area / Location", ["DHA","Gulshan","PECHS","Clifton","Nazimabad","Korangi","North Karachi","Malir","Other"])
            if st.form_submit_button("📩 Submit Connection Request"):
                if nc_name.strip() and nc_phone.strip() and st.session_state.selected_plan:
                    c = db()
                    c.execute("INSERT INTO new_connection_requests(name,phone,area,package,created_at) VALUES(?,?,?,?,?)",
                              (nc_name.strip(), nc_phone.strip(), nc_area,
                               st.session_state.selected_plan,
                               datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    st.success(f"✅ Connection request submitted! We'll contact you at {nc_phone.strip()} within 24 hours.")
                elif not st.session_state.selected_plan:
                    st.error("Please select a plan first.")
                else:
                    st.error("Please fill in all required fields.")

    # ── TAB 3: MY BILL ──
    with tab3:
        c = db()
        c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,))
        bill_row = c.fetchone()
        if bill_row:
            amount, due_date = bill_row
            today = datetime.date.today()
            try:
                due = datetime.date.fromisoformat(due_date)
                overdue = today > due
            except:
                overdue = False
            status_html = '<span class="bill-status-due">⚠️ OVERDUE</span>' if overdue else '<span class="bill-status-ok">✅ PENDING</span>'
            st.markdown(f"""
            <div class="bill-card">
              <div style="font-size:12px;color:#64748b;font-family:'JetBrains Mono',monospace;letter-spacing:.08em;margin-bottom:10px;">CURRENT BILL</div>
              <div class="bill-amount"><span class="bill-currency">PKR</span>{amount:,}</div>
              <div class="bill-due">📅 Due Date: {due_date}</div>
              {status_html}
            </div>""", unsafe_allow_html=True)

            # Ticket history
            c.execute("SELECT ticket_id, issue, priority, status, created_at FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5", (phone,))
            tickets = c.fetchall()
            if tickets:
                st.markdown("<div class='sec-hdr'>Recent Support Tickets</div>", unsafe_allow_html=True)
                for tid, issue, priority, status, created in tickets:
                    card_cls = "resolved" if status == "Resolved" else priority.lower()
                    st.markdown(f"""
                    <div class="ticket-card {card_cls}">
                      <div class="ticket-hdr">
                        <span class="ticket-id">{htmllib.escape(tid)}</span>
                        <span class="ticket-status {'s-resolved' if status=='Resolved' else 's-open'}">{status}</span>
                      </div>
                      <div class="ticket-issue">{htmllib.escape(issue)}</div>
                      <div class="ticket-meta">
                        {pri_tag(priority)}
                        <span class="tag tag-sent">🕐 {htmllib.escape(created)}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("No billing record found for your account.")

    # ── TAB 4: UPGRADE PLAN ──
    with tab4:
        st.markdown(f"""
        <div class="nc-card">
          <div class="nc-title">📶 Upgrade Your Plan</div>
          <div class="nc-sub">Current plan: <strong style="color:#38bdf8;">{htmllib.escape(cust["package"])}</strong> — Select a new plan below and our team will process the upgrade.</div>
        </div>""", unsafe_allow_html=True)

        up_cols = st.columns(4)
        for i, (pname, speed, price) in enumerate(plans_data):
            with up_cols[i]:
                is_current = pname == cust["package"]
                border = "border-color:#38bdf8;" if is_current else ""
                current_badge = '<div style="font-size:10px;color:#38bdf8;font-family:monospace;margin-top:6px;font-weight:700;">CURRENT PLAN</div>' if is_current else ""
                st.markdown(f"""
                <div class="plan-card" style="{border}">
                  <div class="plan-name">{pname}</div>
                  <div class="plan-speed">{speed}</div>
                  <div class="plan-price">{price}</div>
                  <div class="plan-per">/month</div>
                  {current_badge}
                </div>""", unsafe_allow_html=True)
                if not is_current:
                    if st.button(f"Upgrade →", key=f"up_{i}"):
                        # Add to chat as request
                        upgrade_msg = f"I want to upgrade my plan from {cust['package']} to {pname} ({speed}, {price}/month)"
                        st.session_state.chat.append({"role": "user", "text": upgrade_msg})
                        with st.spinner("Processing upgrade request…"):
                            result, err = process_ticket(
                                llm, phone, st.session_state.customer_type,
                                cust["name"], cust["package"], cust["area"],
                                st.session_state.network_status, st.session_state.fix_time,
                                st.session_state.bill_info, st.session_state.history_text,
                                upgrade_msg, lang
                            )
                        if result:
                            st.session_state.chat.append({"role": "ai", "result": result})
                        else:
                            st.session_state.chat.append({"role": "ai", "error": err})
                        st.success(f"Upgrade request for '{pname}' submitted! Check the Support Chat tab for the AI response.")
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
          <div class="login-sub">Enter your admin credentials to access the management dashboard</div>
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
    c.execute("SELECT COUNT(*) FROM customers"); total_cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets"); total_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'"); open_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE priority='High' AND status='Open'"); high_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM new_connection_requests"); conn_reqs = c.fetchone()[0]

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
      <div class="metric-card"><div class="metric-num red">{ht}</div><div class="metric-lbl">High Priority</div></div>
    </div>
    """.format(tc=total_cust, tt=total_tick, ot=open_tick, ht=high_tick), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎫  Tickets", "👥  Customers", "📡  Outages", "🆕  New Requests", "⚙️  Manage"])

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
                      <span class="ticket-id">{htmllib.escape(tid)}</span>
                      <span class="ticket-id">📱 {htmllib.escape(tphone)}</span>
                    </div>
                    <span class="ticket-status {'s-resolved' if status=='Resolved' else 's-open'}">{status}</span>
                  </div>
                  <div class="ticket-issue">{htmllib.escape(issue)}</div>
                  <div class="ticket-meta">
                    {pri_tag(priority)}
                    {cat_tag(issue)}
                    {sent_tag(sentiment)}
                    {tech_tag(tech)}
                    <span class="tag tag-sent">🕐 {htmllib.escape(created)}</span>
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
                color = "#f87171" if status_n == "DOWN" else "#4ade80"
                st.markdown(f"""
                <div style="background:#0b0d15;border:1px solid rgba(56,189,248,.1);border-radius:12px;padding:16px 20px;margin-bottom:10px;border-left:3px solid {color};">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <div style="font-size:15px;font-weight:700;color:#f0f6ff;">📍 {htmllib.escape(area_n)}</div>
                      <div style="font-size:12px;color:#64748b;margin-top:4px;font-family:monospace;">Expected fix: {htmllib.escape(fix_n)}</div>
                    </div>
                    <span style="background:{'rgba(248,113,113,.1)' if status_n=='DOWN' else 'rgba(74,222,128,.1)'};color:{color};padding:6px 16px;border-radius:20px;font-size:12px;font-weight:700;font-family:'JetBrains Mono',monospace;">{status_n}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No outages recorded.")

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
        st.markdown("<div class='sec-hdr'>New Connection Requests</div>", unsafe_allow_html=True)
        c.execute("SELECT name,phone,area,package,created_at FROM new_connection_requests ORDER BY created_at DESC")
        rows = c.fetchall()
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=["Name","Phone","Area","Package","Requested At"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No new connection requests yet.")

    with tab5:
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
