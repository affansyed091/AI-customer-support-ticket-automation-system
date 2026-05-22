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
    page_title="FiberISP · Neural Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════
#  GLOBAL CSS — CYBERPUNK FIBER-OPTIC THEME
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {
  --neon-cyan:   #00f5ff;
  --neon-blue:   #0080ff;
  --neon-purple: #bf00ff;
  --neon-green:  #00ff88;
  --neon-amber:  #ffaa00;
  --neon-red:    #ff3355;
  --bg-void:     #020408;
  --bg-deep:     #040810;
  --bg-panel:    #060c18;
  --bg-card:     rgba(6, 14, 28, 0.85);
  --glass-border:rgba(0, 245, 255, 0.12);
  --glass-glow:  rgba(0, 245, 255, 0.04);
  --text-primary:#e8f4ff;
  --text-muted:  #3a5a7a;
  --text-dim:    #1a3050;
}

/* ── Reset & Base ── */
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html, body, [class*="css"] { 
  font-family: 'Rajdhani', sans-serif !important;
  color: var(--text-primary) !important;
}

/* ── Void Background with animated circuit lines ── */
.stApp {
  background: var(--bg-void) !important;
  background-image:
    radial-gradient(ellipse 120% 60% at 20% -10%, rgba(0,128,255,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 80% 40% at 80% 110%, rgba(191,0,255,0.06) 0%, transparent 50%),
    radial-gradient(ellipse 60% 30% at 50% 50%, rgba(0,245,255,0.02) 0%, transparent 70%) !important;
  background-attachment: fixed !important;
}

.main .block-container {
  padding: 0 2rem 4rem !important;
  max-width: 1400px !important;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden; }

/* ── Scan lines overlay ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 245, 255, 0.008) 2px,
    rgba(0, 245, 255, 0.008) 4px
  );
  animation: scanmove 8s linear infinite;
}
@keyframes scanmove {
  0% { background-position: 0 0; }
  100% { background-position: 0 100vh; }
}

/* ── Circuit grid ── */
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(0,245,255,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,255,0.018) 1px, transparent 1px);
  background-size: 80px 80px;
}

/* ══════════════════ HERO SECTION ══════════════════ */
.hero-wrap {
  position: relative;
  padding: 0;
  margin-bottom: 0;
  overflow: hidden;
}

/* Fiber optic data stream canvas */
.data-stream-bar {
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%, var(--neon-cyan) 30%, var(--neon-blue) 60%, var(--neon-purple) 80%, transparent 100%);
  animation: stream-flow 3s linear infinite;
  background-size: 200% 100%;
  margin-bottom: 0;
}
@keyframes stream-flow {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.hero-main {
  background: linear-gradient(135deg, 
    rgba(0,245,255,0.04) 0%,
    rgba(0,20,40,0.9) 30%,
    rgba(0,5,15,0.95) 60%,
    rgba(191,0,255,0.03) 100%);
  border: 1px solid var(--glass-border);
  border-top: 2px solid rgba(0,245,255,0.3);
  border-radius: 0 0 32px 32px;
  padding: 60px 40px 50px;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 80px rgba(0,245,255,0.05),
    inset 0 1px 0 rgba(0,245,255,0.15),
    0 40px 100px rgba(0,0,0,0.8);
}

/* Corner brackets */
.hero-main::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: 
    linear-gradient(to right, var(--neon-cyan) 2px, transparent 2px) 0 0 / 30px 30px no-repeat,
    linear-gradient(to bottom, var(--neon-cyan) 2px, transparent 2px) 0 0 / 30px 30px no-repeat,
    linear-gradient(to left, var(--neon-cyan) 2px, transparent 2px) 100% 0 / 30px 30px no-repeat,
    linear-gradient(to bottom, var(--neon-cyan) 2px, transparent 2px) 100% 0 / 30px 30px no-repeat,
    linear-gradient(to right, var(--neon-cyan) 2px, transparent 2px) 0 100% / 30px 30px no-repeat,
    linear-gradient(to top, var(--neon-cyan) 2px, transparent 2px) 0 100% / 30px 30px no-repeat,
    linear-gradient(to left, var(--neon-cyan) 2px, transparent 2px) 100% 100% / 30px 30px no-repeat,
    linear-gradient(to top, var(--neon-cyan) 2px, transparent 2px) 100% 100% / 30px 30px no-repeat;
  opacity: 0.4;
  pointer-events: none;
}

.hero-eyebrow {
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  color: var(--neon-cyan);
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 20px;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
}
.hero-eyebrow::before, .hero-eyebrow::after {
  content: '';
  width: 40px;
  height: 1px;
  background: var(--neon-cyan);
  opacity: 0.5;
}

.hero-logo-container {
  position: relative;
  display: inline-block;
  margin-bottom: 24px;
  z-index: 1;
}

.hero-logo-ring {
  position: absolute;
  inset: -16px;
  border-radius: 50%;
  border: 1px solid rgba(0,245,255,0.2);
  animation: ring-spin 12s linear infinite;
}
.hero-logo-ring::after {
  content: '';
  position: absolute;
  top: -3px; left: 50%;
  width: 6px; height: 6px;
  background: var(--neon-cyan);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan);
  transform: translateX(-50%);
}
@keyframes ring-spin { to { transform: rotate(360deg); } }

.hero-logo-ring-2 {
  position: absolute;
  inset: -28px;
  border-radius: 50%;
  border: 1px solid rgba(191,0,255,0.15);
  animation: ring-spin 20s linear infinite reverse;
}
.hero-logo-ring-2::after {
  content: '';
  position: absolute;
  bottom: -3px; left: 30%;
  width: 4px; height: 4px;
  background: var(--neon-purple);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--neon-purple);
  transform: translateX(-50%);
}

.hero-logo-hex {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #001830, #002040);
  border: 2px solid var(--neon-cyan);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  box-shadow: 
    0 0 30px rgba(0,245,255,0.4),
    0 0 60px rgba(0,245,255,0.15),
    inset 0 0 30px rgba(0,245,255,0.05);
  animation: logo-pulse 3s ease-in-out infinite;
  position: relative;
  z-index: 1;
}
@keyframes logo-pulse {
  0%, 100% { box-shadow: 0 0 30px rgba(0,245,255,0.4), 0 0 60px rgba(0,245,255,0.15), inset 0 0 30px rgba(0,245,255,0.05); }
  50% { box-shadow: 0 0 50px rgba(0,245,255,0.6), 0 0 100px rgba(0,245,255,0.25), inset 0 0 40px rgba(0,245,255,0.1); }
}

.hero-title {
  font-family: 'Orbitron', monospace;
  font-size: 72px;
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1;
  margin-bottom: 8px;
  position: relative;
  z-index: 1;
  background: linear-gradient(135deg, 
    #ffffff 0%, 
    var(--neon-cyan) 35%, 
    #60a0ff 65%,
    var(--neon-purple) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 30px rgba(0,245,255,0.3));
  animation: title-shimmer 4s ease-in-out infinite;
}
@keyframes title-shimmer {
  0%, 100% { filter: drop-shadow(0 0 20px rgba(0,245,255,0.3)); }
  50% { filter: drop-shadow(0 0 40px rgba(0,245,255,0.6)); }
}

.hero-subtitle {
  font-family: 'Rajdhani', sans-serif;
  font-size: 18px;
  font-weight: 300;
  color: rgba(232,244,255,0.6);
  letter-spacing: 0.1em;
  margin-bottom: 28px;
  position: relative;
  z-index: 1;
  text-transform: uppercase;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  position: relative;
  z-index: 1;
  margin-top: 24px;
}
.hero-stat {
  text-align: center;
  padding: 12px 24px;
  border: 1px solid rgba(0,245,255,0.1);
  border-radius: 12px;
  background: rgba(0,245,255,0.03);
  backdrop-filter: blur(10px);
}
.hero-stat-num {
  font-family: 'Orbitron', monospace;
  font-size: 24px;
  font-weight: 700;
  color: var(--neon-cyan);
  display: block;
}
.hero-stat-lbl {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--text-muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-top: 2px;
}

/* ══════════════════ TOPBAR ══════════════════ */
.topbar-cyber {
  background: rgba(4, 8, 16, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0,245,255,0.12);
  border-left: none;
  border-right: none;
  border-top: 3px solid transparent;
  background-clip: padding-box;
  border-image: linear-gradient(90deg, transparent, var(--neon-cyan), transparent) 1;
  padding: 14px 32px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 30px rgba(0,0,0,0.8), 0 0 0 1px rgba(0,245,255,0.06);
}

.topbar-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}
.topbar-icon-hex {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,128,255,0.1));
  border: 1px solid rgba(0,245,255,0.35);
  border-radius: 11px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  box-shadow: 0 0 15px rgba(0,245,255,0.2);
  animation: icon-glow 3s ease-in-out infinite alternate;
}
@keyframes icon-glow {
  from { box-shadow: 0 0 10px rgba(0,245,255,0.2); }
  to { box-shadow: 0 0 25px rgba(0,245,255,0.5), inset 0 0 10px rgba(0,245,255,0.1); }
}
.topbar-name {
  font-family: 'Orbitron', monospace;
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: 0.05em;
}
.topbar-sub {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--neon-cyan);
  letter-spacing: 0.25em;
  text-transform: uppercase;
  margin-top: 1px;
  opacity: 0.7;
}

.topbar-right { display: flex; align-items: center; gap: 16px; }

.sys-status {
  display: flex; align-items: center; gap: 8px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--neon-green);
  background: rgba(0,255,136,0.05);
  border: 1px solid rgba(0,255,136,0.2);
  padding: 7px 16px;
  border-radius: 20px;
  letter-spacing: 0.15em;
}
.status-led {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--neon-green);
  box-shadow: 0 0 8px var(--neon-green);
  animation: led-blink 1.5s ease-in-out infinite;
}
@keyframes led-blink {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px var(--neon-green); }
  50% { opacity: 0.3; box-shadow: none; }
}

.topbar-ticker {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--text-dim);
  letter-spacing: 0.12em;
  border-left: 1px solid rgba(0,245,255,0.1);
  padding-left: 16px;
}

/* ══════════════════ WELCOME CHOICE CARDS ══════════════════ */
.choice-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 32px 0;
}

