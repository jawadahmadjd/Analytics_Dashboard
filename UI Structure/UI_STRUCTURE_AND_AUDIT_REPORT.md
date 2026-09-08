# National Bonds Corporation — Executive AI Transformation Prototype
## Comprehensive Desktop UI Visual Audit, Component Placement Matrix & Design System Report

**Document Reference:** `NBC-DESKTOP-UI-AUDIT-2026-V1`  
**System Evaluated:** National Bonds Corporation — Executive Intelligence & Early Warning System (Initiatives 1, 2, and 3)  
**Primary Target Platform:** **Desktop Executive Workstation (1920 x 1080 / 16:9 Wide-Canvas Display)**  
**Host URL:** `http://localhost:8501/`  
**Evaluation Date:** September 8, 2026  
**Audit Author:** Product AI Solutions & Design Engineering  
**Screenshots Repository:** [`UI Structure/`](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure) (36 High-Resolution Visual Captures + Telemetry JSON)

---

## Executive Summary (Desktop Focus)

This report provides an exhaustive, component-level UI/UX visual audit and architectural placement matrix for the **Desktop Executive Experience** of the **National Bonds Corporation Executive Intelligence & Early Warning System**.

The platform serves C-suite executives, Group Chief Commercial Officer (GCCO) leadership, Asset-Liability Committee (ALCO) members, and Relationship Managers across two primary operating modes:
1. **Executive Cockpit (Initiatives 3 & 2):** High-density financial command center featuring an Executive Alert Center, 4 high-level KPI cards, 7 functional sub-systems (PowerBI Analytics Studio with 8 multi-dimensional charts, 6-Step Autonomous Agentic Workflow, 5-Product Portfolio Matrix, Dynamic Diagnostic Engine, Live Action Simulator, Bi-Weekly Product & Market Intelligence Reporting, and GCCO Escalation Briefing).
2. **Frontline Knowledge Assistant (Initiative 1):** Operational single source of truth for branch network and sales teams featuring certified circular retrieval, Sharia fatwa validation, an escalation queue, and an immutable compliance audit trail.
3. **Cross-Cutting JD Copilot:** Persistent floating conversational intelligence assistant anchored to the bottom-right of the desktop canvas.

> [!NOTE]
> **Desktop Baseline Scope:** This audit and placement matrix evaluates the desktop viewport (**1920 x 1080** and continuous vertical layout). Mobile and tablet adaptations are deferred to a dedicated preview section at the very end of this document (**Section 8: Phase 2 Consideration**).

### Desktop Visual Audit Rating: **8.8 / 10 (High-Impact Institutional Desktop Cockpit)**

* **Key Strengths:** Outstanding executive visual presence, institutional color tokens (Navy `#0f172a`, Brand Blue `#0284c7`, Emerald `#10b981`), high information density tailored for executive decisioning, authentic H1 2026 audited ground truth, and clear separation between Executive Cockpit and Frontline personas.
* **Core Desktop Deficiencies Identified:** 
  1. **Plotly Chart Legend-Title Collisions:** Overlapping text nodes on multi-series charts (specifically the Portfolio Matrix and Diagnostic Engine).
  2. **Typography Inheritance Divergence:** Streamlit core markdown falls back to `Source Sans` while custom UI components render with `Plus Jakarta Sans`.
  3. **Streamlit Native Header Clutter:** Native "Deploy" and hamburger icons compete with the custom branded executive header bar.
  4. **JD Copilot Popover Vertical Space:** Suggestion chips and message history push input controls downward on compact desktop heights (< 900px).

---

## 1. Master Desktop Visual Screen Catalog & Screenshot Inventory

All visual captures have been recorded at **1920 x 1080 Viewport (Above-the-Fold)** and **Full-Height Continuous Render** for the Desktop environment, located in [`UI Structure/`](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure).

