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
    page_title="FiberISP - AI Support",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# ENHANCED CUSTOM CSS - PROFESSIONAL DESIGN
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

/* ══════ CHOICE CARDS (Existing/New/Admin) ══════ */
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

/* ══════ AI CHAT MESSAGES ══════ */
.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, rgba(15,23,42,0.3) 0%, rgba(30,41,59,0.3) 100%);
    border-radius: 20px;
    border: 1px solid rgba(14,165,233,0.15);
}
.chat-message {
    margin-bottom: 24px;
    animation: fadeIn 0.4s ease-in;
    display: flex;
    gap: 12px;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.chat-message.user {
    flex-direction: row-reverse;
}
.chat-message.assistant {
    flex-direction: row;
}
.chat-avatar {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.chat-avatar.user {
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    box-shadow: 0 4px 12px rgba(139,92,246,0.4);
}
.chat-avatar.assistant {
    background: linear-gradient(135deg, #0ea5e9, #3b82f6);
    box-shadow: 0 4px 12px rgba(14,165,233,0.4);
}
.chat-bubble {
    max-width: 75%;
    padding: 18px 24px;
    border-radius: 18px;
    position: relative;
}
.chat-bubble.user {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
    color: #ffffff;
    border-bottom-right-radius: 4px;
    box-shadow: 0 4px 16px rgba(14,165,233,0.3);
}
.chat-bubble.assistant {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid rgba(14,165,233,0.25);
    color: #f1f5f9;
    border-bottom-left-radius: 4px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.chat-text {
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 0;
}
.chat-meta {
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid rgba(14,165,233,0.15);
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.chat-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 24px;
    font-family: 'JetBrains Mono', monospace;
}
.badge-ticket {
    background: rgba(14,165,233,0.15);
    color: #7dd3fc;
    border: 1px solid rgba(14,165,233,0.3);
}
.badge-tech {
    background: rgba(167,139,250,0.15);
    color: #c4b5fd;
    border: 1px solid rgba(167,139,250,0.3);
}

/* ══════ RECORD DISPLAY TABLE ══════ */
.record-table {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 14px;
    margin: 16px 0;
    overflow: hidden;
}
.record-row {
    display: flex;
    padding: 14px 20px;
    border-bottom: 1px solid rgba(14,165,233,0.1);
    transition: background 0.2s;
}
.record-row:hover {
    background: rgba(14,165,233,0.05);
}
.record-row:last-child {
    border-bottom: none;
}
.record-label {
    flex: 0 0 160px;
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.record-value {
    flex: 1;
    font-size: 15px;
    color: #f1f5f9;
    font-weight: 600;
}
.record-highlight {
    color: #0ea5e9;
    font-weight: 800;
}
.record-success {
    color: #4ade80;
    font-weight: 800;
}
.record-warning {
    color: #fbbf24;
    font-weight: 800;
}
.record-error {
    color: #f87171;
    font-weight: 800;
}

/* ══════ AI ASSISTANCE BANNER ══════ */
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

/* ══════ STREAMLIT COMPONENT OVERRIDES ══════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #0f172a !important;
    border: 2px solid rgba(14,165,233,0.25) !important;
    border-radius: 14px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 4px rgba(14,165,233,0.18) !important;
}
label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
    margin-bottom: 8px !important;
}
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
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 36px rgba(14,165,233,0.4) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0f172a;
    border-bottom: 2px solid rgba(14,165,233,0.2);
    gap: 0;
    border-radius: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border-bottom: 3px solid transparent !important;
    padding: 16px 28px !important;
}
.stTabs [aria-selected="true"] {
    color: #0ea5e9 !important;
    border-bottom-color: #0ea5e9 !important;
    background: transparent !important;
}
div[data-testid="stChatMessageContent"] {
    background: transparent !important;
}
div[data-testid="stChatMessage"] {
    padding: 0 !important;
    background: transparent !important;
}
.stSuccess {
    background: rgba(74,222,128,0.1) !important;
    border: 1px solid rgba(74,222,128,0.3) !important;
    color: #4ade80 !important;
    border-radius: 12px !important;
}
.stError {
    background: rgba(248,113,113,0.1) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    color: #f87171 !important;
    border-radius: 12px !important;
}
.stInfo {
    background: rgba(14,165,233,0.1) !important;
    border: 1px solid rgba(14,165,233,0.3) !important;
    color: #7dd3fc !important;
    border-radius: 12px !important;
}

/* Hide Streamlit default chat styling */
.stChatFloatingInputContainer {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    border: 2px solid rgba(14,165,233,0.25) !important;
    border-radius: 18px !important;
    padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAKISTAN LOCATIONS - COMPREHENSIVE LIST
# ═══════════════════════════════════════════════════════════════
PAKISTAN_LOCATIONS = [
    # Peshawar & KPK
    "Peshawar - University Town", "Peshawar - Hayatabad", "Peshawar - Saddar",
    "Peshawar - Board Bazaar", "Peshawar - Gulbahar", "Peshawar - Tehkal",
    "Peshawar - Cantt", "Peshawar - Phase 5", "Mardan", "Swat - Mingora",
    "Abbottabad", "Mansehra", "Kohat", "Bannu", "Dera Ismail Khan",
    
    # Islamabad
    "Islamabad - F-6", "Islamabad - F-7", "Islamabad - F-8", "Islamabad - F-10",
    "Islamabad - F-11", "Islamabad - G-6", "Islamabad - G-7", "Islamabad - G-8",
    "Islamabad - G-9", "Islamabad - G-10", "Islamabad - G-11", "Islamabad - Blue Area",
    "Islamabad - I-8", "Islamabad - I-9", "Islamabad - I-10", "Islamabad - E-11",
    "Islamabad - D-12", "Islamabad - Bahria Town", "Islamabad - DHA",
    
    # Rawalpindi
    "Rawalpindi - Satellite Town", "Rawalpindi - Bahria Town", "Rawalpindi - Saddar",
    "Rawalpindi - Commercial Market", "Rawalpindi - PWD", "Rawalpindi - Chaklala",
    "Rawalpindi - Westridge", "Rawalpindi - Askari", "Rawalpindi - Gulzar-e-Quaid",
    
    # Lahore
    "Lahore - DHA", "Lahore - Gulberg", "Lahore - Model Town", "Lahore - Johar Town",
    "Lahore - Cantt", "Lahore - Faisal Town", "Lahore - Iqbal Town", "Lahore - Garden Town",
    "Lahore - Bahria Town", "Lahore - Township", "Lahore - Allama Iqbal Town",
    "Lahore - Wapda Town", "Lahore - Lake City", "Lahore - Valencia Town",
    
    # Karachi
    "Karachi - DHA", "Karachi - Clifton", "Karachi - Gulshan-e-Iqbal",
    "Karachi - PECHS", "Karachi - Nazimabad", "Karachi - Korangi",
    "Karachi - North Karachi", "Karachi - Malir", "Karachi - Saddar",
    "Karachi - Gulistan-e-Johar", "Karachi - North Nazimabad",
    "Karachi - Tariq Road", "Karachi - Bahadurabad", "Karachi - Shahrah-e-Faisal",
    
    # Faisalabad
    "Faisalabad - Peoples Colony", "Faisalabad - Model Town", "Faisalabad - Madina Town",
    "Faisalabad - Susan Road", "Faisalabad - Civil Lines", "Faisalabad - Samanabad",
    
    # Multan
    "Multan - Cantt", "Multan - Gulgasht Colony", "Multan - Model Town",
    "Multan - Shah Rukn-e-Alam Colony", "Multan - Bosan Road", "Multan - DHA",
    
    # Quetta
    "Quetta - Cantt", "Quetta - Satellite Town", "Quetta - Samungli Road",
    "Quetta - Jinnah Town", "Quetta - Chiltan Housing Scheme",
    
    # Other Major Cities
    "Sialkot", "Gujranwala", "Sargodha", "Bahawalpur", "Sukkur",
    "Hyderabad", "Larkana", "Nawabshah", "Mirpur Khas",
    "Gujrat", "Jhang", "Sheikhupura", "Sahiwal", "Okara",
    "Wah Cantt", "Kasur", "Chiniot", "Kamoke", "Hafizabad"
]

# ═══════════════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════════════
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
    
    # Insert pre-registered customer: Affan from Peshawar
    try:
        c.execute("INSERT OR IGNORE INTO customers(name,phone,package,area) VALUES(?,?,?,?)",
                  ("Affan", "03146532146", "Gaming Pro 100Mbps", "Peshawar - University Town"))
        c.execute("INSERT OR IGNORE INTO bills(customer_phone,amount,due_date) VALUES(?,?,?)",
                  ("03146532146", 4000, "2026-06-20"))
        
        # Also keep Ali Khan for testing
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
# AI MODEL CONFIGURATION
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