.choice-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 0;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}
.choice-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--card-accent, linear-gradient(90deg, var(--neon-cyan), var(--neon-blue)));
  box-shadow: 0 0 20px var(--card-accent-color, var(--neon-cyan));
}
.choice-card:hover {
  border-color: rgba(0,245,255,0.35);
  transform: translateY(-6px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 40px var(--card-glow, rgba(0,245,255,0.1));
}
.choice-card-inner {
  padding: 36px 28px 32px;
  text-align: center;
}

/* Holographic scan effect */
.choice-card::after {
  content: '';
  position: absolute;
  top: -100%;
  left: 0; right: 0;
  height: 100%;
  background: linear-gradient(180deg, transparent, rgba(0,245,255,0.04), transparent);
  transition: top 0.6s ease;
}
.choice-card:hover::after { top: 100%; }

.card-badge {
  position: absolute;
  top: 18px; right: 18px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 4px;
  border: 1px solid;
}
.badge-new { color: var(--neon-green); border-color: rgba(0,255,136,0.3); background: rgba(0,255,136,0.05); }
.badge-secure { color: var(--neon-purple); border-color: rgba(191,0,255,0.3); background: rgba(191,0,255,0.05); }

.card-icon-wrap {
  width: 80px; height: 80px;
  border-radius: 20px;
  margin: 0 auto 20px;
  display: flex; align-items: center; justify-content: center;
  font-size: 36px;
  position: relative;
}
.icon-cyan {
  background: linear-gradient(135deg, rgba(0,245,255,0.12), rgba(0,128,255,0.08));
  border: 1px solid rgba(0,245,255,0.25);
  box-shadow: 0 0 30px rgba(0,245,255,0.1);
}
.icon-green {
  background: linear-gradient(135deg, rgba(0,255,136,0.12), rgba(0,200,100,0.08));
  border: 1px solid rgba(0,255,136,0.25);
  box-shadow: 0 0 30px rgba(0,255,136,0.1);
}
.icon-purple {
  background: linear-gradient(135deg, rgba(191,0,255,0.12), rgba(100,0,200,0.08));
  border: 1px solid rgba(191,0,255,0.25);
  box-shadow: 0 0 30px rgba(191,0,255,0.1);
}

.card-title {
  font-family: 'Orbitron', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.05em;
  margin-bottom: 10px;
}
.card-desc {
  font-family: 'Rajdhani', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: var(--text-muted);
  line-height: 1.7;
  margin-bottom: 24px;
}
.card-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: left;
}
.card-feature {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--text-muted);
  letter-spacing: 0.08em;
}
.feature-dot {
  width: 4px; height: 4px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-cyan { background: var(--neon-cyan); box-shadow: 0 0 6px var(--neon-cyan); }
.dot-green { background: var(--neon-green); box-shadow: 0 0 6px var(--neon-green); }
.dot-purple { background: var(--neon-purple); box-shadow: 0 0 6px var(--neon-purple); }

/* section label between hero and cards */
.section-label {
  text-align: center;
  margin: 40px 0 24px;
  position: relative;
}
.section-label-text {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 0.4em;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  gap: 16px;
}
.section-label-text::before, .section-label-text::after {
  content: '';
  display: block;
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
  opacity: 0.3;
}

/* ══════════════════ STREAMLIT BUTTON OVERRIDES ══════════════════ */
/* Default fallback button */
.stButton > button {
  background: linear-gradient(135deg, rgba(0,245,255,0.08), rgba(0,128,255,0.05)) !important;
  border: 1px solid rgba(0,245,255,0.25) !important;
  color: var(--neon-cyan) !important;
  border-radius: 10px !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  letter-spacing: 0.08em !important;
  padding: 12px 20px !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 0 0 rgba(0,245,255,0) !important;
  width: 100% !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,128,255,0.1)) !important;
  border-color: rgba(0,245,255,0.6) !important;
  color: #ffffff !important;
  box-shadow: 0 0 20px rgba(0,245,255,0.2), inset 0 0 20px rgba(0,245,255,0.03) !important;
  transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Icon-only card button ── */
.icon-card-btn > div > .stButton > button {
  width: 80px !important;
  height: 80px !important;
  border-radius: 20px !important;
  font-size: 36px !important;
  padding: 0 !important;
  margin: 0 auto 20px !important;
  letter-spacing: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-card-btn.cyan > div > .stButton > button {
  background: linear-gradient(135deg, rgba(0,245,255,0.12), rgba(0,128,255,0.08)) !important;
  border: 1px solid rgba(0,245,255,0.3) !important;
  box-shadow: 0 0 20px rgba(0,245,255,0.1) !important;
}
.icon-card-btn.cyan > div > .stButton > button:hover {
  background: linear-gradient(135deg, #00f5ff, #0080ff) !important;
  box-shadow: 0 0 40px rgba(0,245,255,0.5), 0 0 0 6px rgba(0,245,255,0.08) !important;
  transform: translateY(-8px) scale(1.08) !important;
}
.icon-card-btn.green > div > .stButton > button {
  background: linear-gradient(135deg, rgba(0,255,136,0.12), rgba(0,200,100,0.08)) !important;
  border: 1px solid rgba(0,255,136,0.3) !important;
  box-shadow: 0 0 20px rgba(0,255,136,0.1) !important;
}
.icon-card-btn.green > div > .stButton > button:hover {
  background: linear-gradient(135deg, #00ff88, #00c864) !important;
  box-shadow: 0 0 40px rgba(0,255,136,0.5), 0 0 0 6px rgba(0,255,136,0.08) !important;
  transform: translateY(-8px) scale(1.08) !important;
}
.icon-card-btn.purple > div > .stButton > button {
  background: linear-gradient(135deg, rgba(191,0,255,0.12), rgba(100,0,200,0.08)) !important;
  border: 1px solid rgba(191,0,255,0.3) !important;
  box-shadow: 0 0 20px rgba(191,0,255,0.1) !important;
}
.icon-card-btn.purple > div > .stButton > button:hover {
  background: linear-gradient(135deg, #bf00ff, #6400c8) !important;
  box-shadow: 0 0 40px rgba(191,0,255,0.5), 0 0 0 6px rgba(191,0,255,0.08) !important;
  transform: translateY(-8px) scale(1.08) !important;
}

/* Back button */
.back-btn > div > .stButton > button {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  color: var(--text-muted) !important;
  font-size: 12px !important;
  padding: 10px 16px !important;
}
.back-btn > div > .stButton > button:hover {
  background: rgba(255,255,255,0.05) !important;
  color: var(--text-primary) !important;
  transform: translateX(-3px) !important;
  box-shadow: none !important;
}

/* Primary action button */
.primary-btn > div > .stButton > button {
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-blue)) !important;
  border: none !important;
  color: #000d1a !important;
  font-family: 'Orbitron', monospace !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  padding: 15px 24px !important;
  border-radius: 12px !important;
  box-shadow: 0 0 30px rgba(0,245,255,0.3), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.primary-btn > div > .stButton > button:hover {
  background: linear-gradient(135deg, #40ffff, #40a0ff) !important;
  box-shadow: 0 0 50px rgba(0,245,255,0.6), 0 8px 30px rgba(0,0,0,0.5) !important;
  transform: translateY(-3px) !important;
  color: #000408 !important;
}

/* Danger/logout */
.danger-btn > div > .stButton > button {
  background: rgba(255,51,85,0.06) !important;
  border: 1px solid rgba(255,51,85,0.25) !important;
  color: var(--neon-red) !important;
  font-size: 11px !important;
}
.danger-btn > div > .stButton > button:hover {
  background: rgba(255,51,85,0.12) !important;
  border-color: var(--neon-red) !important;
  box-shadow: 0 0 20px rgba(255,51,85,0.2) !important;
}

/* ══════════════════ GLASS FORM CARD ══════════════════ */
.glass-card {
  background: rgba(4, 10, 22, 0.92);
  backdrop-filter: blur(40px);
  border: 1px solid rgba(0,245,255,0.12);
  border-radius: 28px;
  padding: 48px 44px 40px;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(0,245,255,0.06),
    0 40px 100px rgba(0,0,0,0.8),
    0 0 80px rgba(0,245,255,0.03);
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
  opacity: 0.5;
}
.glass-card::after {
  content: '';
  position: absolute;
  top: -50%; left: -20%;
  width: 140%; height: 70%;
  background: radial-gradient(ellipse, rgba(0,245,255,0.03) 0%, transparent 70%);
  pointer-events: none;
}

.gc-icon {
  width: 72px; height: 72px;
  border-radius: 18px;
  margin: 0 auto 24px;
  display: flex; align-items: center; justify-content: center;
  font-size: 32px;
  position: relative; z-index: 1;
  animation: gc-float 4s ease-in-out infinite;
}
.gc-icon-cyan {
  background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,80,160,0.1));
  border: 1px solid rgba(0,245,255,0.3);
  box-shadow: 0 0 30px rgba(0,245,255,0.2);
}
.gc-icon-green {
  background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,100,80,0.1));
  border: 1px solid rgba(0,255,136,0.3);
  box-shadow: 0 0 30px rgba(0,255,136,0.2);
}
@keyframes gc-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-8px) rotate(-2deg); }
  66% { transform: translateY(-4px) rotate(2deg); }
}

.gc-title {
  font-family: 'Orbitron', monospace;
  font-size: 24px;
  font-weight: 800;
  text-align: center;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
  background: linear-gradient(135deg, var(--text-primary), var(--neon-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative; z-index: 1;
}
.gc-sub {
  font-size: 13px;
  font-weight: 400;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.75;
  margin-bottom: 28px;
  position: relative; z-index: 1;
}

.gc-divider {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 20px;
}
.gc-divider-line {
  flex: 1; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,245,255,0.2), transparent);
}
.gc-divider-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--neon-cyan);
  letter-spacing: 0.25em;
  text-transform: uppercase;
  opacity: 0.6;
  white-space: nowrap;
}

/* Floating capability tags */
.cap-tags {
  display: flex; flex-wrap: wrap; gap: 8px;
  justify-content: center;
  margin-bottom: 28px;
  position: relative; z-index: 1;
}
.cap-tag {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid;
  letter-spacing: 0.08em;
  animation: tag-float 3s ease-in-out infinite;
}
.cap-tag:nth-child(2) { animation-delay: 0.5s; }
.cap-tag:nth-child(3) { animation-delay: 1s; }
@keyframes tag-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
.tag-c { color: var(--neon-cyan); border-color: rgba(0,245,255,0.25); background: rgba(0,245,255,0.06); }
.tag-g { color: var(--neon-green); border-color: rgba(0,255,136,0.25); background: rgba(0,255,136,0.06); }
.tag-p { color: var(--neon-purple); border-color: rgba(191,0,255,0.25); background: rgba(191,0,255,0.06); }
.tag-a { color: var(--neon-amber); border-color: rgba(255,170,0,0.25); background: rgba(255,170,0,0.06); }