| # | Screen / State Name | Capture Type | File Name | Link | Dimensions | Core Desktop UI Content Captured |
|---|---|---|---|---|---|---|
| **01** | PowerBI Studio — Overview | Viewport (1080p) | `01_Executive_Cockpit_PowerBI_Studio_Top.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/01_Executive_Cockpit_PowerBI_Studio_Top.png) | 1920 x 1080 | Global Header, AUM Ticker (18.34B), Alert Banner, 4 Overview KPIs, PowerBI Hero, Slicers, 4 Sliced Metric Cards |
| **02** | PowerBI Studio — Full Canvas | Full Height | `01b_Executive_Cockpit_PowerBI_Studio_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/01b_Executive_Cockpit_PowerBI_Studio_FullPage.png) | 1920 x 2953 | Complete PowerBI view including all 8 charts: Waterfall, Sunburst, BCG Matrix, Macro Correlation, Heatmap, Monte Carlo Cone, Funnel, Matrix |
| **03** | PowerBI Studio — Charts Mid | Viewport Scroll | `02_Executive_Cockpit_PowerBI_Studio_Charts.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/02_Executive_Cockpit_PowerBI_Studio_Charts.png) | 1920 x 1080 | Zoomed view of Cashflow Waterfall, AUM Sunburst, and 4-Quadrant BCG Matrix |
| **04** | PowerBI Studio — Analytics Lower | Viewport Scroll | `03_Executive_Cockpit_PowerBI_Studio_Table.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/03_Executive_Cockpit_PowerBI_Studio_Table.png) | 1920 x 1080 | 18-Month Deviation Heatmap, Monte Carlo 95% Confidence Cone, Lifecycle Funnel, Segment Channel Cross-Tab |
| **05** | 6-Step Agentic Workflow | Viewport (1080p) | `04_Executive_Cockpit_Agentic_Workflow_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/04_Executive_Cockpit_Agentic_Workflow_Viewport.png) | 1920 x 1080 | Stepper ribbon (01 Monitor to 06 Escalate), Performance Trajectory spline chart, Target vs Actual curve |
| **06** | 6-Step Agentic Workflow | Full Height | `04_Executive_Cockpit_Agentic_Workflow_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/04_Executive_Cockpit_Agentic_Workflow_FullPage.png) | 1920 x 2480 | Complete 6 steps: Anomaly Detection banner, Deep-Dive Investigation telemetry, Root Cause decomposition, Recommendation cards, GCCO dispatch trigger |
| **07** | 5-Product Portfolio Matrix | Viewport (1080p) | `05_Executive_Cockpit_Portfolio_Matrix_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/05_Executive_Cockpit_Portfolio_Matrix_Viewport.png) | 1920 x 1080 | Multi-product tabular comparison, Gross vs Redemptions, Variance % status badges, Target Budget bar chart |
| **08** | 5-Product Portfolio Matrix | Full Height | `05_Executive_Cockpit_Portfolio_Matrix_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/05_Executive_Cockpit_Portfolio_Matrix_FullPage.png) | 1920 x 1940 | Full audited ground truth table, Net Inflow vs Target grouped bars, AUM concentration donut chart |
| **09** | Dynamic Diagnostic Engine | Viewport (1080p) | `06_Executive_Cockpit_Diagnostic_Engine_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/06_Executive_Cockpit_Diagnostic_Engine_Viewport.png) | 1920 x 1080 | Customer Segment Donut, Channel Distribution Bar, Selected Product breakdown |
| **10** | Dynamic Diagnostic Engine | Full Height | `06_Executive_Cockpit_Diagnostic_Engine_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/06_Executive_Cockpit_Diagnostic_Engine_FullPage.png) | 1920 x 2050 | Complete diagnostics: Age distribution bar, Monthly income vs segment scatter plot, root-cause attribution |
| **11** | Live Action Simulator | Viewport (1080p) | `07_Executive_Cockpit_Live_Simulator_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/07_Executive_Cockpit_Live_Simulator_Viewport.png) | 1920 x 1080 | Management intervention checkboxes, Execution efficiency slider, Recovery Lift summary card, Projected Inflow chart |
| **12** | Live Action Simulator | Full Height | `07_Executive_Cockpit_Live_Simulator_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/07_Executive_Cockpit_Live_Simulator_FullPage.png) | 1920 x 1850 | Complete simulator state: Variance gap closing telemetry, interactive sensitivity re-run |
| **13** | Bi-Weekly Intelligence Report | Viewport (1080p) | `08_Executive_Cockpit_BiWeekly_Report_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/08_Executive_Cockpit_BiWeekly_Report_Viewport.png) | 1920 x 1080 | Official Memo Header (Ref: NBC-BIWEEKLY-INTEL-202606), 4 Macro cards (Base Rate 4.65%, Savings Index 121 Pts) |
| **14** | Bi-Weekly Intelligence Report | Full Height | `08_Executive_Cockpit_BiWeekly_Report_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/08_Executive_Cockpit_BiWeekly_Report_FullPage.png) | 1920 x 2620 | Full executive memorandum: Commercial Trajectory charts, Product Narrative, ALCO Sign-off status, PDF generation trigger |
| **15** | GCCO Escalation Briefing | Viewport (1080p) | `09_Executive_Cockpit_GCCO_Briefing_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/09_Executive_Cockpit_GCCO_Briefing_Viewport.png) | 1920 x 1080 | Escalation Routing Table (TO: GCCO, PRODUCT: Saving Bonds, DEFICIT: AED 5.82M), Memo container |
| **16** | GCCO Escalation Briefing | Full Height | `09_Executive_Cockpit_GCCO_Briefing_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/09_Executive_Cockpit_GCCO_Briefing_FullPage.png) | 1920 x 2420 | Complete confidential escalation dossier: Monospace executive brief, Remediation plan, Multi-agent audit trail |
| **17** | JD Copilot Floating Chat Modal | Popover Open | `10_Executive_Cockpit_JD_Copilot_Chat_Open.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/10_Executive_Cockpit_JD_Copilot_Chat_Open.png) | 1920 x 1080 | Circular bottom-right trigger, expanded popover modal (380x600), LIVE AI badge, 6 Suggested Inquiries chips, Reset CTA |
| **18** | JD Copilot Interactive Answer | Chat Response | `10b_Executive_Cockpit_JD_Copilot_Answer.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/10b_Executive_Cockpit_JD_Copilot_Answer.png) | 1920 x 1080 | User query active state, conversational response layout, query input bar |
| **19** | Frontline Knowledge Console | Viewport (1080p) | `11_Frontline_Portal_Ask_Assistant_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/11_Frontline_Portal_Ask_Assistant_Viewport.png) | 1920 x 1080 | Frontline Hero ("Quick Win"), Persona badge ("Ahmed • Relationship Manager"), 4 Operational cards, Query Console |
| **20** | Frontline Knowledge Console | Full Height | `11_Frontline_Portal_Ask_Assistant_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/11_Frontline_Portal_Ask_Assistant_FullPage.png) | 1920 x 1850 | Complete Frontline Tab 0: 6 real-world scenario prompt buttons, Freeform text query input, Query Base button |
| **21** | Frontline Grounded Answer View | Answer Viewport | `11b_Frontline_Portal_Answer_Grounded_View.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/11b_Frontline_Portal_Answer_Grounded_View.png) | 1920 x 1080 | Zero-Hallucination verified ground truth banner, confidence rating (99.4%), retrieval SLA (1.1s) |
| **22** | Frontline Grounded Answer Full | Full Height | `11b_Frontline_Portal_Answer_Grounded_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/11b_Frontline_Portal_Answer_Grounded_FullPage.png) | 1920 x 2050 | Complete grounded answer: Official circular citation (2026/04 Clause 3.2), Sharia Fatwa approval (2026/SH-09), Copy Citation CTA |
| **23** | Approved Document Inventory | Viewport (1080p) | `12_Frontline_Portal_Document_Inventory_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/12_Frontline_Portal_Document_Inventory_Viewport.png) | 1920 x 1080 | Product Filter dropdown, Certified circular cards with "APPROVED" green status chips, Document metadata |
| **24** | Approved Document Inventory | Full Height | `12_Frontline_Portal_Document_Inventory_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/12_Frontline_Portal_Document_Inventory_FullPage.png) | 1920 x 3650 | Complete inventory of 10 official documents (Booster Plan, Second Salary, Saving Bonds, Rewards Program, AML/KYC, etc.) |
| **25** | Escalation Queue Viewport | Viewport (1080p) | `13_Frontline_Portal_Escalations_Queue_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/13_Frontline_Portal_Escalations_Queue_Viewport.png) | 1920 x 1080 | Ticket header, ESC-2026-3041 card, Pending Product Review badge, User: Ahmed (RM) |
| **26** | Escalation Queue Full Page | Full Height | `13_Frontline_Portal_Escalations_Queue_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/13_Frontline_Portal_Escalations_Queue_FullPage.png) | 1920 x 1850 | Complete escalation ticket queue: Query details, Escalation reason (Draft Circular 2026/Promo-X under review), Assigned leads |
| **27** | Compliance & InfoSec Audit | Viewport (1080p) | `14_Frontline_Portal_Compliance_Audit_Viewport.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/14_Frontline_Portal_Compliance_Audit_Viewport.png) | 1920 x 1080 | 4 SLA Metrics (100% Grounding, 0.82s SLA, 100% Fatwa verification, PASSED Audit SLA), Product Inquiry Donut |
| **28** | Compliance & InfoSec Audit | Full Height | `14_Frontline_Portal_Compliance_Audit_FullPage.png` | [View Image](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/14_Frontline_Portal_Compliance_Audit_FullPage.png) | 1920 x 2250 | Complete compliance audit view: Intraday velocity curve, Immutable log table with timestamps, user roles, queries, and latencies |

---

## 2. Desktop Placement & Computed Geometry Matrix (1920 x 1080)

The table below presents the exact coordinate offsets, bounding boxes, layout engines, and computed styles on a standard **1920 x 1080 Desktop Viewport**, as extracted by automated browser telemetry:

```
+---------------------------------------------------------------------------------------------------------------+
| SIDEBAR (0 to 300px)    |  MAIN CONTENT CANVAS (316px to 1904px, Width: 1588px)                               |
|                         |  +-------------------------------------------------------------------------------+  |
| [Logo & Brand]          |  | Header Container (Y: 19px, H: 99px, W: 1428px)                                |  |
| [Operating View Radio]  |  | Title: 23px / 800 | Subtitle: 13px / 600 | AUM Ticker (4 Stats)             |  |
| [Product Selectbox]     |  +-------------------------------------------------------------------------------+  |
| [Cycle Slider (2026-06)]|  | Executive Alert Center Banner (Y: 238px, H: 102px, W: 1428px)                  |  |
| [Threshold Sliders]     |  +-------------------------------------------------------------------------------+  |
| [Product Profile Card]  |  | 4 Overview KPI Cards (Y: 386px, H: 132px, 4x Columns of W: 345px)             |  |
|                         |  +-------------------------------------------------------------------------------+  |
|                         |  | 7 Navigation Tabs Container (Y: 551px, H: 40px)                                |  |
|                         |  | [PowerBI Studio] [Workflow] [Portfolio] [Diagnostic] [Simulator] [Memo] [GCCO]|  |
|                         |  +-------------------------------------------------------------------------------+  |
|                         |  | Tab Panel Content Area (Y: 607px to 2953px)                                    |  |
|                         |  |                                                                                |  |
|                         |  +-------------------------------------------------------------------------------+  |
|                         |                                                               [JD Copilot Avatar]   |
+---------------------------------------------------------------------------------------------------------------+
```

### Detailed Coordinate and Dimension Table

| Component Name | DOM Selector | X (px) | Y (px) | Width (px) | Height (px) | Layout Engine | Computed Background & Border | Computed Typography |
|---|---|---|---|---|---|---|---|---|
| **App Header Bar** | `.header-container` | `396` | `19` | `1428` | `99` | `flex: row, space-between, align-center` | `background: transparent; border-bottom: 1px solid rgba(148,163,184,0.2)` | `Plus Jakarta Sans` / `Source Sans`, 16px |
| **App Title** | `.header-title` | `454` | `19` | `397` | `64` | `display: block` | `background: transparent; border: none` | `23px`, Weight `800`, `#0f172a`, Line: `27.6px`, Letter: `-0.69px` |
| **App Subtitle** | `.header-subtitle` | `454` | `85` | `397` | `21` | `display: block` | `background: transparent; border: none` | `13px`, Weight `600`, `#64748b`, Line: `20.8px` |
| **Sidebar Container** | `section[data-testid="stSidebar"]` | `0` | `0` | `300` | `1080` | `display: block, z-index: 999991` | `background: #f0f2f6; border: none` | `Plus Jakarta Sans`, 16px, Weight `400` |
| **Sidebar Mode Radio** | `div[data-testid="stRadio"]` | `30` | `106` | `240` | `90` | `display: block` | `background: transparent` | `14px`, Weight `600`, Line: `22.4px` |
| **Sidebar Product Select**| `section[data-testid="stSidebar"] selectbox`| `30` | `235` | `240` | `42` | `display: block` | `background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px` | `14px`, `#0f172a` |
| **Sidebar Cycle Slider**| `div[data-testid="stSlider"]` | `30` | `340` | `240` | `40` | `display: block` | `background: transparent; accent: #ef4444` | `13px`, Weight `700`, `#ef4444` |
| **AUM Stat Card** | `.aum-stat-item` | `419` | `150` | `424` | `72` | `flex: column, justify-center` | `background: transparent; border: none` | `Source Sans`, 16px |
| **AUM Stat Label** | `.aum-label` | `419` | `150` | `424` | `18` | `flex: row, align-center, gap: 5px` | `background: transparent; border: none` | `11px`, Weight `700`, `#64748b`, Letter: `0.66px` |
| **AUM Stat Value** | `.aum-value` | `419` | `170` | `424` | `24` | `display: block` | `background: transparent; border: none` | `22px`, Weight `800`, `#0f172a`, Letter: `-0.44px` |
| **Alert Center Banner**| `.exec-alert-card` | `396` | `238` | `1428` | `102` | `display: block, margin: 10px 0 16px` | `background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px` | `Source Sans`, 14px, Weight `600` |
| **Alert Action CTA** | Action Pill Badge | `1682` | `252` | `126` | `32` | `flex: row, align-center` | `background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-radius: 8px` | `11.5px`, Weight `800`, `#ef4444`, Letter: `0.05em` |
| **Overview KPI Card** | `.kpi-card` | `396` | `386` | `345` | `132` | `flex: column, space-between` | `background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; shadow: 0 4px 20px -2px rgba(0,0,0,0.05)` | `Source Sans` / `Plus Jakarta Sans`, 16px |
| **Overview KPI Value**| `.kpi-card-value` | `417` | `438` | `303` | `29` | `display: block` | `background: transparent` | `26px`, Weight `800`, `#0f172a`, Letter: `-0.52px` |
| **Status Pill Badge** | `.status-pill` | `1682` | `273` | `121` | `26` | `flex: row, align-center, gap: 5px` | `background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239,68,68,0.3); border-radius: 20px` | `11.5px`, Weight `700`, `#ef4444`, Letter: `0.345px` |
| **Navigation Tab Bar** | `div[data-testid="stTabs"]` | `396` | `551` | `1428` | `2378` | `display: block` | `background: transparent; border: none` | `Plus Jakarta Sans`, 14px |
| **Navigation Tab Item**| `div[data-testid="stTab"]` | `396` | `551` | `168` | `40` | `flex: row, align-center` | `background: transparent; border-bottom: 2px solid transparent` | `14px`, Weight `500` (Inactive) / `700` (Active) |
| **PowerBI Hero Banner**| `div[style*="rgba(15, 23, 42"]` | `396` | `607` | `1428` | `171` | `display: block, margin-bottom: 20px` | `background: linear-gradient(135deg, #0f172a, #1e293b); border: 1px solid rgba(2,132,199,0.4); border-radius: 12px; shadow: 0 8px 32px rgba(0,0,0,0.25)` | Title: `23px`, Weight `800`, `#f8fafc`; Sub: `13px`, `#94a3b8` |
| **Frontline Hero Banner**| `.frontline-hero` | `396` | `238` | `1428` | `148` | `display: block, margin-bottom: 20px` | `background: linear-gradient(135deg, rgba(2,132,199,0.08), rgba(14,165,233,0.04)); border: 1px solid rgba(2,132,199,0.2); border-radius: 12px` | Title: `22px`, Weight `800`, `#0f172a`; Sub: `13.5px`, `#475569` |
| **Active Persona Card**| `div[style*="Active Frontline"]` | `1540` | `252` | `260` | `90` | `flex: column, align-right` | `background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; shadow: 0 4px 20px -2px rgba(0,0,0,0.05)` | Label: `11px`, `#0284c7`; Name: `14px`, Weight `800`, `#0f172a` |
| **JD Floating Launcher**| `div[data-testid="stPopover"]` | `1840` | `1000` | `56` | `56` | `fixed: bottom 20px, right 20px; z-index: 999999` | `background: #0284c7; border: 2px solid #ffffff; border-radius: 50%; shadow: 0 8px 24px rgba(2,132,199,0.4)` | Icon: `24px` |
| **JD Chat Popover Modal**| `div[data-testid="stPopoverBody"]` | `1420` | `430` | `460` | `560` | `position: absolute; z-index: 999999` | `background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; shadow: 0 20px 40px rgba(0,0,0,0.15)` | Headers: `14.5px`, Weight `800`, `#0284c7`; Text: `13px` |
| **Main Content Canvas**| `div.block-container` | `316` | `0` | `1588` | `2953` | `display: block; padding: 3.2px 80px 24px` | `background: transparent; max-width: 98%` | `Plus Jakarta Sans` |

