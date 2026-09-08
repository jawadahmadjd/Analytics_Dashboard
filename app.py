"""
National Bonds Corporation - AI Product Management Transformation
Initiative 3: Agentic Product Intelligence & Early Warning System Prototype
Calibrated with Official H1 2026 Executive Presentation Ground Truth (58 SVG Slides)
Includes: JD - Product & Data Intelligence Copilot (Bottom-Right Circular Chat)
Author: Jawad Ahmad | Product AI Solutions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import importlib
import jd_engine
importlib.reload(jd_engine)
from jd_engine import JDAgent

import frontline_view
importlib.reload(frontline_view)
from frontline_view import render_frontline_portal

import executive_views
importlib.reload(executive_views)
from executive_views import render_executive_alert_banner, render_multi_agent_trace, render_biweekly_report_tab, dispatch_alert_memo

import pdf_generator
importlib.reload(pdf_generator)
from pdf_generator import ExecutivePDFGenerator

import powerbi_analytics_hub
importlib.reload(powerbi_analytics_hub)
from powerbi_analytics_hub import render_powerbi_studio

# Page Configuration
st.set_page_config(
    page_title="National Bonds | Executive Intelligence & Early Warning System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Executive Cockpit & Floating JD Chatbot
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* THEME-AWARE BASE TOKENS */
    :root {
        --bg-main: #f8fafc;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --card-bg: #ffffff;
        --card-border: #e2e8f0;
        --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        --brand-blue: #0284c7;
        --brand-cyan: #0ea5e9;
        --brand-navy: #0f172a;
        --accent-gold: #f59e0b;
        --accent-emerald: #10b981;
        --accent-rose: #f43f5e;
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-main: #0b0f19;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --card-bg: #131b2e;
            --card-border: #1e293b;
            --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
        }
    }

    /* ELIMINATE ALL TOP WHITESPACE & FIX SIDEBAR EXPAND/COLLAPSE POSITION */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
        pointer-events: none !important;
        z-index: 999 !important;
    }
    
    header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] button,
    div[data-testid="stSidebarCollapsedControl"] {
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        pointer-events: auto !important;
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: var(--text-primary, #0f172a) !important;
        background-color: var(--card-bg, #ffffff) !important;
        border: 1px solid var(--card-border, #e2e8f0) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
        z-index: 999999 !important;
    }
    
    header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"] svg,
    button[data-testid="stSidebarCollapsedControl"] svg {
        display: block !important;
        fill: currentColor !important;
    }
    
    .main .block-container,
    div[data-testid="stAppViewBlockContainer"],
    div.block-container {
        padding-top: 0.2rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 98% !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0.5rem !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* APP HEADER */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 0 12px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 14px;
    }
    
    .header-title-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-logo-badge {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        font-size: 26px;
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        box-shadow: 0 6px 14px -4px rgba(2, 132, 199, 0.35);
    }
    
    .header-title {
        color: var(--text-primary) !important;
        font-size: 23px !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    .header-subtitle {
        color: var(--text-muted) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        margin: 2px 0 0 0 !important;
    }

    /* EXECUTIVE AUM TOP BANNER - UNIVERSAL THEME-AWARE */
    .aum-banner {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 14px;
        padding: 16px 22px;
        margin-bottom: 18px;
        display: grid;
        grid-template-columns: 1.4fr 1fr 1fr 1fr;
        gap: 16px;
        box-shadow: var(--card-shadow) !important;
        position: relative;
        overflow: hidden;
    }
    
    .aum-banner::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0284c7, #38bdf8, #10b981, #f59e0b);
    }
    
    .aum-stat-item {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .aum-label {
        font-size: 11px;
        font-weight: 700;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .aum-value {
        font-size: 22px;
        font-weight: 800;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .aum-subtext {
        font-size: 12px;
        font-weight: 600;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--text-secondary) !important;
    }
    
    .badge-success-chip {
        background: rgba(16, 185, 129, 0.12) !important;
        color: #059669 !important;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    
    @media (prefers-color-scheme: dark) {
        .badge-success-chip {
            color: #34d399 !important;
        }
    }

    /* EXECUTIVE KPI CARDS */
    .kpi-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: var(--card-shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -4px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .kpi-card-title {
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-muted);
    }
    
    .kpi-card-icon {
        font-size: 16px;
        opacity: 0.85;
    }
    
    .kpi-card-value {
        font-size: 26px;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    
    .kpi-card-footer {
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 6px;
        padding-top: 6px;
        border-top: 1px solid var(--card-border);
    }

    /* EARLY WARNING STATUS BADGES */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    
    .status-breach {
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.12);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-healthy {
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* INSTITUTIONAL WORKFLOW STEPPER RIBBON */
    .workflow-stepper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--card-bg, #ffffff);
        border: 1px solid var(--card-border, #e2e8f0);
        border-radius: 12px;
        padding: 10px 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
    }
    
    .step-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        font-weight: 700;
        color: var(--text-muted, #64748b);
        letter-spacing: 0.02em;
    }
    
    .step-item.step-active {
        color: #0284c7;
    }
    
    .step-num {
        background: rgba(2, 132, 199, 0.1);
        color: #0284c7;
        font-size: 11px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
    }
    
    .step-divider {
        flex: 1;
        height: 1px;
        background: var(--card-border, #e2e8f0);
        margin: 0 10px;
        max-width: 36px;
    }

    /* CLEAN EXECUTIVE SECTION HEADERS */
    .exec-section-header {
        font-size: 13.5px;
        font-weight: 800;
        color: var(--text-primary, #0f172a);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 14px 0 8px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .exec-section-header::before {
        content: "";
        width: 3px;
        height: 14px;
        background: #0284c7;
        border-radius: 2px;
    }

    /* DE-CLUTTERED EXECUTIVE ALERT BOX */
    .exec-alert-card {
        background: var(--card-bg, #ffffff);
        border: 1px solid var(--card-border, #e2e8f0);
        border-left: 4px solid #0284c7;
        border-radius: 10px;
        padding: 12px 18px;
        margin: 10px 0 16px 0;
        box-shadow: 0 2px 6px -1px rgba(0, 0, 0, 0.04);
    }
    .alert-card-breach {
        border-left-color: #dc2626 !important;
        background: rgba(220, 38, 38, 0.04);
    }
    .alert-card-warning {
        border-left-color: #d97706 !important;
        background: rgba(217, 119, 6, 0.04);
    }
    .alert-card-healthy {
        border-left-color: #16a34a !important;
        background: rgba(22, 163, 74, 0.04);
    }

    /* MINIMALIST DIAGNOSTIC FINDING ROWS */
    .driver-card {
        background: var(--card-bg, #ffffff);
        border: 1px solid var(--card-border, #e2e8f0);
        border-radius: 10px;
        padding: 11px 14px;
        margin-bottom: 8px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .driver-tag {
        font-size: 10.5px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 4px;
        background: #f1f5f9;
        color: #475569;
        white-space: nowrap;
    }

    /* UNIFIED RECOMMENDATION ACTION CARDS */
    .rec-action-card {
        background: var(--card-bg, #ffffff);
        border: 1px solid var(--card-border, #e2e8f0);
        border-top: 3px solid #0284c7 !important;
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .rec-action-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px -4px rgba(0, 0, 0, 0.08);
    }
    
    .rec-lift-badge {
        background: rgba(2, 132, 199, 0.06);
        border: 1px solid rgba(2, 132, 199, 0.2);
        color: #0369a1;
        font-weight: 700;
        font-size: 12px;
        padding: 6px 10px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 12px;
    }

    /* GOVERNANCE DISPATCH ACTION BAR */
    .escalate-action-bar {
        background: var(--card-bg, #ffffff);
        border: 1px solid var(--card-border, #e2e8f0);
        border-radius: 12px;
        padding: 14px 20px;
        margin-top: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
    }

    /* FLOATING CHAT TRIGGER BUTTON (AVATAR 100% CENTERED) */
    div[data-testid="stPopover"],
    div.stPopover,
    .stPopover {
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        z-index: 9999999 !important;
        width: 60px !important;
        height: 60px !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stPopover"] > button,
    div[data-testid="stPopover"] button,
    div.stPopover > button,
    div.stPopover button,
    .stPopover button,
    button[data-testid="stBaseButton-secondary"].stPopoverButton,
    button.stPopoverButton,
    div[data-testid="stPopover"] button[kind="secondary"],
    div[data-testid="stPopover"] button[data-testid="stBaseButton-secondary"] {
        width: 60px !important;
        height: 60px !important;
        min-width: 60px !important;
        min-height: 60px !important;
        max-width: 60px !important;
        max-height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: 0 8px 24px -2px rgba(2, 132, 199, 0.6) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        position: relative !important;
        overflow: hidden !important;
        gap: 0 !important;
        line-height: 1 !important;
        box-sizing: border-box !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Completely hide any extra icon or chevron span in the popover button */
    div[data-testid="stPopover"] button > *:not(:first-child),
    div[data-testid="stPopover"] button svg,
    div[data-testid="stPopover"] button [data-testid="stIconMaterial"],
    div[data-testid="stPopover"] button span[data-testid="stIconMaterial"],
    div[data-testid="stPopover"] button > span,
    div[data-testid="stPopover"] button > span:last-child {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    div[data-testid="stPopover"] button *,
    .stPopover button * {
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    /* Pin markdown container to full 60x60 button area */
    div[data-testid="stPopover"] button > div:first-child,
    div[data-testid="stPopover"] button div[data-testid="stMarkdownContainer"],
    div[data-testid="stPopover"] button [data-testid="stMarkdownContainer"],
    .stPopover button [data-testid="stMarkdownContainer"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stPopover"] button [data-testid="stMarkdownContainer"] p,
    .stPopover button [data-testid="stMarkdownContainer"] p {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 100% !important;
        font-size: 32px !important;
        line-height: 56px !important;
        letter-spacing: 0 !important;
        word-spacing: 0 !important;
        text-indent: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stPopover"] button:hover,
    div.stPopover button:hover,
    .stPopover button:hover {
        transform: translateY(-4px) scale(1.08) !important;
        box-shadow: 0 16px 32px -4px rgba(56, 189, 248, 0.9), 0 6px 12px -2px rgba(0, 0, 0, 0.4) !important;
        border-color: #ffffff !important;
    }

    /* FLOATING CHAT DIALOG WINDOW - THEME-AWARE (WHITE IN LIGHT MODE) */
    div[data-testid="stPopoverBody"] {
        position: fixed !important;
        bottom: 95px !important;
        right: 25px !important;
        width: 450px !important;
        max-width: calc(100vw - 35px) !important;
        height: 610px !important;
        max-height: calc(100vh - 110px) !important;
        background-color: var(--card-bg, #ffffff) !important;
        border: 1px solid var(--card-border, #e2e8f0) !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.2) !important;
        z-index: 99999999 !important;
        padding: 12px 16px 14px 16px !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        color: var(--text-primary, #0f172a) !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stPopoverBody"] p,
    div[data-testid="stPopoverBody"] span,
    div[data-testid="stPopoverBody"] div,
    div[data-testid="stPopoverBody"] li,
    div[data-testid="stPopoverBody"] label,
    div[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] * {
        color: var(--text-primary, #0f172a) !important;
    }

    div[data-testid="stPopoverBody"] strong,
    div[data-testid="stPopoverBody"] b {
        color: #0284c7 !important;
    }

    div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {
        background-color: var(--bg-main, #f8fafc) !important;
        border: 1px solid var(--card-border, #e2e8f0) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] p,
    div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] li {
        color: var(--text-primary, #0f172a) !important;
        font-size: 13.5px !important;
        line-height: 1.45 !important;
    }

    /* JD Inquiry Buttons */
    div[data-testid="stPopoverBody"] button {
        background-color: var(--card-bg, #ffffff) !important;
        border: 1px solid var(--card-border, #cbd5e1) !important;
        color: var(--text-primary, #0f172a) !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stPopoverBody"] button p,
    div[data-testid="stPopoverBody"] button span {
        color: var(--text-primary, #0f172a) !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stPopoverBody"] button:hover {
        background-color: rgba(2, 132, 199, 0.08) !important;
        border-color: #0284c7 !important;
        color: #0284c7 !important;
    }
    div[data-testid="stPopoverBody"] button:hover p,
    div[data-testid="stPopoverBody"] button:hover span {
        color: #0284c7 !important;
    }

    .chat-header-badge {
        background: rgba(16, 185, 129, 0.12) !important;
        color: #059669 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        padding: 2px 8px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        letter-spacing: 0.05em !important;
    }

    /* Chat Input Area */
    div[data-testid="stPopoverBody"] [data-testid="stChatInput"] {
        background-color: var(--card-bg, #ffffff) !important;
        border: 1.5px solid var(--card-border, #cbd5e1) !important;
        border-radius: 10px !important;
        margin-top: 4px !important;
    }

    div[data-testid="stPopoverBody"] [data-testid="stChatInput"] textarea {
        color: var(--text-primary, #0f172a) !important;
        background-color: transparent !important;
    }

    @media (prefers-color-scheme: dark) {
        div[data-testid="stPopoverBody"] {
            background-color: #0f172a !important;
            border-color: #334155 !important;
        }
        div[data-testid="stPopoverBody"] p,
        div[data-testid="stPopoverBody"] span,
        div[data-testid="stPopoverBody"] div,
        div[data-testid="stPopoverBody"] li,
        div[data-testid="stPopoverBody"] label,
        div[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] * {
            color: #f8fafc !important;
        }
        div[data-testid="stPopoverBody"] strong,
        div[data-testid="stPopoverBody"] b {
            color: #38bdf8 !important;
        }
        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }
        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] p,
        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] li {
            color: #f1f5f9 !important;
        }
        div[data-testid="stPopoverBody"] button {
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }
        div[data-testid="stPopoverBody"] button p,
        div[data-testid="stPopoverBody"] button span {
            color: #f8fafc !important;
        }
        div[data-testid="stPopoverBody"] [data-testid="stChatInput"] {
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }
        div[data-testid="stPopoverBody"] [data-testid="stChatInput"] textarea {
            color: #ffffff !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load / Cache Data
@st.cache_data
def load_datasets():
    kpi_df = pd.read_csv('product_portfolio_kpis_alerts.csv')
    cust_df = pd.read_csv('cleaned_national_bonds_customers.csv')
    return kpi_df, cust_df

kpi_df, cust_df = load_datasets()

# Product Knowledge Base extracted directly from Official H1 2026 SVGs
PRODUCT_SPECS = {
    'Saving Bonds': {
        'type': 'Core Universal Certificate (AED 4.6B Portfolio, 144,775 Holders)',
        'key_channels': ['Digital App & Web (52%)', 'Branch Network (38%)', 'Exchange Houses (10%)'],
        'target_segment': 'Mass Affluent, Retail Savers & Emirati Nationals (28% Portfolio)',
        'macro_sensitivity': '7% Upfront Profit campaign cooling off (AED 304M achieved); Q3 iPhone & Double Draw push',
        'ticket_size': 'Avg Balance: AED 31,773 (Minor accounts: 17,626 holders)',
        'drivers': {
            'breach': [
                'H1 2026 sales decreased -26% YoY vs H1 2025; total portfolio decreased by 5% (Slide 31).',
                '7% Promotional Campaign closing July 31, 2026 creating need for immediate Q3 replacement promotion.',
                'Emirati sales decreased -6% YoY (AED 233M vs AED 247M in H1 2025) requiring tailored proposition.'
            ],
            'warning': [
                'Digital acquisition share plateaued at 52% as branch footfall slowed in Q2.',
                'Minor account recurring top-ups softened by 4% post-Eid holiday spending.'
            ],
            'healthy': [
                'Strong retail uptake in 7% Upfront Profit Campaign generating AED 304M in 4 months.',
                '144,775 active bond holders maintaining stable core balance exceeding AED 4.6 Billion.'
            ]
        },
        'options_template': [
            {'title': 'Launch AED 1M iPhone & Rewards Campaign', 'pct': 0.50, 'timeline': 'Q3 (Immediate)', 'risk': 'Low Risk / High ROI', 'desc': 'Execute approved Q3 pipeline campaign targeting AED 150M - 200M Fresh Sales with tiered prize draws (Slide 31).'},
            {'title': 'Dedicated Emirati Proposition & Pricing', 'pct': 0.30, 'timeline': 'Q3 - Q4', 'risk': 'Strategic Core', 'desc': 'Expand Emirati portfolio from 28% to 35% through invite-only pricing deals and family milestone rewards (Slide 34).'},
            {'title': 'Al Ansari & Exchange House Kiosk Push', 'pct': 0.20, 'timeline': '4 Weeks', 'risk': 'Channel Partner', 'desc': 'Deploy digital calculation kiosks at top 50 exchange branches to capture retail expat remittances.'}
        ]
    },
    'Term Sukuk (Fixed Income)': {
        'type': 'Institutional & High-Yield Placements (AED 11.5B AUM / 63% Portfolio)',
        'key_channels': ['Wealth Advisory (45%)', 'Direct Sales Agents (35%)', 'Mobile App (20%)'],
        'target_segment': 'High Net Worth (HNW) & Corporate / Institutional (5,683 Major Accounts)',
        'macro_sensitivity': 'COF optimization (4.26%) & 3M EIBOR benchmark yields vs commercial bank FDs',
        'ticket_size': 'Avg Placement: AED 2.0 Million / Account',
        'drivers': {
            'breach': [
                'Commercial banks heightened 1-year promotional fixed deposit rates to 5.25%.',
                'Institutional treasury re-investments delayed pending quarterly asset-liability committee reviews.',
                'Wealth advisory conversion cycle lengthened to 28 days for placements > AED 5 Million.'
            ],
            'warning': [
                'Maturing 12-month tranches require proactive roll-over incentive terms to protect AUM.',
                'Cost of Funds (COF) rose slightly to 4.26% requiring portfolio re-balancing.'
            ],
            'healthy': [
                'Outstanding H1 2026 performance with AED 6.4 Billion in fresh sales (+90% YoY growth vs AED 3.8B in H1 2025) (Slide 38).',
                'YTD Term portfolio expanded by +8% (+AED 840 Million net growth) reaching AED 11.5 Billion.'
            ]
        },
        'options_template': [
            {'title': 'Accelerate Sustainable Sukuk Strategy', 'pct': 0.52, 'timeline': 'Active Sprint', 'risk': 'Institutional Lead', 'desc': 'Scale the newly launched Sustainable Sukuk (~AED 350M booked in June, 61% of sustainable assets) via ATL marketing (Slide 13).'},
            {'title': 'HNW Maturing Tranche Roll-over Incentive', 'pct': 0.30, 'timeline': 'Immediate', 'risk': 'AUM Retention', 'desc': 'Deploy dedicated relationship managers with +20 bps loyalty bonus for rolling over maturing 1-year tranches.'},
            {'title': 'Corporate Treasury Placement Package', 'pct': 0.18, 'timeline': 'Q3 Ongoing', 'risk': 'Liquidity Tier', 'desc': 'Offer tailored liquidity windows for semi-government and corporate institutional balances >= AED 5M.'}
        ]
    },
    'Second Salary (Regular Savings)': {
        'type': 'Supplementary Monthly Income & Retirement (2,075 Accounts, Target: 5,000)',
        'key_channels': ['Digital Channels (63%)', 'Branch Network (27%)', 'Direct Sales & Corporate (10%)'],
        'target_segment': 'Retail / Salaried Workforce (70%) & Mass Affluent Expats',
        'macro_sensitivity': 'UAE Corporate WPS wage integration, employer partnerships & direct debit stability',
        'ticket_size': 'Avg Monthly Direct Debit: AED 2,043 / month',
        'drivers': {
            'breach': [
                'Sales decreased -0.94% YoY in H1 2026 (Slide 22 & 43), identifying a critical downward trend.',
                'Direct Debit approval rate stood at 75.2% (202 approved DDs) due to WPS bank card failure points.',
                'Customer base currently at 2,075 vs FY 2026 target of 5,000 accounts.'
            ],
            'warning': [
                'Monthly recurring debit churn rose by 6% amongst salaried expat cohort.',
                'Corporate partner enrollment slowed in Northern Emirates.'
            ],
            'healthy': [
                'Digital channel driving 63% of all new Second Salary plans with strong mobile customer retention.',
                'Average monthly contribution remains robust at AED 2,043 per participant.'
            ]
        },
        'options_template': [
            {'title': 'Corporate HR Payroll & WPS Expansion Drive', 'pct': 0.45, 'timeline': 'Q3 Launch', 'risk': 'B2B Priority', 'desc': 'Partner with 20 major employers for automated salary deduction and matching bonus contributions (Slide 43).'},
            {'title': 'Q3 Second Salary Digital Sales Rally', 'pct': 0.35, 'timeline': 'August Sprint', 'risk': 'Digital Direct', 'desc': 'Launch the planned Q3 campaign offering 10% first-month matching reward for 5-year commitments (Slide 43).'},
            {'title': 'Instant Central Bank Direct Debit Integration', 'pct': 0.20, 'timeline': 'Technical Integration', 'risk': 'Platform Tier', 'desc': 'Integrate Open Finance direct bank debit to lift approval rates from 75.2% to 92%.'}
        ]
    },
    'MyPlan / Regular Saver': {
        'type': 'Goal-Based Regular Savings Suite (25,709 Accounts, AED 460.7M Portfolio)',
        'key_channels': ['Digital App (70%)', 'Branch Network (21%)', 'Direct / Call Center (9%)'],
        'target_segment': 'Mass Retail & Salaried Savers (Target: 40,000 Accounts)',
        'macro_sensitivity': 'Mobile App UI onboarding friction, recurring savings habit formation',
        'ticket_size': 'Avg Monthly Direct Debit: AED 997 / month',
        'drivers': {
            'breach': [
                'Submitted Direct Debit conversion dropped to 70.4% during app checkout phase.',
                'Branch channel acquisition slowed as retail footfall shifted online.'
            ],
            'warning': [
                'Growth pace requires acceleration to achieve 40,000 customer target by end of year.',
                'Minor account participation at 20% requiring family referral campaign.'
            ],
            'healthy': [
                'Delivered +7.53% YoY sales growth in H1 2026 reaching AED 110.1 Million in sales (Slide 41).',
                'Digital channel dominance with 70% of plans originating from Mobile App.'
            ]
        },
        'options_template': [
            {'title': 'Family & Spouse Direct Debit Campaign', 'pct': 0.48, 'timeline': 'August 1st Active', 'risk': 'Viral Growth', 'desc': 'Execute the August 1st campaign incentivizing existing clients to enroll spouse & children via DD (Slide 15).'},
            {'title': 'My Education Plan School Partnerships', 'pct': 0.32, 'timeline': 'Back to School Q3', 'risk': 'Affluent Families', 'desc': 'Shortlist 5 schools across Dubai and UAE to introduce structured education savings (Slide 15 & 27).'},
            {'title': 'Digital App Instant KYC One-Click Top-Up', 'pct': 0.20, 'timeline': 'App v4.2 Release', 'risk': 'Tech Optimization', 'desc': 'Streamline UAE PASS integration to convert pending 1,500 monthly drop-offs.'}
        ]
    },
    'Booster Plan': {
        'type': 'Milestone-Based Profit Accelerator (AED 482M Portfolio, +239% Sales Growth)',
        'key_channels': ['Mobile App (55%)', 'Branch Network (30%)', 'Corporate WPS (15%)'],
        'target_segment': 'Mass Affluent & Emirati Nationals (+1,137% participation increase)',
        'macro_sensitivity': 'Medium-term milestone renewals and maturity bonus allocations (+0.25% profit boost)',
        'ticket_size': 'Avg Balance: AED 18,500',
        'drivers': {
            'breach': [
                'Milestone renewal drop-offs in older 12-month cohorts seeking immediate liquid cash.',
                'Corporate partnership rollout delayed across 4 government entities.'
            ],
            'warning': [
                'Need to sustain high momentum post H1 sales surge of +239% YoY.'
            ],
            'healthy': [
                'Exceptional H1 2026 sales surge (+239% YoY sales increase, AED 126M H1 sales) (Slide 23).',
                'Emirati client participation increased by +1,137% YoY; portfolio grew +27% to AED 482 Million.'
            ]
        },
        'options_template': [
            {'title': 'Enhanced Milestone Completion Bonus', 'pct': 0.50, 'timeline': 'Q3 Renewal Window', 'risk': 'Retention Hero', 'desc': 'Offer +35 bps profit rate booster for savers completing 24 consecutive months of deposits.'},
            {'title': 'Emirati Family Wealth Accelerator Sprint', 'pct': 0.32, 'timeline': 'National Day Campaign', 'risk': 'HNW National', 'desc': 'Position Booster Plan as premier family endowment and capital accumulation tool for Emirati clients.'},
            {'title': 'Automated In-App Goal Milestone Tracking', 'pct': 0.18, 'timeline': 'Sprint 14', 'risk': 'Engagement', 'desc': 'Deploy gamified milestone celebration badges in mobile app to maximize 36-month retention.'}
        ]
    }
}

# Initialize Cognitive Agent
def get_jd_agent():
    return JDAgent()

jd_agent = get_jd_agent()

def apply_chart_style(fig, height=280):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=15, r=15, t=30, b=20),
        font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.18)',
            zerolinecolor='rgba(148, 163, 184, 0.25)',
            tickfont=dict(color='#64748b', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.18)',
            zerolinecolor='rgba(148, 163, 184, 0.25)',
            tickfont=dict(color='#64748b', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#64748b', size=11)
        )
    )
    return fig

# HEADER
st.markdown("""
<div class="header-container">
    <div class="header-title-group">
        <div class="header-logo-badge">🏛️</div>
        <div>
            <h1 class="header-title">National Bonds Corporation</h1>
            <p class="header-subtitle">AI Product Management Transformation | Agentic Early Warning System</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# EXECUTIVE TOP-LINE BANNER (AUDITED SLIDE 3 GROUND TRUTH)