/* ══════════════════ INPUT OVERRIDES ══════════════════ */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stTextArea > div > div > textarea {
  background: rgba(0, 245, 255, 0.03) !important;
  border: 1px solid rgba(0,245,255,0.15) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  padding: 12px 15px !important;
  transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--neon-cyan) !important;
  background: rgba(0,245,255,0.05) !important;
  box-shadow: 0 0 0 3px rgba(0,245,255,0.08), 0 0 20px rgba(0,245,255,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(58,90,122,0.8) !important; }

label {
  color: rgba(0,245,255,0.6) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 10px !important;
  font-weight: 400 !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
}

/* ══════════════════ CUSTOMER DASHBOARD CARD ══════════════════ */
.profile-banner {
  background: linear-gradient(135deg, rgba(0,10,25,0.95), rgba(0,20,40,0.9));
  border: 1px solid rgba(0,245,255,0.15);
  border-top: 2px solid rgba(0,245,255,0.4);
  border-radius: 20px;
  padding: 28px 32px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.6), 0 0 40px rgba(0,245,255,0.04);
}
.profile-banner::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(0,245,255,0.06), transparent);
  pointer-events: none;
}
.profile-name {
  font-family: 'Orbitron', monospace;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.05em;
  margin-bottom: 16px;
}
.profile-chips {
  display: flex; gap: 8px; flex-wrap: wrap;
}
.profile-chip {
  background: rgba(0,245,255,0.04);
  border: 1px solid rgba(0,245,255,0.1);
  border-radius: 8px;
  padding: 6px 14px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  color: var(--text-muted);
}
.profile-chip span { color: var(--text-primary); margin-left: 5px; font-weight: 600; }

.outage-alert {
  background: rgba(255,51,85,0.06);
  border: 1px solid rgba(255,51,85,0.25);
  border-left: 3px solid var(--neon-red);
  border-radius: 10px;
  padding: 12px 18px;
  margin-top: 14px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 12px;
  color: #ff8099;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* ══════════════════ TABS ══════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(0,5,15,0.8) !important;
  border: 1px solid rgba(0,245,255,0.1) !important;
  border-radius: 14px !important;
  padding: 5px !important;
  gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-dim) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  border-radius: 10px !important;
  padding: 10px 20px !important;
  border: none !important;
  transition: all 0.2s !important;
  letter-spacing: 0.05em !important;
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(0,245,255,0.05) !important;
  color: var(--text-muted) !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(0,245,255,0.12), rgba(0,128,255,0.08)) !important;
  color: var(--neon-cyan) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  box-shadow: 0 0 15px rgba(0,245,255,0.08) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ══════════════════ SECTION HEADERS ══════════════════ */
.sec-hdr {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  font-weight: 400;
  color: var(--neon-cyan);
  letter-spacing: 0.35em;
  text-transform: uppercase;
  margin: 24px 0 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0,245,255,0.1);
  opacity: 0.7;
  display: flex;
  align-items: center;
  gap: 10px;
}
.sec-hdr::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, rgba(0,245,255,0.1), transparent);
}

/* ══════════════════ CHAT BANNER ══════════════════ */
.chat-head {
  background: linear-gradient(135deg, rgba(0,10,25,0.9), rgba(0,15,35,0.9));
  border: 1px solid rgba(0,245,255,0.12);
  border-left: 3px solid var(--neon-cyan);
  border-radius: 16px;
  padding: 18px 24px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 18px;
  position: relative;
  overflow: hidden;
}
.chat-head::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 200px; height: 100%;
  background: radial-gradient(ellipse at right, rgba(0,245,255,0.04), transparent);
}
.chat-head-icon {
  width: 46px; height: 46px;
  background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,80,160,0.1));
  border: 1px solid rgba(0,245,255,0.3);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(0,245,255,0.15);
}
.chat-head-name {
  font-family: 'Orbitron', monospace;
  font-size: 14px;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}
.chat-head-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  font-family: 'Rajdhani', sans-serif;
}
.ai-live {
  margin-left: auto;
  display: flex; align-items: center; gap: 6px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--neon-green);
  letter-spacing: 0.2em;
  flex-shrink: 0;
}

/* ══════════════════ PLAN CARDS ══════════════════ */
.plan-card {
  background: linear-gradient(150deg, rgba(4,8,20,0.95), rgba(6,12,28,0.9));
  border: 1px solid rgba(0,245,255,0.08);
  border-radius: 18px;
  padding: 24px 18px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.plan-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--plan-gradient, linear-gradient(90deg, var(--neon-cyan), var(--neon-blue)));
}
.plan-card:hover {
  border-color: rgba(0,245,255,0.3);
  transform: translateY(-5px);
  box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 30px var(--plan-glow, rgba(0,245,255,0.08));
}
.plan-card.current-plan {
  border-color: var(--neon-cyan);
  box-shadow: 0 0 30px rgba(0,245,255,0.1), inset 0 0 30px rgba(0,245,255,0.02);
}
.plan-icon { font-size: 30px; margin-bottom: 10px; }
.plan-name {
  font-family: 'Orbitron', monospace;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}
.plan-speed {
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  color: var(--neon-cyan);
  letter-spacing: 0.1em;
  margin-bottom: 12px;
  opacity: 0.8;
}
.plan-price {
  font-family: 'Orbitron', monospace;
  font-size: 22px;
  font-weight: 800;
  color: var(--neon-amber);
  letter-spacing: -0.02em;
}
.plan-period {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--text-dim);
  margin-bottom: 16px;
  letter-spacing: 0.1em;
}
.plan-features {
  list-style: none;
  text-align: left;
}
.plan-features li {
  font-family: 'Rajdhani', sans-serif;
  font-size: 12px;
  color: var(--text-muted);
  padding: 5px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  display: flex; align-items: center; gap: 7px;
}
.plan-features li:last-child { border-bottom: none; }
.plan-features li::before {
  content: '◆';
  color: var(--neon-cyan);
  font-size: 7px;
  flex-shrink: 0;
  opacity: 0.7;
}
.current-badge {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--neon-cyan);
  border: 1px solid rgba(0,245,255,0.3);
  background: rgba(0,245,255,0.06);
  padding: 3px 10px;
  border-radius: 6px;
  display: inline-block;
  margin-top: 10px;
  letter-spacing: 0.15em;
}

/* ══════════════════ BILL CARD ══════════════════ */
.bill-panel {
  background: linear-gradient(135deg, rgba(4,8,20,0.95), rgba(8,14,30,0.9));
  border: 1px solid rgba(255,170,0,0.15);
  border-top: 2px solid rgba(255,170,0,0.4);
  border-radius: 18px;
  padding: 28px 32px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}
.bill-panel::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 120px; height: 120px;
  background: radial-gradient(circle, rgba(255,170,0,0.06), transparent);
}
.bill-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: rgba(255,170,0,0.6);
  letter-spacing: 0.35em;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.bill-amount {
  font-family: 'Orbitron', monospace;
  font-size: 48px;
  font-weight: 900;
  color: var(--neon-amber);
  letter-spacing: -0.03em;
  line-height: 1;
}
.bill-currency {
  font-size: 16px;
  font-weight: 400;
  color: rgba(255,170,0,0.5);
  margin-right: 6px;
}
.bill-due {
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 8px;
}
.status-ok {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(0,255,136,0.06);
  border: 1px solid rgba(0,255,136,0.2);
  color: var(--neon-green);
  padding: 5px 14px;
  border-radius: 20px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.15em;
  margin-top: 14px;
}
.status-due {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,51,85,0.06);
  border: 1px solid rgba(255,51,85,0.2);
  color: var(--neon-red);
  padding: 5px 14px;
  border-radius: 20px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.15em;
  margin-top: 14px;
}