---

## 3. Desktop Design System Tokens & Foundations

### 3.1 Curated Color Palette
* **Brand Primary:** `#0284c7` (Sky Blue) — Brand badges, interactive elements, tabs, button accents.
* **Brand Secondary:** `#0ea5e9` (Vibrant Cyan) — Gradients, live telemetry chips.
* **Executive Navy:** `#0f172a` — Headings, high-contrast dark cards, PowerBI hero banner.
* **Semantic Status Indicators:**
  - **Optimal (Healthy):** `#10b981` (Emerald) — Net growth, 167% sales targets, zero-hallucination badges.
  - **Early Warning:** `#f59e0b` (Amber Gold) — Deviations between `-8%` and `-15%`.
  - **Material Breach:** `#ef4444` / `#f43f5e` (Crimson / Rose) — Deviations exceeding `-15%` (e.g. Second Salary `-29.8%`).
* **Neutral Grays:** `#ffffff` (Card Surface), `#f8fafc` (Page Background), `#e2e8f0` (Border), `#64748b` (Muted), `#475569` (Secondary Text).

### 3.2 Desktop Typography Scale
* **Display / Big Metric:** `26px` | Weight `800` | Line Height `28.6px` | Letter Spacing `-0.52px`
* **Page & Banner Titles:** `22px` - `23px` | Weight `800` | Line Height `27.6px` | Letter Spacing `-0.02em`
* **Section Headers (H2/H3):** `17px` - `18px` | Weight `700` | Line Height `24px`
* **Card Titles & Tab Text:** `14px` | Weight `700` (Active) / `500` (Inactive) | Line Height `22.4px`
* **Body Text:** `13px` - `13.5px` | Weight `400` / `500` | Line Height `21px`
* **Micro-Caps & Status Chips:** `11px` - `11.5px` | Weight `800` | Letter Spacing `0.05em` | Text-transform: `uppercase`
* **Audit Monospace:** `12px` | `JetBrains Mono`, `monospace` | Weight `500`

