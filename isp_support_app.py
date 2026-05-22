import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import json
import re
import random
import datetime
import html as htmllib
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ══════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="FiberISP · AI Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════
#  GLOBAL CSS (modern, no black, deep blue/cyan)
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

.stApp {
  background: radial-gradient(circle at 10% 20%, #0a1220, #03060c);
  background-attachment: fixed;
}
.main .block-container { padding: 1.5rem 2rem 4rem; max-width: 1300px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* floating chat logo */
.floating-chat-logo {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 25px -5px rgba(14,165,233,0.5);
  cursor: pointer;
  z-index: 999;
  transition: all 0.2s;
  border: 1px solid rgba(255,255,255,0.2);
  font-size: 32px;
  backdrop-filter: blur(4px);
  animation: float 3s infinite;
}
.floating-chat-logo:hover {
  transform: scale(1.08);
  box-shadow: 0 20px 30px -8px rgba(14,165,233,0.7);
}
@keyframes float {
  0%,100%{ transform: translateY(0); }
  50%{ transform: translateY(-8px); }
}

/* welcome hero */
.welcome-hero {
  text-align: center;
  padding: 100px 20px 80px;
  background: radial-gradient(ellipse at 50% 0%, rgba(14,165,233,0.15), rgba(99,102,241,0.05));
  border-radius: 48px;
  margin: 20px 0 60px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(2px);
  border: 1px solid rgba(14,165,233,0.2);
}
.welcome-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(14,165,233,0.08) 0%, transparent 70%);
  animation: rotateSlow 20s linear infinite;
}
@keyframes rotateSlow {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.welcome-logo-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  border-radius: 32px;
  margin-bottom: 30px;
  background: linear-gradient(135deg, #0ea5e9, #3b82f6, #6366f1);
  box-shadow: 0 25px 40px rgba(14,165,233,0.4);
  animation: float 3.5s ease-in-out infinite;
  font-size: 48px;
}
.welcome-title {
  font-family: 'Syne', sans-serif;
  font-size: 72px;
  font-weight: 800;
  letter-spacing: -0.04em;
  background: linear-gradient(135deg, #38bdf8 0%, #a78bfa 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 16px;
}
.welcome-subtitle {
  font-size: 20px;
  color: #7e8ba3;
  margin-bottom: 12px;
  font-weight: 500;
}
.welcome-tagline {
  font-size: 12px;
  color: #2d4a6e;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

/* unified chat container */
.unified-chat-container {
  background: rgba(8,14,28,0.8);
  border-radius: 28px;
  border: 1px solid rgba(14,165,233,0.2);
  padding: 20px 24px;
  margin-top: 20px;
  backdrop-filter: blur(4px);
}
.sec-hdr {
  font-size: 10px;
  font-weight: 800;
  color: #2c5a7a;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(14,165,233,0.12);
  padding-bottom: 8px;
}

/* topbar */
.topbar {
  background: rgba(8,14,28,0.9);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(14,165,233,0.14);
  border-radius: 20px;
  padding: 18px 28px;
  margin-bottom: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);
}
.topbar-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #0ea5e9, #3b82f6);
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  box-shadow: 0 4px 18px rgba(14,165,233,0.35);
}
.topbar-title {
  font-family: 'Syne', sans-serif;
  font-size: 21px;
  font-weight: 800;
  color: #f1f5f9;
}
.topbar-sub {
  font-size: 10px;
  color: #1e3a5f;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}
.status-pill {
  background: rgba(34,197,94,0.07);
  border: 1px solid rgba(34,197,94,0.22);
  color: #4ade80;
  padding: 8px 18px;
  border-radius: 24px;
  font-size: 11.5px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  display: flex;
  align-items: center;
  gap: 8px;
}
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #4ade80;
  animation: blink 2s infinite;
}
@keyframes blink {
  0%,100%{ opacity: 1; box-shadow: 0 0 7px #4ade80; }
  50%{ opacity: 0.2; box-shadow: none; }
}

/* cards */
.cust-card, .form-box, .bill-card, .plan-card, .ticket-card, .choice-card-top {
  background: linear-gradient(145deg, #0e1625, #0a0f1c) !important;
  border: 1px solid rgba(14,165,233,0.16) !important;
  border-radius: 20px;
  padding: 22px 28px;
  margin-bottom: 24px;
}
.cust-name {
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #f1f5f9;
}
.cust-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.cust-chip {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(14,165,233,0.1);
  border-radius: 10px;
  padding: 7px 13px;
  font-size: 12px;
  color: #475569;
}
.cust-chip span {
  color: #e2e8f0;
  margin-left: 4px;
  font-weight: 600;
}
.choice-card-top {
  border-bottom: none;
  border-radius: 22px 22px 0 0;
  text-align: center;
}
.choice-icon-wrap {
  width: 72px;
  height: 72px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(14,165,233,0.1), rgba(99,102,241,0.1));
  border: 1px solid rgba(14,165,233,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
  margin: 0 auto 18px;
}
.choice-title {
  font-family: 'Syne', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #f1f5f9;
}
.choice-desc {
  font-size: 13.5px;
  color: #64748b;
}
.choice-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(14,165,233,0.15);
  border: 1px solid rgba(14,165,233,0.3);
  color: #38bdf8;
  font-size: 9px;
  font-weight: 800;
  padding: 3px 9px;
  border-radius: 8px;
  font-family: 'JetBrains Mono', monospace;
}
.stButton > button {
  background: linear-gradient(135deg, #0ea5e9, #3b82f6) !important;
  border: none !important;
  border-radius: 14px !important;
  font-weight: 600 !important;
  color: white !important;
  transition: 0.2s;
}
.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(14,165,233,0.4);
}
.bottom-logout {
  margin-top: 40px;
  text-align: center;
  border-top: 1px solid rgba(14,165,233,0.12);
  padding-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  CONSTANTS & DATABASE (unchanged – working)
# ══════════════════════════════════════════════
PAKISTAN_LOCATIONS = [
    "Peshawar - University Town","Peshawar - Hayatabad","Peshawar - Saddar",
    "Peshawar - Cantt","Peshawar - Gulbahar","Mardan","Swat - Mingora",
    "Abbottabad","Kohat","Dera Ismail Khan",
    "Islamabad - F-6","Islamabad - F-7","Islamabad - F-8","Islamabad - F-10",
    "Islamabad - F-11","Islamabad - G-7","Islamabad - G-9","Islamabad - G-11",
    "Islamabad - Blue Area","Islamabad - I-8","Islamabad - I-10",
    "Islamabad - Bahria Town","Islamabad - DHA",
    "Rawalpindi - Satellite Town","Rawalpindi - Bahria Town","Rawalpindi - Saddar",
    "Rawalpindi - PWD","Rawalpindi - Chaklala","Rawalpindi - Westridge",
    "Lahore - DHA","Lahore - Gulberg","Lahore - Model Town","Lahore - Johar Town",
    "Lahore - Cantt","Lahore - Faisal Town","Lahore - Bahria Town","Lahore - Township",
    "Lahore - Lake City","Lahore - Wapda Town",
    "Karachi - DHA","Karachi - Clifton","Karachi - Gulshan-e-Iqbal",
    "Karachi - PECHS","Karachi - Nazimabad","Karachi - Korangi",
    "Karachi - North Karachi","Karachi - Malir","Karachi - Saddar",
    "Karachi - Gulistan-e-Johar","Karachi - Tariq Road",
    "Faisalabad - Peoples Colony","Faisalabad - Model Town","Faisalabad - Madina Town",
    "Multan - Cantt","Multan - Gulgasht Colony","Multan - Model Town","Multan - DHA",
    "Quetta - Cantt","Quetta - Satellite Town","Quetta - Jinnah Town",
    "Sialkot","Gujranwala","Sargodha","Bahawalpur","Sukkur",
    "Hyderabad","Larkana","Gujrat","Sheikhupura","Wah Cantt","Other",
]

PLANS_LIST = [
    {"name": "Basic Home",   "speed": "25 Mbps",  "price": "PKR 2,000", "icon": "🏠", "color": "#3b82f6", "features": ["25 Mbps Download", "10 Mbps Upload", "100 GB Fair Use", "Email Support", "Standard Installation"]},
    {"name": "Gaming Pro",   "speed": "100 Mbps", "price": "PKR 4,000", "icon": "🎮", "color": "#8b5cf6", "features": ["100 Mbps Download", "50 Mbps Upload", "Unlimited Data", "Priority 24/7 Support", "Static IP Address", "Free Router"]},
    {"name": "Ultra Fiber",  "speed": "250 Mbps", "price": "PKR 6,500", "icon": "⚡", "color": "#06b6d4", "features": ["250 Mbps Download", "100 Mbps Upload", "Unlimited Data", "VIP Support Line", "2 Static IPs", "Premium Router", "Free Installation"]},
    {"name": "Extreme Fiber","speed": "500 Mbps", "price": "PKR 9,000", "icon": "🚀", "color": "#f59e0b", "features": ["500 Mbps Download", "250 Mbps Upload", "Unlimited Data", "Dedicated Support", "3 Static IPs", "Router + Mesh WiFi", "Free Installation", "SLA Guarantee"]},
]
PLANS_TEXT = "\n".join([f"• {p['name']} → {p['speed']} → {p['price']}/month" for p in PLANS_LIST])

@st.cache_resource
def get_db():
    conn = sqlite3.connect("fiberisp.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT UNIQUE, package TEXT, area TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS tickets(
        ticket_id TEXT, customer_phone TEXT, issue TEXT, priority TEXT,
        sentiment TEXT, technician TEXT, status TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS outages(
        area TEXT UNIQUE, status TEXT, expected_fix_time TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS bills(
        customer_phone TEXT UNIQUE, amount INTEGER, due_date TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS new_connection_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, area TEXT, package TEXT, created_at TEXT)""")
    conn.commit()
    # demo data
    try:
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                  ("Affan","03146532146","Gaming Pro","Peshawar - University Town"))
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES(?,?,?)",
                  ("03146532146",4000,"2026-06-20"))
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                  ("Ali Khan","03001234567","Ultra Fiber","Karachi - DHA"))
        c.execute("INSERT OR IGNORE INTO outages(area,status,expected_fix_time) VALUES(?,?,?)",
                  ("Karachi - DHA","DOWN","2 Hours"))
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES(?,?,?)",
                  ("03001234567",6500,"2026-05-30"))
        conn.commit()
    except: pass
    return conn

conn = get_db()
def db(): return conn.cursor()

# AI config
@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile", temperature=0.3)

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["name","customer_type","package","area","network_status","fix_time","bill_info","history","plans","message"],
    template="""You are a professional AI support agent for FiberISP. Respond in English. Keep replies 2-4 sentences.

Customer: {name} ({customer_type}) | Plan: {package} | Area: {area}
Network: {network_status} (Fix ETA: {fix_time})
Billing: {bill_info}
Past tickets: {history}

Plans:
{plans}

User: {message}

Return JSON: {{"priority":"High/Medium/Low","sentiment":"Positive/Neutral/Frustrated","category":"","technician_required":"yes/no","reply":"","action":"none","new_value":"","show_records":"none"}}
"""
)

def gen_ticket_id():
    return f"FIB-{datetime.datetime.now().year}-{random.randint(1000,9999)}"

def gen_tech():
    return f"TECH-{random.randint(100,999)}"

def process_ticket(llm, phone, customer_type, name, package, area, network_status, fix_time, bill_info, history, message):
    try:
        prompt_text = PROMPT_TEMPLATE.format(
            name=name, customer_type=customer_type, package=package, area=area,
            network_status=network_status, fix_time=fix_time, bill_info=bill_info,
            history=history, plans=PLANS_TEXT, message=message,
        )
        response = get_llm(st.session_state.api_key).invoke(prompt_text)
        raw = response.content.strip().replace("```json","").replace("```","").strip()
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        result = json.loads(m.group(0) if m else raw)
        ticket_id = gen_ticket_id()
        technician = gen_tech() if result.get("technician_required","").lower()=="yes" else "Not Assigned"
        c = db()
        c.execute("INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)", (
            ticket_id, phone, result.get("category","General"),
            result.get("priority","Medium"), result.get("sentiment","Neutral"),
            technician, "Open", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ))
        conn.commit()
        result["ticket_id"] = ticket_id
        result["technician"] = technician
        return result, None
    except Exception as e:
        return None, str(e)

def _handle_result(result, err, phone):
    now = datetime.datetime.now().strftime("%I:%M %p")
    if not result:
        st.session_state.chat.append({"role":"ai","error":err or "Unknown error","time":now})
        return
    action = str(result.get("action","none")).lower()
    new_val = str(result.get("new_value","")).strip()
    if action == "update_name" and new_val and len(new_val) <= 80:
        db().execute("UPDATE customers SET name=? WHERE phone=?", (new_val, phone))
        conn.commit()
        st.session_state.customer["name"] = new_val
        result["record_updated"] = {"field":"name","value":new_val}
    elif action == "update_area" and new_val:
        db().execute("UPDATE customers SET area=? WHERE phone=?", (new_val, phone))
        conn.commit()
        st.session_state.customer["area"] = new_val
        c = db()
        c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (new_val,))
        out = c.fetchone()
        if out:
            st.session_state.network_status = out[0]
            st.session_state.fix_time = out[1]
        result["record_updated"] = {"field":"area","value":new_val}
    elif action == "update_package" and new_val:
        db().execute("UPDATE customers SET package=? WHERE phone=?", (new_val, phone))
        conn.commit()
        st.session_state.customer["package"] = new_val
        result["record_updated"] = {"field":"package","value":new_val}
    show = str(result.get("show_records","none")).lower()
    if show == "bill":
        c = db()
        c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,))
        row = c.fetchone()
        if row:
            try: overdue = datetime.date.today() > datetime.date.fromisoformat(row[1])
            except: overdue = False
            result["bill_data"] = {"amount":row[0],"due_date":row[1],"overdue":overdue}
    elif show == "tickets":
        c = db()
        c.execute("SELECT ticket_id,issue,priority,status,created_at FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 4", (phone,))
        rows = c.fetchall()
        result["tickets_data"] = [{"ticket_id":r[0],"issue":r[1],"priority":r[2],"status":r[3],"created_at":r[4]} for r in rows]
    elif show == "plans":
        result["plans_data"] = True
    result["time"] = now
    st.session_state.chat.append({"role":"ai","result":result,"time":now})

# Chat renderer (with names)
def render_chat(chat_list, customer_name="Customer"):
    if not chat_list:
        st.markdown("""
        <div style="background:rgba(255,255,255,.02);border-radius:20px;padding:60px 20px;text-align:center;">
          <div style="font-size:48px;opacity:.2;">💬</div>
          <div style="font-size:13px;color:#2d5a7e;font-family:monospace;">SELECT A QUICK TOPIC OR TYPE BELOW</div>
        </div>""", unsafe_allow_html=True)
        return
    msgs_html = ""
    for msg in chat_list:
        if msg["role"] == "user":
            txt = htmllib.escape(msg.get("text",""))
            ts = msg.get("time","")
            msgs_html += f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:18px;flex-direction:row-reverse;">
              <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#dbeafe;border-radius:20px 20px 4px 20px;padding:10px 16px;max-width:70%;font-size:13.5px;line-height:1.6;">{txt}</div>
              <div style="width:36px;height:36px;background:#0f2f4f;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;">👤</div>
              <div style="font-size:9px;color:#1e3a5f;align-self:flex-end;">{customer_name} · {ts}</div>
            </div>"""
        elif msg["role"] == "ai":
            ts = msg.get("time","")
            if "error" in msg:
                msgs_html += f"<div style='background:rgba(248,113,113,0.1);padding:12px;border-radius:14px;color:#f87171;'>⚠️ {msg['error']}</div>"
                continue
            r = msg.get("result",{})
            reply_raw = str(r.get("reply","I'm here to help!"))
            reply = htmllib.escape(reply_raw).replace("\n","<br>")
            pri = r.get("priority","Low")
            sent = r.get("sentiment","Neutral")
            msgs_html += f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:18px;">
              <div style="width:36px;height:36px;background:linear-gradient(135deg,#0ea5e9,#3b82f6);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;">🤖</div>
              <div style="flex:1;background:linear-gradient(145deg,#0e1625,#0a0f1c);border-radius:18px;border:1px solid rgba(14,165,233,0.2);padding:12px 16px;">
                <div style="display:flex;gap:8px;align-items:center;border-bottom:1px solid rgba(14,165,233,0.1);padding-bottom:6px;margin-bottom:8px;">
                  <span style="font-weight:800;color:#38bdf8;">✨ FiberISP AI Assistant</span>
                  <span style="font-size:9px;background:rgba(14,165,233,0.1);padding:2px 8px;border-radius:20px;">{pri}</span>
                  <span style="font-size:9px;">{sent}</span>
                </div>
                <div>{reply}</div>
                <div style="font-size:9px;color:#3a6b8c;margin-top:8px;">{ts}</div>
              </div>
            </div>"""
    components.html(f"""
    <div style="height:500px;overflow-y:auto;padding:8px;">
      {msgs_html}
    </div>
    """, height=520, scrolling=False)

# Session state
defaults = {
    "screen":"welcome","phone":"","customer":None,"customer_type":"",
    "bill_info":"","network_status":"ACTIVE","fix_time":"N/A","history_text":"",
    "chat":[],"selected_plan":"","api_key":"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",
    "active_tab":0
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════
#  SCREENS
# ══════════════════════════════════════════════

if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="welcome-hero">
      <div class="welcome-logo-wrap">⚡</div>
      <div class="welcome-title">FiberISP</div>
      <div class="welcome-subtitle">Lightning Fast Fiber Internet Across Pakistan</div>
      <div class="welcome-tagline">AI SUPPORT · 24/7 · UNLIMITED SPEED</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;margin-bottom:20px;font-size:12px;color:#2d5a7e;font-family:monospace;'>CHOOSE ACCOUNT TYPE</div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="choice-card-top"><div class="choice-icon-wrap">👤</div><div class="choice-title">Existing Customer</div><div class="choice-desc">Login with phone number</div></div>', unsafe_allow_html=True)
        if st.button("🔑 Login", key="ex_login"): st.session_state.screen="customer_login"; st.rerun()
    with c2:
        st.markdown('<div class="choice-card-top"><div class="choice-badge">NEW</div><div class="choice-icon-wrap">✨</div><div class="choice-title">New Customer</div><div class="choice-desc">Register for connection</div></div>', unsafe_allow_html=True)
        if st.button("📝 Register", key="new_reg"): st.session_state.screen="new_customer_register"; st.rerun()
    with c3:
        st.markdown('<div class="choice-card-top"><div class="choice-icon-wrap">🛠️</div><div class="choice-title">Admin</div><div class="choice-desc">System management</div></div>', unsafe_allow_html=True)
        if st.button("🔐 Admin", key="admin_btn"): st.session_state.screen="admin_login"; st.rerun()

elif st.session_state.screen == "customer_login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div style="font-size:36px;margin-bottom:14px;">📱</div>
          <div class="form-title">Customer Login</div>
          <div class="form-sub">Enter your registered phone number</div>
        </div>""", unsafe_allow_html=True)
        phone = st.text_input("Phone Number", placeholder="03001234567", key="login_phone")
        if st.button("🔑 Login", key="do_login"):
            if phone.strip():
                c = db()
                c.execute("SELECT name,package,area FROM customers WHERE phone=?", (phone.strip(),))
                cust = c.fetchone()
                if cust:
                    st.session_state.phone = phone.strip()
                    st.session_state.customer = {"name":cust[0],"package":cust[1],"area":cust[2]}
                    st.session_state.customer_type = "Existing Customer"
                    c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone.strip(),))
                    bill = c.fetchone()
                    st.session_state.bill_info = f"PKR {bill[0]:,}, Due: {bill[1]}" if bill else "No billing record"
                    c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (cust[2],))
                    out = c.fetchone()
                    if out:
                        st.session_state.network_status = out[0]
                        st.session_state.fix_time = out[1]
                    c.execute("SELECT issue FROM tickets WHERE customer_phone=?", (phone.strip(),))
                    rows = c.fetchall()
                    st.session_state.history_text = "\n".join([f"- {r[0]}" for r in rows]) if rows else "No previous tickets."
                    st.session_state.chat = []
                    st.session_state.screen = "customer_dashboard"
                    st.rerun()
                else:
                    st.error("❌ Phone not registered. Please register as new customer.")
            else:
                st.error("⚠️ Enter phone number.")
        if st.button("← Back", key="back_login"):
            st.session_state.screen = "welcome"
            st.rerun()
        st.markdown("<p style='text-align:center;font-size:12px;color:#1e3a5f;'>Demo: <code>03001234567</code></p>", unsafe_allow_html=True)

elif st.session_state.screen == "new_customer_register":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div style="font-size:36px;margin-bottom:14px;">✨</div>
          <div class="form-title">New Customer Registration</div>
          <div class="form-sub">Fill in your details to create an account</div>
        </div>""", unsafe_allow_html=True)
        with st.form("reg_form"):
            name = st.text_input("Full Name", placeholder="e.g. Muhammad Ali")
            phone = st.text_input("Phone Number", placeholder="03001234567")
            area = st.selectbox("Your Area", PAKISTAN_LOCATIONS)
            if st.form_submit_button("✅ Create Account"):
                if name.strip() and phone.strip():
                    c = db()
                    try:
                        c.execute("INSERT INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                                  (name.strip(), phone.strip(), "No Package", area))
                        conn.commit()
                        st.session_state.phone = phone.strip()
                        st.session_state.customer = {"name":name.strip(),"package":"No Package","area":area}
                        st.session_state.customer_type = "New Customer"
                        st.session_state.bill_info = "No billing record"
                        st.session_state.history_text = "No previous tickets."
                        st.session_state.chat = []
                        c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (area,))
                        out = c.fetchone()
                        if out:
                            st.session_state.network_status = out[0]
                            st.session_state.fix_time = out[1]
                        st.session_state.screen = "customer_dashboard"
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ Phone already registered. Please login.")
                else:
                    st.error("⚠️ Fill all fields.")
        if st.button("← Back", key="back_reg"):
            st.session_state.screen = "welcome"
            st.rerun()

elif st.session_state.screen == "admin_login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div style="font-size:36px;margin-bottom:14px;">🔐</div>
          <div class="form-title">Admin Access</div>
          <div class="form-sub">Enter admin password</div>
        </div>""", unsafe_allow_html=True)
        pwd = st.text_input("Admin Password", type="password", placeholder="Enter password")
        if st.button("Login →", key="admin_go"):
            if pwd == "admin123":
                st.session_state.screen = "admin"
                st.rerun()
            else:
                st.error("❌ Incorrect password.")
        if st.button("← Back", key="back_admin"):
            st.session_state.screen = "welcome"
            st.rerun()

