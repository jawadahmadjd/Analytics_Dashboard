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

from icons import ICONS, get_icon

# Page Configuration
st.set_page_config(
    page_title="National Bonds | Executive Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Executive Cockpit & Floating Intelligence Copilot
st.markdown("""
<style>
    /* Inter & JetBrains Mono Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');
    
    /* UNIVERSAL INTER FONT ENFORCEMENT - Eliminates Source Sans Fallback */
    html, body, [class*="css"], .stMarkdown, .stText, 
    [data-testid="stMarkdownContainer"] p, 
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] td,
    [data-testid="stMarkdownContainer"] th,
    div, span, p, h1, h2, h3, h4, h5, h6, label, 
    input, textarea, select, button, a, td, th {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Preserve Streamlit Material Symbols Iconography */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-symbols-sharp,
    [class*="material-symbols"],
    [data-testid="stIconMaterial"],
    span[data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapsedControl"] span {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
    }
    
    code, pre, .stCode, [data-testid="stCode"] {
        font-family: 'JetBrains Mono', monospace !important;
    }    /* DESIGN SYSTEM TOKENS (1080p Panoramic Luxury FinTech Palette) */
    :root {
        /* === SURFACES (Warm Ivory Porcelain & Crisp White) === */
        --surface-primary: #FFFFFF;
        --surface-secondary: #FAFBFD;
        --surface-tertiary: #F4F6F9;
        --surface-elevated: #FFFFFF;
        
        --border-primary: #EAEFF5;
        --border-secondary: #F1F4F9;
        --border-interactive: #CBD5E1;
        
        --text-primary: #0B192C;
        --text-secondary: #475569;
        --text-tertiary: #64748B;
        --text-quaternary: #94A3B8;
        
        /* === BRAND (Imperial Navy & Brushed Champagne Gold) === */
        --brand-primary: #0B192C;
        --brand-primary-hover: #1E3E62;
        --brand-gold: #C5A059;
        --brand-gold-hover: #B38E46;
        --brand-gold-subtle: #FDFBF7;
        --brand-gold-border: #E8DCC4;
        --brand-subtle: #F0F4F8;
        --brand-text: #0B192C;
        
        /* === SEMANTIC STATUS === */
        --status-positive: #10B981;
        --status-positive-bg: #ECFDF5;
        --status-positive-border: #A7F3D0;
        
        --status-warning: #D4850A;
        --status-warning-bg: #FFFBEB;
        --status-warning-border: #FDE68A;
        
        --status-critical: #EF4444;
        --status-critical-bg: #FEF2F2;
        --status-critical-border: #FECACA;
        
        --status-info: #0B192C;
        --status-info-bg: #F0F4F8;
        
        /* === DATA VISUALIZATION PALETTE === */
        --chart-primary: #0B192C;
        --chart-secondary: #64748B;
        --chart-tertiary: #CBD5E1;
        --chart-positive: #10B981;
        --chart-negative: #EF4444;
        --chart-accent-1: #C5A059;
        --chart-accent-2: #1E3E62;
        
        /* === ELEVATION === */
        --shadow-xs: 0 1px 2px rgba(11, 25, 44, 0.03);
        --shadow-sm: 0 1px 3px rgba(11, 25, 44, 0.05), 0 1px 2px rgba(11, 25, 44, 0.03);
        --shadow-md: 0 4px 12px rgba(11, 25, 44, 0.05);
        --shadow-lg: 0 8px 24px rgba(11, 25, 44, 0.07);
        
        /* === SPACING SCALE (8px base grid) === */
        --space-1: 4px;
        --space-2: 8px;
        --space-3: 12px;
        --space-4: 16px;
        --space-5: 20px;
        --space-6: 24px;
        --space-8: 32px;
        --space-10: 40px;
        
        /* === BORDER RADIUS === */
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-full: 9999px;

        /* Backward-compatible aliases */
        --bg-main: var(--surface-secondary);
        --card-bg: var(--surface-primary);
        --card-border: var(--border-primary);
        --card-shadow: var(--shadow-sm);
        --text-muted: var(--text-tertiary);
        --brand-blue: #1E3E62;
        --brand-cyan: #38bdf8;
        --brand-navy: #0B192C;
        --accent-gold: var(--brand-gold);
        --accent-emerald: var(--status-positive);
        --accent-rose: var(--status-critical);
    }

    /* ELIMINATE STREAMLIT NATIVE CHROME (Fixes Chrome Clutter Defect) */
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
        pointer-events: none !important;
        z-index: 999 !important;
    }
    header[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDeployButton"], .stAppDeployButton { display: none !important; }
    
    /* CLEAN SIDEBAR COLLAPSE TOGGLE */
    header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] button,
    div[data-testid="stSidebarCollapsedControl"] {
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        pointer-events: auto !important;
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: var(--text-secondary) !important;
        background-color: var(--surface-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: var(--shadow-xs) !important;
        z-index: 999999 !important;
        width: 30px !important;
        height: 30px !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"] svg,
    button[data-testid="stSidebarCollapsedControl"] svg {
        display: block !important;
        fill: currentColor !important;
    }

    /* MAIN CONTAINER & PAGE CANVAS (True 1080p Panoramic Widescreen) */
    .stApp {
        background-color: var(--surface-secondary) !important;
    }
    
    .main .block-container,
    div[data-testid="stAppViewBlockContainer"],
    div.block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1720px !important;
        margin: 0 auto !important;
    }
    
    /* SIDEBAR STYLING (Slim 230px Footprint) */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid var(--border-primary) !important;
        width: 230px !important;
        min-width: 230px !important;
        max-width: 230px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0.5rem !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }

    /* SIDEBAR SECTION LABELS */
    .sidebar-section-title {
        font-size: 10.5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        color: var(--text-tertiary) !important;
        text-transform: uppercase !important;
        margin: 16px 0 6px 0 !important;
    }
    
    .sidebar-section-title:first-child {
        margin-top: 0 !important;
    }

    /* STREAMLIT TAB STYLING OVERRIDE (Luxury Capsule Navigation) */
    div[data-testid="stTabs"] {
        margin-top: 14px;
        margin-bottom: 18px;
    }
    
    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: 1px solid var(--border-primary) !important;
        padding-bottom: 8px !important;
        background: transparent !important;
    }
    
    button[data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        color: var(--text-tertiary) !important;
        padding: 7px 18px !important;
        background: var(--surface-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-full) !important;
        box-shadow: var(--shadow-xs) !important;
        transition: all 150ms ease !important;
    }
    
    button[data-baseweb="tab"]:hover {
        color: var(--brand-primary) !important;
        border-color: var(--brand-gold) !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        font-weight: 600 !important;
        background-color: var(--brand-primary) !important;
        color: #FFFFFF !important;
        border-color: var(--brand-primary) !important;
        box-shadow: 0 2px 6px rgba(11, 25, 44, 0.15) !important;
    }

    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* STREAMLIT SLIDER CONTROLS (Champagne Gold Accents) */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: var(--brand-gold) !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(197, 160, 89, 0.4) !important;
        width: 14px !important;
        height: 14px !important;
    }
    
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {
        background-color: var(--brand-gold) !important;
    }
    
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: var(--brand-primary) !important;
        font-weight: 600 !important;
        font-size: 10.5px !important;
    }

    /* DATAFRAME STYLING */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-md) !important;
        background-color: var(--surface-primary) !important;
    }

    /* BUTTONS */
    button[kind="primary"],
    .stButton > button[kind="primary"] {
        background-color: var(--brand-primary) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        transition: background-color 150ms ease !important;
    }
    
    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        background-color: var(--brand-primary-hover) !important;
    }

    button[kind="secondary"],
    .stButton > button[kind="secondary"] {
        background-color: var(--surface-primary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
    }
    
    button[kind="secondary"]:hover,
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--surface-tertiary) !important;
        border-color: var(--border-interactive) !important;
    }

    /* APP HEADER (Clean, Restrained) */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0 14px 0;
        border-bottom: 1px solid var(--border-primary);
        margin-bottom: 16px;
    }
    
    .header-title-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-logo-badge {
        background: var(--brand-primary);
        color: #ffffff;
        font-size: 18px;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: var(--radius-sm);
    }
    
    .header-title {
        color: var(--text-primary) !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    .header-subtitle {
        color: var(--text-tertiary) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        margin: 2px 0 0 0 !important;
    }

    /* TOP INLINE METRICS (Replaces Rainbow AUM Banner) */
    .aum-banner {
        background: var(--surface-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-md);
        padding: 14px 20px;
        margin-bottom: 16px;
        display: grid;
        grid-template-columns: 1.3fr 1fr 1fr 1fr;
        gap: 20px;
        box-shadow: var(--shadow-xs) !important;
        position: relative;
    }
    
    .aum-stat-item {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .aum-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--text-tertiary) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .aum-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary) !important;
        letter-spacing: -0.01em;
        line-height: 1.2;
        font-variant-numeric: tabular-nums;
    }
    
    .aum-subtext {
        font-size: 12px;
        font-weight: 500;
        margin-top: 3px;
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--text-secondary) !important;
    }
    
    .badge-success-chip {
        background: var(--status-positive-bg) !important;
        color: var(--status-positive) !important;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--status-positive-border);
    }

    /* 1080p PANORAMIC HORIZON KPI CARDS (SLIM 85px FOOTPRINT) */
    .kpi-horizon-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        padding: 12px 18px;
        box-shadow: 0 1px 3px rgba(11, 25, 44, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 85px;
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }
    
    .kpi-horizon-card:hover {
        border-color: var(--brand-gold);
        box-shadow: 0 3px 8px rgba(197, 160, 89, 0.12);
    }
    
    .kpi-horizon-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2px;
    }
    
    .kpi-horizon-title {
        font-size: 10.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-tertiary);
    }
    
    .kpi-horizon-value {
        font-size: 21px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        line-height: 1.15;
        font-variant-numeric: tabular-nums;
    }
    
    .kpi-horizon-subtext {
        font-size: 11px;
        font-weight: 500;
        color: var(--text-quaternary);
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 2px;
    }

    /* REFINED KPI CARDS */
    .kpi-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        box-shadow: var(--shadow-xs);
        transition: border-color 150ms ease;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .kpi-card:hover {
        border-color: var(--border-interactive);
    }
    
    .kpi-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    
    .kpi-card-title {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-tertiary);
    }
    
    .kpi-card-icon {
        color: var(--text-tertiary);
        display: flex;
        align-items: center;
    }
    
    .kpi-card-value {
        font-size: 22px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        line-height: 1.2;
        margin-bottom: 4px;
        font-variant-numeric: tabular-nums;
    }
    
    .kpi-card-footer {
        font-size: 12px;
        font-weight: 400;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 6px;
        padding-top: 6px;
        border-top: 1px solid var(--border-secondary);
    }

    /* STATUS LABELS */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        border-radius: var(--radius-sm);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    
    .status-breach {
        background: var(--status-critical-bg);
        color: var(--status-critical);
        border: 1px solid var(--status-critical-border);
    }
    
    .status-warning {
        background: var(--status-warning-bg);
        color: var(--status-warning);
        border: 1px solid var(--status-warning-border);
    }
    
    .status-healthy {
        background: var(--status-positive-bg);
        color: var(--status-positive);
        border: 1px solid var(--status-positive-border);
    }

    /* WORKFLOW STEPPER RIBBON */
    .workflow-stepper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        padding: 10px 18px;
        margin-bottom: 16px;
        box-shadow: var(--shadow-xs);
    }
    
    .step-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 500;
        color: var(--text-tertiary);
    }
    
    .step-item.step-active {
        color: var(--brand-primary);
        font-weight: 600;
    }
    
    .step-num {
        font-size: 11px;
        font-weight: 700;
        color: var(--text-tertiary);
    }
    
    .step-active .step-num {
        color: var(--brand-primary);
    }
    
    .step-divider {
        flex: 1;
        height: 1px;
        background: var(--border-primary);
        margin: 0 8px;
        max-width: 32px;
    }

    /* CLEAN SECTION HEADERS */
    .exec-section-header {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        margin: 16px 0 8px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ALERT DETECTION BOX */
    .exec-alert-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-left: 3px solid var(--brand-primary);
        border-radius: var(--radius-md);
        padding: 12px 16px;
        margin: 10px 0 14px 0;
    }
    .alert-card-breach {
        border-left-color: var(--status-critical) !important;
        background: var(--status-critical-bg);
    }
    .alert-card-warning {
        border-left-color: var(--status-warning) !important;
        background: var(--status-warning-bg);
    }
    .alert-card-healthy {
        border-left-color: var(--status-positive) !important;
        background: var(--status-positive-bg);
    }

    /* DIAGNOSTIC FINDING ROWS */
    .driver-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-sm);
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .driver-tag {
        font-size: 10.5px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: var(--radius-sm);
        background: var(--surface-tertiary);
        color: var(--text-secondary);
        white-space: nowrap;
    }

    /* RECOMMENDATION ACTION CARDS */
    .rec-action-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: var(--shadow-xs);
    }
    
    .rec-lift-badge {
        background: var(--surface-tertiary);
        border: 1px solid var(--border-primary);
        color: var(--brand-text);
        font-weight: 600;
        font-size: 12px;
        padding: 6px 10px;
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 12px;
    }

    /* GOVERNANCE DISPATCH ACTION BAR */
    .escalate-action-bar {
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        padding: 14px 18px;
        margin-top: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: var(--shadow-xs);
    }

    /* FLOATING CHAT TRIGGER BUTTON (JD COPILOT) */
    div[data-testid="stPopover"],
    div.stPopover,
    .stPopover {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 9999999 !important;
        width: 48px !important;
        height: 48px !important;
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
        width: 48px !important;
        height: 48px !important;
        min-width: 48px !important;
        min-height: 48px !important;
        max-width: 48px !important;
        max-height: 48px !important;
        border-radius: 50% !important;
        background-color: var(--brand-primary) !important;
        background: var(--brand-primary) !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: var(--shadow-md) !important;
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
        transition: transform 150ms ease, opacity 150ms ease !important;
    }

    div[data-testid="stPopover"] button:hover,
    div.stPopover button:hover,
    .stPopover button:hover {
        transform: scale(1.05) !important;
        opacity: 0.95 !important;
        border-color: #ffffff !important;
    }

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

    div[data-testid="stPopover"] button [data-testid="stMarkdownContainer"],
    .stPopover button [data-testid="stMarkdownContainer"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 100% !important;
    }

    div[data-testid="stPopover"] button [data-testid="stMarkdownContainer"] p,
    .stPopover button [data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.05em !important;
        text-align: center !important;
    }

    /* FLOATING CHAT DIALOG WINDOW (Fixes Height Defect) */
    div[data-testid="stPopoverBody"] {
        position: fixed !important;
        bottom: 84px !important;
        right: 24px !important;
        width: 420px !important;
        max-width: calc(100vw - 32px) !important;
        height: 560px !important;
        max-height: 80vh !important;
        overflow-y: auto !important;
        background-color: var(--surface-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow-lg) !important;
        z-index: 99999999 !important;
        padding: 14px 16px !important;
        display: flex !important;
        flex-direction: column !important;
        color: var(--text-primary) !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stPopoverBody"] p,
    div[data-testid="stPopoverBody"] span,
    div[data-testid="stPopoverBody"] div {
        color: var(--text-primary) !important;
    }

    div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {
        background-color: var(--surface-secondary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: var(--radius-sm) !important;
        padding: 8px 12px !important;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] p {
        color: var(--text-primary) !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }

    div[data-testid="stPopoverBody"] button {
        background-color: var(--surface-primary) !important;
        border: 1px solid var(--border-interactive) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        transition: background-color 150ms ease !important;
    }
    
    div[data-testid="stPopoverBody"] button:hover {
        background-color: var(--surface-tertiary) !important;
    }

    div[data-testid="stPopoverBody"] [data-testid="stChatInput"] {
        background-color: var(--surface-primary) !important;
        border: 1px solid var(--border-interactive) !important;
        border-radius: var(--radius-sm) !important;
    }
    
    div[data-testid="stPopoverBody"] [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
    }

    /* RESPONSIVE BREAKPOINTS */
    @media (max-width: 1440px) {
        .main .block-container,
        div[data-testid="stAppViewBlockContainer"],
        div.block-container {
            max-width: 100% !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
    }

    @media (max-width: 992px) {
        .aum-banner {
            grid-template-columns: 1fr 1fr;
            gap: 14px;
        }
    }

    @media (max-width: 640px) {
        .aum-banner {
            grid-template-columns: 1fr;
            gap: 12px;
        }
        div[data-testid="stPopoverBody"] {
            width: calc(100vw - 20px) !important;
            right: 10px !important;
            bottom: 74px !important;
            max-height: 75vh !important;
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

def apply_premium_chart_style(fig, height=280):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=16, r=16, t=36, b=36),
        font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6', size=11),
        title=dict(
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', size=13, color='#1A1F36'),
            x=0.0, xanchor='left', y=0.98, yanchor='top'
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F1F3F6',
            gridwidth=1,
            zerolinecolor='#E8ECF1',
            tickfont=dict(color='#8492A6', size=11, family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
            title_font=dict(color='#4A5468', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F1F3F6',
            gridwidth=1,
            zerolinecolor='#E8ECF1',
            tickfont=dict(color='#8492A6', size=11, family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
            title_font=dict(color='#4A5468', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="left",
            x=0,
            font=dict(color='#4A5468', size=11, family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        hoverlabel=dict(
            bgcolor='#1A1F36',
            font_size=11,
            font_family='Inter, -apple-system, BlinkMacSystemFont, sans-serif',
            font_color='#FFFFFF',
            bordercolor='#1A1F36'
        ),
        colorway=['#1B6EF3', '#8492A6', '#0D9B5C', '#D4850A', '#6E56CF', '#D4380D']
    )
    return fig

apply_chart_style = apply_premium_chart_style

# EXECUTIVE 1080p WIDESCREEN HEADER
st.markdown(f"""
<div class="header-container">
    <div class="header-title-group">
        <div class="header-logo-badge" style="background: var(--brand-primary); color: #fff; width: 34px; height: 34px; border-radius: 6px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(11,25,44,0.2);">
            {get_icon('shield', 18, '#C5A059')}
        </div>
        <div>
            <h1 class="header-title" style="font-size: 16px; font-weight: 700; color: var(--text-primary); margin: 0; line-height: 1.2;">National Bonds Corporation</h1>
            <p class="header-subtitle" style="font-size: 11.5px; color: var(--text-tertiary); margin: 1px 0 0 0; font-weight: 500;">Executive Intelligence Platform &bull; H1 Sovereign Baseline</p>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 16px;">
        <div style="display: flex; align-items: center; gap: 8px; background: var(--surface-primary); border: 1px solid var(--border-primary); padding: 5px 12px; border-radius: 9999px; box-shadow: var(--shadow-xs);">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: #10B981; display: inline-block; box-shadow: 0 0 6px #10B981;"></span>
            <span style="font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.06em;">System Nominal</span>
        </div>
        <div style="font-size: 11.5px; font-weight: 600; color: var(--brand-primary); background: var(--brand-subtle); padding: 5px 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-primary);">
            2026-06 June Cycle
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TOP LEVEL ROLE / OPERATING MODE SWITCHER
st.sidebar.markdown("<div class='sidebar-section-title'>Workspace</div>", unsafe_allow_html=True)
operating_view = st.sidebar.radio(
    "Transformation Operating View",
    options=["Executive Cockpit", "Frontline Knowledge Assistant"],
    index=0,
    label_visibility="collapsed"
)

if "Frontline" in operating_view:
    render_frontline_portal(jd_agent)
else:
    # SIDEBAR CONTROLS (Compact, Shifted Up, No Scrollbar)
    st.sidebar.markdown("<div class='sidebar-section-title'>Analysis Context</div>", unsafe_allow_html=True)
    products_list = list(kpi_df['product_name'].unique())
    selected_product = st.sidebar.selectbox("Select Pilot Product", products_list, index=1)
    
    available_months = sorted(list(kpi_df['month'].unique()))
    selected_cycle = st.sidebar.select_slider(
        "Monitoring Cycle",
        options=available_months,
        value=available_months[-1]
    )
    
    st.sidebar.markdown("<div class='sidebar-section-title'>Governance Thresholds</div>", unsafe_allow_html=True)
    warning_threshold = st.sidebar.slider("Early Warning Deficit (%)", -25, 0, -8, step=1)
    breach_threshold = st.sidebar.slider("Material Breach Deficit (%)", -35, -5, -15, step=1)
    
    # Dynamic Product Metadata
    spec = PRODUCT_SPECS.get(selected_product, PRODUCT_SPECS['Saving Bonds'])
    
    st.sidebar.markdown("<div class='sidebar-section-title'>Product Profile</div>", unsafe_allow_html=True)
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
        dev_color = "#D4380D"
        status_label = "MATERIAL BREACH"
        status_pill_class = "status-breach"
    elif dev <= warning_threshold:
        state_key = 'warning'
        dev_color = "#D4850A"
        status_label = "EARLY WARNING"
        status_pill_class = "status-warning"
    else:
        state_key = 'healthy'
        dev_color = "#0D9B5C"
        status_label = "OPTIMAL"
        status_pill_class = "status-healthy"
    
    # MASTER 1080p HORIZON KPI STRIP (SLIM 85px FOOTPRINT)
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    
    with col_k1:
        st.markdown(f"""
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header">
                <span class="kpi-horizon-title">Total AUM</span>
                <span style="color: var(--brand-gold);">{get_icon('shield', 14, 'var(--brand-gold)')}</span>
            </div>
            <div class="kpi-horizon-value">AED 18.34B</div>
            <div class="kpi-horizon-subtext">
                <span class="badge-success-chip">208% Plan</span> <span>&middot; 154K Verified Savers</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k2:
        st.markdown(f"""
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header">
                <span class="kpi-horizon-title">Net Capital Inflow</span>
                <span style="color: var(--text-tertiary);">{get_icon('dollar-sign', 14, 'var(--text-tertiary)')}</span>
            </div>
            <div class="kpi-horizon-value">AED {net_inflow_aed/1e6:.2f}M</div>
            <div class="kpi-horizon-subtext">
                <span>Gross: AED {prod_data['gross_inflows_aed']/1e6:.1f}M &middot; Redemptions: AED {prod_data['redemptions_aed']/1e6:.1f}M</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k3:
        st.markdown(f"""
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header">
                <span class="kpi-horizon-title">Plan Target</span>
                <span style="color: var(--text-tertiary);">{get_icon('target', 14, 'var(--text-tertiary)')}</span>
            </div>
            <div class="kpi-horizon-value">AED {target_inflow_aed/1e6:.2f}M</div>
            <div class="kpi-horizon-subtext">
                <span style="color: {dev_color}; font-weight: 600;">Variance: AED {abs(net_inflow_aed - target_inflow_aed)/1e6:.2f}M ({dev:+.1f}%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k4:
        delta_icon = get_icon('trending-up', 13, dev_color) if dev >= 0 else get_icon('trending-down', 13, dev_color)
        st.markdown(f"""
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header">
                <span class="kpi-horizon-title">Governance Status</span>
                <span style="color: {dev_color};">{delta_icon}</span>
            </div>
            <div class="kpi-horizon-value" style="color: {dev_color}; font-size: 19px; display: flex; align-items: center; gap: 6px;">
                {status_label}
            </div>
            <div class="kpi-horizon-subtext">
                <span class="status-pill {status_pill_class}">{dev:+.1f}% vs Threshold</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # EXECUTIVE EARLY WARNING ALERT BANNER (INITIATIVE 3)
    render_executive_alert_banner(kpi_df, selected_cycle, warning_threshold, breach_threshold)
    
    tab_pbi, tab_workflow, tab_portfolio, tab_diagnostics, tab_simulator, tab_biweekly, tab_export = st.tabs([
        "Analytics",
        "Workflow", 
        "Portfolio", 
        "Diagnostics", 
        "Simulator",
        "Intelligence",
        "Escalation"
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
                <span class="step-num">01</span> Monitor
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">02</span> Detect
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">03</span> Investigate
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">04</span> Analyse
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">05</span> Recommend
            </div>
            <div class="step-divider"></div>
            <div class="step-item step-active">
                <span class="step-num">06</span> Escalate
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        # ==========================================
        # STEP 1: MONITOR — Continuous Performance Trajectory
        # ==========================================
        st.markdown("<div class='exec-section-header'>1. Monitor: Continuous Performance Trajectory</div>", unsafe_allow_html=True)
        history_df = kpi_df[kpi_df['product_name'] == selected_product].sort_values('month')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history_df['month'], y=history_df['target_inflows_aed']/1e6,
            mode='lines', name='Target Plan',
            line=dict(color='#8492A6', dash='dash', width=2, shape='spline'),
            hovertemplate="<b>%{x} Target:</b> AED %{y:.2f}M<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=history_df['month'], y=history_df['net_inflows_aed']/1e6,
            mode='lines+markers', name='Actual Net Inflow',
            line=dict(color='#1B6EF3', width=2.5, shape='spline'),
            marker=dict(size=5, color='#1B6EF3'),
            fill='tozeroy',
            fillcolor='rgba(27, 110, 243, 0.08)',
            hovertemplate="<b>%{x} Actual:</b> AED %{y:.2f}M<extra></extra>"
        ))
        fig.add_vline(
            x=selected_cycle, line_width=1.5, line_dash="dot", line_color="#D4850A"
        )
        fig = apply_chart_style(fig, height=270)
        fig.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="left", x=0))
        st.plotly_chart(fig, use_container_width=True)
    
        # ==========================================
        # STEP 2: DETECT — Deviation & Anomaly Recognition
        # ==========================================
        st.markdown("<div class='exec-section-header'>2. Detect: Deviation & Anomaly Recognition</div>", unsafe_allow_html=True)
        if state_key == 'breach':
            st.markdown(f"""
            <div class="exec-alert-card alert-card-breach">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {get_icon('alert-circle', 16, '#D4380D')}
                        <strong style="color: var(--status-critical); font-size: 13px; letter-spacing: 0.01em;">Material Deficit Breach Detected</strong>
                    </div>
                    <span class="status-pill status-breach">SHORTFALL {abs(dev):.1f}%</span>
                </div>
                <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5; margin-left: 24px;">
                    <b>{selected_product}</b> breached corporate tolerance in <b>{selected_cycle}</b> with Actual Net <b>AED {net_inflow_aed/1e6:.2f}M</b> vs Target <b>AED {target_inflow_aed/1e6:.2f}M</b> (Deficit: <b style="color: var(--status-critical);">AED {deficit_aed/1e6:.2f}M</b>). Autonomous multi-agent diagnostic triggered.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif state_key == 'warning':
            st.markdown(f"""
            <div class="exec-alert-card alert-card-warning">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {get_icon('alert-triangle', 16, '#D4850A')}
                        <strong style="color: var(--status-warning); font-size: 13px; letter-spacing: 0.01em;">Early Warning Deficit Notice</strong>
                    </div>
                    <span class="status-pill status-warning">DEVIATION {abs(dev):.1f}%</span>
                </div>
                <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5; margin-left: 24px;">
                    <b>{selected_product}</b> net inflow is trending below tolerance limit in <b>{selected_cycle}</b> (Actual: <b>AED {net_inflow_aed/1e6:.2f}M</b> vs Target: <b>AED {target_inflow_aed/1e6:.2f}M</b>). Preemptive diagnostic initiated.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="exec-alert-card alert-card-healthy">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {get_icon('check-circle', 16, '#0D9B5C')}
                        <strong style="color: var(--status-positive); font-size: 13px; letter-spacing: 0.01em;">Performance Stable & On Track</strong>
                    </div>
                    <span class="status-pill status-healthy">AHEAD +{dev:.1f}%</span>
                </div>
                <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5; margin-left: 24px;">
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
        st.markdown("<div class='exec-section-header'>3. Investigate: Channel Flow Variance Attribution</div>", unsafe_allow_html=True)
        st.caption(f"Channel distribution attribution for **{selected_product}** — Primary variance driver: **{worst_channel}** ({worst_var:+.1f}%)")
        
        bar_colors = ['#D4380D' if v < 0 else '#1B6EF3' for v in chan_summary['Channel Variance (%)']]
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
            textfont=dict(size=11, color='#1A1F36', family='Inter, sans-serif'),
            hovertemplate="<b>%{x}</b><br>Variance: %{y:+.1f}%<extra></extra>"
        ))
        fig_ch = apply_chart_style(fig_ch, height=250)
        fig_ch.update_layout(
            yaxis_title="Variance (%)",
            yaxis=dict(range=[y_min, y_max], zeroline=True, zerolinecolor='#E8ECF1', gridcolor='#F1F3F6'),
            xaxis=dict(tickfont=dict(family='Inter, sans-serif', size=11)),
            margin=dict(t=35, b=25, l=40, r=20),
            showlegend=False
        )
        st.plotly_chart(fig_ch, use_container_width=True)
    
        # ==========================================
        # STEP 4: ANALYSE — Specialist Agent Intelligence Findings
        # ==========================================
        st.markdown("<div class='exec-section-header'>4. Analyse: Specialist Agent Intelligence Findings</div>", unsafe_allow_html=True)
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
            <div class="driver-card" style="border-left: 3px solid var(--brand-primary); height: calc(100% - 8px);">
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <span class="driver-tag" style="background: var(--brand-subtle); color: var(--brand-text); align-self: flex-start;">Macro Sensitivity</span>
                    <span style="font-size: 12.5px; color: var(--text-primary); line-height: 1.45;">{spec['macro_sensitivity']}</span>
                    <span style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Audited Source: H1 2026 Executive Performance Review (Slides 30-48).</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # ==========================================
        # STEP 5: RECOMMEND — Actionable Management Options & Projected Recovery
        # ==========================================
        st.markdown("<div class='exec-section-header'>5. Recommend: Actionable Management Options & Projected Recovery</div>", unsafe_allow_html=True)
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
                            <span style="color: var(--brand-primary); font-weight: 700; font-size: 12px; letter-spacing: 0.04em;">OPTION {chr(65+i)}</span>
                            <span style="font-size: 10.5px; font-weight: 600; background: var(--surface-tertiary); padding: 2px 6px; border-radius: 4px; color: var(--text-secondary);">{opt.get('risk', 'Standard')}</span>
                        </div>
                        <strong style="color: var(--text-primary); font-size: 13px; display: block; margin-bottom: 6px; line-height: 1.35;">{opt['title']}</strong>
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
        st.markdown("<div class='exec-section-header'>6. Escalate: Executive Governance & Accountable Decision</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="escalate-action-bar">
            <div style="display: flex; align-items: center; gap: 8px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.45;">
                {get_icon('shield', 16, 'var(--brand-primary)')}
                <span><b>Human-in-the-Loop Governance:</b> Autonomous multi-agent synthesis completed for <b>{selected_product}</b>. Executive sign-off required from GCCO.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # MULTI-AGENT COLLABORATION TRACE (INITIATIVE 3)
        render_multi_agent_trace(selected_product, selected_cycle, dev, state_key)

        col_esc_btn, col_esc_space = st.columns([1.2, 1.8])
        with col_esc_btn:
            if st.button("Dispatch Real-Time Alert to GCCO & Steering Committee", type="primary", use_container_width=True, key="btn_gcco_dispatch_tab1"):
                receipt = dispatch_alert_memo(selected_product, selected_cycle, dev, deficit_aed/1e6, user_name="Jawad Ahmad")
                st.success(f"Alert Dispatched! Receipt: `{receipt['receipt_id']}` | Status: {receipt['delivery_status']} (Corporate SMTP & Teams)")
    
    # ==========================================
    # TAB 2: PORTFOLIO MATRIX
    # ==========================================
    with tab_portfolio:
        st.markdown("<div class='exec-section-header'>Portfolio Performance Matrix (H1 2026 Trajectory)</div>", unsafe_allow_html=True)
        st.caption(f"Commercial trajectory of all 5 pilot products for cycle: {selected_cycle} (Total Company AUM: AED 18.34B)")
        
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
                color_discrete_sequence=['#1B6EF3', '#8492A6']
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
                color_discrete_sequence=['#1B6EF3', '#38bdf8', '#0D9B5C', '#D4850A', '#6E56CF']
            )
            fig_donut = apply_chart_style(fig_donut, height=280)
            st.plotly_chart(fig_donut, use_container_width=True)

        # Row 2 of Portfolio Charts
        col_p3, col_p4 = st.columns([1.1, 1.1])
        with col_p3:
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
                color_discrete_map={'HEALTHY': '#0D9B5C', 'WARNING': '#D4850A', 'BREACH': '#D4380D'}
            )
            fig_scat.update_traces(textposition='top center')
            fig_scat = apply_chart_style(fig_scat, height=280)
            st.plotly_chart(fig_scat, use_container_width=True)

        with col_p4:
            bar_colors = ['#D4380D' if d <= -15 else ('#D4850A' if d <= -8 else '#0D9B5C') for d in cycle_matrix['deviation_pct']]
            short_p_names = [p.split(" (")[0] for p in cycle_matrix['product_name']]
            fig_var = go.Figure(go.Bar(
                x=short_p_names,
                y=cycle_matrix['deviation_pct'],
                marker=dict(color=bar_colors),
                text=[f"{d:+.1f}%" for d in cycle_matrix['deviation_pct']],
                textposition='outside'
            ))
            fig_var.add_hline(y=0, line_dash="solid", line_color="#8492A6", line_width=1)
            fig_var.add_hline(y=warning_threshold, line_dash="dash", line_color="#D4850A", annotation_text="Warning Threshold")
            fig_var.add_hline(y=breach_threshold, line_dash="dash", line_color="#D4380D", annotation_text="Breach Threshold")
            fig_var.update_layout(title="Budget Target Variance Gap by Product (%)", yaxis_title="Variance (%)")
            fig_var = apply_chart_style(fig_var, height=280)
            st.plotly_chart(fig_var, use_container_width=True)
    
    # ==========================================
    # TAB 3: DIAGNOSTICS
    # ==========================================
    with tab_diagnostics:
        st.markdown(f"<div class='exec-section-header'>Customer Analytics: {selected_product}</div>", unsafe_allow_html=True)
        st.caption(f"Calibrated with verified customer database (154,000 Verified Accounts)")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            seg_dist = adopters_df.groupby('customer_segment')[selected_product].sum().reset_index()
            fig_seg = px.pie(
                seg_dist, values=selected_product, names='customer_segment',
                title=f"Holders by Customer Segment: {selected_product}",
                hole=0.42,
                color_discrete_sequence=['#1B6EF3', '#38bdf8', '#0D9B5C', '#D4850A', '#6E56CF']
            )
            fig_seg = apply_chart_style(fig_seg, height=280)
            # Position legend cleanly below chart to avoid collision (Audit Defect #1)
            fig_seg.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="left", x=0))
            st.plotly_chart(fig_seg, use_container_width=True)
            
        with col_d2:
            fig_chan_all = px.bar(
                chan_summary, x='Channel', y='Active_Holders',
                title=f"Active Account Distribution by Channel: {selected_product}",
                color='Channel',
                color_discrete_sequence=['#1B6EF3', '#38bdf8', '#0D9B5C', '#D4850A', '#6E56CF']
            )
            fig_chan_all = apply_chart_style(fig_chan_all, height=280)
            fig_chan_all.update_layout(showlegend=False)
            st.plotly_chart(fig_chan_all, use_container_width=True)
    
        col_d3, col_d4 = st.columns(2)
        with col_d3:
            fig_age = px.histogram(
                adopters_df, x='age', nbins=25,
                title=f"Age Distribution for {selected_product} Base (Peak: 35-45 yrs)",
                color_discrete_sequence=['#1B6EF3']
            )
            fig_age = apply_chart_style(fig_age, height=260)
            st.plotly_chart(fig_age, use_container_width=True)

        with col_d4:
            fig_box = px.box(
                adopters_df, x='customer_segment', y='income_aed',
                color='customer_segment',
                title=f"Monthly Income Distribution by Segment (AED)",
                color_discrete_sequence=['#1B6EF3', '#0D9B5C', '#D4850A']
            )
            fig_box = apply_chart_style(fig_box, height=260)
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
    
    # ==========================================
    # TAB 4: SIMULATOR
    # ==========================================
    with tab_simulator:
        st.markdown(f"<div class='exec-section-header'>Governance & Recovery Action Simulator</div>", unsafe_allow_html=True)
        st.caption("Simulate the impact of executing approved Q3 management interventions before submitting to GCCO.")
        
        col_sim_ctrl, col_sim_view = st.columns([1, 1])
        
        with col_sim_ctrl:
            st.markdown(f"<p style='font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px;'>Select Interventions to Execute for {selected_product}:</p>", unsafe_allow_html=True)
            
            apply_opt_a = st.checkbox(f"Option A: {rec_options[0]['title']}", value=True)
            apply_opt_b = st.checkbox(f"Option B: {rec_options[1]['title']}", value=False)
            apply_opt_c = st.checkbox(f"Option C: {rec_options[2]['title']}", value=False)
            
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
            <div class="kpi-card" style="border: 1px solid var(--border-primary); background: var(--surface-primary);">
                <div class="kpi-card-header">
                    <span class="kpi-card-title">Projected Next-Cycle Recovery Lift</span>
                    <span class="status-pill status-healthy">Simulation Active</span>
                </div>
                <div class="kpi-card-value" style="color: var(--status-positive) !important;">+AED {total_lift/1e6:.2f}M</div>
                <div class="kpi-card-footer" style="flex-direction: column; align-items: flex-start; gap: 4px;">
                    <span>Original Actual: <b>AED {net_inflow_aed/1e6:.2f}M ({dev:+.1f}%)</b></span>
                    <span>Simulated Net Inflow: <b>AED {simulated_net_inflow/1e6:.2f}M</b></span>
                    <span>Projected Variance: <b style="color: {'var(--status-positive)' if simulated_variance >= -8 else 'var(--status-warning)'};">{simulated_variance:+.1f}%</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig_sim = go.Figure(data=[
                go.Bar(name='Current Actual', x=[selected_product], y=[net_inflow_aed/1e6], marker_color='#D4380D' if dev <= breach_threshold else '#D4850A'),
                go.Bar(name='Simulated Recovery', x=[selected_product], y=[simulated_net_inflow/1e6], marker_color='#0D9B5C'),
                go.Bar(name='Target Budget', x=[selected_product], y=[target_inflow_aed/1e6], marker_color='#8492A6')
            ])
            fig_sim = apply_chart_style(fig_sim, height=240)
            fig_sim.update_layout(barmode='group', title="Projected Inflow vs Target (AED M)")
            st.plotly_chart(fig_sim, use_container_width=True)
    
    # ==========================================
    # TAB 5: BI-WEEKLY REPORT
    # ==========================================
    with tab_biweekly:
        render_biweekly_report_tab(selected_cycle)

    # ==========================================
    # TAB 6: GCCO ESCALATION BRIEFING
    # ==========================================
    with tab_export:
        st.markdown("<div class='exec-section-header'>GCCO Escalation Briefing Dossier</div>", unsafe_allow_html=True)
        st.caption("Executive briefing dossier referencing audited H1 performance ground truth.")
        
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
        <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-radius: var(--radius-md); padding: 18px 22px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; border-bottom: 1px solid var(--border-primary); padding-bottom: 10px;">
                <div>
                    <h3 style="margin: 0; color: var(--text-primary); font-size: 15px; font-weight: 700; letter-spacing: -0.01em;">NATIONAL BONDS CORPORATION</h3>
                    <span style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em;">Executive Early Warning & Remediation Briefing</span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 12px; font-weight: 500; color: var(--text-tertiary);">{datetime.now().strftime('%d %B %Y')}</span><br>
                    <span class="status-pill {status_pill_class}">{status_label}</span>
                </div>
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 12.5px;">
                <tr>
                    <td style="padding: 4px 8px 4px 0; color: var(--text-tertiary); font-weight: 600; width: 12%;">TO:</td>
                    <td style="padding: 4px 16px 4px 0; color: var(--text-primary); font-weight: 500; width: 38%;">Group Chief Commercial Officer (GCCO)</td>
                    <td style="padding: 4px 8px 4px 0; color: var(--text-tertiary); font-weight: 600; width: 14%;">PRODUCT:</td>
                    <td style="padding: 4px 0; color: var(--text-primary); font-weight: 600; width: 36%;">{selected_product}</td>
                </tr>
                <tr>
                    <td style="padding: 4px 8px 4px 0; color: var(--text-tertiary); font-weight: 600;">FROM:</td>
                    <td style="padding: 4px 16px 4px 0; color: var(--text-primary); font-weight: 500;">AI Product Intelligence & Early Warning</td>
                    <td style="padding: 4px 8px 4px 0; color: var(--text-tertiary); font-weight: 600;">CYCLE:</td>
                    <td style="padding: 4px 0; color: var(--text-primary); font-weight: 600;">{selected_cycle}</td>
                </tr>
                <tr>
                    <td style="padding: 4px 8px 4px 0; color: var(--text-tertiary); font-weight: 600;">ACTUAL NET:</td>
                    <td style="padding: 4px 16px 4px 0; color: var(--text-primary); font-weight: 600; font-variant-numeric: tabular-nums;">AED {net_inflow_aed/1e6:.2f}M (Target: AED {target_inflow_aed/1e6:.2f}M)</td>
                    <td style="padding: 4px 8px 4px 0; color: var(--text-tertiary); font-weight: 600;">VARIANCE GAP:</td>
                    <td style="padding: 4px 0; color: {dev_color}; font-weight: 700; font-variant-numeric: tabular-nums;">{dev:+.1f}% (Deficit: AED {deficit_aed/1e6:.2f}M)</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
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
                label="Download Boardroom PDF Escalation Dossier",
                data=pdf_memo_bytes,
                file_name=f"GCCO_Escalation_Dossier_{selected_product.replace(' ', '_')}_{selected_cycle}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            with st.expander("Export Raw Text / Markdown (.txt)", expanded=False):
                st.download_button(
                    label="Download Raw Text (.txt)",
                    data=briefing_text,
                    file_name=f"GCCO_Briefing_{selected_product.replace(' ', '_')}_{selected_cycle}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        with col_exp2:
            if st.button("Dispatch Official Escalation to GCCO", type="primary", use_container_width=True, key="btn_dispatch_tab_export"):
                receipt = dispatch_alert_memo(selected_product, selected_cycle, dev, deficit_aed/1e6, user_name="Jawad Ahmad")
                st.success(f"Dispatched via Secure Exchange & MS Teams! Receipt: `{receipt['receipt_id']}`")
    
    # ==============================================================================
# FLOATING INTELLIGENCE COPILOT ("JD")
# ==============================================================================

# Initialize Chat Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I am **JD**, your National Bonds Financial Intelligence Assistant. Ask me anything about Portfolio Performance, Product KPIs, Early Warnings, or Q3 Management Interventions."}
    ]

