"""
ConnectPK — Chat UI Upgrade
===========================
Drop these two things into your main app file:

1. Replace your existing CSS block with ENHANCED_CSS (add inside st.markdown(...))
2. Replace your render_chat() function with the one below
3. Replace the Tab 1 quick-topics block with the improved version at the bottom

Requires no new dependencies — pure Streamlit + HTML/CSS.
"""

# ══════════════════════════════════════════════════════════
#  ENHANCED CSS  — paste inside your st.markdown(""" ... """, unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════

ENHANCED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: #07090f !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stSidebar"] { display: none; }
[data-testid="stToolbar"] { display: none; }
.block-container { max-width: 900px !important; padding: 2rem 1.5rem !important; }

/* ── Section header ── */
.sec-hdr {
    font-size: 11px; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: #475569;
    margin: 28px 0 14px; padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,.05);
}

/* ════════════════════════════════
   CUSTOMER INFO CARD
════════════════════════════════ */
.cust-card {
    background: linear-gradient(135deg, #0d1117 0%, #111827 100%);
    border: 1px solid rgba(56,189,248,.18);
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(56,189,248,.06);
}
.cust-name { font-size: 20px; font-weight: 800; color: #f0f6ff; }
.cust-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.cust-chip {
    display: flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 30px; padding: 5px 14px;
    font-size: 12.5px; color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}
.cust-chip span { color: #e2e8f0; }
.outage-warn {
    margin-top: 14px; background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,.25); border-radius: 10px;
    padding: 10px 16px; font-size: 13px; color: #fca5a5;
}

/* ════════════════════════════════
   QUICK TOPICS  — pill chips
════════════════════════════════ */
.qt-wrapper {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-bottom: 24px;
}
.qt-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(15,23,42,1);
    border: 1px solid rgba(56,189,248,.18);
    border-radius: 100px;
    padding: 8px 16px;
    font-size: 13px; font-weight: 600; color: #7dd3fc;
    cursor: pointer;
    transition: all .18s ease;
    font-family: 'Plus Jakarta Sans', sans-serif;
    white-space: nowrap;
}
.qt-pill:hover {
    background: rgba(56,189,248,.12);
    border-color: rgba(56,189,248,.45);
    color: #bae6fd;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(56,189,248,.12);
}

/* ════════════════════════════════
   CHAT WINDOW
════════════════════════════════ */
.chat-window {
    background: #0b0e18;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px;
    padding: 20px 16px;
    min-height: 220px;
    max-height: 520px;
    overflow-y: auto;
    scroll-behavior: smooth;
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
    gap: 18px;
}
.chat-window::-webkit-scrollbar { width: 4px; }
.chat-window::-webkit-scrollbar-track { background: transparent; }
.chat-window::-webkit-scrollbar-thumb { background: rgba(56,189,248,.2); border-radius: 4px; }

/* ── Message rows ── */
.msg-row { display: flex; align-items: flex-end; gap: 10px; animation: fadeUp .25s ease both; }
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.agent { flex-direction: row; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Avatars ── */
.avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.avatar.user-av  { background: linear-gradient(135deg,#1e40af,#3b82f6); }
.avatar.agent-av { background: linear-gradient(135deg,#0f766e,#14b8a6); }

/* ── Bubbles ── */
.bubble {
    max-width: 72%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 14px; line-height: 1.6;
    word-break: break-word;
    position: relative;
}
.bubble.user-bubble {
    background: linear-gradient(135deg,#1e3a5f,#1e40af);
    color: #e0f2fe;
    border-bottom-right-radius: 4px;
    box-shadow: 0 4px 20px rgba(59,130,246,.2);
}
.bubble.agent-bubble {
    background: #111827;
    border: 1px solid rgba(56,189,248,.15);
    color: #e2e8f0;
    border-bottom-left-radius: 4px;
    box-shadow: 0 4px 20px rgba(0,0,0,.3);
}

/* ── Timestamp ── */
.msg-time {
    font-size: 10px; color: #334155;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px;
    text-align: right;
}
.msg-row.agent .msg-time { text-align: left; }

/* ── AI response card inside bubble ── */
.ai-card {
    background: #0d1117;
    border: 1px solid rgba(56,189,248,.2);
    border-radius: 14px;
    overflow: hidden;
    max-width: 78%;
    box-shadow: 0 8px 32px rgba(0,0,0,.4);
    animation: fadeUp .3s ease both;
}
.ai-card-header {
    background: linear-gradient(90deg, rgba(14,165,233,.12), rgba(20,184,166,.08));
    border-bottom: 1px solid rgba(56,189,248,.12);
    padding: 12px 16px;
    display: flex; align-items: center; gap: 10px;
}
.ai-card-header .badge {
    font-size: 10px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; font-family: 'JetBrains Mono', monospace;
    padding: 3px 10px; border-radius: 20px;
}
.badge-high   { background: rgba(239,68,68,.15);  color: #f87171; border: 1px solid rgba(239,68,68,.3); }
.badge-medium { background: rgba(234,179,8,.12);  color: #fbbf24; border: 1px solid rgba(234,179,8,.3); }
.badge-low    { background: rgba(74,222,128,.1);  color: #4ade80; border: 1px solid rgba(74,222,128,.25); }
.badge-ticket { background: rgba(56,189,248,.1);  color: #38bdf8; border: 1px solid rgba(56,189,248,.2); }
.badge-sent-pos { background: rgba(74,222,128,.1);  color: #4ade80; border: 1px solid rgba(74,222,128,.25); }
.badge-sent-neg { background: rgba(239,68,68,.1);  color: #f87171; border: 1px solid rgba(239,68,68,.25); }
.badge-sent-neu { background: rgba(148,163,184,.08); color: #94a3b8; border: 1px solid rgba(148,163,184,.2); }

.ai-card-body { padding: 16px; }
.ai-card-body .response-text {
    font-size: 14px; line-height: 1.75; color: #cbd5e1;
    margin-bottom: 14px;
}
.ai-meta {
    display: flex; flex-wrap: wrap; gap: 7px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,.06);
}
.meta-chip {
    font-size: 11px; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    padding: 4px 10px; border-radius: 20px;
    display: flex; align-items: center; gap: 5px;
}
.meta-tech { background: rgba(168,85,247,.1);  color: #c084fc; border: 1px solid rgba(168,85,247,.2); }
.meta-cat  { background: rgba(56,189,248,.08); color: #38bdf8; border: 1px solid rgba(56,189,248,.18); }
.meta-tid  { background: rgba(255,255,255,.04); color: #64748b; border: 1px solid rgba(255,255,255,.08); }

/* ── Steps / checklist in AI response ── */
.step-list { margin: 10px 0; padding-left: 0; list-style: none; display: flex; flex-direction: column; gap: 8px; }
.step-item {
    display: flex; align-items: flex-start; gap: 10px;
    font-size: 13.5px; color: #94a3b8; line-height: 1.5;
}
.step-num {
    width: 22px; height: 22px; border-radius: 50%;
    background: rgba(56,189,248,.12); border: 1px solid rgba(56,189,248,.25);
    color: #38bdf8; font-size: 11px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Typing indicator ── */
.typing-row { display: flex; align-items: flex-end; gap: 10px; }
.typing-bubble {
    background: #111827; border: 1px solid rgba(56,189,248,.15);
    border-radius: 18px; border-bottom-left-radius: 4px;
    padding: 14px 18px; display: flex; gap: 5px; align-items: center;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #38bdf8; opacity: .6;
    animation: bounce 1.2s infinite ease-in-out;
}
.dot:nth-child(2) { animation-delay: .2s; }
.dot:nth-child(3) { animation-delay: .4s; }
@keyframes bounce {
    0%,80%,100% { transform: translateY(0); opacity:.4; }
    40%          { transform: translateY(-6px); opacity:1; }
}

/* ── Empty state ── */
.chat-empty {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: 48px 20px; gap: 12px;
    color: #1e293b;
}
.chat-empty .icon { font-size: 42px; opacity: .4; }
.chat-empty .txt  { font-size: 13px; color: #334155; }

/* ════════════════════════════════
   TICKET CARDS  (admin + history)
════════════════════════════════ */
.ticket-card {
    background: #0b0e18;
    border: 1px solid rgba(255,255,255,.07);
    border-left: 3px solid #334155;
    border-radius: 14px; padding: 14px 18px; margin-bottom: 10px;
}
.ticket-card.high     { border-left-color: #ef4444; }
.ticket-card.medium   { border-left-color: #f59e0b; }
.ticket-card.low      { border-left-color: #22c55e; }
.ticket-card.resolved { border-left-color: #3b82f6; opacity: .7; }
.ticket-hdr { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.ticket-id  { font-family: 'JetBrains Mono',monospace; font-size: 11px; color: #475569; }
.ticket-status { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; font-family: 'JetBrains Mono',monospace; }
.s-open     { background: rgba(234,179,8,.12); color: #fbbf24; border: 1px solid rgba(234,179,8,.25); }
.s-resolved { background: rgba(59,130,246,.1);  color: #60a5fa; border: 1px solid rgba(59,130,246,.2); }
.ticket-issue { font-size: 14px; color: #e2e8f0; font-weight: 600; margin-bottom: 8px; }
.ticket-meta  { display: flex; flex-wrap: wrap; gap: 6px; }
.tag { font-size: 11px; padding: 3px 9px; border-radius: 20px; font-family: 'JetBrains Mono',monospace; }
.tag-high   { background: rgba(239,68,68,.1);  color: #f87171; border: 1px solid rgba(239,68,68,.2); }
.tag-medium { background: rgba(245,158,11,.1); color: #fbbf24; border: 1px solid rgba(245,158,11,.2); }
.tag-low    { background: rgba(34,197,94,.08); color: #4ade80; border: 1px solid rgba(34,197,94,.2); }
.tag-sent   { background: rgba(255,255,255,.04); color: #64748b; border: 1px solid rgba(255,255,255,.07); }
.tag-tech   { background: rgba(168,85,247,.08); color: #c084fc; border: 1px solid rgba(168,85,247,.18); }

/* ════════════════════════════════
   PLAN CARDS
════════════════════════════════ */
.plan-card {
    background: #0b0e18;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 16px; padding: 20px 14px;
    text-align: center; transition: all .2s;
    margin-bottom: 8px;
}
.plan-card:hover, .plan-card.selected {
    border-color: rgba(56,189,248,.4);
    background: rgba(56,189,248,.05);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(56,189,248,.1);
}
.plan-name  { font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: .06em; }
.plan-speed { font-size: 22px; font-weight: 800; color: #38bdf8; margin: 8px 0 4px; }
.plan-price { font-size: 16px; font-weight: 700; color: #f0f6ff; }
.plan-per   { font-size: 11px; color: #475569; margin-top: 2px; }

/* ════════════════════════════════
   BILL CARD
════════════════════════════════ */
.bill-card {
    background: linear-gradient(135deg,#0b0e18,#111827);
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 18px; padding: 28px 24px;
    text-align: center; margin-bottom: 20px;
}
.bill-amount { font-size: 44px; font-weight: 800; color: #f0f6ff; margin: 8px 0; }
.bill-currency { font-size: 20px; color: #38bdf8; margin-right: 4px; vertical-align: super; }
.bill-due { font-size: 13px; color: #64748b; margin-bottom: 12px; }
.bill-status-ok  { background: rgba(34,197,94,.1);  color: #4ade80; border: 1px solid rgba(34,197,94,.25);  padding: 5px 18px; border-radius: 30px; font-size: 12px; font-weight: 700; font-family: 'JetBrains Mono',monospace; }
.bill-status-due { background: rgba(239,68,68,.1);  color: #f87171; border: 1px solid rgba(239,68,68,.25);  padding: 5px 18px; border-radius: 30px; font-size: 12px; font-weight: 700; font-family: 'JetBrains Mono',monospace; }

/* ════════════════════════════════
   LOGIN / REGISTRATION BOXES
════════════════════════════════ */
.login-box {
    background: #0b0e18; border: 1px solid rgba(56,189,248,.15);
    border-radius: 20px; padding: 32px 28px; text-align: center; margin-bottom: 24px;
}
.login-title { font-size: 22px; font-weight: 800; color: #f0f6ff; margin-bottom: 8px; }
.login-sub   { font-size: 13px; color: #475569; }

/* ════════════════════════════════
   NEW CONNECTION CARD
════════════════════════════════ */
.nc-card {
    background: #0b0e18; border: 1px solid rgba(56,189,248,.12);
    border-radius: 16px; padding: 22px 24px; margin-bottom: 20px;
}
.nc-title { font-size: 17px; font-weight: 700; color: #f0f6ff; margin-bottom: 6px; }
.nc-sub   { font-size: 13px; color: #64748b; }

/* ════════════════════════════════
   ADMIN METRICS
════════════════════════════════ */
.metric-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 24px; }
.metric-card {
    background: #0b0e18; border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px; padding: 20px; text-align: center;
}
.metric-num { font-size: 34px; font-weight: 800; color: #f87171; }
.metric-num.blue   { color: #38bdf8; }
.metric-num.yellow { color: #fbbf24; }
.metric-num.red    { color: #f87171; }
.metric-lbl { font-size: 11px; color: #475569; margin-top: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; }

/* ════════════════════════════════
   LANGUAGE SELECTION CARDS
════════════════════════════════ */
.lang-card {
    background: #0b0e18; border: 1px solid rgba(56,189,248,.15);
    border-radius: 18px; padding: 28px 20px; text-align: center;
    transition: all .2s; cursor: pointer; margin-bottom: 10px;
}
.lang-card:hover { border-color: rgba(56,189,248,.4); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(56,189,248,.1); }
.lang-emoji { font-size: 40px; margin-bottom: 10px; }
.lang-title { font-size: 18px; font-weight: 800; color: #f0f6ff; }
.lang-sub   { font-size: 12px; color: #475569; margin-top: 4px; }

/* ════════════════════════════════
   STREAMLIT BUTTON OVERRIDES
════════════════════════════════ */
[data-testid="stButton"] > button {
    background: rgba(14,165,233,.1) !important;
    border: 1px solid rgba(56,189,248,.25) !important;
    color: #7dd3fc !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    transition: all .2s !important;
}
[data-testid="stButton"] > button:hover {
    background: rgba(56,189,248,.18) !important;
    border-color: rgba(56,189,248,.5) !important;
    color: #bae6fd !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(56,189,248,.15) !important;
}
/* Primary / CTA buttons */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#0ea5e9,#14b8a6) !important;
    border: none !important;
    color: #fff !important;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stTextInput"] textarea {
    background: #0b0e18 !important;
    border: 1px solid rgba(56,189,248,.2) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(56,189,248,.5) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.08) !important;
}

/* Chat input bar */
[data-testid="stChatInput"] textarea {
    background: #0f1520 !important;
    border: 1px solid rgba(56,189,248,.2) !important;
    color: #e2e8f0 !important;
    border-radius: 14px !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #0b0e18 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid rgba(255,255,255,.06) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #475569 !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(56,189,248,.12) !important;
    color: #38bdf8 !important;
}
</style>
"""


# ══════════════════════════════════════════════════════════
#  IMPROVED render_chat() — replace your existing function
# ══════════════════════════════════════════════════════════

import html as htmllib
import datetime

def render_chat(chat: list):
    """
    Renders chat messages as modern, styled chat bubbles.
    User messages: right-aligned blue bubble.
    AI responses:  left-aligned structured card with metadata.
    """
    from datetime import datetime as dt
    now_str = dt.now().strftime("%I:%M %p")

    html_parts = ['<div class="chat-window" id="chat-end">']

    if not chat:
        html_parts.append("""
        <div class="chat-empty">
            <div class="icon">💬</div>
            <div class="txt">Tap a quick topic above or type your issue to start.</div>
        </div>""")
    else:
        for i, msg in enumerate(chat):
            if msg["role"] == "user":
                text = htmllib.escape(msg.get("text", ""))
                html_parts.append(f"""
                <div class="msg-row user" style="animation-delay:{i*0.05}s">
                    <div>
                        <div class="bubble user-bubble">{text}</div>
                        <div class="msg-time">{now_str}</div>
                    </div>
                    <div class="avatar user-av">👤</div>
                </div>""")

            elif msg["role"] == "ai":
                if "error" in msg:
                    err = htmllib.escape(str(msg["error"]))
                    html_parts.append(f"""
                    <div class="msg-row agent" style="animation-delay:{i*0.05}s">
                        <div class="avatar agent-av">🤖</div>
                        <div class="bubble agent-bubble" style="border-color:rgba(239,68,68,.3);color:#fca5a5;">
                            ⚠️ {err}
                        </div>
                    </div>""")

                elif "result" in msg:
                    r = msg["result"]
                    # --- pull fields (defensive) ---
                    response_text = htmllib.escape(str(r.get("response", r.get("message", "Here to help!"))))
                    priority  = str(r.get("priority", "Low"))
                    sentiment = str(r.get("sentiment", "Neutral"))
                    category  = str(r.get("category", "General"))
                    technician= str(r.get("technician_required", r.get("tech", "No")))
                    ticket_id = str(r.get("ticket_id", ""))
                    steps     = r.get("steps", [])

                    # badge classes
                    pri_cls   = {"High":"badge-high","Medium":"badge-medium","Low":"badge-low"}.get(priority,"badge-low")
                    sent_cls  = "badge-sent-pos" if "pos" in sentiment.lower() or sentiment.lower()=="happy" \
                                else "badge-sent-neg" if "neg" in sentiment.lower() or "frust" in sentiment.lower() \
                                else "badge-sent-neu"

                    # steps HTML
                    steps_html = ""
                    if steps:
                        items = "".join(
                            f'<li class="step-item"><div class="step-num">{j+1}</div><span>{htmllib.escape(str(s))}</span></li>'
                            for j, s in enumerate(steps)
                        )
                        steps_html = f'<ul class="step-list">{items}</ul>'

                    # response text — convert newlines to <br>
                    response_html = response_text.replace("\\n", "<br>").replace("\n", "<br>")

                    tech_html = f'<span class="meta-chip meta-tech">🔧 Technician: {htmllib.escape(technician)}</span>' if technician and technician != "No" else ""
                    tid_html  = f'<span class="meta-chip meta-tid">🎫 {htmllib.escape(ticket_id)}</span>' if ticket_id else ""

                    html_parts.append(f"""
                    <div class="msg-row agent" style="animation-delay:{i*0.05}s">
                        <div class="avatar agent-av">🤖</div>
                        <div class="ai-card">
                            <div class="ai-card-header">
                                <span style="font-size:15px;">✨</span>
                                <span style="font-size:13px;font-weight:700;color:#94a3b8;flex:1;">ConnectPK AI Support</span>
                                <span class="badge {pri_cls}">{priority}</span>
                                <span class="badge {sent_cls}">{sentiment}</span>
                            </div>
                            <div class="ai-card-body">
                                <div class="response-text">{response_html}</div>
                                {steps_html}
                                <div class="ai-meta">
                                    <span class="meta-chip meta-cat">📂 {htmllib.escape(category)}</span>
                                    {tech_html}
                                    {tid_html}
                                    <span class="meta-chip" style="background:rgba(255,255,255,.03);color:#334155;border:1px solid rgba(255,255,255,.06);">🕐 {now_str}</span>
                                </div>
                            </div>
                        </div>
                    </div>""")

    html_parts.append('</div>')  # close chat-window

    # Auto-scroll script
    html_parts.append("""
    <script>
        const el = document.getElementById('chat-end');
        if(el) el.scrollTop = el.scrollHeight;
    </script>""")

    import streamlit as st
    st.markdown("".join(html_parts), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  IMPROVED TAB 1 — Quick Topics section
#  Replace the "Render as a row of styled buttons" block
# ══════════════════════════════════════════════════════════

QUICK_TOPICS_SNIPPET = '''
# ── Quick Topics ──
st.markdown("<div class='sec-hdr'>Quick Topics</div>", unsafe_allow_html=True)

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

# Render pills in 2 rows of 5 using columns
cols = st.columns(5)
for i, (icon, label) in enumerate(quick_topics):
    with cols[i % 5]:
        if st.button(f"{icon} {label}", key=f"qt_{i}", use_container_width=True):
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

st.markdown("<div class='sec-hdr'>Conversation</div>", unsafe_allow_html=True)
'''
