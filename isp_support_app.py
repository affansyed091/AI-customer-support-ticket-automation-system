import streamlit as st
import sqlite3
import json
import random
import datetime
import html as htmllib
import re
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FiberISP - AI Support",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# ENHANCED CUSTOM CSS (same as original, no changes)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp { 
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 100%);
    background-attachment: fixed;
}
.main .block-container { padding: 1.5rem 2rem 4rem; max-width: 1300px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ══════ WELCOME SCREEN ══════ */
.welcome-hero {
    text-align: center;
    padding: 80px 20px 60px;
    background: linear-gradient(135deg, rgba(14,165,233,0.12) 0%, rgba(59,130,246,0.08) 100%);
    border-radius: 28px;
    border: 1px solid rgba(14,165,233,0.25);
    margin: 20px 0 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.welcome-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, transparent 70%);
    animation: pulse 6s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
    50% { transform: scale(1.1) rotate(180deg); opacity: 0.8; }
}
.welcome-logo {
    font-size: 90px;
    margin-bottom: 24px;
    filter: drop-shadow(0 10px 30px rgba(14,165,233,0.5));
    position: relative;
    z-index: 1;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
.welcome-title {
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
    letter-spacing: -0.04em;
    position: relative;
    z-index: 1;
}
.welcome-subtitle {
    font-size: 20px;
    color: #94a3b8;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
    font-weight: 500;
}
.welcome-tagline {
    font-size: 14px;
    color: #64748b;
    position: relative;
    z-index: 1;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
}

/* ══════ TOP BAR ══════ */
.topbar {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(14,165,233,0.25);
    border-radius: 22px;
    padding: 22px 36px;
    margin-bottom: 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 18px;
}
.topbar-icon {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #0ea5e9, #3b82f6);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 8px 28px rgba(14,165,233,0.5);
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { box-shadow: 0 8px 28px rgba(14,165,233,0.4); }
    to { box-shadow: 0 8px 36px rgba(14,165,233,0.7); }
}
.topbar-title {
    font-size: 26px;
    font-weight: 900;
    color: #f1f5f9;
    letter-spacing: -0.03em;
}
.topbar-sub {
    font-size: 11px;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 3px;
}
.status-pill {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.35);
    color: #4ade80;
    padding: 10px 22px;
    border-radius: 28px;
    font-size: 13px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 10px;
}
.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #4ade80;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; box-shadow: 0 0 10px #4ade80; }
    50% { opacity: 0.3; box-shadow: none; }
}

/* ══════ CHOICE CARDS ══════ */
.choice-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid rgba(14,165,233,0.2);
    border-radius: 24px;
    padding: 48px 32px;
    cursor: pointer;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.choice-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(14,165,233,0.15), transparent);
    transition: left 0.6s;
}
.choice-card:hover::before {
    left: 100%;
}
.choice-card:hover {
    border-color: rgba(14,165,233,0.6);
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 60px rgba(14,165,233,0.25);
}
.choice-icon {
    font-size: 64px;
    margin-bottom: 20px;
    filter: drop-shadow(0 6px 20px rgba(14,165,233,0.4));
}
.choice-title {
    font-size: 26px;
    font-weight: 900;
    color: #f1f5f9;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}
.choice-desc {
    font-size: 15px;
    color: #94a3b8;
    line-height: 1.7;
}

/* ══════ LOGIN/FORM BOX ══════ */
.form-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid rgba(14,165,233,0.25);
    border-radius: 28px;
    padding: 44px 40px;
    max-width: 520px;
    margin: 0 auto;
    box-shadow: 0 12px 60px rgba(0,0,0,0.4);
}
.form-title {
    font-size: 28px;
    font-weight: 900;
    color: #f1f5f9;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}
.form-sub {
    font-size: 15px;
    color: #94a3b8;
    margin-bottom: 32px;
    line-height: 1.7;
}

/* ══════ CUSTOMER INFO CARD ══════ */
.cust-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid rgba(14,165,233,0.25);
    border-radius: 24px;
    padding: 28px 32px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.cust-name {
    font-size: 28px;
    font-weight: 900;
    color: #f1f5f9;
    margin-bottom: 18px;
    letter-spacing: -0.02em;
}
.cust-meta {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}
.cust-chip {
    background: rgba(15,19,32,0.95);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 12px;
    padding: 10px 18px;
    font-size: 14px;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}
.cust-chip span {
    color: #f1f5f9;
    margin-left: 6px;
    font-weight: 700;
}
.outage-warn {
    background: rgba(248,113,113,0.1);
    border: 2px solid rgba(248,113,113,0.3);
    border-radius: 14px;
    padding: 14px 20px;
    font-size: 14px;
    color: #fca5a5;
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
}

/* ══════ AI BANNER ══════ */
.ai-banner {
    background: linear-gradient(135deg, rgba(14,165,233,0.18) 0%, rgba(59,130,246,0.12) 100%);
    border: 2px solid rgba(14,165,233,0.35);
    border-radius: 20px;
    padding: 24px 28px;
    margin: 24px 0;
    text-align: center;
    box-shadow: 0 8px 32px rgba(14,165,233,0.15);
}
.ai-banner-title {
    font-size: 22px;
    font-weight: 800;
    color: #0ea5e9;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
.ai-banner-sub {
    font-size: 14px;
    color: #94a3b8;
    font-weight: 500;
}

/* ══════ SECTION HEADERS ══════ */
.sec-hdr {
    font-size: 12px;
    font-weight: 800;
    color: #64748b;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin: 28px 0 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(14,165,233,0.12);
}

/* ══════ PLAN CARDS ══════ */
.plan-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid rgba(14,165,233,0.15);
    border-radius: 18px;
    padding: 24px;
    cursor: pointer;
    transition: all 0.3s;
    text-align: center;
}
.plan-card:hover {
    border-color: #0ea5e9;
    box-shadow: 0 10px 40px rgba(14,165,233,0.15);
    transform: translateY(-4px);
}
.plan-card.selected {
    border-color: #0ea5e9;
    background: rgba(14,165,233,0.08);
    box-shadow: 0 0 30px rgba(14,165,233,0.2);
}
.plan-name {
    font-size: 18px;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 6px;
}
.plan-speed {
    font-size: 13px;
    color: #0ea5e9;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 12px;
    font-weight: 600;
}
.plan-price {
    font-size: 24px;
    font-weight: 900;
    color: #fbbf24;
}
.plan-per {
    font-size: 12px;
    color: #64748b;
}

/* ══════ BILL CARD ══════ */
.bill-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 2px solid rgba(251,191,36,0.25);
    border-radius: 20px;
    padding: 32px 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(251,191,36,0.1);
}
.bill-amount {
    font-size: 48px;
    font-weight: 900;
    color: #fbbf24;
    letter-spacing: -0.04em;
}
.bill-currency {
    font-size: 20px;
    color: #94a3b8;
    margin-right: 6px;
}
.bill-due {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 8px;
    font-family: 'JetBrains Mono', monospace;
}
.bill-status-ok {
    background: rgba(74,222,128,0.12);
    border: 1px solid rgba(74,222,128,0.3);
    color: #4ade80;
    padding: 8px 20px;
    border-radius: 24px;
    font-size: 13px;
    font-weight: 700;
    display: inline-block;
    margin-top: 16px;
    font-family: 'JetBrains Mono', monospace;
}
.bill-status-due {
    background: rgba(248,113,113,0.12);
    border: 1px solid rgba(248,113,113,0.3);
    color: #f87171;
    padding: 8px 20px;
    border-radius: 24px;
    font-size: 13px;
    font-weight: 700;
    display: inline-block;
    margin-top: 16px;
    font-family: 'JetBrains Mono', monospace;
}

