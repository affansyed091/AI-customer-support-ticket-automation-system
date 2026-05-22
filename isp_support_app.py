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
#  GLOBAL CSS  (completely redesigned)
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Reset & Base ── */
*{margin:0;padding:0;box-sizing:border-box;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif !important;}
.stApp{
  background:#060b14;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(14,165,233,.12), transparent),
    linear-gradient(180deg,#060b14 0%,#080e1c 100%);
  background-attachment:fixed;
}
.main .block-container{padding:1.5rem 2rem 4rem;max-width:1200px;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}

/* ── Grid Background ── */
.stApp::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(14,165,233,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(14,165,233,.025) 1px, transparent 1px);
  background-size:60px 60px;
}

/* ══════════════════ WELCOME HERO ══════════════════ */
.welcome-hero{
  text-align:center;padding:90px 20px 70px;
  background:linear-gradient(135deg,rgba(14,165,233,.07),rgba(99,102,241,.04));
  border-radius:28px;border:1px solid rgba(14,165,233,.16);
  margin:24px 0 48px;position:relative;overflow:hidden;
  box-shadow:0 30px 80px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.05);
}
.welcome-hero::before{
  content:'';position:absolute;top:-40%;left:-40%;width:180%;height:180%;
  background:radial-gradient(circle at 50% 40%, rgba(14,165,233,.09) 0%, transparent 65%);
  animation:hpulse 8s ease-in-out infinite;
}
.welcome-hero::after{
  content:'';position:absolute;bottom:-2px;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(14,165,233,.4),transparent);
}
@keyframes hpulse{0%,100%{transform:scale(1);opacity:.5;}50%{transform:scale(1.1);opacity:1;}}

.welcome-logo-wrap{
  display:inline-flex;align-items:center;justify-content:center;
  width:90px;height:90px;border-radius:28px;margin-bottom:24px;
  background:linear-gradient(135deg,#0ea5e9,#3b82f6,#6366f1);
  box-shadow:0 20px 50px rgba(14,165,233,.35);
  animation:float 3.5s ease-in-out infinite;position:relative;z-index:1;
  font-size:42px;
}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-12px);}}