---

## 4. Desktop Component Deep Dive by Section

### 4.1 Executive Cockpit (Tabs 1 to 7)

#### Tab 1: PowerBI Analytics Studio
* **Hero Banner:** Full-width container (`1428px` wide, `171px` high) displaying AUM (`AED 18.34B`) and active verified customer metrics.
* **Interactive Slicers:** 4-column filter bar providing real-time slicing across 18 reporting months, 5 product families, customer tiers, and acquisition channels.
* **8 Multi-Dimensional Visualizations:**
  1. *Cashflow Waterfall Bridge:* High-visibility inflow vs outflow bar bridge.
  2. *AUM Allocation Sunburst:* Interactive drill-down into tenor duration and customer volume bands.
  3. *BCG Strategic Matrix:* Bubble chart correlating annualized yields against net growth.
  4. *Macro Correlation Combo:* Net inflows juxtaposed against CBUAE Base Rate (4.65%) and 3M EIBOR (4.52%).
  5. *18-Month Performance Heatmap:* Cross-temporal deviation matrix.
  6. *Monte Carlo Predictive Cone:* Forward 6-month predictive bounds with 95% confidence intervals.
  7. *Customer Lifecycle Funnel:* Conversion velocity across 6 stages.
  8. *Segment x Channel Matrix:* Cross-tabulation heatmap.