/* ══════════════════ TICKET CARDS ══════════════════ */
.ticket-node {
  background: rgba(4, 8, 20, 0.9);
  border: 1px solid rgba(0,245,255,0.07);
  border-left: 3px solid var(--ticket-accent, #1a3050);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 10px;
  transition: all 0.2s ease;
  position: relative;
}
.ticket-node:hover {
  border-color: rgba(0,245,255,0.2);
  box-shadow: 0 6px 24px rgba(0,0,0,0.5);
  transform: translateX(3px);
}
.ticket-node.high { --ticket-accent: var(--neon-red); }
.ticket-node.medium { --ticket-accent: var(--neon-amber); }
.ticket-node.low { --ticket-accent: var(--neon-green); }
.ticket-node.resolved { --ticket-accent: #1a2a3a; opacity: 0.55; }
.ticket-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.ticket-id {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 0.1em;
}
.ticket-status-badge {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 12px;
  letter-spacing: 0.1em;
}
.s-open { background: rgba(0,245,255,0.08); color: var(--neon-cyan); border: 1px solid rgba(0,245,255,0.15); }
.s-resolved { background: rgba(26,42,60,0.3); color: #2a4060; border: 1px solid rgba(26,42,60,0.4); }
.ticket-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}
.ticket-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.t-tag {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  padding: 2px 8px;
  border-radius: 10px;
  letter-spacing: 0.08em;
  border: 1px solid;
}
.t-high { color: var(--neon-red); border-color: rgba(255,51,85,0.2); background: rgba(255,51,85,0.05); }
.t-med { color: var(--neon-amber); border-color: rgba(255,170,0,0.2); background: rgba(255,170,0,0.05); }
.t-low { color: var(--neon-green); border-color: rgba(0,255,136,0.2); background: rgba(0,255,136,0.05); }
.t-info { color: var(--text-muted); border-color: rgba(58,90,122,0.2); background: transparent; }

/* ══════════════════ METRIC GRID ══════════════════ */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.metric-node {
  background: linear-gradient(150deg, rgba(4,8,20,0.95), rgba(6,12,28,0.9));
  border: 1px solid rgba(0,245,255,0.08);
  border-radius: 16px;
  padding: 22px 24px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s;
}
.metric-node::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: var(--metric-bar, linear-gradient(90deg, transparent, var(--neon-cyan), transparent));
  opacity: 0.4;
}
.metric-node:hover { border-color: rgba(0,245,255,0.2); }
.metric-num {
  font-family: 'Orbitron', monospace;
  font-size: 38px;
  font-weight: 900;
  color: var(--text-primary);
  line-height: 1;
}
.metric-num.c { color: var(--neon-cyan); }
.metric-num.g { color: var(--neon-green); }
.metric-num.a { color: var(--neon-amber); }
.metric-num.r { color: var(--neon-red); }
.metric-lbl {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: var(--text-dim);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-top: 8px;
}

/* ══════════════════ QUICK TOPICS ══════════════════ */
.stButton.qt-btn > button {
  background: rgba(0,245,255,0.04) !important;
  border: 1px solid rgba(0,245,255,0.12) !important;
  color: rgba(0,245,255,0.7) !important;
  border-radius: 10px !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  letter-spacing: 0.03em !important;
  padding: 10px 12px !important;
  box-shadow: none !important;
  transition: all 0.2s !important;
}
.stButton.qt-btn > button:hover {
  background: rgba(0,245,255,0.1) !important;
  border-color: rgba(0,245,255,0.35) !important;
  color: var(--neon-cyan) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 15px rgba(0,245,255,0.1) !important;
}

/* ══════════════════ ALERTS ══════════════════ */
.stSuccess {
  background: rgba(0,255,136,0.05) !important;
  border: 1px solid rgba(0,255,136,0.2) !important;
  border-radius: 12px !important;
  color: var(--neon-green) !important;
}
.stError {
  background: rgba(255,51,85,0.05) !important;
  border: 1px solid rgba(255,51,85,0.2) !important;
  border-radius: 12px !important;
  color: var(--neon-red) !important;
}
.stInfo {
  background: rgba(0,245,255,0.05) !important;
  border: 1px solid rgba(0,245,255,0.15) !important;
  border-radius: 12px !important;
  color: var(--neon-cyan) !important;
}

/* ══════════════════ CHAT INPUT ══════════════════ */
div[data-testid="stChatInput"] {
  background: rgba(4,8,20,0.9) !important;
  border-top: 1px solid rgba(0,245,255,0.08) !important;
}
div[data-testid="stChatInput"] textarea {
  background: rgba(0,245,255,0.03) !important;
  border: 1px solid rgba(0,245,255,0.12) !important;
  color: var(--text-primary) !important;
  border-radius: 12px !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 14px !important;
}

/* ══════════════════ FORM SUBMIT ══════════════════ */
div[data-testid="stForm"] .stButton > button {
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-blue)) !important;
  border: none !important;
  color: #000d1a !important;
  font-family: 'Orbitron', monospace !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  border-radius: 12px !important;
  padding: 14px !important;
  box-shadow: 0 0 30px rgba(0,245,255,0.25) !important;
}
div[data-testid="stForm"] .stButton > button:hover {
  background: linear-gradient(135deg, #40ffff, #40a0ff) !important;
  box-shadow: 0 0 50px rgba(0,245,255,0.5) !important;
  transform: translateY(-3px) !important;
}

/* ══════════════════ ADMIN SECTION ══════════════════ */
.admin-login-wrap {
  background: rgba(4,8,20,0.9);
  border: 1px solid rgba(191,0,255,0.15);
  border-top: 2px solid rgba(191,0,255,0.4);
  border-radius: 24px;
  padding: 48px 44px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.admin-login-wrap::before {
  content: '';
  position: absolute; top: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--neon-purple), transparent);
  opacity: 0.5;
}

/* ══════════════════ DATAFRAME ══════════════════ */
.stDataFrame { border-radius: 14px !important; overflow: hidden !important; }

/* ══════════════════ SPINNER ══════════════════ */
.stSpinner > div { border-top-color: var(--neon-cyan) !important; }

/* ══════════════════ SELECTBOX ══════════════════ */
.stSelectbox > div > div { 
  background: rgba(0,245,255,0.03) !important; 
  border: 1px solid rgba(0,245,255,0.15) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
}

/* ══════════════════ DEMO HINT ══════════════════ */
.demo-hint {
  text-align: center;
  margin-top: 18px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 0.1em;
}
.demo-code {
  font-family: 'Share Tech Mono', monospace;
  background: rgba(0,245,255,0.06);
  border: 1px solid rgba(0,245,255,0.15);
  color: var(--neon-cyan);
  padding: 2px 10px;
  border-radius: 5px;
  font-size: 11px;
  letter-spacing: 0.05em;
}