elif st.session_state.screen == "admin":
    # Admin dashboard (keep original, just a summary)
    c = db()
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;">
      <div style="background:#0e1625;border-radius:16px;padding:20px;"><div style="font-size:36px;color:#0ea5e9;">{c.execute('SELECT COUNT(*) FROM customers').fetchone()[0]}</div><div>Customers</div></div>
      <div style="background:#0e1625;border-radius:16px;padding:20px;"><div style="font-size:36px;">{c.execute('SELECT COUNT(*) FROM tickets').fetchone()[0]}</div><div>Tickets</div></div>
      <div style="background:#0e1625;border-radius:16px;padding:20px;"><div style="font-size:36px;color:#fbbf24;">{c.execute('SELECT COUNT(*) FROM tickets WHERE status="Open"').fetchone()[0]}</div><div>Open Tickets</div></div>
      <div style="background:#0e1625;border-radius:16px;padding:20px;"><div style="font-size:36px;color:#f87171;">{c.execute('SELECT COUNT(*) FROM tickets WHERE priority="High" AND status="Open"').fetchone()[0]}</div><div>High Priority</div></div>
    </div>""", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Tickets", "Customers"])
    with tab1:
        for row in c.execute("SELECT * FROM tickets ORDER BY created_at DESC").fetchall():
            st.write(f"{row[0]} | {row[2]} | {row[3]} | {row[6]}")
    with tab2:
        st.dataframe(c.execute("SELECT name,phone,package,area FROM customers").fetchall(), use_container_width=True)
    if st.button("← Logout", key="admin_logout"):
        for k in defaults: st.session_state[k] = defaults[k]
        st.rerun()

elif st.session_state.screen == "customer_dashboard":
    cust = st.session_state.customer
    phone = st.session_state.phone

    # Top bar
    st.markdown("""
    <div class="topbar">
      <div style="display:flex;gap:14px;"><div class="topbar-icon">⚡</div><div><div class="topbar-title">FiberISP</div><div class="topbar-sub">AI CUSTOMER SUPPORT</div></div></div>
      <div class="status-pill"><div class="status-dot"></div>ONLINE</div>
    </div>""", unsafe_allow_html=True)

    # Customer info card
    outage_html = ""
    if st.session_state.network_status == "DOWN":
        outage_html = f'<div style="background:rgba(248,113,113,0.1);padding:10px;border-radius:12px;margin-top:12px;">⚠️ Outage in {cust["area"]} — Fix ETA: {st.session_state.fix_time}</div>'
    st.markdown(f"""
    <div class="cust-card">
      <div style="display:flex;justify-content:space-between;">
        <div class="cust-name">👋 Welcome, {htmllib.escape(cust['name'])}</div>
        <span style="font-size:11px;background:rgba(14,165,233,0.1);padding:4px 12px;border-radius:20px;">🇬🇧 EN</span>
      </div>
      <div class="cust-meta">
        <div class="cust-chip">📱 {htmllib.escape(phone)}</div>
        <div class="cust-chip">📦 {htmllib.escape(cust['package'])}</div>
        <div class="cust-chip">📍 {htmllib.escape(cust['area'])}</div>
        <div class="cust-chip">💳 {htmllib.escape(st.session_state.bill_info)}</div>
      </div>
      {outage_html}
    </div>""", unsafe_allow_html=True)

    # Tabs
    tab_names = ["💬 AI Support Chat", "🔌 New Connection", "💳 Bill & Tickets", "⬆️ Upgrade Plan"]
    cols = st.columns(len(tab_names))
    for i, name in enumerate(tab_names):
        if cols[i].button(name, key=f"tab_{i}", use_container_width=True):
            st.session_state.active_tab = i
            st.rerun()
        if st.session_state.active_tab == i:
            st.markdown(f"<style>div[data-testid='column']:nth-child({i+1}) button {{background: linear-gradient(135deg,#0f2b3f,#142c44) !important; color:#38bdf8 !important; border:1px solid rgba(14,165,233,0.3) !important;}}</style>", unsafe_allow_html=True)

    # TAB 0: Chat
    if st.session_state.active_tab == 0:
        st.markdown('<div class="unified-chat-container">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;background:rgba(14,165,233,0.05);border-radius:20px;padding:12px 20px;">
          <div style="width:48px;height:48px;background:linear-gradient(135deg,#0ea5e9,#6366f1);border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:24px;">🤖</div>
          <div><div style="font-weight:800;color:#38bdf8;">FiberISP AI Assistant</div><div style="font-size:12px;color:#6c8eae;">Ask about bills, outages, or say "change my name to Ahmed"</div></div>
          <div style="margin-left:auto;"><span class="status-dot"></span> <span style="color:#4ade80;font-size:12px;">ONLINE</span></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="sec-hdr">QUICK TOPICS</div>', unsafe_allow_html=True)
        quick = [("🐌","Slow internet speed"),("📡","WiFi not working"),("⛔","No internet connection"),("💳","Show my bill"),("⬆️","Upgrade my plan"),("🔁","Restart router"),("📶","Weak WiFi signal"),("🔧","Request technician"),("📋","Show my tickets"),("📦","Available plans")]
        qcols = st.columns(5)
        for idx, (icon, label) in enumerate(quick):
            with qcols[idx%5]:
                if st.button(f"{icon} {label}", key=f"qt_{idx}", use_container_width=True):
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.chat.append({"role":"user","text":label,"time":now})
                    with st.spinner("AI is thinking..."):
                        res, err = process_ticket(None, phone, st.session_state.customer_type, cust["name"], cust["package"], cust["area"], st.session_state.network_status, st.session_state.fix_time, st.session_state.bill_info, st.session_state.history_text, label)
                    _handle_result(res, err, phone)
                    st.rerun()
        st.markdown('<div class="sec-hdr">CONVERSATION</div>', unsafe_allow_html=True)
        render_chat(st.session_state.chat, customer_name=cust["name"])
        user_msg = st.chat_input("Type your message... e.g. 'change my name to Ahmed'")
        if user_msg:
            now = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state.chat.append({"role":"user","text":user_msg,"time":now})
            with st.spinner("AI is thinking..."):
                res, err = process_ticket(None, phone, st.session_state.customer_type, cust["name"], cust["package"], cust["area"], st.session_state.network_status, st.session_state.fix_time, st.session_state.bill_info, st.session_state.history_text, user_msg)
            _handle_result(res, err, phone)
            st.rerun()
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 1: New Connection
    elif st.session_state.active_tab == 1:
        st.markdown("""
        <div style="background:linear-gradient(150deg,#0d1524,#0f1d35);border-radius:18px;padding:24px 28px;margin-bottom:24px;">
          <div style="font-size:20px;font-weight:700;">🔌 Request a New Internet Connection</div>
          <div>Our team will contact you within 24 hours.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='sec-hdr'>Select a Plan</div>", unsafe_allow_html=True)
        pcols = st.columns(4)
        for i, p in enumerate(PLANS_LIST):
            with pcols[i]:
                st.markdown(f"""
                <div class="plan-card" style="border:1px solid rgba(14,165,233,0.2);border-radius:16px;padding:15px;text-align:center;">
                  <div style="font-size:28px;">{p['icon']}</div>
                  <div><b>{p['name']}</b></div>
                  <div style="color:#0ea5e9;">{p['speed']}</div>
                  <div style="font-size:22px;color:#fbbf24;">{p['price']}<span style="font-size:10px;">/mo</span></div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Select", key=f"plan_{i}", use_container_width=True):
                    st.session_state.selected_plan = p["name"]
                    st.rerun()
        if st.session_state.selected_plan:
            st.info(f"Selected: {st.session_state.selected_plan}")
        with st.form("nc_form"):
            nc_name = st.text_input("Full Name", value=cust["name"])
            nc_phone = st.text_input("Phone Number", value=phone)
            nc_area = st.selectbox("Installation Area", PAKISTAN_LOCATIONS, index=PAKISTAN_LOCATIONS.index(cust["area"]) if cust["area"] in PAKISTAN_LOCATIONS else 0)
            if st.form_submit_button("Submit Request"):
                if nc_name.strip() and nc_phone.strip() and st.session_state.selected_plan:
                    db().execute("INSERT INTO new_connection_requests(name,phone,area,package,created_at) VALUES(?,?,?,?,?)",
                                 (nc_name.strip(), nc_phone.strip(), nc_area, st.session_state.selected_plan, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    st.success("Request submitted!")
                    st.session_state.selected_plan = ""
                else:
                    st.error("Please fill all fields and select a plan.")

    # TAB 2: Bill & Tickets
    elif st.session_state.active_tab == 2:
        c = db()
        bill = c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,)).fetchone()
        if bill:
            amt, due = bill
            st.markdown(f"""
            <div class="bill-card">
              <div style="font-size:10px;">CURRENT BILL</div>
              <div style="font-size:36px;font-weight:800;color:#fbbf24;">PKR {amt:,}</div>
              <div>Due: {due}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("No billing record.")
        st.markdown("<div class='sec-hdr'>Recent Support Tickets</div>", unsafe_allow_html=True)
        tickets = c.execute("SELECT ticket_id,issue,priority,status,created_at FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5", (phone,)).fetchall()
        for t in tickets:
            st.markdown(f"<div class='ticket-card'><b>{t[0]}</b> - {t[1]}<br>Priority: {t[2]} | Status: {t[3]}</div>", unsafe_allow_html=True)

    # TAB 3: Upgrade Plan
    elif st.session_state.active_tab == 3:
        st.markdown(f"""
        <div style="background:linear-gradient(150deg,#0d1524,#0f1d35);border-radius:18px;padding:24px 28px;margin-bottom:24px;">
          <div style="font-size:20px;font-weight:700;">⬆️ Upgrade Your Plan</div>
          <div>Current: <strong>{cust['package']}</strong></div>
        </div>""", unsafe_allow_html=True)
        up_cols = st.columns(4)
        for i, p in enumerate(PLANS_LIST):
            with up_cols[i]:
                is_cur = p["name"].lower() in cust["package"].lower()
                st.markdown(f"""
                <div class="plan-card" style="border:1px solid rgba(14,165,233,0.2);border-radius:16px;padding:15px;text-align:center;">
                  <div style="font-size:28px;">{p['icon']}</div>
                  <div><b>{p['name']}</b></div>
                  <div style="color:#0ea5e9;">{p['speed']}</div>
                  <div style="font-size:22px;color:#fbbf24;">{p['price']}<span style="font-size:10px;">/mo</span></div>
                </div>""", unsafe_allow_html=True)
                if not is_cur:
                    if st.button(f"Upgrade to {p['name']}", key=f"up_{i}", use_container_width=True):
                        msg = f"I want to upgrade from {cust['package']} to {p['name']}"
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        st.session_state.chat.append({"role":"user","text":msg,"time":now})
                        with st.spinner("Processing..."):
                            res, err = process_ticket(None, phone, st.session_state.customer_type, cust["name"], cust["package"], cust["area"], st.session_state.network_status, st.session_state.fix_time, st.session_state.bill_info, st.session_state.history_text, msg)
                        _handle_result(res, err, phone)
                        st.success(f"Upgrade to {p['name']} requested. Check AI chat.")
                        st.rerun()

    # Logout button at bottom
    st.markdown('<div class="bottom-logout">', unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_bottom"):
        for k in defaults: st.session_state[k] = defaults[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Floating chat logo (switches to tab 0)
    st.markdown("""
    <div class="floating-chat-logo" onclick="document.querySelector('div[data-testid=\"stButton\"] button').click();">
      💬
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="hidden_chat_trigger", help="Open AI Chat"):
        st.session_state.active_tab = 0
        st.rerun()
    st.markdown("<style>div[data-testid='stButton']:has(button:contains('hidden_chat_trigger')) {display: none;}</style>", unsafe_allow_html=True)