.welcome-title{
  font-family:'Syne',sans-serif;font-size:56px;font-weight:800;letter-spacing:-.04em;
  background:linear-gradient(135deg,#38bdf8 0%,#6366f1 60%,#a78bfa 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:16px;position:relative;z-index:1;
}
.welcome-subtitle{font-size:19px;color:#94a3b8;margin-bottom:12px;z-index:1;position:relative;font-weight:500;}
.welcome-tagline{
  font-size:11px;color:#1e3a5f;z-index:1;position:relative;
  font-family:'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;
}

/* ══════════════════ TOP BAR ══════════════════ */
.topbar{
  background:rgba(8,14,28,.9);backdrop-filter:blur(24px);
  border:1px solid rgba(14,165,233,.14);border-radius:20px;
  padding:18px 28px;margin-bottom:28px;
  display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 8px 40px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.04);
}
.topbar-icon{
  width:44px;height:44px;
  background:linear-gradient(135deg,#0ea5e9,#3b82f6);
  border-radius:13px;display:flex;align-items:center;justify-content:center;
  font-size:22px;box-shadow:0 4px 18px rgba(14,165,233,.35);
  animation:glow 2.5s ease-in-out infinite alternate;
}
@keyframes glow{from{box-shadow:0 4px 18px rgba(14,165,233,.3);}to{box-shadow:0 4px 28px rgba(14,165,233,.6);}}
.topbar-title{font-family:'Syne',sans-serif;font-size:21px;font-weight:800;color:#f1f5f9;letter-spacing:-.02em;}
.topbar-sub{font-size:10px;color:#1e3a5f;font-family:'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;margin-top:2px;}
.status-pill{
  background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.22);
  color:#4ade80;padding:8px 18px;border-radius:24px;
  font-size:11.5px;font-weight:700;font-family:'JetBrains Mono',monospace;
  display:flex;align-items:center;gap:8px;
}
.status-dot{width:7px;height:7px;border-radius:50%;background:#4ade80;animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1;box-shadow:0 0 7px #4ade80;}50%{opacity:.2;box-shadow:none;}}

/* ══════════════════ CHOICE CARDS (Landing) ══════════════════ */
/* The card top half — icon + title + desc */
.choice-card-top{
  background:linear-gradient(150deg,#0d1524,#0f1d35);
  border:1px solid rgba(14,165,233,.14);
  border-bottom:none;
  border-radius:22px 22px 0 0;
  padding:40px 28px 28px;
  text-align:center;
  position:relative;overflow:hidden;
  transition:border-color .3s,background .3s;
}
.choice-card-top::before{
  content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(14,165,233,.06),transparent);
  transition:left .5s;
}
.choice-card-top:hover::before{left:100%;}
.choice-icon-wrap{
  width:72px;height:72px;border-radius:20px;
  background:linear-gradient(135deg,rgba(14,165,233,.1),rgba(99,102,241,.1));
  border:1px solid rgba(14,165,233,.18);
  display:flex;align-items:center;justify-content:center;
  font-size:34px;margin:0 auto 18px;
  transition:all .3s;
}
.choice-title{
  font-family:'Syne',sans-serif;font-size:20px;font-weight:700;
  color:#f1f5f9;margin-bottom:10px;
}
.choice-desc{font-size:13.5px;color:#475569;line-height:1.75;}
.choice-badge{
  position:absolute;top:14px;right:14px;
  background:rgba(14,165,233,.15);border:1px solid rgba(14,165,233,.3);
  color:#38bdf8;font-size:9px;font-weight:800;padding:3px 9px;
  border-radius:8px;font-family:'JetBrains Mono',monospace;letter-spacing:.1em;
}

/* ── Button fused to card bottom ── */
.stButton > button {
  background:linear-gradient(135deg,#0ea5e9,#3b82f6) !important;
  color:white !important;border:none !important;
  border-radius:12px !important;
  font-family:'DM Sans',sans-serif !important;font-weight:600 !important;font-size:14px !important;
  padding:12px 24px !important;transition:all .25s !important;width:100% !important;
  box-shadow:0 4px 18px rgba(14,165,233,.22) !important;
}
.stButton > button:hover{
  transform:translateY(-2px) !important;
  box-shadow:0 8px 28px rgba(14,165,233,.35) !important;
  background:linear-gradient(135deg,#38bdf8,#6366f1) !important;
}
.stButton > button:active{transform:translateY(0) !important;}

/* Landing card wrapper — fuses card top + button */
.landing-col > div > div > div > div:nth-child(1) > div{
  margin-bottom:-1px !important;
}

/* ══════════════════ FORM BOX ══════════════════ */
.form-box{
  background:linear-gradient(150deg,#0d1524,#0f1d35);
  border:1px solid rgba(14,165,233,.16);border-radius:24px;
  padding:40px 36px;max-width:480px;margin:0 auto;
  box-shadow:0 16px 60px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.04);
}
.form-title{font-family:'Syne',sans-serif;font-size:26px;font-weight:700;color:#f1f5f9;margin-bottom:8px;}
.form-sub{font-size:14px;color:#475569;margin-bottom:28px;line-height:1.75;}

/* ══════════════════ CUSTOMER CARD ══════════════════ */
.cust-card{
  background:linear-gradient(150deg,#0d1524,#0f1d35);
  border:1px solid rgba(14,165,233,.16);border-radius:20px;
  padding:22px 28px;margin-bottom:24px;
  box-shadow:0 8px 32px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.04);
}
.cust-name{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:#f1f5f9;margin-bottom:14px;letter-spacing:-.02em;}
.cust-meta{display:flex;gap:8px;flex-wrap:wrap;}
.cust-chip{
  background:rgba(255,255,255,.04);border:1px solid rgba(14,165,233,.1);
  border-radius:10px;padding:7px 13px;font-size:12px;color:#475569;
  font-family:'JetBrains Mono',monospace;
}
.cust-chip span{color:#e2e8f0;margin-left:4px;font-weight:600;}
.outage-warn{
  background:rgba(248,113,113,.06);border:1px solid rgba(248,113,113,.2);
  border-radius:10px;padding:10px 16px;font-size:13px;color:#fca5a5;margin-top:12px;font-weight:600;
}

/* ══════════════════ SECTION HEADER ══════════════════ */
.sec-hdr{
  font-size:10px;font-weight:800;color:#1e3a5f;letter-spacing:.2em;text-transform:uppercase;
  font-family:'JetBrains Mono',monospace;margin:24px 0 14px;
  padding-bottom:8px;border-bottom:1px solid rgba(14,165,233,.07);
}

/* ══════════════════ CHAT BANNER ══════════════════ */
.chat-banner{
  background:linear-gradient(135deg,rgba(14,165,233,.07),rgba(99,102,241,.04));
  border:1px solid rgba(14,165,233,.16);border-radius:16px;
  padding:16px 22px;margin-bottom:18px;display:flex;align-items:center;gap:16px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04);
}
.chat-banner-icon{
  width:44px;height:44px;
  background:linear-gradient(135deg,#0ea5e9,#3b82f6);
  border-radius:13px;display:flex;align-items:center;justify-content:center;
  font-size:22px;flex-shrink:0;box-shadow:0 4px 14px rgba(14,165,233,.3);
}
.chat-banner-title{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#38bdf8;margin-bottom:3px;}
.chat-banner-sub{font-size:12.5px;color:#334155;line-height:1.6;}
.online-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#4ade80;margin-right:5px;animation:blink 2s infinite;vertical-align:middle;}

/* ══════════════════ PLAN CARDS ══════════════════ */
.plan-card{
  background:linear-gradient(150deg,#0d1524,#0f1d35);
  border:1px solid rgba(14,165,233,.1);border-radius:18px;
  padding:22px 18px;text-align:center;transition:all .28s;
  position:relative;overflow:hidden;
}
.plan-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:var(--plan-accent,linear-gradient(90deg,#0ea5e9,#3b82f6));
  opacity:.6;
}
.plan-card:hover{border-color:rgba(14,165,233,.38);transform:translateY(-4px);box-shadow:0 14px 40px rgba(14,165,233,.1);}
.plan-card.selected,.plan-card.current{border-color:#0ea5e9;background:rgba(14,165,233,.05);}
.plan-name{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:4px;}
.plan-speed{font-size:11px;color:#0ea5e9;font-family:'JetBrains Mono',monospace;margin-bottom:12px;letter-spacing:.06em;}
.plan-price{font-size:24px;font-weight:800;color:#fbbf24;letter-spacing:-.03em;}
.plan-per{font-size:10.5px;color:#334155;margin-top:3px;margin-bottom:14px;font-family:'JetBrains Mono',monospace;}
.plan-features{list-style:none;text-align:left;margin-bottom:0;}
.plan-features li{
  font-size:12px;color:#475569;padding:5px 0;
  border-bottom:1px solid rgba(255,255,255,.03);
  display:flex;align-items:center;gap:7px;
}
.plan-features li:last-child{border-bottom:none;}
.plan-features li::before{content:'✓';color:#0ea5e9;font-weight:700;font-size:11px;flex-shrink:0;}
.plan-current-badge{
  display:inline-block;font-size:9px;font-weight:800;
  color:#0ea5e9;font-family:'JetBrains Mono',monospace;
  letter-spacing:.08em;margin-top:10px;padding:3px 10px;
  background:rgba(14,165,233,.08);border:1px solid rgba(14,165,233,.2);border-radius:10px;
}

/* ══════════════════ BILL CARD ══════════════════ */
.bill-card{
  background:linear-gradient(150deg,#0d1524,#0f1d35);
  border:1px solid rgba(251,191,36,.16);border-radius:18px;
  padding:26px 28px;margin-bottom:20px;
  box-shadow:0 8px 32px rgba(0,0,0,.4);
}
.bill-amount{font-family:'Syne',sans-serif;font-size:48px;font-weight:800;color:#fbbf24;letter-spacing:-.04em;}
.bill-currency{font-size:18px;color:#64748b;margin-right:5px;font-weight:400;}
.bill-due{font-size:12px;color:#475569;margin-top:6px;font-family:'JetBrains Mono',monospace;}
.bill-status-ok{background:rgba(74,222,128,.07);border:1px solid rgba(74,222,128,.22);color:#4ade80;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;}
.bill-status-due{background:rgba(248,113,113,.07);border:1px solid rgba(248,113,113,.22);color:#f87171;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;}

/* ══════════════════ TICKET CARD ══════════════════ */
.ticket-card{
  background:#0a1120;border:1px solid rgba(14,165,233,.08);
  border-radius:14px;padding:16px 20px;margin-bottom:10px;
  border-left:3px solid #1e293b;transition:all .22s;
}
.ticket-card:hover{box-shadow:0 8px 24px rgba(14,165,233,.06);transform:translateX(2px);}
.ticket-card.high{border-left-color:#f87171;}
.ticket-card.medium{border-left-color:#fbbf24;}
.ticket-card.low{border-left-color:#4ade80;}
.ticket-card.resolved{border-left-color:#1e293b;opacity:.55;}
.ticket-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.ticket-id{font-family:'JetBrains Mono',monospace;font-size:11px;color:#334155;font-weight:600;}
.ticket-status{font-size:10px;font-weight:700;padding:3px 10px;border-radius:18px;}
.s-open{background:rgba(14,165,233,.09);color:#7dd3fc;border:1px solid rgba(14,165,233,.15);}
.s-resolved{background:rgba(51,65,85,.3);color:#475569;border:1px solid rgba(51,65,85,.4);}
.ticket-issue{font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:8px;}
.ticket-meta{display:flex;gap:6px;flex-wrap:wrap;}
.tag{font-size:10px;font-weight:700;padding:3px 9px;border-radius:18px;font-family:'JetBrains Mono',monospace;}
.tag-high{background:rgba(248,113,113,.09);color:#f87171;border:1px solid rgba(248,113,113,.18);}
.tag-medium{background:rgba(251,191,36,.09);color:#fbbf24;border:1px solid rgba(251,191,36,.18);}
.tag-low{background:rgba(74,222,128,.07);color:#4ade80;border:1px solid rgba(74,222,128,.18);}
.tag-sent{background:rgba(100,116,139,.08);color:#475569;border:1px solid rgba(100,116,139,.16);}

/* ══════════════════ METRIC GRID ══════════════════ */
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;}
.metric-card{
  background:linear-gradient(150deg,#0d1524,#0f1d35);
  border:1px solid rgba(14,165,233,.1);border-radius:16px;padding:20px 22px;
  transition:border-color .2s;
}
.metric-card:hover{border-color:rgba(14,165,233,.25);}
.metric-num{font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#f1f5f9;}
.metric-num.blue{color:#0ea5e9;}.metric-num.yellow{color:#fbbf24;}.metric-num.red{color:#f87171;}.metric-num.green{color:#4ade80;}
.metric-lbl{font-size:10px;color:#1e3a5f;font-family:'JetBrains Mono',monospace;margin-top:7px;letter-spacing:.12em;text-transform:uppercase;}

/* ══════════════════ QUICK TOPIC BUTTONS ══════════════════ */
.stButton.quick-wrap > button {
  background:rgba(14,165,233,.07) !important;
  border:1px solid rgba(14,165,233,.18) !important;
  color:#93c5fd !important;
  border-radius:10px !important;
  font-size:13px !important;
  font-weight:500 !important;
  padding:10px 12px !important;
  box-shadow:none !important;
  transition:all .2s !important;
}
.stButton.quick-wrap > button:hover{
  background:rgba(14,165,233,.15) !important;
  border-color:rgba(14,165,233,.38) !important;
  color:#bae6fd !important;
  transform:translateY(-1px) !important;
  box-shadow:0 4px 12px rgba(14,165,233,.12) !important;
}

/* ══════════════════ STREAMLIT OVERRIDES ══════════════════ */
.stTextInput>div>div>input,
.stSelectbox>div>div>div,
.stTextArea>div>div>textarea{
  background:#0a1120 !important;
  border:1px solid rgba(14,165,233,.18) !important;
  border-radius:12px !important;color:#f1f5f9 !important;
  font-family:'DM Sans',sans-serif !important;
  padding:11px 15px !important;font-size:14px !important;
  transition:all .2s !important;
}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
  border-color:#0ea5e9 !important;
  box-shadow:0 0 0 3px rgba(14,165,233,.1) !important;
}
label{
  color:#334155 !important;font-size:11px !important;font-weight:700 !important;
  letter-spacing:.1em !important;text-transform:uppercase !important;
  font-family:'JetBrains Mono',monospace !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,.03);
  border:1px solid rgba(14,165,233,.1);
  border-radius:14px;padding:5px;gap:4px;
}
.stTabs [data-baseweb="tab"]{
  background:transparent !important;
  color:#334155 !important;
  font-family:'DM Sans',sans-serif !important;font-weight:600 !important;font-size:13.5px !important;
  border-radius:10px !important;padding:10px 18px !important;
  border:none !important;transition:all .2s !important;
}
.stTabs [data-baseweb="tab"]:hover{
  background:rgba(255,255,255,.05) !important;
  color:#94a3b8 !important;
}
.stTabs [aria-selected="true"]{
  background:rgba(14,165,233,.12) !important;
  color:#38bdf8 !important;
  border:1px solid rgba(14,165,233,.22) !important;
}
.stTabs [data-baseweb="tab-highlight"]{display:none !important;}
.stTabs [data-baseweb="tab-border"]{display:none !important;}

/* Alerts */
.stSuccess{background:rgba(74,222,128,.06) !important;border:1px solid rgba(74,222,128,.2) !important;color:#4ade80 !important;border-radius:12px !important;}
.stError{background:rgba(248,113,113,.06) !important;border:1px solid rgba(248,113,113,.2) !important;color:#f87171 !important;border-radius:12px !important;}
.stInfo{background:rgba(14,165,233,.06) !important;border:1px solid rgba(14,165,233,.2) !important;color:#7dd3fc !important;border-radius:12px !important;}

/* Chat input */
div[data-testid="stChatInput"]{background:#0a1120 !important;}
div[data-testid="stChatInput"] textarea{
  background:#0a1120 !important;
  border:1px solid rgba(14,165,233,.16) !important;
  color:#f1f5f9 !important;border-radius:14px !important;
  font-family:'DM Sans',sans-serif !important;font-size:14px !important;
}

/* Dataframe */
.stDataFrame{border-radius:14px !important;overflow:hidden;}

/* Spinner */
.stSpinner > div{border-top-color:#0ea5e9 !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  CONSTANTS
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
    {
        "name": "Basic Home",   "speed": "25 Mbps",  "price": "PKR 2,000", "icon": "🏠",
        "color": "#3b82f6",
        "features": ["25 Mbps Download", "10 Mbps Upload", "100 GB Fair Use",
                     "Email Support", "Standard Installation"],
    },
    {
        "name": "Gaming Pro",   "speed": "100 Mbps", "price": "PKR 4,000", "icon": "🎮",
        "color": "#8b5cf6",
        "features": ["100 Mbps Download", "50 Mbps Upload", "Unlimited Data",
                     "Priority 24/7 Support", "Static IP Address", "Free Router"],
    },
    {
        "name": "Ultra Fiber",  "speed": "250 Mbps", "price": "PKR 6,500", "icon": "⚡",
        "color": "#06b6d4",
        "features": ["250 Mbps Download", "100 Mbps Upload", "Unlimited Data",
                     "VIP Support Line", "2 Static IPs", "Premium Router", "Free Installation"],
    },
    {
        "name": "Extreme Fiber","speed": "500 Mbps", "price": "PKR 9,000", "icon": "🚀",
        "color": "#f59e0b",
        "features": ["500 Mbps Download", "250 Mbps Upload", "Unlimited Data",
                     "Dedicated Support", "3 Static IPs", "Router + Mesh WiFi",
                     "Free Installation", "SLA Guarantee"],
    },
]

PLANS_TEXT = "\n".join([f"• {p['name']} → {p['speed']} → {p['price']}/month" for p in PLANS_LIST])

# ══════════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════════
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
    except Exception:
        pass
    return conn

conn = get_db()
def db(): return conn.cursor()

# ══════════════════════════════════════════════
#  AI CONFIG
# ══════════════════════════════════════════════
@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["name","customer_type","package","area","network_status",
                     "fix_time","bill_info","history","plans","message"],
    template="""You are a professional AI support agent for FiberISP — a Pakistani fiber internet provider.
You are friendly, concise, and helpful. Always respond in English only.

CUSTOMER PROFILE:
  Name: {name} ({customer_type})
  Package: {package} | Area: {area}
  Network: {network_status} (Fix ETA: {fix_time})
  Billing: {bill_info}
  Past tickets: {history}

AVAILABLE PLANS:
{plans}

USER MESSAGE: {message}

YOUR CAPABILITIES — set the matching fields:
1. RECORD ACTIONS (set "action" + "new_value"):
   - "update_name"    → user wants to change their display name
   - "update_area"    → user wants to change their registered area
   - "update_package" → user wants to upgrade/change plan (new_value = exact plan name from list)
   - "none"           → no record change needed

2. SHOW DATA CARDS (set "show_records"):
   - "bill"    → user asks about bill, amount, payment, due date
   - "tickets" → user asks about ticket history, past complaints, status
   - "plans"   → user asks to see available plans or compare options
   - "none"    → no special data card needed

RULES:
- Keep "reply" to 2-4 sentences. Be empathetic and professional.
- For connectivity issues: give 2-3 step troubleshooting tips.
- Only mention outage if network_status is DOWN.
- priority: High (no internet/outage), Medium (slow/degraded), Low (billing/info queries)
- sentiment: Positive / Neutral / Frustrated / Angry

Return ONLY valid JSON (no markdown, no code blocks, no extra text):
{{"priority":"","sentiment":"","category":"","technician_required":"yes/no","reply":"","action":"none","new_value":"","show_records":"none"}}
"""
)

# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def gen_ticket_id():
    return f"FIB-{datetime.datetime.now().year}-{random.randint(1000,9999)}"

def gen_tech():
    return f"TECH-{random.randint(100,999)}"

def process_ticket(llm, phone, customer_type, name, package, area,
                   network_status, fix_time, bill_info, history, message):
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
            ticket_id, phone,
            result.get("category","General"),
            result.get("priority","Medium"),
            result.get("sentiment","Neutral"),
            technician, "Open",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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


# ══════════════════════════════════════════════
#  CHAT RENDERER  (self-contained HTML component)
# ══════════════════════════════════════════════
def render_chat(chat_list):
    if not chat_list:
        st.markdown("""
        <div style="background:rgba(255,255,255,.02);border:1px solid rgba(14,165,233,.08);
             border-radius:16px;padding:60px 20px;text-align:center;">
          <div style="font-size:48px;margin-bottom:16px;opacity:.15;">💬</div>
          <div style="font-size:13px;color:#1e3a5f;font-family:'JetBrains Mono',monospace;letter-spacing:.06em;">
            SELECT A QUICK TOPIC ABOVE OR TYPE BELOW TO BEGIN
          </div>
        </div>""", unsafe_allow_html=True)
        return

    msgs_html = ""

    for msg in chat_list:
        if msg["role"] == "user":
            txt = htmllib.escape(msg.get("text",""))
            ts  = msg.get("time","")
            msgs_html += f"""
            <div class="row user-row">
              <div class="umsg">
                <div class="ubub">{txt}</div>
                <div class="utime">{htmllib.escape(ts)} · You</div>
              </div>
              <div class="av uav">👤</div>
            </div>"""

        elif msg["role"] == "ai":
            ts = msg.get("time","")
            if "error" in msg:
                err = htmllib.escape(str(msg["error"]))
                msgs_html += f"""
                <div class="row bot-row">
                  <div class="av bav">🤖</div>
                  <div class="ebub">⚠️ Something went wrong: {err}</div>
                </div>"""
                continue

            r = msg.get("result", {})
            reply_raw = str(r.get("reply","I'm here to help!") or "I'm here to help!")
            reply  = htmllib.escape(reply_raw).replace("\\n","<br>").replace("\n","<br>")
            pri    = r.get("priority","Low")
            sent   = r.get("sentiment","Neutral")
            cat    = htmllib.escape(str(r.get("category","General")))
            tech   = str(r.get("technician","Not Assigned"))
            tid    = htmllib.escape(str(r.get("ticket_id","")))

            PRI_C = {
                "High":   ("#f87171","rgba(248,113,113,.1)","rgba(248,113,113,.25)"),
                "Medium": ("#fbbf24","rgba(251,191,36,.1)","rgba(251,191,36,.25)"),
                "Low":    ("#4ade80","rgba(74,222,128,.08)","rgba(74,222,128,.2)"),
            }
            pc, pbg, pbo = PRI_C.get(pri, PRI_C["Low"])
            pri_e = htmllib.escape(pri)

            sl = sent.lower()
            if any(x in sl for x in ["pos","happy"]):
                sc, sbg = "#4ade80","rgba(74,222,128,.09)"
            elif any(x in sl for x in ["frust","angry","neg"]):
                sc, sbg = "#f87171","rgba(248,113,113,.09)"
            else:
                sc, sbg = "#94a3b8","rgba(148,163,184,.07)"
            sent_e = htmllib.escape(sent)

            rec_html = ""

            if r.get("bill_data"):
                bd  = r["bill_data"]
                amt = f"{int(bd.get('amount',0)):,}"
                dd  = htmllib.escape(str(bd.get("due_date","N/A")))
                if bd.get("overdue"):
                    st_c, st_bg, st_bo, st_txt = "#f87171","rgba(248,113,113,.09)","rgba(248,113,113,.22)","⚠️ OVERDUE"
                else:
                    st_c, st_bg, st_bo, st_txt = "#4ade80","rgba(74,222,128,.07)","rgba(74,222,128,.2)","✅ CURRENT"
                rec_html = f"""
                <div class="rec-card">
                  <div class="rec-lbl">💳 BILLING INFORMATION</div>
                  <div style="display:flex;align-items:baseline;gap:6px;margin:10px 0 6px;">
                    <span style="font-size:12px;color:#334155;font-family:monospace;">PKR</span>
                    <span style="font-size:30px;font-weight:800;color:#fbbf24;letter-spacing:-.03em;">{amt}</span>
                  </div>
                  <div style="font-size:11px;color:#334155;font-family:monospace;margin-bottom:10px;">📅 Due: {dd}</div>
                  <span style="font-size:10px;font-weight:800;padding:3px 11px;border-radius:12px;
                    background:{st_bg};color:{st_c};border:1px solid {st_bo};font-family:monospace;letter-spacing:.06em;">{st_txt}</span>
                </div>"""

            elif r.get("tickets_data"):
                rows = ""
                for t in r["tickets_data"]:
                    iss  = htmllib.escape(str(t.get("issue",""))[:50])
                    tid2 = htmllib.escape(str(t.get("ticket_id","")))
                    sts  = htmllib.escape(str(t.get("status","Open")))
                    p2   = str(t.get("priority","Low"))
                    tc   = {"High":"#f87171","Medium":"#fbbf24","Low":"#4ade80"}.get(p2,"#4ade80")
                    rows += f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                         padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);">
                      <div>
                        <div style="font-size:13px;font-weight:600;color:#e2e8f0;">{iss}</div>
                        <div style="font-size:9px;color:#1e3a5f;font-family:monospace;margin-top:2px;">{tid2}</div>
                      </div>
                      <span style="font-size:9px;font-weight:700;padding:2px 8px;border-radius:10px;
                        background:rgba(14,165,233,.08);color:#38bdf8;white-space:nowrap;border:1px solid rgba(14,165,233,.14);">{sts}</span>
                    </div>"""
                rec_html = f"""
                <div class="rec-card">
                  <div class="rec-lbl">🎫 RECENT SUPPORT TICKETS</div>
                  {rows if rows else '<div style="font-size:12px;color:#1e3a5f;padding:8px 0;font-family:monospace;">No tickets found.</div>'}
                </div>"""

            elif r.get("plans_data"):
                pcards = ""
                for p in PLANS_LIST:
                    feats = "".join([f'<li style="font-size:10px;color:#475569;padding:3px 0;list-style:none;display:flex;align-items:center;gap:5px;"><span style="color:{p["color"]};font-size:9px;">✓</span>{htmllib.escape(f)}</li>' for f in p["features"][:4]])
                    pcards += f"""
                    <div style="background:rgba(0,0,0,.3);border:1px solid rgba(14,165,233,.1);
                         border-radius:10px;padding:12px;text-align:left;border-top:2px solid {p['color']};">
                      <div style="font-size:10px;margin-bottom:4px;">{p['icon']}</div>
                      <div style="font-size:11px;font-weight:700;color:#f1f5f9;">{htmllib.escape(p['name'])}</div>
                      <div style="font-size:18px;font-weight:800;color:{p['color']};margin:4px 0 2px;">{htmllib.escape(p['speed'])}</div>
                      <div style="font-size:12px;font-weight:700;color:#fbbf24;margin-bottom:8px;">{htmllib.escape(p['price'])}<span style="font-size:9px;color:#334155;font-family:monospace;">/mo</span></div>
                      <ul style="padding:0;">{feats}</ul>
                    </div>"""
                rec_html = f"""
                <div class="rec-card">
                  <div class="rec-lbl">📶 AVAILABLE PLANS</div>
                  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:8px;">{pcards}</div>
                </div>"""

            upd_html = ""
            if r.get("record_updated"):
                upd   = r["record_updated"]
                field = htmllib.escape(str(upd.get("field","Record")).title())
                val   = htmllib.escape(str(upd.get("value","")))
                upd_html = f"""
                <div style="margin-top:10px;padding:10px 14px;border-radius:10px;
                     background:rgba(74,222,128,.05);border:1px solid rgba(74,222,128,.16);
                     font-size:12.5px;color:#4ade80;">
                  ✅ <strong>{field}</strong> updated to <strong>"{val}"</strong>
                </div>"""

            tech_chip = (f'<span class="tc">🔧 {htmllib.escape(tech)}</span>' if tech != "Not Assigned" else "")
            tid_chip  = (f'<span class="idc">🎫 {htmllib.escape(tid)}</span>' if tid else "")

            msgs_html += f"""
            <div class="row bot-row">
              <div class="av bav">🤖</div>
              <div class="acard">
                <div class="ahdr">
                  <span class="albl">✦ FiberISP AI</span>
                  <span class="pbadge" style="background:{pbg};color:{pc};border:1px solid {pbo};">{pri_e}</span>
                  <span class="sbadge" style="background:{sbg};color:{sc};">{sent_e}</span>
                </div>
                <div class="abody">
                  <div class="reply">{reply}</div>
                  {rec_html}
                  {upd_html}
                </div>
                <div class="aftr">
                  <span class="cc">{cat}</span>
                  {tech_chip}
                  {tid_chip}
                  <span class="ts-chip">{htmllib.escape(ts)}</span>
                </div>
              </div>
            </div>"""

    h = 40
    for m in chat_list:
        if m["role"] == "user":       h += 90
        elif m["role"] == "ai":
            res = m.get("result", {})
            h += 200
            if res.get("bill_data"):      h += 130
            if res.get("tickets_data"):   h += max(90, len(res["tickets_data"]) * 54 + 44)
            if res.get("plans_data"):     h += 260
            if res.get("record_updated"): h += 55
    height = min(580, max(300, h))

    component_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#06090f;font-family:'DM Sans',sans-serif;height:{height}px;overflow:hidden;}}
.cw{{height:{height}px;overflow-y:auto;padding:18px 16px;display:flex;flex-direction:column;gap:16px;scroll-behavior:smooth;}}
.cw::-webkit-scrollbar{{width:3px;}}
.cw::-webkit-scrollbar-thumb{{background:rgba(14,165,233,.2);border-radius:4px;}}
.row{{display:flex;align-items:flex-end;gap:10px;animation:su .25s ease both;}}
.user-row{{flex-direction:row-reverse;}}
.bot-row{{flex-direction:row;}}
@keyframes su{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.av{{width:33px;height:33px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;}}
.uav{{background:linear-gradient(135deg,#1e3a8a,#2563eb);}}
.bav{{background:linear-gradient(135deg,#0f766e,#0ea5e9);box-shadow:0 4px 12px rgba(14,165,233,.25);}}
.umsg{{display:flex;flex-direction:column;align-items:flex-end;max-width:70%;}}
.ubub{{
  background:linear-gradient(135deg,#1e3461,#1d4ed8);
  color:#dbeafe;border-radius:18px 18px 4px 18px;
  padding:11px 16px;font-size:13.5px;line-height:1.7;word-break:break-word;
  box-shadow:0 4px 18px rgba(29,78,216,.2);
}}
.utime{{font-size:9.5px;color:#1e3461;font-family:'JetBrains Mono',monospace;margin-top:4px;}}
.ebub{{max-width:74%;background:rgba(248,113,113,.06);border:1px solid rgba(248,113,113,.18);border-radius:14px;padding:12px 15px;font-size:13px;color:#f87171;}}
.acard{{
  max-width:82%;
  background:linear-gradient(150deg,#0c1220,#101c34);
  border:1px solid rgba(14,165,233,.14);
  border-radius:4px 18px 18px 18px;
  overflow:hidden;box-shadow:0 10px 35px rgba(0,0,0,.55);
}}
.ahdr{{
  background:linear-gradient(90deg,rgba(14,165,233,.08),rgba(99,102,241,.04));
  border-bottom:1px solid rgba(14,165,233,.08);
  padding:8px 14px;display:flex;align-items:center;gap:7px;
}}
.albl{{font-size:10px;font-weight:700;color:#1e3a5f;flex:1;font-family:'JetBrains Mono',monospace;letter-spacing:.08em;}}
.pbadge,.sbadge{{font-size:9px;font-weight:800;padding:2px 8px;border-radius:14px;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.05em;}}
.sbadge{{border:1px solid rgba(255,255,255,.06);}}
.abody{{padding:13px 15px;}}
.reply{{font-size:13.5px;line-height:1.75;color:#94a3b8;}}
.rec-card{{margin-top:12px;background:rgba(0,0,0,.35);border:1px solid rgba(14,165,233,.09);border-radius:12px;padding:13px;}}
.rec-lbl{{font-size:9px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#1e3a5f;font-family:'JetBrains Mono',monospace;margin-bottom:7px;}}
.aftr{{padding:8px 12px;border-top:1px solid rgba(255,255,255,.04);display:flex;gap:5px;flex-wrap:wrap;align-items:center;}}
.cc,.tc,.idc,.ts-chip{{font-size:9.5px;font-weight:600;font-family:'JetBrains Mono',monospace;padding:2px 8px;border-radius:9px;}}
.cc{{background:rgba(255,255,255,.04);color:#1e3a5f;border:1px solid rgba(255,255,255,.06);}}
.tc{{background:rgba(167,139,250,.07);color:#a78bfa;border:1px solid rgba(167,139,250,.14);}}
.idc{{background:rgba(14,165,233,.06);color:#38bdf8;border:1px solid rgba(14,165,233,.13);}}
.ts-chip{{background:transparent;color:#1e3461;border:none;}}
</style>
</head>
<body>
<div class="cw" id="cw">
{msgs_html}
</div>
<script>var c=document.getElementById('cw');if(c)c.scrollTop=c.scrollHeight;</script>
</body>
</html>"""

    components.html(component_html, height=height, scrolling=False)


# ══════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════
defaults = {
    "screen":         "welcome",
    "phone":          "",
    "customer":       None,
    "customer_type":  "",
    "bill_info":      "",
    "network_status": "ACTIVE",
    "fix_time":       "N/A",
    "history_text":   "",
    "chat":           [],
    "selected_plan":  "",
    "api_key":        "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",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
#  RESULT HANDLER
# ══════════════════════════════════════════════
def _handle_result(result, err, phone):
    now = datetime.datetime.now().strftime("%I:%M %p")
    if not result:
        st.session_state.chat.append({"role":"ai","error":err or "Unknown error","time":now})
        return

    action  = str(result.get("action","none")).lower()
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
            st.session_state.fix_time       = out[1]
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
            try:   overdue = datetime.date.today() > datetime.date.fromisoformat(row[1])
            except: overdue = False
            result["bill_data"] = {"amount":row[0],"due_date":row[1],"overdue":overdue}

    elif show == "tickets":
        c = db()
        c.execute("SELECT ticket_id,issue,priority,status,created_at FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 4", (phone,))
        rows = c.fetchall()
        result["tickets_data"] = [
            {"ticket_id":r[0],"issue":r[1],"priority":r[2],"status":r[3],"created_at":r[4]}
            for r in rows
        ]

    elif show == "plans":
        result["plans_data"] = True

    result["time"] = now
    st.session_state.chat.append({"role":"ai","result":result,"time":now})


# ══════════════════════════════════════════════
#  TOP BAR  (all screens except welcome)
# ══════════════════════════════════════════════
if st.session_state.screen != "welcome":
    st.markdown("""
    <div class="topbar">
      <div style="display:flex;align-items:center;gap:14px;">
        <div class="topbar-icon">⚡</div>
        <div>
          <div class="topbar-title">FiberISP</div>
          <div class="topbar-sub">AI-POWERED CUSTOMER SUPPORT</div>
        </div>
      </div>
      <div class="status-pill">
        <div class="status-dot"></div>SYSTEM ONLINE
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: WELCOME
# ══════════════════════════════════════════════
if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="welcome-hero">
      <div class="welcome-logo-wrap">⚡</div>
      <div class="welcome-title">FiberISP</div>
      <div class="welcome-subtitle">Ultra-Fast Fiber Internet Across Pakistan</div>
      <div class="welcome-tagline">AI-POWERED SUPPORT &nbsp;·&nbsp; 24/7 ASSISTANCE &nbsp;·&nbsp; LIGHTNING SPEED</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;margin:0 0 28px;'>"
        "<span style='font-size:12px;color:#1e3a5f;font-family:JetBrains Mono,monospace;"
        "letter-spacing:.18em;text-transform:uppercase;'>CHOOSE YOUR ACCOUNT TYPE</span></div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3, gap="large")

    # ── Card 1: Existing Customer ──
    with c1:
        st.markdown("""
        <div class="choice-card-top">
          <div class="choice-icon-wrap">👤</div>
          <div class="choice-title">Existing Customer</div>
          <div class="choice-desc">Login with your phone number and access your full AI support dashboard.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔑 Customer Login", key="btn_existing"):
            st.session_state.screen = "customer_login"
            st.rerun()

    # ── Card 2: New Customer ──
    with c2:
        st.markdown("""
        <div class="choice-card-top">
          <div class="choice-badge">NEW</div>
          <div class="choice-icon-wrap">✨</div>
          <div class="choice-title">New Customer</div>
          <div class="choice-desc">Register for a new connection and get instant AI-powered support.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("📝 Register Now", key="btn_new"):
            st.session_state.screen = "new_customer_register"
            st.rerun()

    # ── Card 3: Admin ──
    with c3:
        st.markdown("""
        <div class="choice-card-top">
          <div class="choice-icon-wrap">🛠️</div>
          <div class="choice-title">Admin Panel</div>
          <div class="choice-desc">Manage customers, tickets, outages, and system operations.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔐 Admin Access", key="btn_admin"):
            st.session_state.screen = "admin_login"
            st.rerun()

    # Fuse cards to buttons via CSS override
    st.markdown("""
    <style>
    /* Remove gap between card-top and button */
    section[data-testid="stMain"] .stColumns .stColumn > div {
        gap: 0 !important;
    }
    section[data-testid="stMain"] .stColumns .stColumn .stMarkdown {
        margin-bottom: 0 !important;
    }
    section[data-testid="stMain"] .stColumns .stColumn > div > div:last-child .stButton > button {
        border-radius: 0 0 22px 22px !important;
        margin-top: 0 !important;
        border-top: 1px solid rgba(14,165,233,.1) !important;
        background: linear-gradient(135deg,rgba(14,165,233,.12),rgba(99,102,241,.08)) !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 16px 24px !important;
        box-shadow: none !important;
        border-left: 1px solid rgba(14,165,233,.14) !important;
        border-right: 1px solid rgba(14,165,233,.14) !important;
        border-bottom: 1px solid rgba(14,165,233,.14) !important;
    }
    section[data-testid="stMain"] .stColumns .stColumn > div > div:last-child .stButton > button:hover {
        background: linear-gradient(135deg,rgba(14,165,233,.22),rgba(99,102,241,.14)) !important;
        color: #7dd3fc !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: CUSTOMER LOGIN
# ══════════════════════════════════════════════
elif st.session_state.screen == "customer_login":
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div style="font-size:36px;margin-bottom:14px;">📱</div>
          <div class="form-title">Customer Login</div>
          <div class="form-sub">Enter your registered phone number to access your account instantly.</div>
        </div>""", unsafe_allow_html=True)

        phone = st.text_input("Phone Number", placeholder="03001234567", key="login_phone")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Login", key="do_login"):
                if phone.strip():
                    c = db()
                    c.execute("SELECT name,package,area FROM customers WHERE phone=?", (phone.strip(),))
                    cust = c.fetchone()
                    if cust:
                        st.session_state.phone         = phone.strip()
                        st.session_state.customer      = {"name":cust[0],"package":cust[1],"area":cust[2]}
                        st.session_state.customer_type = "Existing Customer"
                        c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone.strip(),))
                        bill = c.fetchone()
                        st.session_state.bill_info = f"PKR {bill[0]:,}, Due: {bill[1]}" if bill else "No billing record"
                        c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (cust[2],))
                        out = c.fetchone()
                        if out:
                            st.session_state.network_status = out[0]
                            st.session_state.fix_time       = out[1]
                        c.execute("SELECT issue FROM tickets WHERE customer_phone=?", (phone.strip(),))
                        rows = c.fetchall()
                        st.session_state.history_text = "\n".join([f"- {r[0]}" for r in rows]) if rows else "No previous tickets."
                        st.session_state.chat = []
                        st.session_state.screen = "customer_dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Phone number not registered. Please register as a new customer.")
                else:
                    st.error("⚠️ Please enter your phone number.")
        with c2:
            if st.button("← Back", key="back_login"):
                st.session_state.screen = "welcome"
                st.rerun()

        st.markdown(
            "<p style='text-align:center;font-size:12px;color:#1e3a5f;margin-top:16px;"
            "font-family:JetBrains Mono,monospace;'>Demo: try "
            "<code style='background:rgba(14,165,233,.08);border:1px solid rgba(14,165,233,.16);"
            "padding:2px 7px;border-radius:5px;color:#38bdf8;'>03001234567</code></p>",
            unsafe_allow_html=True
        )


# ══════════════════════════════════════════════
#  SCREEN: NEW CUSTOMER REGISTER
# ══════════════════════════════════════════════
elif st.session_state.screen == "new_customer_register":
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div style="font-size:36px;margin-bottom:14px;">✨</div>
          <div class="form-title">New Customer Registration</div>
          <div class="form-sub">Fill in your details to create an account and get started with FiberISP.</div>
        </div>""", unsafe_allow_html=True)

        with st.form("reg_form"):
            name  = st.text_input("Full Name",    placeholder="e.g. Muhammad Ali")
            phone = st.text_input("Phone Number", placeholder="03001234567")
            area  = st.selectbox("Your Area",     PAKISTAN_LOCATIONS)
            if st.form_submit_button("✅ Create Account"):
                if name.strip() and phone.strip():
                    c = db()
                    try:
                        c.execute("INSERT INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                                  (name.strip(), phone.strip(), "No Package", area))
                        conn.commit()
                        st.session_state.phone         = phone.strip()
                        st.session_state.customer      = {"name":name.strip(),"package":"No Package","area":area}
                        st.session_state.customer_type = "New Customer"
                        st.session_state.bill_info     = "No billing record"
                        st.session_state.history_text  = "No previous tickets."
                        st.session_state.chat          = []
                        c.execute("SELECT status,expected_fix_time FROM outages WHERE area=?", (area,))
                        out = c.fetchone()
                        if out:
                            st.session_state.network_status = out[0]
                            st.session_state.fix_time       = out[1]
                        st.session_state.screen = "customer_dashboard"
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ This phone number is already registered. Please login instead.")
                else:
                    st.error("⚠️ Please fill in all fields.")

        if st.button("← Back", key="back_reg"):
            st.session_state.screen = "welcome"
            st.rerun()


# ══════════════════════════════════════════════
#  SCREEN: CUSTOMER DASHBOARD
# ══════════════════════════════════════════════
elif st.session_state.screen == "customer_dashboard":
    cust  = st.session_state.customer
    phone = st.session_state.phone

    outage_html = ""
    if st.session_state.network_status == "DOWN":
        outage_html = (
            f'<div class="outage-warn">⚠️ <strong>Network Outage in {htmllib.escape(cust["area"])}</strong>'
            f' — Expected fix: {htmllib.escape(st.session_state.fix_time)}</div>'
        )

    lang_badge = (
        '<span style="font-size:11px;background:rgba(14,165,233,.08);'
        'border:1px solid rgba(14,165,233,.16);padding:5px 14px;border-radius:20px;'
        'color:#38bdf8;font-family:JetBrains Mono,monospace;font-weight:700;">🇬🇧 English</span>'
    )

    st.markdown(f"""
    <div class="cust-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
        <div class="cust-name">👋 Welcome, {htmllib.escape(cust["name"])}</div>
        {lang_badge}
      </div>
      <div class="cust-meta">
        <div class="cust-chip">📱 <span>{htmllib.escape(phone)}</span></div>
        <div class="cust-chip">📦 <span>{htmllib.escape(cust["package"])}</span></div>
        <div class="cust-chip">📍 <span>{htmllib.escape(cust["area"])}</span></div>
        <div class="cust-chip">💳 <span>{htmllib.escape(st.session_state.bill_info)}</span></div>
      </div>
      {outage_html}
    </div>""", unsafe_allow_html=True)

    col_out, _ = st.columns([1, 8])
    with col_out:
        if st.button("🚪 Logout", key="logout"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬  AI Support Chat",
        "🔌  New Connection",
        "💳  My Bill & Tickets",
        "⬆️  Upgrade Plan",
    ])

    # ────────────────────────────────────────
    #  TAB 1: AI SUPPORT CHAT
    # ────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="chat-banner">
          <div class="chat-banner-icon">🤖</div>
          <div style="flex:1;">
            <div class="chat-banner-title">FiberISP AI Assistant</div>
            <div class="chat-banner-sub">
              Ask about your bill, connection issues, or say things like
              <em style="color:#475569;">"change my name to Ahmed"</em> or
              <em style="color:#475569;">"show me my tickets"</em>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:6px;flex-shrink:0;">
            <span class="online-dot"></span>
            <span style="font-size:11px;color:#4ade80;font-family:JetBrains Mono,monospace;font-weight:600;">ONLINE</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-hdr'>Quick Topics</div>", unsafe_allow_html=True)

        quick_topics = [
            ("🐌","Slow internet speed"),("📡","WiFi not working"),
            ("⛔","No internet connection"),("💳","Show my bill"),
            ("⬆️","Upgrade my plan"),("🔁","How to restart my router"),
            ("📶","Weak WiFi signal"),("🔧","Request a technician"),
            ("📋","Show my tickets"),("📦","What plans are available"),
        ]
        cols = st.columns(5)
        for i, (icon, label) in enumerate(quick_topics):
            with cols[i % 5]:
                if st.button(f"{icon} {label}", key=f"qt_{i}", use_container_width=True):
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.chat.append({"role":"user","text":label,"time":now})
                    with st.spinner("AI is thinking…"):
                        result, err = process_ticket(
                            None, phone, st.session_state.customer_type,
                            cust["name"], cust["package"], cust["area"],
                            st.session_state.network_status, st.session_state.fix_time,
                            st.session_state.bill_info, st.session_state.history_text, label,
                        )
                    _handle_result(result, err, phone)
                    st.rerun()

        st.markdown("<div class='sec-hdr'>Conversation</div>", unsafe_allow_html=True)
        render_chat(st.session_state.chat)

        user_msg = st.chat_input("Type your message… (e.g. 'change my name to Ahmed')")
        if user_msg and user_msg.strip():
            now = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state.chat.append({"role":"user","text":user_msg.strip(),"time":now})
            with st.spinner("AI is thinking…"):
                result, err = process_ticket(
                    None, phone, st.session_state.customer_type,
                    cust["name"], cust["package"], cust["area"],
                    st.session_state.network_status, st.session_state.fix_time,
                    st.session_state.bill_info, st.session_state.history_text, user_msg.strip(),
                )
            _handle_result(result, err, phone)
            st.rerun()

        if st.session_state.chat:
            if st.button("🗑️ Clear Chat", key="clear_chat"):
                st.session_state.chat = []
                st.rerun()

    # ────────────────────────────────────────
    #  TAB 2: NEW CONNECTION
    # ────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="background:linear-gradient(150deg,#0d1524,#0f1d35);
             border:1px solid rgba(14,165,233,.14);border-radius:18px;
             padding:24px 28px;margin-bottom:24px;
             box-shadow:inset 0 1px 0 rgba(255,255,255,.04);">
          <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:#f1f5f9;margin-bottom:6px;">
            🔌 Request a New Internet Connection
          </div>
          <div style="font-size:13.5px;color:#475569;line-height:1.7;">
            Our team will contact you within 24 hours to schedule installation.
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-hdr'>Select a Plan</div>", unsafe_allow_html=True)
        pcols = st.columns(4)
        for i, p in enumerate(PLANS_LIST):
            with pcols[i]:
                sel_cls = "selected" if st.session_state.selected_plan == p["name"] else ""
                features_html = "".join([f'<li>{htmllib.escape(f)}</li>' for f in p["features"][:4]])
                st.markdown(f"""
                <div class="plan-card {sel_cls}" style="--plan-accent:{p['color']};">
                  <div style="font-size:28px;margin-bottom:8px;">{p['icon']}</div>
                  <div class="plan-name">{htmllib.escape(p['name'])}</div>
                  <div class="plan-speed">{htmllib.escape(p['speed'])}</div>
                  <div class="plan-price">{htmllib.escape(p['price'])}</div>
                  <div class="plan-per">/month</div>
                  <ul class="plan-features">{features_html}</ul>
                </div>""", unsafe_allow_html=True)
                if st.button("Select", key=f"plan_{i}", use_container_width=True):
                    st.session_state.selected_plan = p["name"]
                    st.rerun()

        if st.session_state.selected_plan:
            st.markdown(
                f"<div style='background:rgba(74,222,128,.06);border:1px solid rgba(74,222,128,.18);"
                f"border-radius:10px;padding:10px 16px;font-size:13px;color:#4ade80;margin:12px 0;'>"
                f"✅ Selected: <strong>{htmllib.escape(st.session_state.selected_plan)}</strong></div>",
                unsafe_allow_html=True
            )

        st.markdown("<div class='sec-hdr'>Your Details</div>", unsafe_allow_html=True)
        with st.form("nc_form", clear_on_submit=True):
            nc_name  = st.text_input("Full Name",         value=cust["name"])
            nc_phone = st.text_input("Phone Number",      value=phone)
            nc_area  = st.selectbox(
                "Installation Area", PAKISTAN_LOCATIONS,
                index=PAKISTAN_LOCATIONS.index(cust["area"]) if cust["area"] in PAKISTAN_LOCATIONS else 0
            )
            if st.form_submit_button("📩 Submit Request"):
                if nc_name.strip() and nc_phone.strip() and st.session_state.selected_plan:
                    db().execute(
                        "INSERT INTO new_connection_requests(name,phone,area,package,created_at) VALUES(?,?,?,?,?)",
                        (nc_name.strip(), nc_phone.strip(), nc_area,
                         st.session_state.selected_plan,
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    conn.commit()
                    st.success(f"✅ Request submitted! We'll contact {nc_phone.strip()} within 24 hours.")
                    st.session_state.selected_plan = ""
                elif not st.session_state.selected_plan:
                    st.error("⚠️ Please select a plan first.")
                else:
                    st.error("⚠️ Please fill in all fields.")

    # ────────────────────────────────────────
    #  TAB 3: BILL & TICKETS
    # ────────────────────────────────────────
    with tab3:
        c = db()
        c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,))
        bill_row = c.fetchone()

        if bill_row:
            amount, due_date = bill_row
            try:    overdue = datetime.date.today() > datetime.date.fromisoformat(due_date)
            except: overdue = False
            st_html = (
                '<span class="bill-status-due">⚠️ OVERDUE</span>'
                if overdue else
                '<span class="bill-status-ok">✅ CURRENT</span>'
            )
            st.markdown(f"""
            <div class="bill-card">
              <div style="font-size:10px;color:#1e3a5f;font-family:'JetBrains Mono',monospace;
                letter-spacing:.14em;text-transform:uppercase;margin-bottom:10px;">
                CURRENT BILL AMOUNT
              </div>
              <div class="bill-amount">
                <span class="bill-currency">PKR</span>{amount:,}
              </div>
              <div class="bill-due">📅 Due Date: {htmllib.escape(due_date)}</div>
              {st_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("💳 No billing record found.")

        st.markdown("<div class='sec-hdr'>Recent Support Tickets</div>", unsafe_allow_html=True)
        c.execute(
            "SELECT ticket_id,issue,priority,status,created_at FROM tickets "
            "WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5",
            (phone,)
        )
        tickets = c.fetchall()
        if tickets:
            for tid, issue, priority, status, created in tickets:
                card_cls = "resolved" if status == "Resolved" else priority.lower()
                st.markdown(f"""
                <div class="ticket-card {card_cls}">
                  <div class="ticket-hdr">
                    <span class="ticket-id">{htmllib.escape(tid)}</span>
                    <span class="ticket-status {'s-resolved' if status=='Resolved' else 's-open'}">{htmllib.escape(status)}</span>
                  </div>
                  <div class="ticket-issue">{htmllib.escape(issue)}</div>
                  <div class="ticket-meta">
                    {pri_tag(priority)}
                    <span class="tag tag-sent">🕐 {htmllib.escape(created)}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("📋 No tickets found. Chat with AI Support to create one.")

    # ────────────────────────────────────────
    #  TAB 4: UPGRADE PLAN
    # ────────────────────────────────────────
    with tab4:
        st.markdown(f"""
        <div style="background:linear-gradient(150deg,#0d1524,#0f1d35);
             border:1px solid rgba(14,165,233,.14);border-radius:18px;
             padding:24px 28px;margin-bottom:28px;
             box-shadow:inset 0 1px 0 rgba(255,255,255,.04);">
          <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:#f1f5f9;margin-bottom:6px;">
            ⬆️ Upgrade Your Plan
          </div>
          <div style="font-size:13.5px;color:#475569;">
            Current Package: <strong style="color:#0ea5e9;">{htmllib.escape(cust["package"])}</strong>
          </div>
        </div>""", unsafe_allow_html=True)

        up_cols = st.columns(4)
        for i, p in enumerate(PLANS_LIST):
            with up_cols[i]:
                is_cur    = p["name"].lower() in cust["package"].lower()
                cur_badge = '<div class="plan-current-badge">✓ CURRENT PLAN</div>' if is_cur else ""
                features_html = "".join([f'<li>{htmllib.escape(f)}</li>' for f in p["features"]])
                border_style  = "border-color:#0ea5e9;" if is_cur else ""
                st.markdown(f"""
                <div class="plan-card {'current' if is_cur else ''}"
                     style="--plan-accent:{p['color']};{border_style}">
                  <div style="font-size:30px;margin-bottom:10px;">{p['icon']}</div>
                  <div class="plan-name">{htmllib.escape(p['name'])}</div>
                  <div class="plan-speed">{htmllib.escape(p['speed'])}</div>
                  <div class="plan-price">{htmllib.escape(p['price'])}</div>
                  <div class="plan-per">/month</div>
                  <ul class="plan-features">{features_html}</ul>
                  {cur_badge}
                </div>""", unsafe_allow_html=True)
                if not is_cur:
                    if st.button(f"⬆️ Upgrade", key=f"up_{i}", use_container_width=True):
                        upgrade_msg = (
                            f"I want to upgrade my plan from {cust['package']} to "
                            f"{p['name']} ({p['speed']}, {p['price']}/month)"
                        )
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        st.session_state.chat.append({"role":"user","text":upgrade_msg,"time":now})
                        with st.spinner("Processing upgrade…"):
                            result, err = process_ticket(
                                None, phone, st.session_state.customer_type,
                                cust["name"], cust["package"], cust["area"],
                                st.session_state.network_status, st.session_state.fix_time,
                                st.session_state.bill_info, st.session_state.history_text, upgrade_msg,
                            )
                        _handle_result(result, err, phone)
                        st.success(f"✅ Upgrade to '{p['name']}' submitted! Check AI Chat for confirmation.")
                        st.rerun()


# ══════════════════════════════════════════════
#  SCREEN: ADMIN LOGIN
# ══════════════════════════════════════════════
elif st.session_state.screen == "admin_login":
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div style="font-size:36px;margin-bottom:14px;">🔐</div>
          <div class="form-title">Admin Access</div>
          <div class="form-sub">Enter your administrator password to access the management dashboard.</div>
        </div>""", unsafe_allow_html=True)

        pwd = st.text_input("Admin Password", type="password", placeholder="Enter password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login →", key="admin_go"):
                if pwd == "admin123":
                    st.session_state.screen = "admin"
                    st.rerun()
                else:
                    st.error("❌ Incorrect password.")
        with c2:
            if st.button("← Back", key="back_admin"):
                st.session_state.screen = "welcome"
                st.rerun()


# ══════════════════════════════════════════════
#  SCREEN: ADMIN DASHBOARD
# ══════════════════════════════════════════════
elif st.session_state.screen == "admin":
    c = db()
    c.execute("SELECT COUNT(*) FROM customers");              total_cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets");                total_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'"); open_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE priority='High' AND status='Open'"); high_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM new_connection_requests"); conn_reqs  = c.fetchone()[0]

    col_out, _ = st.columns([1, 8])
    with col_out:
        if st.button("← Logout", key="admin_logout"):
            st.session_state.screen = "welcome"
            st.rerun()

    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-num blue">{total_cust}</div>
        <div class="metric-lbl">Total Customers</div>
      </div>
      <div class="metric-card">
        <div class="metric-num">{total_tick}</div>
        <div class="metric-lbl">Total Tickets</div>
      </div>
      <div class="metric-card">
        <div class="metric-num yellow">{open_tick}</div>
        <div class="metric-lbl">Open Tickets</div>
      </div>
      <div class="metric-card">
        <div class="metric-num red">{high_tick}</div>
        <div class="metric-lbl">High Priority</div>
      </div>
    </div>""", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs([
        "🎫 Tickets", "👥 Customers", "📡 Outages", "🔌 New Requests", "⚙️ Manage",
    ])

    with t1:
        st.markdown("<div class='sec-hdr'>All Tickets</div>", unsafe_allow_html=True)
        c.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        for row in c.fetchall():
            tid, tphone, issue, priority, sentiment, tech, status, created = row
            card_cls = "resolved" if status == "Resolved" else priority.lower()
            st.markdown(f"""
            <div class="ticket-card {card_cls}">
              <div class="ticket-hdr">
                <div style="display:flex;gap:10px;">
                  <span class="ticket-id">{htmllib.escape(tid)}</span>
                  <span class="ticket-id">📱 {htmllib.escape(tphone)}</span>
                </div>
                <span class="ticket-status {'s-resolved' if status=='Resolved' else 's-open'}">{htmllib.escape(status)}</span>
              </div>
              <div class="ticket-issue">{htmllib.escape(issue)}</div>
              <div class="ticket-meta">
                {pri_tag(priority)} {sent_tag(sentiment)}
                <span class="tag tag-sent">🔧 {htmllib.escape(tech)}</span>
                <span class="tag tag-sent">🕐 {htmllib.escape(created)}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='sec-hdr'>Registered Customers</div>", unsafe_allow_html=True)
        c.execute("SELECT name,phone,package,area FROM customers")
        rows = c.fetchall()
        if rows:
            import pandas as pd
            st.dataframe(
                pd.DataFrame(rows, columns=["Name","Phone","Package","Area"]),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No customers found.")

    with t3:
        st.markdown("<div class='sec-hdr'>Active Outages</div>", unsafe_allow_html=True)
        c.execute("SELECT * FROM outages")
        for area_n, status_n, fix_n in c.fetchall():
            color = "#f87171" if status_n == "DOWN" else "#4ade80"
            st.markdown(f"""
            <div style="background:#0a1120;border:1px solid rgba(14,165,233,.08);border-radius:12px;
                 padding:14px 18px;margin-bottom:8px;border-left:3px solid {color};">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div style="font-size:14px;font-weight:700;color:#e2e8f0;">📍 {htmllib.escape(area_n)}</div>
                  <div style="font-size:11px;color:#334155;font-family:monospace;margin-top:3px;">
                    Fix ETA: {htmllib.escape(fix_n)}
                  </div>
                </div>
                <span style="font-size:11px;font-weight:700;padding:4px 14px;border-radius:16px;
                  background:{'rgba(248,113,113,.08)' if status_n=='DOWN' else 'rgba(74,222,128,.07)'};
                  color:{color};font-family:monospace;border:1px solid {color+'44'};">{htmllib.escape(status_n)}</span>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-hdr'>Add / Update Outage</div>", unsafe_allow_html=True)
        with st.form("add_outage"):
            oa = st.text_input("Area",                placeholder="e.g. Karachi - DHA")
            os = st.selectbox("Status",               ["DOWN","ACTIVE"])
            of = st.text_input("Expected Fix Time",   placeholder="e.g. 3 Hours")
            if st.form_submit_button("💾 Save Outage"):
                db().execute(
                    "INSERT OR REPLACE INTO outages(area,status,expected_fix_time) VALUES(?,?,?)",
                    (oa, os, of)
                )
                conn.commit()
                st.success(f"Outage for {oa} saved.")
                st.rerun()

    with t4:
        st.markdown("<div class='sec-hdr'>New Connection Requests</div>", unsafe_allow_html=True)
        c.execute("SELECT name,phone,area,package,created_at FROM new_connection_requests ORDER BY created_at DESC")
        rows = c.fetchall()
        if rows:
            import pandas as pd
            st.dataframe(
                pd.DataFrame(rows, columns=["Name","Phone","Area","Package","Requested At"]),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No new requests yet.")

    with t5:
        st.markdown("<div class='sec-hdr'>Resolve a Ticket</div>", unsafe_allow_html=True)
        with st.form("resolve_form"):
            tid_input = st.text_input("Ticket ID", placeholder="FIB-2026-XXXX")
            if st.form_submit_button("✓ Mark as Resolved"):
                db().execute("UPDATE tickets SET status='Resolved' WHERE ticket_id=?", (tid_input,))
                conn.commit()
                st.success(f"Ticket {tid_input} resolved.")
                st.rerun()

        st.markdown("<div class='sec-hdr'>API Key</div>", unsafe_allow_html=True)
        new_key = st.text_input("Groq API Key", value=st.session_state.api_key, type="password")
        if st.button("💾 Update Key"):
            st.session_state.api_key = new_key
            st.success("API key updated.")