#### Tab 2: 6-Step Autonomous Agentic Workflow (Initiative 3)
* **Visual Stepper:** 6-stage linear breadcrumb (`01 MONITOR`, `02 DETECT`, `03 INVESTIGATE`, `04 ANALYSE`, `05 RECOMMEND`, `06 ESCALATE`).
* **Continuous Trajectory Spline:** High-definition interactive Plotly spline contrasting actual performance against budget trajectories.
* **Detection & Attribution Telemetry:** Dynamic alert card identifying threshold breaches, followed by causal attribution trees.

#### Tab 3: 5-Product Portfolio Matrix
* **Audited Tabular Matrix:** Ground-truth data table tracking Term Sukuk, Saving Bonds, MyPlan, Booster Plan, and Second Salary.
* **Grouped Comparison Bars & AUM Concentration Donut:** Side-by-side volume comparisons.

#### Tab 4: Dynamic Diagnostic Engine
* **Segment Breakdown Donut:** Mass Affluent (`36.9%`), Emirati National (`28.4%`), Retail (`25.8%`), HNW (`5.96%`), Youth (`2.96%`).
* **Channel Distribution Bar Chart & Demographic Histograms:** Visualizing customer concentration and income tiers.

#### Tab 5: Live Action Simulator
* **Remediation Checkboxes:** Interactive selection of approved interventions.
* **Efficiency Slider:** 0% to 100% sensitivity control with live recalculation of recovery lift (+AED 2.91M).
* **Projected Outcome Chart:** Visual gap closing comparing current actuals to simulated post-intervention recovery.