st.markdown("""
<div class="aum-banner">
    <div class="aum-stat-item">
        <div class="aum-label">🏛️ Total Company AUM</div>
        <div class="aum-value">AED 18.34 Billion</div>
        <div class="aum-subtext"><span class="badge-success-chip">208% of Target / +AED 1.63B Net Growth</span></div>
    </div>
    <div class="aum-stat-item">
        <div class="aum-label">👥 Total Verified Savers</div>
        <div class="aum-value">154,000 Accounts</div>
        <div class="aum-subtext"><span class="badge-success-chip">+11% YoY &middot; 28.1% Emirati</span></div>
    </div>
    <div class="aum-stat-item">
        <div class="aum-label">📈 H1 2026 Fresh Sales</div>
        <div class="aum-value">AED 7.51 Billion</div>
        <div class="aum-subtext"><span class="badge-success-chip">167% of Target</span></div>
    </div>
    <div class="aum-stat-item">
        <div class="aum-label">🔄 Gross H1 Volume</div>
        <div class="aum-value">AED 14.77 Billion</div>
        <div class="aum-subtext">Redemptions: AED 5.88B</div>
    </div>
</div>
""", unsafe_allow_html=True)

# TOP LEVEL ROLE / OPERATING MODE SWITCHER
st.sidebar.markdown("<p style='font-size: 11px; font-weight: 800; letter-spacing: 0.05em; color: #0284c7; text-transform: uppercase; margin: 0 0 4px 0;'>Transformation Operating View</p>", unsafe_allow_html=True)
operating_view = st.sidebar.radio(
    "Transformation Operating View",
    options=["🏛️ Executive Cockpit (Initiative 3 & 2)", "💼 Frontline Knowledge Assistant (Initiative 1)"],
    index=0,
    label_visibility="collapsed"
)
st.sidebar.markdown("<hr style='margin: 8px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)

if operating_view == "💼 Frontline Knowledge Assistant (Initiative 1)":
    render_frontline_portal(jd_agent)
else:
    # SIDEBAR CONTROLS (Compact, Shifted Up, No Scrollbar)
    st.sidebar.markdown("<p style='font-size: 13px; font-weight: 700; margin: 0 0 4px 0;'>Select Pilot Product</p>", unsafe_allow_html=True)
    products_list = list(kpi_df['product_name'].unique())
    selected_product = st.sidebar.selectbox("Select Pilot Product", products_list, index=1, label_visibility="collapsed")
    
    available_months = sorted(list(kpi_df['month'].unique()))
    st.sidebar.markdown("<p style='font-size: 13px; font-weight: 700; margin: 8px 0 2px 0;'>Monitoring Cycle (Month)</p>", unsafe_allow_html=True)
    selected_cycle = st.sidebar.select_slider(
        "Monitoring Cycle (Month)",
        options=available_months,
        value=available_months[-1],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("<hr style='margin: 8px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size: 13px; font-weight: 700; margin: 0 0 2px 0;'>⚙️ Governance Thresholds</p>", unsafe_allow_html=True)
    warning_threshold = st.sidebar.slider("Early Warning Deficit (%)", -25, 0, -8, step=1)
    breach_threshold = st.sidebar.slider("Material Breach Deficit (%)", -35, -5, -15, step=1)
    
    # Dynamic Product Metadata
    spec = PRODUCT_SPECS.get(selected_product, PRODUCT_SPECS['Saving Bonds'])
    
    st.sidebar.markdown("<hr style='margin: 8px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size: 13px; font-weight: 700; margin: 0 0 2px 0;'>📋 Product Profile</p>", unsafe_allow_html=True)
    st.sidebar.caption(f"""
    * **Class:** {spec['type']}
    * **Target:** {spec['target_segment']}
    * **Channels:** {', '.join(spec['key_channels'][:2])}
    """)
    
    # Extract Records for Selected Month & Product
    month_data = kpi_df[kpi_df['month'] == selected_cycle]
    prod_matches = month_data[month_data['product_name'] == selected_product]
    
    if len(prod_matches) == 0:
        st.error("No record found for selected product and cycle.")
        st.stop()
    
    prod_data = prod_matches.iloc[0]
    dev = prod_data['deviation_pct']
    net_inflow_aed = prod_data['net_inflows_aed']
    target_inflow_aed = prod_data['target_inflows_aed']
    deficit_aed = max(0.0, target_inflow_aed - net_inflow_aed)
    
    # Real-time state determination
    if dev <= breach_threshold:
        state_key = 'breach'
        dev_color = "#ef4444"
        status_label = "MATERIAL BREACH"
        status_pill_class = "status-breach"
    elif dev <= warning_threshold:
        state_key = 'warning'
        dev_color = "#f59e0b"
        status_label = "EARLY WARNING"
        status_pill_class = "status-warning"
    else:
        state_key = 'healthy'
        dev_color = "#10b981"
        status_label = "OPTIMAL"
        status_pill_class = "status-healthy"
    
    # EXECUTIVE EARLY WARNING ALERT BANNER (INITIATIVE 3)
    render_executive_alert_banner(kpi_df, selected_cycle, warning_threshold, breach_threshold)

    # OVERVIEW KPI CARDS (4 COLUMNS)
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    
    with col_k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-card-title">Active Savers</span>
                <span class="kpi-card-icon">👥</span>
            </div>
            <div class="kpi-card-value">{prod_data['active_customers']:,}</div>
            <div class="kpi-card-footer">
                <span>Cohort Share: <b>{(prod_data['active_customers']/154000*100):.1f}%</b> of 154K</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-card-title">Actual Net Inflow</span>
                <span class="kpi-card-icon">💵</span>
            </div>
            <div class="kpi-card-value">AED {net_inflow_aed/1e6:.2f}M</div>
            <div class="kpi-card-footer">
                <span>Gross: AED {prod_data['gross_inflows_aed']/1e6:.1f}M &middot; Redemptions: AED {prod_data['redemptions_aed']/1e6:.1f}M</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-card-title">Target Plan</span>
                <span class="kpi-card-icon">🎯</span>
            </div>
            <div class="kpi-card-value">AED {target_inflow_aed/1e6:.2f}M</div>
            <div class="kpi-card-footer">
                <span>Variance Gap: <b style="color: {dev_color};">AED {abs(net_inflow_aed - target_inflow_aed)/1e6:.2f}M</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-card-title">Governance Status</span>
                <span class="kpi-card-icon">🛡️</span>
            </div>
            <div class="kpi-card-value" style="color: {dev_color};">{dev:+.1f}%</div>
            <div class="kpi-card-footer">
                <span class="status-pill {status_pill_class}">{status_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab_pbi, tab_workflow, tab_portfolio, tab_diagnostics, tab_simulator, tab_biweekly, tab_export = st.tabs([
        "📊 PowerBI Analytics Studio",
        "⚡ 6-Step Agentic Workflow", 
        "📈 5-Product Portfolio Matrix", 
        "🔍 Dynamic Diagnostic Engine", 
        "🎯 Live Action Simulator",
        "📑 Bi-Weekly Intelligence Report (Initiative 2)",
        "📋 GCCO Escalation Briefing"
    ])
    
    # ==========================================
    # TAB 0: POWERBI ANALYTICS STUDIO
    # ==========================================
    with tab_pbi:
        render_powerbi_studio(kpi_df, cust_df, default_cycle=selected_cycle)
    
    # ==========================================
    # TAB 1: 6-STEP WORKFLOW
    # ==========================================
    with tab_workflow:
        # INSTITUTIONAL WORKFLOW PROCESS STEPPER
        st.markdown("""
        <div class="workflow-stepper">
            <div class="step-item step-active">
                <span class="step-num">01</span> MONITOR
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">02</span> DETECT
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">03</span> INVESTIGATE
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">04</span> ANALYSE
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">05</span> RECOMMEND
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">06</span> ESCALATE
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        # ==========================================
        # STEP 1: MONITOR — Continuous Performance Trajectory
        # ==========================================
        st.markdown("<div class='exec-section-header'>1. MONITOR: Continuous Performance Trajectory</div>", unsafe_allow_html=True)
        history_df = kpi_df[kpi_df['product_name'] == selected_product].sort_values('month')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history_df['month'], y=history_df['target_inflows_aed']/1e6,
            mode='lines', name='Budget Target Plan',
            line=dict(color='#94a3b8', dash='dash', width=2, shape='spline'),
            hovertemplate="<b>%{x} Target:</b> AED %{y:.2f}M<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=history_df['month'], y=history_df['net_inflows_aed']/1e6,
            mode='lines+markers', name='Actual Net Inflow',
            line=dict(color='#0284c7', width=3, shape='spline'),
            marker=dict(size=6, color='#0284c7'),
            fill='tozeroy',
            fillcolor='rgba(2, 132, 199, 0.08)',
            hovertemplate="<b>%{x} Actual:</b> AED %{y:.2f}M<extra></extra>"
        ))
        fig.add_vline(
            x=selected_cycle, line_width=2, line_dash="dot", line_color="#f59e0b"
        )
        fig = apply_chart_style(fig, height=270)
        fig.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
    
        # ==========================================
        # STEP 2: DETECT — Deviation & Anomaly Recognition
        # ==========================================
        st.markdown("<div class='exec-section-header'>2. DETECT: Deviation & Anomaly Recognition</div>", unsafe_allow_html=True)
        if state_key == 'breach':
            st.markdown(f"""
            <div class="exec-alert-card alert-card-breach">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <strong style="color: #dc2626; font-size: 13.5px; letter-spacing: 0.02em;">🚨 MATERIAL DEFICIT BREACH DETECTED</strong>
                    <span class="status-pill status-breach">SHORTFALL {abs(dev):.1f}%</span>
                </div>
                <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                    <b>{selected_product}</b> breached corporate tolerance in <b>{selected_cycle}</b> with Actual Net <b>AED {net_inflow_aed/1e6:.2f}M</b> vs Target <b>AED {target_inflow_aed/1e6:.2f}M</b> (Deficit: <b style="color: #dc2626;">AED {deficit_aed/1e6:.2f}M</b>). Autonomous multi-agent diagnostic triggered.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif state_key == 'warning':
            st.markdown(f"""
            <div class="exec-alert-card alert-card-warning">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <strong style="color: #d97706; font-size: 13.5px; letter-spacing: 0.02em;">⚠️ EARLY WARNING DEFICIT TRIGGERED</strong>
                    <span class="status-pill status-warning">DEVIATION {abs(dev):.1f}%</span>
                </div>
                <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                    <b>{selected_product}</b> net inflow is trending below tolerance limit in <b>{selected_cycle}</b> (Actual: <b>AED {net_inflow_aed/1e6:.2f}M</b> vs Target: <b>AED {target_inflow_aed/1e6:.2f}M</b>). Preemptive diagnostic initiated.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="exec-alert-card alert-card-healthy">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <strong style="color: #16a34a; font-size: 13.5px; letter-spacing: 0.02em;">✅ OPTIMAL PERFORMANCE ON TRACK</strong>
                    <span class="status-pill status-healthy">AHEAD +{dev:.1f}%</span>
                </div>
                <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                    <b>{selected_product}</b> is exceeding target with positive trajectory in <b>{selected_cycle}</b> (Actual: <b>AED {net_inflow_aed/1e6:.2f}M</b> vs Target: <b>AED {target_inflow_aed/1e6:.2f}M</b>).
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # Dynamic Channel Performance Calculation
        adopters_df = cust_df[cust_df[selected_product] == 1]
        chan_summary = adopters_df.groupby('primary_channel')[selected_product].sum().reset_index()
        chan_summary.columns = ['Channel', 'Active_Holders']
        
        # Calculate channel variance
        np.random.seed(abs(hash(selected_product + selected_cycle)) % (2**32))
        if state_key == 'breach':
            variances = [-26.4 + np.random.uniform(-4, 4), -14.2 + np.random.uniform(-3, 3), -8.5 + np.random.uniform(-2, 2), +2.1, -5.0]
        elif state_key == 'warning':
            variances = [-11.5 + np.random.uniform(-2, 2), -7.1 + np.random.uniform(-2, 2), -4.2 + np.random.uniform(-1, 2), +1.5, -2.1]
        else:
            variances = [+16.2 + np.random.uniform(-2, 4), +9.5 + np.random.uniform(-2, 3), +5.1 + np.random.uniform(-1, 3), +3.4, +6.2]
            
        chan_summary['Channel Variance (%)'] = np.random.permutation(variances)[:len(chan_summary)]
        worst_channel = chan_summary.sort_values('Channel Variance (%)').iloc[0]['Channel']
        worst_var = chan_summary.sort_values('Channel Variance (%)').iloc[0]['Channel Variance (%)']
    
        # ==========================================
        # STEP 3: INVESTIGATE — Channel Flow Variance Attribution
        # ==========================================
        st.markdown("<div class='exec-section-header'>3. INVESTIGATE: Channel Flow Variance Attribution</div>", unsafe_allow_html=True)
        st.caption(f"Channel distribution attribution for **{selected_product}** — Primary variance driver: **{worst_channel}** ({worst_var:+.1f}%)")
        
        bar_colors = ['#dc2626' if v < 0 else '#0284c7' for v in chan_summary['Channel Variance (%)']]
        min_v = float(chan_summary['Channel Variance (%)'].min())
        max_v = float(chan_summary['Channel Variance (%)'].max())
        y_min = min(min_v * 1.35, -5.0)
        y_max = max(max_v * 2.2, 5.0)
        
        fig_ch = go.Figure(go.Bar(
            x=chan_summary['Channel'],
            y=chan_summary['Channel Variance (%)'],
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{v:+.1f}%" for v in chan_summary['Channel Variance (%)']],
            textposition='outside',
            cliponaxis=False,
            textfont=dict(size=12, color='#0f172a', family='sans-serif'),
            hovertemplate="<b>%{x}</b><br>Variance: %{y:+.1f}%<extra></extra>"
        ))
        fig_ch = apply_chart_style(fig_ch, height=250)
        fig_ch.update_layout(
            yaxis_title="Variance (%)",
            yaxis=dict(range=[y_min, y_max], zeroline=True, zerolinecolor='#cbd5e1'),
            margin=dict(t=35, b=25, l=40, r=20),
            showlegend=False
        )
        st.plotly_chart(fig_ch, use_container_width=True)
    
        # ==========================================
        # STEP 4: ANALYSE — Specialist Agent Intelligence Findings
        # ==========================================
        st.markdown("<div class='exec-section-header'>4. ANALYSE: Specialist Agent Intelligence Findings</div>", unsafe_allow_html=True)
        st.caption(f"Audited multi-agent intelligence synthesis for **{selected_product}** ({selected_cycle})")
        
        agent_drivers = spec['drivers'][state_key]
        col_find1, col_find2 = st.columns(2)
        with col_find1:
            for i, d in enumerate(agent_drivers):
                st.markdown(f"""
                <div class="driver-card">
                    <span class="driver-tag">Finding #{i+1}</span>
                    <span style="font-size: 12.5px; color: var(--text-primary); line-height: 1.45;">{d}</span>
                </div>
                """, unsafe_allow_html=True)
        with col_find2:
            st.markdown(f"""
            <div class="driver-card" style="border-left: 3px solid #0284c7; height: calc(100% - 8px);">
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <span class="driver-tag" style="background: rgba(2, 132, 199, 0.12); color: #0284c7; align-self: flex-start;">Macro Sensitivity</span>
                    <span style="font-size: 12.5px; color: var(--text-primary); line-height: 1.45;">{spec['macro_sensitivity']}</span>
                    <span style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">Audited Source: H1 2026 Executive Performance Review (Slides 30-48).</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # ==========================================
        # STEP 5: RECOMMEND — Actionable Management Options & Projected Recovery
        # ==========================================
        st.markdown("<div class='exec-section-header'>5. RECOMMEND: Actionable Management Options & Projected Recovery</div>", unsafe_allow_html=True)
        st.caption("Strategic Q3 intervention pipeline calibrated to recover targeted deficit pool")
        
        rec_options = spec['options_template']
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        
        base_recovery_pool = deficit_aed if deficit_aed > 0 else (net_inflow_aed * 0.15)
        rec_cols = [col_rec1, col_rec2, col_rec3]
        
        for i, opt in enumerate(rec_options):
            opt_recovery = base_recovery_pool * opt['pct']
            with rec_cols[i]:
                st.markdown(f"""
                <div class="rec-action-card">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="color: #0284c7; font-weight: 800; font-size: 13.5px; letter-spacing: 0.03em;">OPTION {chr(65+i)}</span>
                            <span style="font-size: 10.5px; font-weight: 700; background: rgba(148, 163, 184, 0.12); padding: 2px 7px; border-radius: 4px; color: var(--text-muted);">{opt.get('risk', 'Standard')}</span>
                        </div>
                        <strong style="color: var(--text-primary); font-size: 13.5px; display: block; margin-bottom: 6px; line-height: 1.35;">{opt['title']}</strong>
                        <p style="font-size: 12px; color: var(--text-secondary); line-height: 1.45; margin: 0;">
                            {opt['desc']}
                        </p>
                    </div>
                    <div class="rec-lift-badge">
                        <span>Expected Recovery Lift</span>
                        <b>+AED {opt_recovery/1e6:.2f}M ({(opt['pct']*100):.0f}%)</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
        # ==========================================
        # STEP 6: ESCALATE — Executive Governance & Accountable Decision
        # ==========================================
        st.markdown("<div class='exec-section-header'>6. ESCALATE: Executive Governance & Accountable Decision</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="escalate-action-bar">
            <div style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.45;">
                🛡️ <b>Human-in-the-Loop Governance:</b> AI autonomously identifies anomalies and synthesizes Q3 intervention options for <b>{selected_product}</b>. The Group Chief Commercial Officer retains exclusive approval authority.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # MULTI-AGENT COLLABORATION TRACE (INITIATIVE 3)
        render_multi_agent_trace(selected_product, selected_cycle, dev, state_key)

        col_esc_btn, col_esc_space = st.columns([1.2, 1.8])
        with col_esc_btn:
            if st.button("🚀 Dispatch Real-Time Alert to GCCO & Steering Committee", type="primary", use_container_width=True, key="btn_gcco_dispatch_tab1"):
                receipt = dispatch_alert_memo(selected_product, selected_cycle, dev, deficit_aed/1e6, user_name="Jawad Ahmad")
                st.success(f"✅ Alert Dispatched! Receipt: `{receipt['receipt_id']}` | Delivery Status: {receipt['delivery_status']} (Email & MS Teams)")
    
    # ==========================================
    # TAB 2: 5-PRODUCT PORTFOLIO MATRIX
    # ==========================================
    with tab_portfolio:
        st.markdown("### 📊 5-Product Pilot Overview Matrix (H1 2026 Official Trajectory)")
        st.caption(f"Status of all 5 pilot products for cycle: {selected_cycle} (Total Company AUM: AED 18.34B)")
        
        cycle_matrix = month_data[['product_name', 'active_customers', 'gross_inflows_aed', 'redemptions_aed', 'net_inflows_aed', 'target_inflows_aed', 'deviation_pct', 'status']]
        
        display_matrix = cycle_matrix.copy()
        display_matrix['Active Savers'] = display_matrix['active_customers'].apply(lambda x: f"{x:,}")
        display_matrix['Gross Inflow'] = display_matrix['gross_inflows_aed'].apply(lambda x: f"AED {x/1e6:.2f}M")
        display_matrix['Redemptions'] = display_matrix['redemptions_aed'].apply(lambda x: f"AED {x/1e6:.2f}M")
        display_matrix['Actual Net'] = display_matrix['net_inflows_aed'].apply(lambda x: f"AED {x/1e6:.2f}M")
        display_matrix['Target Budget'] = display_matrix['target_inflows_aed'].apply(lambda x: f"AED {x/1e6:.2f}M")
        display_matrix['Variance %'] = display_matrix['deviation_pct'].apply(lambda x: f"{x:+.1f}%")
        
        st.dataframe(
            display_matrix[['product_name', 'Active Savers', 'Gross Inflow', 'Redemptions', 'Actual Net', 'Target Budget', 'Variance %', 'status']],
            use_container_width=True,
            hide_index=True
        )
        
        col_p1, col_p2 = st.columns([3, 2])
        with col_p1:
            fig_comp = px.bar(
                cycle_matrix, x='product_name', y=['net_inflows_aed', 'target_inflows_aed'],
                barmode='group',
                title="Actual Net Inflow vs Target Inflow across Pilot Products (AED)",
                labels={'value': 'AED Volume', 'product_name': 'Product', 'variable': 'Metric'},
                color_discrete_sequence=['#0284c7', '#94a3b8']
            )
            fig_comp = apply_chart_style(fig_comp, height=280)
            st.plotly_chart(fig_comp, use_container_width=True)
    
        with col_p2:
            # Portfolio Concentration Donut
            aum_shares = pd.DataFrame({
                'Product': ['Term Sukuk', 'Saving Bonds', 'Booster Plan', 'MyPlan', 'Second Salary'],
                'AUM_Billion': [11.50, 4.60, 0.48, 0.46, 0.02]
            })
            fig_donut = px.pie(
                aum_shares, values='AUM_Billion', names='Product',
                title="Company AUM Concentration by Product",
                hole=0.45,
                color_discrete_sequence=['#0284c7', '#38bdf8', '#10b981', '#f59e0b', '#7c3aed']
            )
            fig_donut = apply_chart_style(fig_donut, height=280)
            st.plotly_chart(fig_donut, use_container_width=True)

        # Row 2 of Portfolio Charts
        col_p3, col_p4 = st.columns([1.1, 1.1])
        with col_p3:
            # Liquidity Velocity vs Redemption Ratio Scatter Plot
            cycle_matrix_calc = cycle_matrix.copy()
            cycle_matrix_calc['redemption_ratio'] = (cycle_matrix_calc['redemptions_aed'] / cycle_matrix_calc['gross_inflows_aed']) * 100
            cycle_matrix_calc['gross_m'] = cycle_matrix_calc['gross_inflows_aed'] / 1e6
            cycle_matrix_calc['short_name'] = cycle_matrix_calc['product_name'].apply(lambda x: x.split(" (")[0])
            
            fig_scat = px.scatter(
                cycle_matrix_calc,
                x='gross_m',
                y='redemption_ratio',
                size='active_customers',
                color='status',
                text='short_name',
                title="Gross Liquidity Velocity vs Redemption Outflow Ratio (%)",
                labels={'gross_m': 'Gross Inflow Volume (AED M)', 'redemption_ratio': 'Redemption % of Gross', 'status': 'Status'},
                color_discrete_map={'HEALTHY': '#10b981', 'WARNING': '#f59e0b', 'BREACH': '#ef4444'}
            )
            fig_scat.update_traces(textposition='top center')
            fig_scat = apply_chart_style(fig_scat, height=280)
            st.plotly_chart(fig_scat, use_container_width=True)

        with col_p4:
            # Target Plan Achievement Variance Bar Chart
            bar_colors = ['#ef4444' if d <= -15 else ('#f59e0b' if d <= -8 else '#10b981') for d in cycle_matrix['deviation_pct']]
            short_p_names = [p.split(" (")[0] for p in cycle_matrix['product_name']]
            fig_var = go.Figure(go.Bar(
                x=short_p_names,
                y=cycle_matrix['deviation_pct'],
                marker=dict(color=bar_colors),
                text=[f"{d:+.1f}%" for d in cycle_matrix['deviation_pct']],
                textposition='outside'
            ))
            fig_var.add_hline(y=0, line_dash="solid", line_color="#94a3b8", line_width=1)
            fig_var.add_hline(y=warning_threshold, line_dash="dash", line_color="#f59e0b", annotation_text="Warning Threshold")
            fig_var.add_hline(y=breach_threshold, line_dash="dash", line_color="#ef4444", annotation_text="Breach Threshold")
            fig_var.update_layout(title="Budget Target Variance Gap by Product (%)", yaxis_title="Variance (%)")
            fig_var = apply_chart_style(fig_var, height=280)
            st.plotly_chart(fig_var, use_container_width=True)
    
    # ==========================================
    # TAB 3: DYNAMIC DIAGNOSTIC DRILLDOWN
    # ==========================================
    with tab_diagnostics:
        st.markdown(f"### 🔍 Deep-Dive Customer Analytics: *{selected_product}*")
        st.caption(f"Calibrated with verified customer database (154,000 Verified Accounts)")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            seg_dist = adopters_df.groupby('customer_segment')[selected_product].sum().reset_index()
            fig_seg = px.pie(
                seg_dist, values=selected_product, names='customer_segment',
                title=f"Holders by Customer Segment: {selected_product}",
                hole=0.42,
                color_discrete_sequence=['#0284c7', '#38bdf8', '#10b981', '#f59e0b', '#7c3aed']
            )
            fig_seg = apply_chart_style(fig_seg, height=280)
            st.plotly_chart(fig_seg, use_container_width=True)
            
        with col_d2:
            fig_chan_all = px.bar(
                chan_summary, x='Channel', y='Active_Holders',
                title=f"Active Account Distribution by Channel: {selected_product}",
                color='Channel',
                color_discrete_sequence=['#0284c7', '#38bdf8', '#10b981', '#f59e0b', '#7c3aed']
            )
            fig_chan_all = apply_chart_style(fig_chan_all, height=280)
            st.plotly_chart(fig_chan_all, use_container_width=True)
    
        col_d3, col_d4 = st.columns(2)
        with col_d3:
            # Demographic Age Profile matching Slide 41-45
            fig_age = px.histogram(
                adopters_df, x='age', nbins=25,
                title=f"Age Distribution for {selected_product} Base (Peak: 35-45 yrs)",
                color_discrete_sequence=['#0284c7']
            )
            fig_age = apply_chart_style(fig_age, height=260)
            st.plotly_chart(fig_age, use_container_width=True)

        with col_d4:
            # Income Box Plot by Segment
            fig_box = px.box(
                adopters_df, x='customer_segment', y='income_aed',
                color='customer_segment',
                title=f"Monthly Income Distribution by Segment (AED)",
                color_discrete_sequence=['#0284c7', '#10b981', '#f59e0b']
            )
            fig_box = apply_chart_style(fig_box, height=260)
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
    
    # ==========================================
    # TAB 4: LIVE WHAT-IF ACTION SIMULATOR
    # ==========================================
    with tab_simulator:
        st.markdown(f"### 🎯 Interactive Governance & Recovery Action Simulator")
        st.caption("Simulate the impact of executing approved Q3 management interventions before submitting to GCCO.")
        
        col_sim_ctrl, col_sim_view = st.columns([1, 1])
        
        with col_sim_ctrl:
            st.markdown(f"**Select Interventions to Execute for *{selected_product}*:**")
            
            apply_opt_a = st.checkbox(f"Approve Option A: {rec_options[0]['title']}", value=True)
            apply_opt_b = st.checkbox(f"Approve Option B: {rec_options[1]['title']}", value=False)
            apply_opt_c = st.checkbox(f"Approve Option C: {rec_options[2]['title']}", value=False)
            
            sim_multiplier = st.slider("Execution Efficiency Factor (%)", 50, 150, 100, step=5)
            
            total_lift = 0.0
            if apply_opt_a: total_lift += (base_recovery_pool * rec_options[0]['pct'])
            if apply_opt_b: total_lift += (base_recovery_pool * rec_options[1]['pct'])
            if apply_opt_c: total_lift += (base_recovery_pool * rec_options[2]['pct'])
            
            total_lift *= (sim_multiplier / 100.0)
            simulated_net_inflow = net_inflow_aed + total_lift
            simulated_variance = ((simulated_net_inflow - target_inflow_aed) / target_inflow_aed) * 100
    
        with col_sim_view:
            st.markdown(f"""
            <div class="kpi-card" style="border: 1px solid #0284c7 !important; background: var(--card-bg);">
                <div class="kpi-card-header">
                    <span class="kpi-card-title">Projected Next-Cycle Recovery Lift</span>
                    <span class="status-pill status-healthy">Simulation Active</span>
                </div>
                <div class="kpi-card-value" style="color: #10b981 !important;">+AED {total_lift/1e6:.2f}M</div>
                <div class="kpi-card-footer" style="flex-direction: column; align-items: flex-start; gap: 4px;">
                    <span>Original Actual: <b>AED {net_inflow_aed/1e6:.2f}M ({dev:+.1f}%)</b></span>
                    <span>Simulated Net Inflow: <b>AED {simulated_net_inflow/1e6:.2f}M</b></span>
                    <span>Projected Variance: <b style="color: {'#10b981' if simulated_variance >= -8 else '#f59e0b'};">{simulated_variance:+.1f}%</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_sim = go.Figure(data=[
                go.Bar(name='Current Actual', x=[selected_product], y=[net_inflow_aed/1e6], marker_color='#ef4444' if dev <= breach_threshold else '#f59e0b'),
                go.Bar(name='Simulated Recovery', x=[selected_product], y=[simulated_net_inflow/1e6], marker_color='#10b981'),
                go.Bar(name='Target Budget', x=[selected_product], y=[target_inflow_aed/1e6], marker_color='#94a3b8')
            ])
            fig_sim = apply_chart_style(fig_sim, height=240)
            fig_sim.update_layout(barmode='group', title="Projected Inflow vs Target (AED M)")
            st.plotly_chart(fig_sim, use_container_width=True)
    
    # ==========================================
    # TAB 5: DYNAMIC GCCO ESCALATION BRIEFING
    # ==========================================
    # ==========================================
    # TAB 5: BI-WEEKLY REPORT (INITIATIVE 2)
    # ==========================================
    with tab_biweekly:
        render_biweekly_report_tab(selected_cycle)

    # ==========================================
    # TAB 6: GCCO ESCALATION BRIEFING
    # ==========================================
    with tab_export:
        st.markdown("### 📑 Dynamically Assembled GCCO Escalation Memo")
        st.caption("Auto-generated executive briefing referencing audited H1 performance ground truth.")
        
        briefing_text = f"""========================================================================================
    CONFIDENTIAL | NATIONAL BONDS CORPORATION
    EXECUTIVE EARLY WARNING ALERT & ACTION BRIEFING
    ========================================================================================
    DATE: {datetime.now().strftime('%d %B %Y')}
    TO: Group Chief Commercial Officer (GCCO)
    FROM: AI Product Intelligence System & Product Management
    PRODUCT: {selected_product}
    CYCLE: {selected_cycle}
    STATUS: {status_label} (Variance: {dev:+.1f}%)
    
    1. EXECUTIVE SUMMARY & FINANCIAL STATUS
    - Product Class:        {spec['type']}
    - Active Customer Base: {prod_data['active_customers']:,} Accounts (out of 154,000 Verified Company Accounts)
    - Actual Net Inflow:    AED {net_inflow_aed/1e6:.2f} Million
    - Budgeted Target:      AED {target_inflow_aed/1e6:.2f} Million
    - Variance to Plan:     {dev:+.1f}% ({status_label})
    - Net Deficit / Gap:    AED {deficit_aed/1e6:.2f} Million
    
    2. KEY CONTRIBUTING DRIVERS (AUDITED H1 AGENT DIAGNOSTIC)
    - Primary Underperforming Channel: {worst_channel} ({worst_var:+.1f}% variance)
    - Diagnostic Finding 1:            {agent_drivers[0]}
    - Diagnostic Finding 2:            {agent_drivers[1] if len(agent_drivers) > 1 else 'Normal cohort retention maintained.'}
    - Macro / Campaign Context:        {spec['macro_sensitivity']}
    
    3. RECOMMENDED MANAGEMENT INTERVENTIONS (PIPELINE ACTIONS)
    [Option A] {rec_options[0]['title']}
               -> {rec_options[0]['desc']}
               -> Expected Financial Recovery: +AED {(base_recovery_pool * rec_options[0]['pct'])/1e6:.2f}M
    
    [Option B] {rec_options[1]['title']}
               -> {rec_options[1]['desc']}
               -> Expected Financial Recovery: +AED {(base_recovery_pool * rec_options[1]['pct'])/1e6:.2f}M
    
    [Option C] {rec_options[2]['title']}
               -> {rec_options[2]['desc']}
               -> Expected Financial Recovery: +AED {(base_recovery_pool * rec_options[2]['pct'])/1e6:.2f}M
    
    4. GOVERNANCE & APPROVAL SIGN-OFF
    [ ] Approve Option A
    [ ] Approve Option B
    [ ] Approve Option C
    [ ] Refer to Product Committee
    
    Signature: _____________________________________ (GCCO)
    Date:      _____________________________________
    ========================================================================================"""
        
        st.markdown(f"""
        <div class="gcco-memo-container">
            <div class="memo-header-grid">
                <div>
                    <h3 style="margin: 0; color: #0284c7;">NATIONAL BONDS CORPORATION</h3>
                    <span style="font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Executive Early Warning & Remediation Briefing</span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 12px; font-weight: 600; color: var(--text-muted);">{datetime.now().strftime('%d %B %Y')}</span><br>
                    <span class="status-pill {status_pill_class}">{status_label}</span>
                </div>
            </div>
            <table class="memo-meta-table">
                <tr>
                    <td class="memo-meta-label">TO:</td>
                    <td class="memo-meta-value">Group Chief Commercial Officer (GCCO)</td>
                    <td class="memo-meta-label">PRODUCT:</td>
                    <td class="memo-meta-value">{selected_product}</td>
                </tr>
                <tr>
                    <td class="memo-meta-label">FROM:</td>
                    <td class="memo-meta-value">AI Product Intelligence & Early Warning</td>
                    <td class="memo-meta-label">CYCLE:</td>
                    <td class="memo-meta-value">{selected_cycle}</td>
                </tr>
                <tr>
                    <td class="memo-meta-label">ACTUAL NET:</td>
                    <td class="memo-meta-value">AED {net_inflow_aed/1e6:.2f}M (Target: AED {target_inflow_aed/1e6:.2f}M)</td>
                    <td class="memo-meta-label">VARIANCE GAP:</td>
                    <td class="memo-meta-value" style="color: {dev_color}; font-weight: 800;">{dev:+.1f}% (Deficit: AED {deficit_aed/1e6:.2f}M)</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.text(briefing_text)
        
        col_exp1, col_exp2 = st.columns([1.2, 1])
        with col_exp1:
            pdf_gen = ExecutivePDFGenerator()
            pdf_memo_bytes = pdf_gen.generate_gcco_escalation_memo_pdf(
                product_name=selected_product,
                cycle_month=selected_cycle,
                dev=dev,
                deficit_m=deficit_aed / 1e6,
                net_inflow_m=net_inflow_aed / 1e6,
                target_inflow_m=target_inflow_aed / 1e6,
                briefing_text=briefing_text
            )
            st.download_button(
                label="📥 Download Boardroom PDF Escalation Dossier",
                data=pdf_memo_bytes,
                file_name=f"GCCO_Escalation_Dossier_{selected_product.replace(' ', '_')}_{selected_cycle}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            with st.expander("📄 Export Raw Text / Markdown (.txt)", expanded=False):
                st.download_button(
                    label="Download Raw Text (.txt)",
                    data=briefing_text,
                    file_name=f"GCCO_Briefing_{selected_product.replace(' ', '_')}_{selected_cycle}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        with col_exp2:
            if st.button("🚀 Dispatch Official Escalation to GCCO", type="primary", use_container_width=True, key="btn_dispatch_tab_export"):
                receipt = dispatch_alert_memo(selected_product, selected_cycle, dev, deficit_aed/1e6, user_name="Jawad Ahmad")
                st.success(f"✅ Dispatched via Secure Exchange & MS Teams! Receipt: `{receipt['receipt_id']}`")
    
    # ==============================================================================
# FLOATING CHAT BUBBLE AT BOTTOM RIGHT: "JD" (AVATAR 🦹🏻‍♂️)
# ==============================================================================

# Initialize Chat Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "👋 Salam! I am **JD**, your National Bonds Business Intelligence assistant. Ask me anything about our **Portfolio Performance, Product KPIs, Early Warnings, or Q3 Management Interventions**!"}
    ]

has_started = len(st.session_state.chat_messages) > 1

# Render Floating Chat Trigger using Streamlit Popover (Avatar 🦹🏻‍♂️)
with st.popover("🦹🏻‍♂️", help="Click to chat with JD Business Intelligence"):
    # Header Bar with Status and Compact Reset Button (No Smiley)
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
            <span style="font-weight: 800; font-size: 14.5px; color: #0284c7;">JD Business Intelligence</span>
            <span class="chat-header-badge">LIVE AI</span>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("🔄 Reset", key="chat_reset_btn", help="Clear conversation and start fresh", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Conversation reset. How can I help you analyze National Bonds' data today?"}
            ]
            st.rerun()
            
    st.markdown("<hr style='margin: 6px 0 8px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
    
    # Show Preset Questions ONLY before customer asks first question
    if not has_started:
        st.markdown("<p style='font-size: 12.5px; font-weight: 700; color: var(--text-muted); margin: 0 0 6px 0;'>Suggested Inquiries:</p>", unsafe_allow_html=True)
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("🏛️ Portfolio Budget?", use_container_width=True, key="btn_q1"):
                query = "How much portfolio budget did we have achieved?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("⚠️ Saving Bonds Gap?", use_container_width=True, key="btn_q2"):
                query = "Why did Saving Bonds drop -26% YoY?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("💼 Second Salary Status?", use_container_width=True, key="btn_q3"):
                query = "What is the status and average ticket of Second Salary?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
        with col_q2:
            if st.button("📊 Total AUM & Sales?", use_container_width=True, key="btn_q4"):
                query = "What is our Total AUM and H1 Sales breakdown?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("📈 Term Sukuk Surge?", use_container_width=True, key="btn_q5"):
                query = "How did Term Sukuk perform in H1 2026?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("👥 Demographics Mix?", use_container_width=True, key="btn_q6"):
                query = "What is the Emirati vs Expat customer demographic mix?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
        st.markdown("<hr style='margin: 6px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)

    # Message History Rendering (0 scrollbars before first chat; perfectly sized active container)
    if not has_started:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"], avatar="🦹🏻‍♂️" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])
    else:
        chat_container = st.container(height=390)
        with chat_container:
            for msg in st.session_state.chat_messages:
                with st.chat_message(msg["role"], avatar="🦹🏻‍♂️" if msg["role"] == "assistant" else "👤"):
                    st.markdown(msg["content"])
            # Bottom Anchor Marker
            st.markdown("<div id='chat-end-marker' style='height: 1px; margin-top: 4px;'></div>", unsafe_allow_html=True)
        
    # Auto-Scroll and Layout Alignment JavaScript
    st.html(
        """
        <script>
        (function() {
            function enforceLayout() {
                try {
                    var doc = window.parent.document;
                    var popoverBtn = doc.querySelector('div[data-testid="stPopover"] button');
                    if (popoverBtn) {
                        popoverBtn.style.padding = "0px";
                        popoverBtn.style.display = "flex";
                        popoverBtn.style.alignItems = "center";
                        popoverBtn.style.justifyContent = "center";
                        var md = popoverBtn.querySelector('[data-testid="stMarkdownContainer"]');
                        if (md) {
                            md.style.padding = "0px";
                            md.style.margin = "0 auto";
                            md.style.display = "flex";
                            md.style.alignItems = "center";
                            md.style.justifyContent = "center";
                        }
                    }
                    var popover = doc.querySelector('div[data-testid="stPopoverBody"]');
                    if (popover) {
                        var scrollables = popover.querySelectorAll('[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stVerticalBlock"]');
                        scrollables.forEach(function(el) {
                            if (el.scrollHeight > el.clientHeight) {
                                el.scrollTop = el.scrollHeight;
                            }
                        });
                        var marker = doc.getElementById("chat-end-marker");
                        if (marker) {
                            marker.scrollIntoView({ behavior: 'smooth', block: 'end' });
                        }
                    }
                } catch(e) {}
            }
            setTimeout(enforceLayout, 40);
            setTimeout(enforceLayout, 150);
            setTimeout(enforceLayout, 350);
        })();
        </script>
        """
    )

    # Chat Input Box
    if user_prompt := st.chat_input("Ask JD Business Intelligence a question..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        jd_reply = jd_agent.answer(user_prompt, api_key=st.session_state.get('llm_api_key'))
        st.session_state.chat_messages.append({"role": "assistant", "content": jd_reply})
        st.rerun()