/* ══════════════════ CONNECTION REQUEST CARD ══════════════════ */
.conn-info {
  background: rgba(0,245,255,0.03);
  border: 1px solid rgba(0,245,255,0.1);
  border-radius: 12px;
  padding: 14px 18px;
  margin: 10px 0;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-family: 'Rajdhani', sans-serif;
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
}
.conn-info strong { color: var(--neon-cyan); }
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
        "gradient": "linear-gradient(90deg, #0080ff, #00c8ff)",
        "glow": "rgba(0,128,255,0.15)",
        "features": ["25 Mbps Download", "10 Mbps Upload", "100 GB Fair Use",
                     "Email Support", "Standard Installation"],
    },
    {
        "name": "Gaming Pro",   "speed": "100 Mbps", "price": "PKR 4,000", "icon": "🎮",
        "gradient": "linear-gradient(90deg, #bf00ff, #8040ff)",
        "glow": "rgba(191,0,255,0.15)",
        "features": ["100 Mbps Download", "50 Mbps Upload", "Unlimited Data",
                     "Priority 24/7 Support", "Static IP Address", "Free Router"],
    },
    {
        "name": "Ultra Fiber",  "speed": "250 Mbps", "price": "PKR 6,500", "icon": "⚡",
        "gradient": "linear-gradient(90deg, #00f5ff, #0080ff)",
        "glow": "rgba(0,245,255,0.15)",
        "features": ["250 Mbps Download", "100 Mbps Upload", "Unlimited Data",
                     "VIP Support Line", "2 Static IPs", "Premium Router", "Free Installation"],
    },
    {
        "name": "Extreme Fiber","speed": "500 Mbps", "price": "PKR 9,000", "icon": "🚀",
        "gradient": "linear-gradient(90deg, #ffaa00, #ff6600)",
        "glow": "rgba(255,170,0,0.15)",
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
    cls = {"High":"t-high","Medium":"t-med","Low":"t-low"}.get(p,"t-low")
    return f'<span class="t-tag {cls}">{htmllib.escape(p)}</span>'

def sent_tag(s):
    return f'<span class="t-tag t-info">{htmllib.escape(s)}</span>'


# ══════════════════════════════════════════════
#  CHAT RENDERER
# ══════════════════════════════════════════════
def render_chat(chat_list):
    if not chat_list:
        st.markdown("""
        <div style="background:rgba(0,245,255,0.02);border:1px solid rgba(0,245,255,0.07);
             border-radius:16px;padding:60px 20px;text-align:center;">
          <div style="font-size:40px;margin-bottom:16px;opacity:0.2;">◈</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#1a3050;
               letter-spacing:0.35em;text-transform:uppercase;">
            SELECT A QUICK TOPIC OR TYPE TO INITIALIZE SEQUENCE
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
                <div class="utime">{htmllib.escape(ts)} · YOU</div>
              </div>
              <div class="av uav">◈</div>
            </div>"""

        elif msg["role"] == "ai":
            ts = msg.get("time","")
            if "error" in msg:
                err = htmllib.escape(str(msg["error"]))
                msgs_html += f"""
                <div class="row bot-row">
                  <div class="av bav">⬡</div>
                  <div class="ebub">⚠ ERROR: {err}</div>
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

            PRI_COLORS = {
                "High":   ("#ff3355","rgba(255,51,85,0.08)","rgba(255,51,85,0.25)"),
                "Medium": ("#ffaa00","rgba(255,170,0,0.08)","rgba(255,170,0,0.25)"),
                "Low":    ("#00ff88","rgba(0,255,136,0.06)","rgba(0,255,136,0.2)"),
            }
            pc, pbg, pbo = PRI_COLORS.get(pri, PRI_COLORS["Low"])
            pri_e = htmllib.escape(pri)

            sl = sent.lower()
            if any(x in sl for x in ["pos","happy"]):
                sc, sbg = "#00ff88","rgba(0,255,136,0.07)"
            elif any(x in sl for x in ["frust","angry","neg"]):
                sc, sbg = "#ff3355","rgba(255,51,85,0.07)"
            else:
                sc, sbg = "#94a3b8","rgba(148,163,184,0.06)"
            sent_e = htmllib.escape(sent)

            rec_html = ""

            if r.get("bill_data"):
                bd  = r["bill_data"]
                amt = f"{int(bd.get('amount',0)):,}"
                dd  = htmllib.escape(str(bd.get("due_date","N/A")))
                if bd.get("overdue"):
                    st_c, st_bg, st_bo, st_txt = "#ff3355","rgba(255,51,85,0.07)","rgba(255,51,85,0.2)","⚠ OVERDUE"
                else:
                    st_c, st_bg, st_bo, st_txt = "#00ff88","rgba(0,255,136,0.06)","rgba(0,255,136,0.2)","✓ CURRENT"
                rec_html = f"""
                <div class="rec-card">
                  <div class="rec-lbl">◈ BILLING DATA</div>
                  <div style="display:flex;align-items:baseline;gap:6px;margin:10px 0 6px;">
                    <span style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#2a4060;">PKR</span>
                    <span style="font-family:'Orbitron',monospace;font-size:28px;font-weight:900;
                      color:#ffaa00;letter-spacing:-0.03em;">{amt}</span>
                  </div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#2a4060;margin-bottom:10px;">
                    DUE: {dd}
                  </div>
                  <span style="font-family:'Share Tech Mono',monospace;font-size:9px;font-weight:700;
                    padding:3px 12px;border-radius:10px;letter-spacing:0.12em;
                    background:{st_bg};color:{st_c};border:1px solid {st_bo};">{st_txt}</span>
                </div>"""

            elif r.get("tickets_data"):
                rows = ""
                for t in r["tickets_data"]:
                    iss  = htmllib.escape(str(t.get("issue",""))[:50])
                    tid2 = htmllib.escape(str(t.get("ticket_id","")))
                    sts  = htmllib.escape(str(t.get("status","Open")))
                    p2   = str(t.get("priority","Low"))
                    accent = {"High":"#ff3355","Medium":"#ffaa00","Low":"#00ff88"}.get(p2,"#00ff88")
                    rows += f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                         padding:8px 0;border-bottom:1px solid rgba(0,245,255,0.05);">
                      <div>
                        <div style="font-family:'Rajdhani',sans-serif;font-size:13px;
                             font-weight:600;color:#c8d8e8;">{iss}</div>
                        <div style="font-family:'Share Tech Mono',monospace;font-size:9px;
                             color:#1a3050;margin-top:2px;letter-spacing:0.1em;">{tid2}</div>
                      </div>
                      <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                        padding:2px 8px;border-radius:8px;letter-spacing:0.08em;
                        background:rgba(0,245,255,0.06);color:#00d4e8;border:1px solid rgba(0,245,255,0.12);
                        white-space:nowrap;">{sts}</span>
                    </div>"""
                rec_html = f"""
                <div class="rec-card">
                  <div class="rec-lbl">◈ TICKET HISTORY</div>
                  {rows if rows else '<div style="font-family:Share Tech Mono,monospace;font-size:10px;color:#1a3050;padding:8px 0;letter-spacing:0.1em;">NO RECORDS FOUND</div>'}
                </div>"""

            elif r.get("plans_data"):
                pcards = ""
                for p in PLANS_LIST:
                    feats = "".join([f'<li style="font-size:10px;color:#2a4060;padding:3px 0;list-style:none;display:flex;align-items:center;gap:5px;font-family:Rajdhani,sans-serif;"><span style="font-size:8px;opacity:0.7;">◆</span>{htmllib.escape(f)}</li>' for f in p["features"][:4]])
                    pcards += f"""
                    <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(0,245,255,0.08);
                         border-radius:10px;padding:12px;text-align:left;
                         border-top:2px solid;border-image:{p['gradient']} 1;">
                      <div style="font-size:18px;margin-bottom:4px;">{p['icon']}</div>
                      <div style="font-family:'Orbitron',monospace;font-size:11px;font-weight:700;color:#c8d8e8;
                           letter-spacing:0.05em;">{htmllib.escape(p['name'])}</div>
                      <div style="font-family:'Share Tech Mono',monospace;font-size:16px;font-weight:900;
                           color:#ffaa00;margin:4px 0 8px;">{htmllib.escape(p['speed'])}</div>
                      <ul style="padding:0;">{feats}</ul>
                    </div>"""
                rec_html = f"""
                <div class="rec-card">
                  <div class="rec-lbl">◈ AVAILABLE PLANS</div>
                  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:8px;">{pcards}</div>
                </div>"""

            upd_html = ""
            if r.get("record_updated"):
                upd   = r["record_updated"]
                field = htmllib.escape(str(upd.get("field","Record")).upper())
                val   = htmllib.escape(str(upd.get("value","")))
                upd_html = f"""
                <div style="margin-top:10px;padding:10px 14px;border-radius:10px;
                     background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.15);
                     font-family:'Share Tech Mono',monospace;font-size:11px;color:#00ff88;
                     letter-spacing:0.08em;">
                  ✓ {field} → UPDATED TO "{val}"
                </div>"""

            tech_chip = (f'<span class="fc">⬡ {htmllib.escape(tech)}</span>' if tech != "Not Assigned" else "")
            tid_chip  = (f'<span class="idc">◈ {htmllib.escape(tid)}</span>' if tid else "")

            msgs_html += f"""
            <div class="row bot-row">
              <div class="av bav">⬡</div>
              <div class="acard">
                <div class="ahdr">
                  <span class="albl">FIBERISP · NEURAL AI</span>
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
                  <span class="ts">{htmllib.escape(ts)}</span>
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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;600;700;800&family=Share+Tech+Mono&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{
  background:#020408;
  font-family:'Rajdhani',sans-serif;
  height:{height}px;
  overflow:hidden;
  background-image:
    linear-gradient(rgba(0,245,255,0.012) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,255,0.012) 1px, transparent 1px);
  background-size:60px 60px;
}}
.cw{{
  height:{height}px;
  overflow-y:auto;
  padding:18px 16px;
  display:flex;
  flex-direction:column;
  gap:16px;
  scroll-behavior:smooth;
}}
.cw::-webkit-scrollbar{{width:2px;}}
.cw::-webkit-scrollbar-thumb{{background:rgba(0,245,255,0.15);border-radius:4px;}}
.row{{display:flex;align-items:flex-end;gap:10px;animation:su .3s ease both;}}
.user-row{{flex-direction:row-reverse;}}
@keyframes su{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.av{{
  width:32px;height:32px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:14px;flex-shrink:0;font-family:'Share Tech Mono',monospace;
}}
.uav{{
  background:linear-gradient(135deg,rgba(0,128,255,0.2),rgba(0,80,160,0.15));
  border:1px solid rgba(0,128,255,0.3);
  color:#0080ff;
  box-shadow:0 0 12px rgba(0,128,255,0.15);
}}
.bav{{
  background:linear-gradient(135deg,rgba(0,245,255,0.15),rgba(0,80,160,0.1));
  border:1px solid rgba(0,245,255,0.3);
  color:#00f5ff;
  box-shadow:0 0 12px rgba(0,245,255,0.15);
}}
.umsg{{display:flex;flex-direction:column;align-items:flex-end;max-width:70%;}}
.ubub{{
  background:linear-gradient(135deg,rgba(0,30,80,0.9),rgba(0,50,120,0.8));
  border:1px solid rgba(0,128,255,0.25);
  border-radius:14px 14px 4px 14px;
  padding:12px 16px;
  font-size:14px;
  line-height:1.7;
  color:#b8d4f0;
  word-break:break-word;
  box-shadow:0 4px 20px rgba(0,80,180,0.2);
  font-family:'Rajdhani',sans-serif;
  font-weight:500;
}}
.utime{{
  font-family:'Share Tech Mono',monospace;
  font-size:9px;color:#1a3050;
  margin-top:5px;letter-spacing:0.12em;
}}
.ebub{{
  max-width:74%;
  background:rgba(255,51,85,0.06);
  border:1px solid rgba(255,51,85,0.2);
  border-left:3px solid #ff3355;
  border-radius:12px;
  padding:12px 16px;
  font-size:13px;color:#ff8099;
  font-family:'Share Tech Mono',monospace;
  letter-spacing:0.05em;
}}
.acard{{
  max-width:82%;
  background:linear-gradient(150deg,rgba(4,8,20,0.97),rgba(6,12,30,0.95));
  border:1px solid rgba(0,245,255,0.12);
  border-radius:4px 14px 14px 14px;
  overflow:hidden;
  box-shadow:0 10px 40px rgba(0,0,0,0.7),0 0 30px rgba(0,245,255,0.02);
}}
.ahdr{{
  background:linear-gradient(90deg,rgba(0,245,255,0.06),transparent);
  border-bottom:1px solid rgba(0,245,255,0.07);
  padding:8px 14px;
  display:flex;align-items:center;gap:7px;
}}
.albl{{
  font-family:'Share Tech Mono',monospace;
  font-size:9px;font-weight:700;color:#1a3a5a;
  flex:1;letter-spacing:0.15em;
}}
.pbadge,.sbadge{{
  font-family:'Share Tech Mono',monospace;
  font-size:8px;font-weight:700;
  padding:2px 8px;border-radius:10px;
  letter-spacing:0.1em;text-transform:uppercase;
}}
.sbadge{{border:1px solid rgba(255,255,255,0.05);}}
.abody{{padding:14px 16px;}}
.reply{{
  font-family:'Rajdhani',sans-serif;
  font-size:14px;line-height:1.75;
  color:#8aa8c8;font-weight:400;
}}
.rec-card{{
  margin-top:12px;
  background:rgba(0,245,255,0.025);
  border:1px solid rgba(0,245,255,0.08);
  border-radius:12px;padding:13px;
}}
.rec-lbl{{
  font-family:'Share Tech Mono',monospace;
  font-size:8px;font-weight:700;
  letter-spacing:0.25em;text-transform:uppercase;
  color:#0a3050;margin-bottom:8px;
}}
.aftr{{
  padding:8px 12px;
  border-top:1px solid rgba(0,245,255,0.05);
  display:flex;gap:6px;flex-wrap:wrap;align-items:center;
}}
.cc,.fc,.idc,.ts{{
  font-family:'Share Tech Mono',monospace;
  font-size:9px;padding:2px 8px;border-radius:6px;
  letter-spacing:0.08em;
}}
.cc{{background:rgba(0,245,255,0.04);color:#1a3a5a;border:1px solid rgba(0,245,255,0.08);}}
.fc{{background:rgba(191,0,255,0.06);color:#8040c0;border:1px solid rgba(191,0,255,0.12);}}
.idc{{background:rgba(0,245,255,0.05);color:#006080;border:1px solid rgba(0,245,255,0.1);}}
.ts{{background:transparent;color:#0a2030;border:none;}}
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
#  TOP BAR — all screens except welcome
# ══════════════════════════════════════════════
if st.session_state.screen != "welcome":
    now_str = datetime.datetime.now().strftime("%Y.%m.%d · %H:%M")
    st.markdown(f"""
    <div class="topbar-cyber">
      <div class="topbar-brand">
        <div class="topbar-icon-hex">⚡</div>
        <div>
          <div class="topbar-name">FIBER<span style="color:var(--neon-cyan);">ISP</span></div>
          <div class="topbar-sub">NEURAL SUPPORT SYSTEM · v4.2</div>
        </div>
      </div>
      <div class="topbar-right">
        <div class="sys-status">
          <div class="status-led"></div>
          SYS ONLINE
        </div>
        <div class="topbar-ticker">{now_str}</div>
      </div>
    </div>
    <div class="data-stream-bar"></div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: WELCOME
# ══════════════════════════════════════════════
if st.session_state.screen == "welcome":

    st.markdown('<div class="data-stream-bar"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-main">
      <div class="hero-eyebrow">PAKISTAN'S FASTEST FIBER NETWORK</div>

      <div class="hero-logo-container">
        <div class="hero-logo-ring"></div>
        <div class="hero-logo-ring-2"></div>
        <div class="hero-logo-hex">⚡</div>
      </div>

      <div class="hero-title">FiberISP</div>
      <div class="hero-subtitle">Ultra-Fast Fiber · Nationwide Coverage · AI-Powered Support</div>

      <div class="hero-stats">
        <div class="hero-stat">
          <span class="hero-stat-num">500</span>
          <span class="hero-stat-lbl">Mbps Max Speed</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat-num">24/7</span>
          <span class="hero-stat-lbl">Neural AI Support</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat-num">99.9%</span>
          <span class="hero-stat-lbl">Uptime SLA</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat-num">60+</span>
          <span class="hero-stat-lbl">Cities Covered</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label">
      <span class="section-label-text">SELECT ACCESS MODE</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown("""
        <div class="choice-card" style="--card-accent:linear-gradient(90deg,#00f5ff,#0080ff);
             --card-accent-color:#00f5ff;--card-glow:rgba(0,245,255,0.12);">
          <div class="choice-card-inner">
        """, unsafe_allow_html=True)
        st.markdown('<div class="icon-card-btn cyan" style="display:flex;justify-content:center;">', unsafe_allow_html=True)
        if st.button("◈", key="btn_existing"):
            st.session_state.screen = "customer_login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card-title">Existing Customer</div>
            <div class="card-desc">Login with your registered phone number and access your full support dashboard.</div>
            <div class="card-features">
              <div class="card-feature"><div class="feature-dot dot-cyan"></div>REAL-TIME TICKET TRACKING</div>
              <div class="card-feature"><div class="feature-dot dot-cyan"></div>AI DIAGNOSTIC SUPPORT</div>
              <div class="card-feature"><div class="feature-dot dot-cyan"></div>BILLING MANAGEMENT</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="choice-card" style="--card-accent:linear-gradient(90deg,#00ff88,#00c864);
             --card-accent-color:#00ff88;--card-glow:rgba(0,255,136,0.1);">
          <span class="card-badge badge-new">NEW</span>
          <div class="choice-card-inner">
        """, unsafe_allow_html=True)
        st.markdown('<div class="icon-card-btn green" style="display:flex;justify-content:center;">', unsafe_allow_html=True)
        if st.button("✦", key="btn_new"):
            st.session_state.screen = "new_customer_register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card-title">New Customer</div>
            <div class="card-desc">Register your account and get connected with ultra-fast fiber internet today.</div>
            <div class="card-features">
              <div class="card-feature"><div class="feature-dot dot-green"></div>INSTANT AI ONBOARDING</div>
              <div class="card-feature"><div class="feature-dot dot-green"></div>PLAN SELECTION GUIDE</div>
              <div class="card-feature"><div class="feature-dot dot-green"></div>24HR INSTALLATION SLA</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="choice-card" style="--card-accent:linear-gradient(90deg,#bf00ff,#6400c8);
             --card-accent-color:#bf00ff;--card-glow:rgba(191,0,255,0.1);">
          <span class="card-badge badge-secure">SECURE</span>
          <div class="choice-card-inner">
        """, unsafe_allow_html=True)
        st.markdown('<div class="icon-card-btn purple" style="display:flex;justify-content:center;">', unsafe_allow_html=True)
        if st.button("⬡", key="btn_admin"):
            st.session_state.screen = "admin_login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card-title">Admin Panel</div>
            <div class="card-desc">Manage customers, tickets, network outages, and system operations.</div>
            <div class="card-features">
              <div class="card-feature"><div class="feature-dot dot-purple"></div>NETWORK OPERATIONS</div>
              <div class="card-feature"><div class="feature-dot dot-purple"></div>CUSTOMER DATABASE</div>
              <div class="card-feature"><div class="feature-dot dot-purple"></div>TICKET MANAGEMENT</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: CUSTOMER LOGIN
# ══════════════════════════════════════════════
elif st.session_state.screen == "customer_login":

    # Animated background orbs
    st.markdown("""
    <style>
    @keyframes orb-rise{
      0%{transform:translate(0,0) scale(1);opacity:0;}
      10%{opacity:.5;}90%{opacity:.2;}
      100%{transform:translate(var(--tx),var(--ty)) scale(var(--ts));opacity:0;}
    }
    .orb{position:fixed;border-radius:50%;pointer-events:none;z-index:0;filter:blur(3px);
         animation:orb-rise var(--dur) ease-in infinite var(--delay);}
    .o1{width:100px;height:100px;bottom:5%;left:8%;
        background:radial-gradient(circle,rgba(0,245,255,0.3),transparent);
        --tx:80px;--ty:-500px;--ts:1.4;--dur:8s;--delay:0s;}
    .o2{width:70px;height:70px;bottom:12%;left:60%;
        background:radial-gradient(circle,rgba(0,128,255,0.35),transparent);
        --tx:-60px;--ty:-600px;--ts:.8;--dur:10s;--delay:2s;}
    .o3{width:50px;height:50px;bottom:3%;left:35%;
        background:radial-gradient(circle,rgba(0,245,255,0.4),transparent);
        --tx:40px;--ty:-450px;--ts:1.1;--dur:7s;--delay:4s;}
    .o4{width:80px;height:80px;bottom:20%;left:85%;
        background:radial-gradient(circle,rgba(191,0,255,0.25),transparent);
        --tx:-100px;--ty:-400px;--ts:1.2;--dur:9s;--delay:1s;}
    .o5{width:40px;height:40px;bottom:8%;left:20%;
        background:radial-gradient(circle,rgba(0,255,136,0.3),transparent);
        --tx:20px;--ty:-550px;--ts:.9;--dur:11s;--delay:5s;}
    .o6{width:60px;height:60px;bottom:30%;left:48%;
        background:radial-gradient(circle,rgba(0,245,255,0.25),transparent);
        --tx:-80px;--ty:-480px;--ts:1.3;--dur:8.5s;--delay:2.5s;}
    </style>
    <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
    <div class="orb o4"></div><div class="orb o5"></div><div class="orb o6"></div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown('<div class="gc-icon gc-icon-cyan" style="text-align:center;">📡</div>', unsafe_allow_html=True)
        st.markdown('<div class="gc-title">SYSTEM ACCESS</div>', unsafe_allow_html=True)
        st.markdown('<div class="gc-sub">Enter your registered phone number to authenticate and access the support neural network.</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="cap-tags">
          <span class="cap-tag tag-c">⚡ INSTANT ACCESS</span>
          <span class="cap-tag tag-g">◈ AI DIAGNOSTICS</span>
          <span class="cap-tag tag-a">🔒 ENCRYPTED</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="gc-divider">
          <div class="gc-divider-line"></div>
          <div class="gc-divider-label">PHONE NUMBER</div>
          <div class="gc-divider-line"></div>
        </div>""", unsafe_allow_html=True)

        phone = st.text_input("", placeholder="03001234567", key="login_phone",
                              label_visibility="collapsed")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        bc1, bc2 = st.columns([2, 1])
        with bc1:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            login_clicked = st.button("AUTHENTICATE →", key="do_login", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with bc2:
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            back_clicked = st.button("← BACK", key="back_login", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if login_clicked:
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
                    st.error("⚠ Phone number not found. Please register as a new customer.")
            else:
                st.error("⚠ Phone number required.")

        if back_clicked:
            st.session_state.screen = "welcome"
            st.rerun()

        st.markdown("""
        <div class="demo-hint">
          DEMO ACCESS: <span class="demo-code">03001234567</span> or <span class="demo-code">03146532146</span>
        </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: NEW CUSTOMER REGISTER
# ══════════════════════════════════════════════
elif st.session_state.screen == "new_customer_register":

    st.markdown("""
    <style>
    @keyframes orb-rise2{
      0%{transform:translate(0,0) scale(1);opacity:0;}
      10%{opacity:.45;}90%{opacity:.18;}
      100%{transform:translate(var(--tx2),var(--ty2)) scale(var(--ts2));opacity:0;}
    }
    .orb2{position:fixed;border-radius:50%;pointer-events:none;z-index:0;filter:blur(3px);
          animation:orb-rise2 var(--dur2) ease-in infinite var(--del2);}
    .r1{width:90px;height:90px;bottom:6%;left:12%;
        background:radial-gradient(circle,rgba(0,255,136,0.3),transparent);
        --tx2:-70px;--ty2:-500px;--ts2:1.3;--dur2:9s;--del2:0s;}
    .r2{width:65px;height:65px;bottom:18%;left:65%;
        background:radial-gradient(circle,rgba(191,0,255,0.32),transparent);
        --tx2:60px;--ty2:-550px;--ts2:.9;--dur2:11s;--del2:1.5s;}
    .r3{width:45px;height:45px;bottom:4%;left:40%;
        background:radial-gradient(circle,rgba(255,170,0,0.3),transparent);
        --tx2:30px;--ty2:-430px;--ts2:1.1;--dur2:7s;--del2:3s;}
    .r4{width:75px;height:75px;bottom:25%;left:82%;
        background:radial-gradient(circle,rgba(0,245,255,0.25),transparent);
        --tx2:-90px;--ty2:-460px;--ts2:1.2;--dur2:8s;--del2:.7s;}
    </style>
    <div class="orb2 r1"></div><div class="orb2 r2"></div>
    <div class="orb2 r3"></div><div class="orb2 r4"></div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="glass-card" style="border-color:rgba(0,255,136,0.12);border-top-color:rgba(0,255,136,0.4);">', unsafe_allow_html=True)

        st.markdown('<div class="gc-icon gc-icon-green" style="text-align:center;">✦</div>', unsafe_allow_html=True)
        st.markdown('<div class="gc-title" style="background:linear-gradient(135deg,#e8f4ff,#00ff88);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">NEW CONNECTION</div>', unsafe_allow_html=True)
        st.markdown('<div class="gc-sub">Register your account to join FiberISP\'s neural support network and get connected.</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="cap-tags">
          <span class="cap-tag tag-g">🚀 FAST SETUP</span>
          <span class="cap-tag tag-c">📡 60+ CITIES</span>
          <span class="cap-tag tag-p">💎 PREMIUM PLANS</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="gc-divider" style="--gc-color:rgba(0,255,136,0.2);">
          <div class="gc-divider-line" style="background:linear-gradient(90deg,transparent,rgba(0,255,136,0.2),transparent);"></div>
          <div class="gc-divider-label" style="color:var(--neon-green);">REGISTRATION DATA</div>
          <div class="gc-divider-line" style="background:linear-gradient(90deg,transparent,rgba(0,255,136,0.2),transparent);"></div>
        </div>""", unsafe_allow_html=True)

        with st.form("reg_form"):
            nc1, nc2 = st.columns(2)
            with nc1:
                name = st.text_input("Full Name", placeholder="Muhammad Ali")
            with nc2:
                phone = st.text_input("Phone Number", placeholder="03001234567")

            area = st.selectbox("Service Area", PAKISTAN_LOCATIONS)

            st.markdown("""
            <div class="conn-info">
              <span style="font-size:20px;flex-shrink:0;">◈</span>
              <span>Our team will contact you within <strong>24 hours</strong> to confirm and schedule installation at your location.</span>
            </div>""", unsafe_allow_html=True)

            submitted = st.form_submit_button("✦  INITIALIZE ACCOUNT  →", use_container_width=True)

            if submitted:
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
                        st.error("⚠ Phone number already registered. Please use the login screen.")
                else:
                    st.error("⚠ All fields are required.")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← BACK TO HOME", key="back_reg", use_container_width=True):
            st.session_state.screen = "welcome"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: CUSTOMER DASHBOARD
# ══════════════════════════════════════════════
elif st.session_state.screen == "customer_dashboard":
    cust  = st.session_state.customer
    phone = st.session_state.phone

    outage_html = ""
    if st.session_state.network_status == "DOWN":
        outage_html = f"""
        <div class="outage-alert">
          <span style="font-size:18px;">⚠</span>
          <span>NETWORK OUTAGE DETECTED IN {htmllib.escape(cust["area"].upper())} — ETA: {htmllib.escape(st.session_state.fix_time)}</span>
        </div>"""

    net_color = "var(--neon-red)" if st.session_state.network_status == "DOWN" else "var(--neon-green)"
    net_icon  = "▼" if st.session_state.network_status == "DOWN" else "▲"

    st.markdown(f"""
    <div class="profile-banner">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;">
        <div class="profile-name">◈ {htmllib.escape(cust["name"])}</div>
        <div style="display:flex;align-items:center;gap:8px;
             font-family:'Share Tech Mono',monospace;font-size:10px;
             color:{net_color};letter-spacing:0.2em;">
          {net_icon} NET {htmllib.escape(st.session_state.network_status)}
        </div>
      </div>
      <div class="profile-chips">
        <div class="profile-chip">📱<span>{htmllib.escape(phone)}</span></div>
        <div class="profile-chip">◈<span>{htmllib.escape(cust["package"])}</span></div>
        <div class="profile-chip">📍<span>{htmllib.escape(cust["area"])}</span></div>
        <div class="profile-chip">💳<span>{htmllib.escape(st.session_state.bill_info)}</span></div>
      </div>
      {outage_html}
    </div>""", unsafe_allow_html=True)

    col_out, _ = st.columns([1, 9])
    with col_out:
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("⬡ EXIT", key="logout"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "⬡  AI Support",
        "◈  New Connection",
        "▲  Billing & Tickets",
        "✦  Upgrade Plan",
    ])

    with tab1:
        st.markdown("""
        <div class="chat-head">
          <div class="chat-head-icon">⬡</div>
          <div style="flex:1;">
            <div class="chat-head-name">FIBERISP NEURAL AI</div>
            <div class="chat-head-desc">
              Ask about your bill, diagnose connectivity issues, or say
              <em style="color:#1a3a5a;">"change my name to Ahmed"</em> or
              <em style="color:#1a3a5a;">"show my tickets"</em>
            </div>
          </div>
          <div class="ai-live">
            <div class="status-led"></div>LIVE
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hdr">QUICK COMMANDS</div>', unsafe_allow_html=True)

        quick_topics = [
            ("▼","Slow internet speed"),("◈","WiFi not working"),
            ("⬡","No internet connection"),("💳","Show my bill"),
            ("✦","Upgrade my plan"),("↻","How to restart router"),
            ("▲","Weak WiFi signal"),("⬢","Request a technician"),
            ("◈","Show my tickets"),("▦","Available plans"),
        ]
        cols = st.columns(5)
        for i, (icon, label) in enumerate(quick_topics):
            with cols[i % 5]:
                if st.button(f"{icon} {label}", key=f"qt_{i}", use_container_width=True):
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.chat.append({"role":"user","text":label,"time":now})
                    with st.spinner("Neural AI processing..."):
                        result, err = process_ticket(
                            None, phone, st.session_state.customer_type,
                            cust["name"], cust["package"], cust["area"],
                            st.session_state.network_status, st.session_state.fix_time,
                            st.session_state.bill_info, st.session_state.history_text, label,
                        )
                    _handle_result(result, err, phone)
                    st.rerun()

        st.markdown('<div class="sec-hdr">CONVERSATION STREAM</div>', unsafe_allow_html=True)
        render_chat(st.session_state.chat)

        user_msg = st.chat_input("Transmit message to Neural AI...")
        if user_msg and user_msg.strip():
            now = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state.chat.append({"role":"user","text":user_msg.strip(),"time":now})
            with st.spinner("Neural AI processing..."):
                result, err = process_ticket(
                    None, phone, st.session_state.customer_type,
                    cust["name"], cust["package"], cust["area"],
                    st.session_state.network_status, st.session_state.fix_time,
                    st.session_state.bill_info, st.session_state.history_text, user_msg.strip(),
                )
            _handle_result(result, err, phone)
            st.rerun()

        if st.session_state.chat:
            if st.button("⬡ PURGE CONVERSATION", key="clear_chat"):
                st.session_state.chat = []
                st.rerun()

    with tab2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(0,245,255,0.04),rgba(0,80,160,0.03));
             border:1px solid rgba(0,245,255,0.12);border-top:2px solid rgba(0,245,255,0.3);
             border-radius:18px;padding:24px 28px;margin-bottom:28px;">
          <div style="font-family:'Orbitron',monospace;font-size:18px;font-weight:700;
               color:var(--text-primary);letter-spacing:0.05em;margin-bottom:6px;">
            ◈ REQUEST NEW CONNECTION
          </div>
          <div style="font-size:14px;color:var(--text-muted);font-family:'Rajdhani',sans-serif;line-height:1.6;">
            Submit your installation request and our team will contact you within 24 hours.
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hdr">SELECT PLAN</div>', unsafe_allow_html=True)
        pcols = st.columns(4)
        for i, p in enumerate(PLANS_LIST):
            with pcols[i]:
                sel_cls = "current-plan" if st.session_state.selected_plan == p["name"] else ""
                features_html = "".join([f'<li>{htmllib.escape(f)}</li>' for f in p["features"][:4]])
                st.markdown(f"""
                <div class="plan-card {sel_cls}"
                     style="--plan-gradient:{p['gradient']};--plan-glow:{p['glow']};">
                  <div class="plan-icon">{p['icon']}</div>
                  <div class="plan-name">{htmllib.escape(p['name'])}</div>
                  <div class="plan-speed">{htmllib.escape(p['speed'])}</div>
                  <div class="plan-price">{htmllib.escape(p['price'])}</div>
                  <div class="plan-period">/MONTH</div>
                  <ul class="plan-features">{features_html}</ul>
                </div>""", unsafe_allow_html=True)
                if st.button("SELECT", key=f"plan_{i}", use_container_width=True):
                    st.session_state.selected_plan = p["name"]
                    st.rerun()

        if st.session_state.selected_plan:
            st.markdown(
                f"<div style='background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.15);"
                f"border-left:3px solid var(--neon-green);border-radius:10px;padding:12px 18px;"
                f"font-family:Share Tech Mono,monospace;font-size:11px;color:var(--neon-green);"
                f"letter-spacing:0.1em;margin:12px 0;'>"
                f"✓ SELECTED: {htmllib.escape(st.session_state.selected_plan)}</div>",
                unsafe_allow_html=True
            )

        st.markdown('<div class="sec-hdr">INSTALLATION DETAILS</div>', unsafe_allow_html=True)
        with st.form("nc_form", clear_on_submit=True):
            nc1, nc2 = st.columns(2)
            with nc1: nc_name  = st.text_input("Full Name", value=cust["name"])
            with nc2: nc_phone = st.text_input("Phone Number", value=phone)
            nc_area = st.selectbox(
                "Installation Area", PAKISTAN_LOCATIONS,
                index=PAKISTAN_LOCATIONS.index(cust["area"]) if cust["area"] in PAKISTAN_LOCATIONS else 0
            )
            if st.form_submit_button("◈  SUBMIT REQUEST  →", use_container_width=True):
                if nc_name.strip() and nc_phone.strip() and st.session_state.selected_plan:
                    db().execute(
                        "INSERT INTO new_connection_requests(name,phone,area,package,created_at) VALUES(?,?,?,?,?)",
                        (nc_name.strip(), nc_phone.strip(), nc_area,
                         st.session_state.selected_plan,
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    conn.commit()
                    st.success(f"✓ Request transmitted. We'll contact {nc_phone.strip()} within 24 hours.")
                    st.session_state.selected_plan = ""
                elif not st.session_state.selected_plan:
                    st.error("⚠ Select a plan to proceed.")
                else:
                    st.error("⚠ All fields are required.")

    with tab3:
        c = db()
        c.execute("SELECT amount,due_date FROM bills WHERE customer_phone=?", (phone,))
        bill_row = c.fetchone()

        if bill_row:
            amount, due_date = bill_row
            try:    overdue = datetime.date.today() > datetime.date.fromisoformat(due_date)
            except: overdue = False
            status_html = (
                '<div class="status-due">⚠ PAYMENT OVERDUE</div>'
                if overdue else
                '<div class="status-ok">✓ ACCOUNT CURRENT</div>'
            )
            st.markdown(f"""
            <div class="bill-panel">
              <div class="bill-label">CURRENT BILLING CYCLE</div>
              <div class="bill-amount">
                <span class="bill-currency">PKR</span>{amount:,}
              </div>
              <div class="bill-due">DUE DATE · {htmllib.escape(due_date)}</div>
              {status_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("◈ No billing record on file.")

        st.markdown('<div class="sec-hdr">SUPPORT TICKETS</div>', unsafe_allow_html=True)
        c.execute(
            "SELECT ticket_id,issue,priority,status,created_at FROM tickets "
            "WHERE customer_phone=? ORDER BY created_at DESC LIMIT 5", (phone,)
        )
        tickets = c.fetchall()
        if tickets:
            for tid, issue, priority, status, created in tickets:
                card_cls = "resolved" if status == "Resolved" else priority.lower()
                st.markdown(f"""
                <div class="ticket-node {card_cls}">
                  <div class="ticket-header">
                    <span class="ticket-id">{htmllib.escape(tid)}</span>
                    <span class="ticket-status-badge {'s-resolved' if status=='Resolved' else 's-open'}">{htmllib.escape(status)}</span>
                  </div>
                  <div class="ticket-title">{htmllib.escape(issue)}</div>
                  <div class="ticket-tags">
                    {pri_tag(priority)}
                    <span class="t-tag t-info">◈ {htmllib.escape(created)}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("◈ No support tickets. Use AI Chat to create one.")

    with tab4:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(0,245,255,0.04),rgba(0,80,160,0.03));
             border:1px solid rgba(0,245,255,0.12);border-top:2px solid rgba(0,245,255,0.3);
             border-radius:18px;padding:24px 28px;margin-bottom:28px;">
          <div style="font-family:'Orbitron',monospace;font-size:18px;font-weight:700;
               color:var(--text-primary);letter-spacing:0.05em;margin-bottom:6px;">
            ✦ PLAN UPGRADE CENTER
          </div>
          <div style="font-size:14px;color:var(--text-muted);font-family:'Rajdhani',sans-serif;">
            CURRENT PACKAGE: <span style="font-family:'Orbitron',monospace;font-size:13px;
            color:var(--neon-cyan);font-weight:700;">{htmllib.escape(cust["package"])}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        up_cols = st.columns(4)
        for i, p in enumerate(PLANS_LIST):
            with up_cols[i]:
                is_cur = p["name"].lower() in cust["package"].lower()
                cur_badge = '<div class="current-badge">✓ ACTIVE PLAN</div>' if is_cur else ""
                features_html = "".join([f'<li>{htmllib.escape(f)}</li>' for f in p["features"]])
                st.markdown(f"""
                <div class="plan-card {'current-plan' if is_cur else ''}"
                     style="--plan-gradient:{p['gradient']};--plan-glow:{p['glow']};">
                  <div class="plan-icon">{p['icon']}</div>
                  <div class="plan-name">{htmllib.escape(p['name'])}</div>
                  <div class="plan-speed">{htmllib.escape(p['speed'])}</div>
                  <div class="plan-price">{htmllib.escape(p['price'])}</div>
                  <div class="plan-period">/MONTH</div>
                  <ul class="plan-features">{features_html}</ul>
                  {cur_badge}
                </div>""", unsafe_allow_html=True)
                if not is_cur:
                    if st.button(f"✦ UPGRADE", key=f"up_{i}", use_container_width=True):
                        msg = f"I want to upgrade my plan from {cust['package']} to {p['name']} ({p['speed']}, {p['price']}/month)"
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        st.session_state.chat.append({"role":"user","text":msg,"time":now})
                        with st.spinner("Processing upgrade request..."):
                            result, err = process_ticket(
                                None, phone, st.session_state.customer_type,
                                cust["name"], cust["package"], cust["area"],
                                st.session_state.network_status, st.session_state.fix_time,
                                st.session_state.bill_info, st.session_state.history_text, msg,
                            )
                        _handle_result(result, err, phone)
                        st.success(f"✓ Upgrade request to '{p['name']}' submitted.")
                        st.rerun()


# ══════════════════════════════════════════════
#  SCREEN: ADMIN LOGIN
# ══════════════════════════════════════════════
elif st.session_state.screen == "admin_login":
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("""
        <div class="glass-card" style="border-color:rgba(191,0,255,0.12);
             box-shadow:0 40px 100px rgba(0,0,0,0.8),0 0 80px rgba(191,0,255,0.04);">
          <div style="text-align:center;">
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gc-icon" style="background:linear-gradient(135deg,rgba(191,0,255,0.15),rgba(100,0,200,0.1));
             border:1px solid rgba(191,0,255,0.3);box-shadow:0 0 30px rgba(191,0,255,0.2);
             margin:0 auto 24px;">🔐</div>
        <div class="gc-title" style="background:linear-gradient(135deg,#e8f4ff,#bf00ff);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">ADMIN ACCESS</div>
        <div class="gc-sub">Restricted access. Authenticate with administrator credentials to proceed.</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gc-divider">
          <div class="gc-divider-line" style="background:linear-gradient(90deg,transparent,rgba(191,0,255,0.2),transparent);"></div>
          <div class="gc-divider-label" style="color:var(--neon-purple);">CREDENTIALS</div>
          <div class="gc-divider-line" style="background:linear-gradient(90deg,transparent,rgba(191,0,255,0.2),transparent);"></div>
        </div>
        """, unsafe_allow_html=True)

        pwd = st.text_input("Admin Password", type="password", placeholder="••••••••••")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        bc1, bc2 = st.columns([2, 1])
        with bc1:
            st.markdown('<div class="primary-btn" style="--p-c1:var(--neon-purple);--p-c2:#6400c8;">', unsafe_allow_html=True)
            go = st.button("AUTHENTICATE →", key="admin_go", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with bc2:
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            bk = st.button("← BACK", key="back_admin", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if go:
            if pwd == "admin123":
                st.session_state.screen = "admin"
                st.rerun()
            else:
                st.error("⚠ Access denied. Invalid credentials.")
        if bk:
            st.session_state.screen = "welcome"
            st.rerun()

        st.markdown("""
        <div class="demo-hint">DEMO: <span class="demo-code">admin123</span></div>
        """, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SCREEN: ADMIN DASHBOARD
# ══════════════════════════════════════════════
elif st.session_state.screen == "admin":
    c = db()
    c.execute("SELECT COUNT(*) FROM customers");               total_cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets");                 total_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'"); open_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE priority='High' AND status='Open'"); high_tick = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM new_connection_requests"); conn_reqs = c.fetchone()[0]

    col_out, _ = st.columns([1, 9])
    with col_out:
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("⬡ EXIT", key="admin_logout"):
            st.session_state.screen = "welcome"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-node" style="--metric-bar:linear-gradient(90deg,transparent,var(--neon-cyan),transparent);">
        <div class="metric-num c">{total_cust}</div>
        <div class="metric-lbl">TOTAL CUSTOMERS</div>
      </div>
      <div class="metric-node" style="--metric-bar:linear-gradient(90deg,transparent,#6080c0,transparent);">
        <div class="metric-num">{total_tick}</div>
        <div class="metric-lbl">TOTAL TICKETS</div>
      </div>
      <div class="metric-node" style="--metric-bar:linear-gradient(90deg,transparent,var(--neon-amber),transparent);">
        <div class="metric-num a">{open_tick}</div>
        <div class="metric-lbl">OPEN TICKETS</div>
      </div>
      <div class="metric-node" style="--metric-bar:linear-gradient(90deg,transparent,var(--neon-red),transparent);">
        <div class="metric-num r">{high_tick}</div>
        <div class="metric-lbl">HIGH PRIORITY</div>
      </div>
    </div>""", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs([
        "◈ Tickets", "⬡ Customers", "▲ Outages", "✦ Requests", "⬢ Manage",
    ])

    with t1:
        st.markdown('<div class="sec-hdr">ALL SUPPORT TICKETS</div>', unsafe_allow_html=True)
        c.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        for row in c.fetchall():
            tid, tphone, issue, priority, sentiment, tech, status, created = row
            card_cls = "resolved" if status == "Resolved" else priority.lower()
            st.markdown(f"""
            <div class="ticket-node {card_cls}">
              <div class="ticket-header">
                <div style="display:flex;gap:12px;align-items:center;">
                  <span class="ticket-id">{htmllib.escape(tid)}</span>
                  <span class="ticket-id">📱 {htmllib.escape(tphone)}</span>
                </div>
                <span class="ticket-status-badge {'s-resolved' if status=='Resolved' else 's-open'}">{htmllib.escape(status)}</span>
              </div>
              <div class="ticket-title">{htmllib.escape(issue)}</div>
              <div class="ticket-tags">
                {pri_tag(priority)} {sent_tag(sentiment)}
                <span class="t-tag t-info">⬡ {htmllib.escape(tech)}</span>
                <span class="t-tag t-info">◈ {htmllib.escape(created)}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="sec-hdr">REGISTERED CUSTOMERS</div>', unsafe_allow_html=True)
        c.execute("SELECT name,phone,package,area FROM customers")
        rows = c.fetchall()
        if rows:
            import pandas as pd
            st.dataframe(
                pd.DataFrame(rows, columns=["Name","Phone","Package","Area"]),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No customer records.")

    with t3:
        st.markdown('<div class="sec-hdr">NETWORK STATUS</div>', unsafe_allow_html=True)
        c.execute("SELECT * FROM outages")
        for area_n, status_n, fix_n in c.fetchall():
            accent = "var(--neon-red)" if status_n == "DOWN" else "var(--neon-green)"
            st.markdown(f"""
            <div class="ticket-node {'high' if status_n=='DOWN' else 'low'}">
              <div class="ticket-header">
                <div>
                  <div class="ticket-title" style="font-size:14px;">📍 {htmllib.escape(area_n)}</div>
                  <span class="ticket-id">ETA · {htmllib.escape(fix_n)}</span>
                </div>
                <span style="font-family:'Share Tech Mono',monospace;font-size:10px;font-weight:700;
                  padding:4px 14px;border-radius:10px;letter-spacing:0.15em;
                  color:{accent};background:transparent;border:1px solid {accent};opacity:0.8;">
                  {htmllib.escape(status_n)}
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hdr">ADD / UPDATE OUTAGE</div>', unsafe_allow_html=True)
        with st.form("add_outage"):
            oa = st.text_input("Area", placeholder="Karachi - DHA")
            os = st.selectbox("Status", ["DOWN","ACTIVE"])
            of = st.text_input("Expected Fix Time", placeholder="3 Hours")
            if st.form_submit_button("◈  SAVE OUTAGE  →", use_container_width=True):
                db().execute(
                    "INSERT OR REPLACE INTO outages(area,status,expected_fix_time) VALUES(?,?,?)",
                    (oa, os, of)
                )
                conn.commit()
                st.success(f"✓ Outage record saved for {oa}.")
                st.rerun()

    with t4:
        st.markdown('<div class="sec-hdr">NEW CONNECTION REQUESTS</div>', unsafe_allow_html=True)
        c.execute("SELECT name,phone,area,package,created_at FROM new_connection_requests ORDER BY created_at DESC")
        rows = c.fetchall()
        if rows:
            import pandas as pd
            st.dataframe(
                pd.DataFrame(rows, columns=["Name","Phone","Area","Package","Requested At"]),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("◈ No pending requests.")

    with t5:
        st.markdown('<div class="sec-hdr">RESOLVE TICKET</div>', unsafe_allow_html=True)
        with st.form("resolve_form"):
            tid_input = st.text_input("Ticket ID", placeholder="FIB-2026-XXXX")
            if st.form_submit_button("✓  MARK RESOLVED  →", use_container_width=True):
                db().execute("UPDATE tickets SET status='Resolved' WHERE ticket_id=?", (tid_input,))
                conn.commit()
                st.success(f"✓ Ticket {tid_input} resolved.")
                st.rerun()

        st.markdown('<div class="sec-hdr">API CONFIGURATION</div>', unsafe_allow_html=True)
        new_key = st.text_input("Groq API Key", value=st.session_state.api_key, type="password")
        if st.button("◈  UPDATE KEY  →"):
            st.session_state.api_key = new_key
            st.success("✓ API key updated.")