#### Tab 6: Bi-Weekly Product & Market Intelligence Report (Initiative 2)
* **Memo Dossier Container:** Official executive memorandum header (`NBC-BIWEEKLY-INTEL-202606`), macro summary cards, product trajectory charts, and PDF download triggers.

#### Tab 7: GCCO Escalation Briefing
* **Sign-Off Table & Monospace Dossier:** Formal briefing memo formatted for board and ALCO submission with multi-agent audit trails.

---

### 4.2 Cross-Cutting: JD Product & Data Intelligence Copilot
* **Floating Launcher:** Fixed `56x56px` circular avatar button anchored to bottom-right (`bottom: 20px`, `right: 20px`).
* **Popover Modal Dialog:** Width `460px`, height `560px` featuring:
  - Header with "LIVE AI" chip and reset action.
  - 2x3 Grid of 6 suggested inquiry chips.
  - Conversational chat message stream.
  - Text input with submit trigger.

---

### 4.3 Frontline Knowledge Assistant (Initiative 1)
* **Hero Banner & Persona Chip:** "Ahmed • Relationship Manager — Direct Sales & Branch Network".
* **4 Operational Summary Cards:** Approved Documents (`10 Docs`), Grounding Standard (`Zero Hallucination`), Retrieval SLA (`< 1.5s`), Open Escalations (`1 Tickets`).
* **Tab 1 (Ask Assistant):** 6 scenario prompt buttons, query bar, verified ground truth response card, certified circular citation (Product Circular 2026/04 Clause 3.2), Sharia Fatwa approval badge (`2026/SH-09`), and Copy Citation trigger.
* **Tab 2 (Approved Documents):** Catalog of 10 official circulars and manuals with version badges and PDF download triggers.
* **Tab 3 (Escalation Queue):** Real-time ticket management queue for ambiguous frontline queries.
* **Tab 4 (Compliance & Audit Trail):** 4 SLA cards, query distribution donut, intraday velocity curve, and immutable SHA-256 audit ledger.