/* ══════ TICKET CARD ══════ */
.ticket-card {
    background: #0f172a;
    border: 1px solid rgba(14,165,233,0.15);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    border-left: 4px solid #0ea5e9;
    transition: all 0.2s;
}
.ticket-card:hover {
    border-left-width: 6px;
    box-shadow: 0 8px 24px rgba(14,165,233,0.1);
}
.ticket-card.high { border-left-color: #f87171; }
.ticket-card.medium { border-left-color: #fbbf24; }
.ticket-card.low { border-left-color: #4ade80; }
.ticket-card.resolved { border-left-color: #334155; opacity: 0.7; }
.ticket-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.ticket-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #94a3b8;
    font-weight: 600;
}
.ticket-status {
    font-size: 11px;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 24px;
}
.s-open {
    background: rgba(14,165,233,0.12);
    color: #7dd3fc;
}
.s-resolved {
    background: rgba(51,65,85,0.4);
    color: #94a3b8;
}
.ticket-issue {
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 10px;
}
.ticket-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.tag {
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 24px;
    font-family: 'JetBrains Mono', monospace;
}
.tag-high { background: rgba(248,113,113,0.12); color: #f87171; }
.tag-medium { background: rgba(251,191,36,0.12); color: #fbbf24; }
.tag-low { background: rgba(74,222,128,0.12); color: #4ade80; }
.tag-tech { background: rgba(14,165,233,0.12); color: #7dd3fc; }
.tag-cat { background: rgba(167,139,250,0.12); color: #c4b5fd; }
.tag-sent { background: rgba(100,116,139,0.12); color: #94a3b8; }

/* ══════ METRIC CARDS (Admin) ══════ */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.metric-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid rgba(14,165,233,0.2);
    border-radius: 18px;
    padding: 24px 28px;
    transition: all 0.3s;
}
.metric-card:hover {
    border-color: rgba(14,165,233,0.4);
    transform: translateY(-4px);
}
.metric-num {
    font-size: 36px;
    font-weight: 900;
    color: #f1f5f9;
    letter-spacing: -0.04em;
}
.metric-lbl {
    font-size: 12px;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 8px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.metric-num.red { color: #f87171; }
.metric-num.yellow { color: #fbbf24; }
.metric-num.green { color: #4ade80; }
.metric-num.blue { color: #0ea5e9; }


/* ══════ STREAMLIT INPUTS ══════ */
/* ══════ STREAMLIT INPUTS ══════ */

/* TEXT INPUTS */
.stTextInput input,
.stTextArea textarea {
    background: #0f172a !important;
    border: 2px solid rgba(14,165,233,0.25) !important;
    border-radius: 14px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    transition: all 0.25s ease !important;
}

/* INPUT FOCUS */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 4px rgba(14,165,233,0.18) !important;
}

/* SELECTBOX MAIN */
div[data-baseweb="select"] > div {
    background: #0f172a !important;
    border: 2px solid rgba(14,165,233,0.25) !important;
    border-radius: 14px !important;
    min-height: 52px !important;
    display: flex !important;
    align-items: center !important;
    padding-left: 10px !important;
    transition: all 0.25s ease !important;
}

/* SELECTBOX HOVER */
div[data-baseweb="select"] > div:hover {
    border-color: rgba(14,165,233,0.55) !important;
    box-shadow: 0 0 18px rgba(14,165,233,0.15) !important;
}

/* SELECTED TEXT */
div[data-baseweb="select"] span {
    color: #f1f5f9 !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
}

/* INPUT TEXT INSIDE SELECT */
div[data-baseweb="select"] input {
    color: #f1f5f9 !important;
    font-size: 15px !important;
}

/* DROPDOWN ICON */
div[data-baseweb="select"] svg {
    color: #ffffff !important;
}

/* DROPDOWN ICON BUTTON */
div[data-baseweb="select"] div[role="button"] {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    border-radius: 10px !important;
    margin-right: 6px !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    min-height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.25s ease !important;
}

/* DROPDOWN ICON HOVER */
div[data-baseweb="select"] div[role="button"]:hover {
    box-shadow: 0 0 18px rgba(14,165,233,0.5) !important;
    transform: scale(1.05);
}

/* DROPDOWN MENU */
ul[role="listbox"] {
    background: #0f172a !important;
    border: 1px solid rgba(14,165,233,0.25) !important;
    border-radius: 12px !important;
    padding: 6px !important;
}

/* OPTIONS */
ul[role="listbox"] li {
    color: #f1f5f9 !important;
    background: transparent !important;
    padding: 12px 14px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

/* OPTION HOVER */
ul[role="listbox"] li:hover {
    background: rgba(14,165,233,0.15) !important;
}

/* LABELS */
label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
    margin-bottom: 8px !important;
}

/* NORMAL BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 14px 32px !important;
    transition: all 0.3s !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(14,165,233,0.3) !important;
}

/* BUTTON HOVER */
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 36px rgba(14,165,233,0.4) !important;
}

/* CLICKABLE WELCOME CARDS ONLY */
.element-container:has(.choice-card-overlay) {
    position: relative;
    margin-top: -320px;
}

.element-container:has(.choice-card-overlay) .stButton > button {
    opacity: 0 !important;
    height: 320px !important;
    position: absolute !important;
    inset: 0 !important;
    z-index: 10 !important;
    cursor: pointer !important;
}
/* PRIMARY BLUE BUTTONS */
.stForm button,
div.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(14,165,233,0.35) !important;
}

/* HOVER */
.stForm button:hover,
div.stButton > button:hover {
    background: linear-gradient(135deg, #38bdf8, #3b82f6) !important;
    box-shadow: 0 8px 28px rgba(14,165,233,0.45) !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS & DATABASE
# ═══════════════════════════════════════════════════════════════
PAKISTAN_LOCATIONS = [
    "Peshawar - University Town", "Peshawar - Hayatabad", "Peshawar - Saddar",
    "Peshawar - Board Bazaar", "Peshawar - Gulbahar", "Peshawar - Tehkal",
    "Peshawar - Cantt", "Peshawar - Phase 5", "Mardan", "Swat - Mingora",
    "Abbottabad", "Mansehra", "Kohat", "Bannu", "Dera Ismail Khan",
    "Islamabad - F-6", "Islamabad - F-7", "Islamabad - F-8", "Islamabad - F-10",
    "Islamabad - F-11", "Islamabad - G-6", "Islamabad - G-7", "Islamabad - G-8",
    "Islamabad - G-9", "Islamabad - G-10", "Islamabad - G-11", "Islamabad - Blue Area",
    "Islamabad - I-8", "Islamabad - I-9", "Islamabad - I-10", "Islamabad - E-11",
    "Islamabad - D-12", "Islamabad - Bahria Town", "Islamabad - DHA",
    "Rawalpindi - Satellite Town", "Rawalpindi - Bahria Town", "Rawalpindi - Saddar",
    "Rawalpindi - Commercial Market", "Rawalpindi - PWD", "Rawalpindi - Chaklala",
    "Rawalpindi - Westridge", "Rawalpindi - Askari", "Rawalpindi - Gulzar-e-Quaid",
    "Lahore - DHA", "Lahore - Gulberg", "Lahore - Model Town", "Lahore - Johar Town",
    "Lahore - Cantt", "Lahore - Faisal Town", "Lahore - Iqbal Town", "Lahore - Garden Town",
    "Lahore - Bahria Town", "Lahore - Township", "Lahore - Allama Iqbal Town",
    "Lahore - Wapda Town", "Lahore - Lake City", "Lahore - Valencia Town",
    "Karachi - DHA", "Karachi - Clifton", "Karachi - Gulshan-e-Iqbal",
    "Karachi - PECHS", "Karachi - Nazimabad", "Karachi - Korangi",
    "Karachi - North Karachi", "Karachi - Malir", "Karachi - Saddar",
    "Karachi - Gulistan-e-Johar", "Karachi - North Nazimabad",
    "Karachi - Tariq Road", "Karachi - Bahadurabad", "Karachi - Shahrah-e-Faisal",
    "Faisalabad - Peoples Colony", "Faisalabad - Model Town", "Faisalabad - Madina Town",
    "Faisalabad - Susan Road", "Faisalabad - Civil Lines", "Faisalabad - Samanabad",
    "Multan - Cantt", "Multan - Gulgasht Colony", "Multan - Model Town",
    "Multan - Shah Rukn-e-Alam Colony", "Multan - Bosan Road", "Multan - DHA",
    "Quetta - Cantt", "Quetta - Satellite Town", "Quetta - Samungli Road",
    "Quetta - Jinnah Town", "Quetta - Chiltan Housing Scheme",
    "Sialkot", "Gujranwala", "Sargodha", "Bahawalpur", "Sukkur",
    "Hyderabad", "Larkana", "Nawabshah", "Mirpur Khas",
    "Gujrat", "Jhang", "Sheikhupura", "Sahiwal", "Okara",
    "Wah Cantt", "Kasur", "Chiniot", "Kamoke", "Hafizabad"
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
    conn = sqlite3.connect("fiberisp_system.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT UNIQUE, package TEXT, area TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT, customer_phone TEXT, issue TEXT, priority TEXT,
        sentiment TEXT, technician TEXT, status TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS outages (
        area TEXT UNIQUE, status TEXT, expected_fix_time TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS bills (
        customer_phone TEXT UNIQUE, amount INTEGER, due_date TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS new_connection_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, area TEXT, package TEXT, created_at TEXT)""")
    conn.commit()
    try:
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                  ("Affan", "03146532146", "Gaming Pro 100Mbps", "Peshawar - University Town"))
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES(?,?,?)",
                  ("03146532146", 4000, "2026-06-20"))
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                  ("Ali Khan", "03001234567", "Ultra Fiber 250Mbps", "DHA"))
        c.execute("INSERT OR IGNORE INTO outages(area,status,expected_fix_time) VALUES(?,?,?)",
                  ("DHA", "DOWN", "2 Hours"))
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES(?,?,?)",
                  ("03001234567", 6500, "2026-05-30"))
        conn.commit()
    except:
        pass
    return conn

conn = get_db()
def db():
    return conn.cursor()

# ═══════════════════════════════════════════════════════════════
# AI MODEL (language fixed to English)
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["customer_type", "name", "current_package", "area",
                     "network_status", "fix_time", "bill_info", "history_text",
                     "plans", "message", "is_first_message"],
    template="""
You are a professional ISP AI support agent for FiberISP, a Pakistani fiber internet provider.

Customer Information:
- Name: {name} ({customer_type})
- Package: {current_package}
- Area: {area}
- Network Status: {network_status} | Fix Time: {fix_time}
- Billing: {bill_info}
- Previous Tickets: {history_text}

Available Plans:
{plans}

Customer Message: {message}

LANGUAGE: English only. Reply entirely in English.

GREETING RULE:
- is_first_message: {is_first_message}
- If is_first_message is "yes", start with a warm, welcoming greeting.
- If is_first_message is "no", DO NOT greet - just address their concern directly.

ACTION HANDLING (set these fields in JSON):
1. If user wants to change their name (e.g., "change my name to Ahmed"): set "action": "update_name", "new_value": "Ahmed"
2. If user wants to change area: set "action": "update_area", "new_value": "area name"
3. If user wants to upgrade/change package: set "action": "update_package", "new_value": "exact plan name from list (Basic Home, Gaming Pro, Ultra Fiber, Extreme Fiber)"
4. Otherwise set "action": "none"

DATA DISPLAY (set "show_records"):
- "bill" if user asks about bill, amount, due date, payment
- "tickets" if user asks about ticket history, past complaints
- "plans" if user asks to see available plans
- "none" if no data card needed

Analysis Tasks:
1. Detect sentiment: Positive/Neutral/Frustrated/Angry
2. Assign priority: High (urgent)/Medium/ Low
3. Determine category from message content
4. Recommend technician if hardware/physical issue: yes or no
5. Mention outage only if network_status is DOWN
6. Be empathetic, professional, and solution-focused (2-4 sentences)

Return ONLY valid JSON:
{{"category":"","priority":"","sentiment":"","technician_required":"yes/no","reply":"","action":"none","new_value":"","show_records":"none"}}
"""
)

def gen_ticket_id():
    return f"FIB-{datetime.datetime.now().year}-{random.randint(1000,9999)}"

def gen_tech():
    return f"TECH-{random.randint(100,999)}"

def process_ticket(llm, phone, customer_type, name, current_package,
                   area, network_status, fix_time, bill_info, history_text,
                   message, is_first_message=False):
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
            plans=PLANS_TEXT,
            message=message,
            is_first_message="yes" if is_first_message else "no"
        )
        response = llm.invoke(prompt_text)
        raw = response.content.strip().replace("```json", "").replace("```", "").strip()
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        result = json.loads(m.group(0) if m else raw)
        
        # Process actions
        action = result.get("action", "none")
        new_val = result.get("new_value", "").strip()
        
        if action == "update_name" and new_val:
            db().execute("UPDATE customers SET name=? WHERE phone=?", (new_val, phone))
            conn.commit()
            if st.session_state.customer and st.session_state.customer["name"] == name:
                st.session_state.customer["name"] = new_val
            result["record_updated"] = {"field":"name","value":new_val}
        elif action == "update_area" and new_val:
            db().execute("UPDATE customers SET area=? WHERE phone=?", (new_val, phone))
            conn.commit()
            if st.session_state.customer and st.session_state.customer["area"] == area:
                st.session_state.customer["area"] = new_val
            c = db()
            c.execute("SELECT status, expected_fix_time FROM outages WHERE area=?", (new_val,))
            out = c.fetchone()
            if out:
                st.session_state.network_status = out[0]
                st.session_state.fix_time = out[1]
            result["record_updated"] = {"field":"area","value":new_val}
        elif action == "update_package" and new_val:
            db().execute("UPDATE customers SET package=? WHERE phone=?", (new_val, phone))
            conn.commit()
            if st.session_state.customer:
                st.session_state.customer["package"] = new_val
            result["record_updated"] = {"field":"package","value":new_val}
        
        # Process data display
        show = result.get("show_records", "none")
        if show == "bill":
            c = db()
            c.execute("SELECT amount, due_date FROM bills WHERE customer_phone=?", (phone,))
            row = c.fetchone()
            if row:
                try:
                    overdue = datetime.date.today() > datetime.date.fromisoformat(row[1])
                except:
                    overdue = False
                result["bill_data"] = {"amount":row[0],"due_date":row[1],"overdue":overdue}
        elif show == "tickets":
            c = db()
            c.execute("SELECT ticket_id, issue, priority, status, created_at FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 4", (phone,))
            rows = c.fetchall()
            result["tickets_data"] = [{"ticket_id":r[0],"issue":r[1],"priority":r[2],"status":r[3],"created_at":r[4]} for r in rows]
        elif show == "plans":
            result["plans_data"] = True
        
        # Create ticket in database
        ticket_id = gen_ticket_id()
        technician = gen_tech() if result.get("technician_required", "").lower() == "yes" else "Not Assigned"
        c = db()
        c.execute("INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)", (
            ticket_id, phone, result.get("category","General"),
            result.get("priority","Medium"), result.get("sentiment","Neutral"),
            technician, "Open", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

def render_chat(chat_list):
    """Render conversation with extra data cards"""
    for msg in chat_list:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["text"])
        elif msg["role"] == "ai":
            with st.chat_message("assistant", avatar="🤖"):
                if "error" in msg:
                    st.error(f"Something went wrong: {msg['error']}")
                else:
                    r = msg["result"]
                    st.write(r.get("reply", ""))
                    
                    # Show data cards if present
                    if "bill_data" in r:
                        bd = r["bill_data"]
                        due_text = f"Due: {bd['due_date']}"
                        status_color = "#f87171" if bd.get("overdue") else "#4ade80"
                        status_text = "OVERDUE" if bd.get("overdue") else "CURRENT"
                        with st.expander("💳 View Bill Details"):
                            st.markdown(f"""
                            <div style="background:#0f172a;border-radius:12px;padding:16px;">
                                <div style="font-size:28px;font-weight:800;color:#fbbf24;">PKR {bd['amount']:,}</div>
                                <div>{due_text}</div>
                                <div style="color:{status_color};">{status_text}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    if "tickets_data" in r:
                        tickets = r["tickets_data"]
                        with st.expander(f"🎫 Recent Tickets ({len(tickets)})"):
                            for t in tickets:
                                st.markdown(f"**{t['ticket_id']}** - {t['issue']}  \nPriority: {t['priority']} | Status: {t['status']}")
                    if "plans_data" in r:
                        with st.expander("📶 Available Plans"):
                            for p in PLANS_LIST:
                                st.markdown(f"**{p['name']}** – {p['speed']} – {p['price']}/month")
                    if "record_updated" in r:
                        upd = r["record_updated"]
                        st.success(f"✅ **{upd['field'].title()}** updated to: *{upd['value']}*")
                    
                    # Ticket info
                    tid = r.get("ticket_id", "")
                    tech = r.get("technician", "Not Assigned")
                    caption_parts = [f"🎫 Ticket: {tid}"]
                    if tech != "Not Assigned":
                        caption_parts.append(f"🔧 Assigned: {tech}")
                    st.caption("  ·  ".join(caption_parts))

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
defaults = {
    "screen": "welcome",
    "phone": "",
    "customer": None,
    "customer_type": "",
    "bill_info": "",
    "network_status": "ACTIVE",
    "fix_time": "N/A",
    "history_text": "",
    "chat": [],
    "api_key": "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",
    "first_message_sent": False,
    "new_customer_data": None,
    "selected_plan": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
# TOP BAR (show on non-welcome screens)
# ═══════════════════════════════════════════════════════════════
if st.session_state.screen != "welcome":
    st.markdown("""
    <div class="topbar">
      <div class="topbar-brand">
        <div class="topbar-icon">🌐</div>
        <div>
          <div class="topbar-title">FiberISP</div>
          <div class="topbar-sub">AI-POWERED CUSTOMER SUPPORT</div>
        </div>
      </div>
      <div class="status-pill"><div class="status-dot"></div> SYSTEM ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SCREEN ROUTING
# ═══════════════════════════════════════════════════════════════

# WELCOME
if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="welcome-hero">
        <div class="welcome-logo">🌐</div>
        <div class="welcome-title">Welcome to FiberISP</div>
        <div class="welcome-subtitle">Experience Ultra-Fast Fiber Internet</div>
        <div class="welcome-tagline">AI-Powered Support • 24/7 Assistance • Lightning Speed</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 48px 0 28px;'><span style='font-size:18px; color:#94a3b8; font-weight:600;'>Choose your account type to continue</span></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-icon">👤</div>
            <div class="choice-title">Existing Customer</div>
            <div class="choice-desc">Login with your phone number to access your account, check bills, and get AI support.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔑 Login", key="btn_existing", use_container_width=True):
            st.session_state.customer_type = "existing"
            st.session_state.screen = "customer_login"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-icon">🆕</div>
            <div class="choice-title">New Customer</div>
            <div class="choice-desc">Sign up for a new FiberISP connection and get instant AI-powered support.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝 Register", key="btn_new", use_container_width=True):
            st.session_state.customer_type = "new"
            st.session_state.screen = "new_customer_register"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-icon">🛠️</div>
            <div class="choice-title">Admin Panel</div>
            <div class="choice-desc">Manage customers, monitor tickets, configure outages, and oversee system operations.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔐 Admin Access", key="btn_admin", use_container_width=True):
            st.session_state.screen = "admin_login"
            st.rerun() 

# CUSTOMER LOGIN (NO OTP)
elif st.session_state.screen == "customer_login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div class="form-title">📱 Customer Login</div>
          <div class="form-sub">Enter your registered phone number to access your account</div>
        </div>
        """, unsafe_allow_html=True)
        phone = st.text_input("Phone Number", placeholder="Your Registered Phone Number", key="login_phone")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Login", key="do_login"):
                if phone.strip():
                    c = db()
                    c.execute("SELECT name, package, area FROM customers WHERE phone=?", (phone.strip(),))
                    cust = c.fetchone()
                    if cust:
                        st.session_state.phone = phone.strip()
                        st.session_state.customer = {"name": cust[0], "package": cust[1], "area": cust[2]}
                        st.session_state.customer_type = "Existing Customer"
                        area = cust[2]
                        c.execute("SELECT amount, due_date FROM bills WHERE customer_phone=?", (phone.strip(),))
                        bill = c.fetchone()
                        st.session_state.bill_info = f"PKR {bill[0]:,}, Due: {bill[1]}" if bill else "No billing record"
                        if area:
                            c.execute("SELECT status, expected_fix_time FROM outages WHERE area=?", (area,))
                            out = c.fetchone()
                            if out:
                                st.session_state.network_status = out[0]
                                st.session_state.fix_time = out[1]
                        c.execute("SELECT issue FROM tickets WHERE customer_phone=?", (phone.strip(),))
                        rows = c.fetchall()
                        st.session_state.history_text = "\n".join([f"- {r[0]}" for r in rows]) if rows else "No previous tickets."
                        st.session_state.first_message_sent = False
                        st.session_state.chat = []
                        st.session_state.screen = "customer_dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Phone number not registered. Please register as a new customer.")
                else:
                    st.error("⚠️ Please enter a valid phone number.")
        with c2:
            if st.button("← Back", key="back_login"):
                st.session_state.screen = "welcome"
                st.rerun()

# NEW CUSTOMER REGISTRATION (NO OTP)
elif st.session_state.screen == "new_customer_register":

    _, col, _ = st.columns([1, 2, 1])

    with col:

        st.markdown("""
        <div class="form-box">
            <div class="form-title">🆕 New Customer Registration</div>
            <div class="form-sub">
                Complete your profile to start using FiberISP services
            </div>
        </div>
        """, unsafe_allow_html=True)

        # FORM
        with st.form("new_cust_form"):

            name = st.text_input(
                "FULL NAME",
                placeholder="Type Your Full Name"
            )

            phone = st.text_input(
                "PHONE NUMBER",
                placeholder="Correct Phone Number"
            )

            area = st.selectbox(
                "YOUR AREA",
                PAKISTAN_LOCATIONS,
                index=None,
                placeholder="Choose your area"
            )

            submit = st.form_submit_button("✅ Create Account")

            if submit:

                if name.strip() and phone.strip() and area is not None:

                    c = db()

                    try:
                        c.execute(
                            """
                            INSERT INTO customers(name, phone, package, area)
                            VALUES(?,?,?,?)
                            """,
                            (
                                name.strip(),
                                phone.strip(),
                                "No Package",
                                area
                            )
                        )

                        conn.commit()

                        st.session_state.phone = phone.strip()

                        st.session_state.customer = {
                            "name": name.strip(),
                            "package": "No Package",
                            "area": area
                        }

                        st.session_state.customer_type = "New Customer"
                        st.session_state.bill_info = "No billing record"

                        c.execute(
                            """
                            SELECT status, expected_fix_time
                            FROM outages
                            WHERE area=?
                            """,
                            (area,)
                        )

                        out = c.fetchone()

                        if out:
                            st.session_state.network_status = out[0]
                            st.session_state.fix_time = out[1]

                        st.session_state.history_text = "No previous tickets."
                        st.session_state.first_message_sent = False
                        st.session_state.chat = []

                        st.success(
                            "✅ Registration successful! Welcome to FiberISP!"
                        )

                        st.session_state.screen = "customer_dashboard"
                        st.rerun()

                    except sqlite3.IntegrityError:
                        st.error(
                            "❌ This phone number is already registered."
                        )

                else:
                    st.error(
                        "⚠️ Please fill all fields and select a valid area."
                    )

        if st.button("← Back", key="back_new_reg"):
            st.session_state.screen = "welcome"
            st.rerun()
# ADMIN LOGIN
elif st.session_state.screen == "admin_login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("""
        <div class="form-box">
          <div class="form-title">🔐 Admin Access</div>
          <div class="form-sub">Enter administrator password</div>
        </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Admin Password", type="password", placeholder="admin123")
        if st.button("Login →", key="admin_go"):
            if pwd == "xxxxxxxxx":
                st.session_state.screen = "admin"
                st.rerun()
            else:
                st.error("❌ Incorrect password.")
        if st.button("← Back", key="back_admin"):
            st.session_state.screen = "welcome"
            st.rerun()

# ADMIN DASHBOARD
elif st.session_state.screen == "admin":
    c = db()
    total_cust = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    total_tick = c.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    open_tick = c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'").fetchone()[0]
    high_tick = c.execute("SELECT COUNT(*) FROM tickets WHERE priority='High' AND status='Open'").fetchone()[0]
    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card"><div class="metric-num blue">{total_cust}</div><div class="metric-lbl">Customers</div></div>
      <div class="metric-card"><div class="metric-num">{total_tick}</div><div class="metric-lbl">Total Tickets</div></div>
      <div class="metric-card"><div class="metric-num yellow">{open_tick}</div><div class="metric-lbl">Open Tickets</div></div>
      <div class="metric-card"><div class="metric-num red">{high_tick}</div><div class="metric-lbl">High Priority</div></div>
    </div>
    """, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🎫 Tickets", "👥 Customers", "📡 Outages"])
    with tab1:
        for row in c.execute("SELECT * FROM tickets ORDER BY created_at DESC").fetchall():
            st.markdown(f"**{row[0]}** | {row[2]} | {row[3]} | {row[6]}")
    with tab2:
        st.dataframe(c.execute("SELECT name,phone,package,area FROM customers").fetchall(), use_container_width=True)
    with tab3:
        for row in c.execute("SELECT * FROM outages").fetchall():
            st.write(f"{row[0]} – {row[1]} – Fix: {row[2]}")
        with st.form("add_outage"):
            oa = st.text_input("Area")
            os = st.selectbox("Status", ["DOWN","ACTIVE"])
            of = st.text_input("Expected Fix Time")
            if st.form_submit_button("Save"):
                db().execute("INSERT OR REPLACE INTO outages VALUES(?,?,?)", (oa, os, of))
                conn.commit()
                st.rerun()
    if st.button("← Logout", key="admin_logout"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

# CUSTOMER DASHBOARD (MAIN)
elif st.session_state.screen == "customer_dashboard":
    cust = st.session_state.customer
    phone = st.session_state.phone
    llm = get_llm(st.session_state.api_key)
    lang = "English"  # fixed
    
    # Customer info card
    outage_html = ""
    if st.session_state.network_status == "DOWN":
        outage_html = f'''
        <div class="outage-warn">
          ⚠️ <strong>Network Outage Detected in {htmllib.escape(cust["area"])}</strong> — 
          Expected resolution: {htmllib.escape(st.session_state.fix_time)}
        </div>
        '''
    st.markdown(f"""
    <div class="cust-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div class="cust-name">👋 Welcome To FiberISP Customer Dashboard, {htmllib.escape(cust["name"])}</div>
        <span style="font-size:13px;background:rgba(14,165,233,.12);border:1px solid rgba(14,165,233,.25);padding:6px 16px;border-radius:24px;color:#0ea5e9;font-family:'JetBrains Mono',monospace;font-weight:700;">🇬🇧 English</span>
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
    
    # Logout button
    col_logout, _ = st.columns([1,5])
    with col_logout:
        if st.button("🚪 Logout", key="logout_cust"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Support Chat", "🆕 New Connection", "💳 My Bill & Tickets", "📶 Upgrade Plan"])
    
    # ========== TAB 1: AI CHAT ==========
    with tab1:
        st.markdown("""
        <div class="ai-banner">
          <div class="ai-banner-title">✨ Try our new AI assistant – ask anything, anytime</div>
          <div class="ai-banner-sub"></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='sec-hdr'>Quick Topics — Tap for Instant Help</div>", unsafe_allow_html=True)
        quick_topics = [
            ("🐌", "Slow internet speed"), ("📡", "WiFi not working"), ("⛔", "No internet connection"),
            ("💳", "Check my bill"), ("⬆️", "Upgrade my plan"), ("🔁", "Router restart help"),
            ("📶", "Weak signal"), ("🔧", "Request a technician"), ("📋", "My ticket status"),
            ("📦", "What plans are available")
        ]
        cols = st.columns(5)
        for i, (icon, label) in enumerate(quick_topics):
            with cols[i % 5]:
                if st.button(f"{icon} {label}", key=f"qt_{i}"):
                    st.session_state.chat.append({"role": "user", "text": label})
                    with st.spinner("🤖 AI is analyzing your request..."):
                        is_first = not st.session_state.first_message_sent
                        result, err = process_ticket(
                            llm, phone, st.session_state.customer_type,
                            cust["name"], cust["package"], cust["area"],
                            st.session_state.network_status, st.session_state.fix_time,
                            st.session_state.bill_info, st.session_state.history_text,
                            label, is_first
                        )
                        st.session_state.first_message_sent = True
                    if result:
                        st.session_state.chat.append({"role": "ai", "result": result})
                    else:
                        st.session_state.chat.append({"role": "ai", "error": err})
                    st.rerun()
        
        st.markdown("<div class='sec-hdr'>Conversation History</div>", unsafe_allow_html=True)
        if not st.session_state.chat:
            st.info("💬 Our AI assistant is here 24/7 to answer your queries and resolve your issues—instantly.")
        else:
            render_chat(st.session_state.chat)
        
        user_msg = st.chat_input("Select from quick topic or start conversation with our AI assistant")
        if user_msg and user_msg.strip():
            st.session_state.chat.append({"role": "user", "text": user_msg.strip()})
            with st.spinner("🤖 AI is thinking..."):
                is_first = not st.session_state.first_message_sent
                result, err = process_ticket(
                    llm, phone, st.session_state.customer_type,
                    cust["name"], cust["package"], cust["area"],
                    st.session_state.network_status, st.session_state.fix_time,
                    st.session_state.bill_info, st.session_state.history_text,
                    user_msg.strip(), is_first
                )
                st.session_state.first_message_sent = True
            if result:
                st.session_state.chat.append({"role": "ai", "result": result})
            else:
                st.session_state.chat.append({"role": "ai", "error": err})
            st.rerun()
        if st.session_state.chat:
            if st.button("🗑️ Clear Chat History", key="clear_chat"):
                st.session_state.chat = []
                st.session_state.first_message_sent = False
                st.rerun()
    
    # ========== TAB 2: NEW CONNECTION ==========
    with tab2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:2px solid rgba(14,165,233,.25);border-radius:20px;padding:28px 32px;margin-bottom:24px;">
          <div style="font-size:22px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">🆕 Request New Internet Connection</div>
          <div style="font-size:15px;color:#94a3b8;line-height:1.7;">Fill in the details below and our team will contact you within 24 hours to schedule your installation.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='sec-hdr'>Choose Your Plan</div>", unsafe_allow_html=True)
        plan_cols = st.columns(4)
        plans_data = [("Basic Home", "25 Mbps", "PKR 2,000"), ("Gaming Pro", "100 Mbps", "PKR 4,000"),
                      ("Ultra Fiber", "250 Mbps", "PKR 6,500"), ("Extreme Fiber", "500 Mbps", "PKR 9,000")]
        for i, (pname, speed, price) in enumerate(plans_data):
            with plan_cols[i]:
                selected_cls = "selected" if st.session_state.selected_plan == pname else ""
                st.markdown(f"""
                <div class="plan-card {selected_cls}">
                  <div class="plan-name">{pname}</div>
                  <div class="plan-speed">{speed}</div>
                  <div class="plan-price">{price}</div>
                  <div class="plan-per">/month</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"✓ Select", key=f"new_plan_{i}"):
                    st.session_state.selected_plan = pname
                    st.rerun()
        st.markdown("<div class='sec-hdr'>Your Contact Details</div>", unsafe_allow_html=True)
        with st.form("new_conn_form", clear_on_submit=True):
            nc_name = st.text_input("Full Name", value=cust["name"])
            nc_phone = st.text_input("Phone Number", value=phone)
            nc_area = st.selectbox("Installation Area", PAKISTAN_LOCATIONS, index=PAKISTAN_LOCATIONS.index(cust["area"]) if cust["area"] in PAKISTAN_LOCATIONS else 0)
            if st.form_submit_button("📩 Submit Connection Request"):
                if nc_name.strip() and nc_phone.strip() and st.session_state.selected_plan:
                    c = db()
                    c.execute("INSERT INTO new_connection_requests(name,phone,area,package,created_at) VALUES(?,?,?,?,?)",
                              (nc_name.strip(), nc_phone.strip(), nc_area, st.session_state.selected_plan, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    st.success(f"✅ Request submitted! We'll contact you at {nc_phone.strip()} within 24 hours.")
                    st.session_state.selected_plan = ""
                elif not st.session_state.selected_plan:
                    st.error("⚠️ Please select a plan first.")
                else:
                    st.error("⚠️ Please fill in all required fields.")
    
    # ========== TAB 3: BILL & TICKETS ==========
    with tab3:
        c = db()
        c.execute("SELECT amount, due_date FROM bills WHERE customer_phone=?", (phone,))
        bill_row = c.fetchone()
        if bill_row:
            amount, due_date = bill_row
            today = datetime.date.today()
            try:
                due = datetime.date.fromisoformat(due_date)
                overdue = today > due
            except:
                overdue = False
            status_html = '<span class="bill-status-due">⚠️ OVERDUE</span>' if overdue else '<span class="bill-status-ok">✅ CURRENT</span>'
            st.markdown(f"""
            <div class="bill-card">
              <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;letter-spacing:.1em;margin-bottom:12px;text-transform:uppercase;">Current Bill Amount</div>
              <div class="bill-amount"><span class="bill-currency">PKR</span>{amount:,}</div>
              <div class="bill-due">📅 Due Date: {due_date}</div>
              {status_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💳 No billing record found for your account.")
        st.markdown("<div class='sec-hdr'>Recent Support Tickets</div>", unsafe_allow_html=True)
        c.execute("SELECT ticket_id, issue, priority, status, created_at FROM tickets WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5", (phone,))
        tickets = c.fetchall()
        if tickets:
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
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📋 No support tickets found.")
    
    # ========== TAB 4: UPGRADE PLAN ==========
    with tab4:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:2px solid rgba(14,165,233,.25);border-radius:20px;padding:28px 32px;margin-bottom:24px;">
          <div style="font-size:22px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">📶 Upgrade Your Internet Plan</div>
          <div style="font-size:15px;color:#94a3b8;">
            Current plan: <strong style="color:#0ea5e9;">{htmllib.escape(cust["package"])}</strong><br>
            Select a new plan below to upgrade your connection speed
          </div>
        </div>
        """, unsafe_allow_html=True)
        up_cols = st.columns(4)
        for i, (pname, speed, price) in enumerate(plans_data):
            with up_cols[i]:
                is_current = pname in cust["package"]
                border = "border-color:#0ea5e9;box-shadow:0 0 30px rgba(14,165,233,0.2);" if is_current else ""
                current_badge = '<div style="font-size:11px;color:#0ea5e9;font-family:monospace;margin-top:10px;font-weight:800;">✓ CURRENT PLAN</div>' if is_current else ""
                st.markdown(f"""
                <div class="plan-card" style="{border}">
                  <div class="plan-name">{pname}</div>
                  <div class="plan-speed">{speed}</div>
                  <div class="plan-price">{price}</div>
                  <div class="plan-per">/month</div>
                  {current_badge}
                </div>
                """, unsafe_allow_html=True)
                if not is_current:
                    if st.button(f"⬆️ Upgrade", key=f"upgrade_plan_{i}"):
                        upgrade_msg = f"I want to upgrade my plan from {cust['package']} to {pname} ({speed}, {price}/month)"
                        st.session_state.chat.append({"role": "user", "text": upgrade_msg})
                        with st.spinner("🤖 Processing upgrade request..."):
                            is_first = not st.session_state.first_message_sent
                            result, err = process_ticket(
                                llm, phone, st.session_state.customer_type,
                                cust["name"], cust["package"], cust["area"],
                                st.session_state.network_status, st.session_state.fix_time,
                                st.session_state.bill_info, st.session_state.history_text,
                                upgrade_msg, is_first
                            )
                            st.session_state.first_message_sent = True
                        if result:
                            st.session_state.chat.append({"role": "ai", "result": result})
                        else:
                            st.session_state.chat.append({"role": "ai", "error": err})
                        st.success(f"✅ Upgrade request for '{pname}' submitted! Check the AI Support Chat tab for details.")
                        st.rerun()