has_started = len(st.session_state.chat_messages) > 1

# Render Floating Chat Trigger using Streamlit Popover
with st.popover("AI", help="Click to open Financial Intelligence Assistant"):
    # Header Bar with Status and Compact Reset Button
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; padding: 2px 0;">
            <span style="font-weight: 700; font-size: 14px; color: var(--brand-primary);">Financial Intelligence Assistant</span>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("Reset", key="chat_reset_btn", help="Clear conversation and start fresh", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Conversation reset. How can I help you analyze National Bonds data today?"}
            ]
            st.rerun()
            
    st.markdown("<hr style='margin: 6px 0 8px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)
    
    # Show Preset Questions ONLY before customer asks first question
    if not has_started:
        st.markdown("<p style='font-size: 12px; font-weight: 600; color: var(--text-tertiary); margin: 0 0 6px 0;'>Suggested Inquiries:</p>", unsafe_allow_html=True)
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("Portfolio Budget Performance", use_container_width=True, key="btn_q1"):
                query = "How much portfolio budget did we have achieved?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("Saving Bonds Variance", use_container_width=True, key="btn_q2"):
                query = "Why did Saving Bonds drop -26% YoY?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("Second Salary Overview", use_container_width=True, key="btn_q3"):
                query = "What is the status and average ticket of Second Salary?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
        with col_q2:
            if st.button("Total AUM & Fresh Sales", use_container_width=True, key="btn_q4"):
                query = "What is our Total AUM and H1 Sales breakdown?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("Term Sukuk Growth", use_container_width=True, key="btn_q5"):
                query = "How did Term Sukuk perform in H1 2026?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            if st.button("Customer Demographics Mix", use_container_width=True, key="btn_q6"):
                query = "What is the Emirati vs Expat customer demographic mix?"
                st.session_state.chat_messages.append({"role": "user", "content": query})
                reply = jd_agent.answer(query, api_key=st.session_state.get('llm_api_key'))
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
        st.markdown("<hr style='margin: 6px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)

    # Message History Rendering
    if not has_started:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"], avatar="assistant" if msg["role"] == "assistant" else "user"):
                st.markdown(msg["content"])
    else:
        chat_container = st.container(height=390)
        with chat_container:
            for msg in st.session_state.chat_messages:
                with st.chat_message(msg["role"], avatar="assistant" if msg["role"] == "assistant" else "user"):
                    st.markdown(msg["content"])
            st.markdown("<div id='chat-end-marker' style='height: 1px; margin-top: 4px;'></div>", unsafe_allow_html=True)
        
    # Auto-Scroll and Layout Alignment JavaScript
    st.html(
        """
        <script>
        (function() {
            function enforceLayout() {
                try {
                    var doc = window.parent.document;
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
    if user_prompt := st.chat_input("Ask Financial Intelligence Assistant a question..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        jd_reply = jd_agent.answer(user_prompt, api_key=st.session_state.get('llm_api_key'))
        st.session_state.chat_messages.append({"role": "assistant", "content": jd_reply})
        st.rerun()