---

## 5. Desktop Visual Audit Findings & Defect Analysis

### Defect 1: Plotly Chart Legend & Title Collisions (Severity: High)
* **Issue:** In the **Portfolio Matrix** (Tab 3) and **Dynamic Diagnostic Engine** (Tab 4), the horizontal legend (`orientation="h"`, `y=1.1`) overlaps directly with the chart title text.
* **Impact:** In the "Holders by Customer Segment" donut chart, legend labels ("Mass Affluent", "Emirati National", "Retail") collide with the title, degrading readability during executive reviews.
* **Root Cause:** Top margin clearance (`t=40px`) is insufficient when both a chart title and an overhead horizontal legend are present.
* **Evidence:** Documented in [`05_Executive_Cockpit_Portfolio_Matrix_Viewport.png`](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/05_Executive_Cockpit_Portfolio_Matrix_Viewport.png) and [`06_Executive_Cockpit_Diagnostic_Engine_Viewport.png`](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/06_Executive_Cockpit_Diagnostic_Engine_Viewport.png).

---

### Defect 2: Typography Font-Family Inheritance Split (Severity: Medium)
* **Issue:** Custom HTML cards and sidebar elements compute to `Plus Jakarta Sans`, whereas native Streamlit Markdown elements compute to `Source Sans`.
* **Impact:** Visual inconsistency across font weights and letter-spacings between custom metric cards and native text.
* **Evidence:** Confirmed in `ui_component_metrics.json` (lines 13, 44, 106, and 338).

---

### Defect 3: Streamlit Native Header Clutter on Desktop (Severity: Low)
* **Issue:** The native Streamlit header displays the "Deploy" button and hamburger menu in the top right, competing with the custom executive title group.
* **Impact:** Mild visual clutter that distracts from a bespoke, white-labeled enterprise appearance.

---

### Defect 4: JD Copilot Popover Height on Smaller Desktop Displays (Severity: Medium)
* **Issue:** On desktop monitors with vertical resolution under 900px, the 6 preset inquiry chips push the chat input bar partially below the screen edge.
* **Evidence:** Captured in [`10_Executive_Cockpit_JD_Copilot_Chat_Open.png`](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/10_Executive_Cockpit_JD_Copilot_Chat_Open.png).

---

## 6. Actionable Desktop Code Remediation

### 6.1 Plotly Chart Layout Optimization (Python Snippet)
Apply this layout pattern to all Plotly figures in `app.py`, `powerbi_analytics_hub.py`, and `executive_views.py`:

```python
# FIX: REPOSITION LEGEND BELOW CHART AND EXPAND MARGINS
fig.update_layout(
    title=dict(
        text="<b>Holders by Customer Segment: Saving Bonds</b>",
        font=dict(family="Plus Jakarta Sans", size=15, color="#0f172a"),
        x=0.02,
        y=0.98,
        xanchor="left",
        yanchor="top"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,                 # Relocated below the chart
        xanchor="center",
        x=0.5,
        font=dict(family="Plus Jakarta Sans", size=11, color="#475569")
    ),
    margin=dict(t=55, b=65, l=40, r=40),  # Generous clearance
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
```

---

### 6.2 Universal Typography & Header Cleanup (CSS Fix)
Add to the custom `<style>` block in `app.py`:

```css
/* 1. ENFORCE PLUS JAKARTA SANS UNCONDITIONALLY */
html, body, [class*="css"], .stMarkdown, .stText, [data-testid="stMarkdownContainer"] p, div, span {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* 2. CONCEAL STREAMLIT NATIVE CHROME FOR CLEAN WHITE-LABELING */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header [data-testid="stToolbar"] { visibility: hidden !important; }

/* 3. FLUID VERTICAL AUTO-SCROLLING FOR JD COPILOT POPOVER */
div[data-testid="stPopoverBody"] {
    max-height: 82vh !important;
    overflow-y: auto !important;
}

/* 4. PREMIUM CARD HOVER MICRO-ANIMATIONS */
.kpi-card {
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease !important;
}
.kpi-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px -4px rgba(2, 132, 199, 0.12) !important;
    border-color: rgba(2, 132, 199, 0.3) !important;
}
```

---

## 7. Desktop Implementation Roadmap

| Priority | Action Item | Target Component | Expected Outcome |
|---|---|---|---|
| **P0 (Immediate)** | Adjust Plotly Chart Margins & Legends | `app.py`, `powerbi_analytics_hub.py` | Eliminates all legend-to-title text collisions on desktop screens. |
| **P1 (High)** | Universal Typography Override | Main `<style>` block in `app.py` | Harmonizes font rendering across all widgets to `Plus Jakarta Sans`. |
| **P2 (Medium)**| Popover `max-height: 82vh` with Auto-Scroll | `stPopoverBody` selector | Ensures the JD chat input remains accessible on all desktop monitor sizes. |
| **P3 (Polish)**| Clean Header & Card Hover Effects | Global CSS | Removes native Streamlit clutter and adds subtle interactive elevation on hover. |

---

## 8. Phase 2 Consideration: Future Mobile & Tablet UI Adaptation

*(Deferred from Phase 1 Desktop Baseline)*

As requested, mobile phone and tablet considerations are isolated here as reference for **Phase 2** responsive development.

### Phase 2 Preview Visuals & Screenshots
The following responsive screen captures illustrate the current baseline before Phase 2 responsive refactoring:

| Device Viewport | Orientation / Resolution | Screenshot Reference | Visual Link |
|---|---|---|---|
| **iPad / Tablet** | 768 x 1024 (Portrait) | `15_Tablet_Responsive_768x1024.png` | [View Tablet Screen](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/15_Tablet_Responsive_768x1024.png) |
| **iPad / Tablet** | 768 x 2950 (Full Canvas) | `15b_Tablet_Responsive_FullPage.png` | [View Tablet Full Page](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/15b_Tablet_Responsive_FullPage.png) |
| **iPhone / Mobile** | 390 x 844 (Mobile Viewport) | `16_Mobile_Responsive_390x844.png` | [View Mobile Screen](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/16_Mobile_Responsive_390x844.png) |
| **iPhone / Mobile** | 390 x 3100 (Full Canvas) | `16b_Mobile_Responsive_FullPage.png` | [View Mobile Full Page](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/UI%20Structure/16b_Mobile_Responsive_FullPage.png) |

### Phase 2 Architectural Recommendations
When transitioning to mobile and tablet support in Phase 2:
1. **Column Wrapping:** In `div[data-testid="column"]`, implement `@media (max-width: 992px) { min-width: 48% !important; }` (tablet 2-column layout) and `@media (max-width: 640px) { min-width: 100% !important; }` (mobile 1-column layout) so 4-column KPI cards stack vertically instead of squeezing horizontally.
2. **Touch-Friendly Tap Targets:** Expand button heights to a minimum of `44px` on touch viewports.
3. **Sidebar Auto-Collapse:** Ensure the sidebar collapses automatically on mobile viewports with a floating toggle trigger.

---

*This document represents the definitive Desktop UI Baseline and Reference Specification for National Bonds Corporation's AI transformation cockpit.*
