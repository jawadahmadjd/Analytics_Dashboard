# National Bonds Corporation — Data Analysis & AI Platform

**Initiative:** Agentic Product Intelligence & Early Warning System Prototype  
**Author:** Jawad Ahmad | Product AI Solutions  
**Target Viewports:** 1920x1080 Desktop Cockpit & Clean ChatGPT Intelligence Experience  

---

## 🚀 Quick Start & How to Run Both Interfaces

You can run both user interfaces simultaneously on different ports to compare them side-by-side:

### 1. Classic Executive Cockpit (V1) — Port 8501
High-density financial command center featuring PowerBI Studio, 6-step agentic escalation workflow, 5-product portfolio matrix, frontline RM portal, and PDF memo generation.
```powershell
streamlit run app.py --server.port 8501
```
🌐 **URL:** `http://localhost:8501`

### 2. Modern ChatGPT-Style Intelligence Copilot (V2) — Port 8502
Minimalist conversational intelligence interface powered by `JDAgent`. Ask freeform questions about portfolio metrics, target variances, or certified product circulars with zero-hallucination citations.
```powershell
streamlit run app_v2.py --server.port 8502
```
🌐 **URL:** `http://localhost:8502`

---

## 📁 Repository Directory Map

The codebase has been organized into clear, dedicated folders so you always know where to look:

```
24- Data Analysis/
│
├── app.py                             # [ENTRYPOINT V1] Classic Executive Cockpit
├── app_v2.py                          # [ENTRYPOINT V2] ChatGPT-Style AI Copilot Interface
├── README.md                          # This directory guide
│
├── 📁 backend/                        # Core AI, Analytics & Generation Engines
│   ├── jd_engine.py                   # JDAgent (RAG, BM25, DeepSeek NLP, Analytics)
│   ├── pdf_generator.py               # Executive PDF Report Generator
│   └── report_generator.py            # Automated memorandum & dispatch generator
│
├── 📁 data/                           # Platform Datasets & Ground Truth Files
│   ├── cleaned_national_bonds_customers.csv   # 154K verified customer cohort
│   ├── product_portfolio_kpis_alerts.csv      # 18-month KPI time series
│   ├── product_knowledge_base.json            # Official T&Cs, circulars & fatwas
│   ├── svg_extracted_data.json                # Audited text & metrics from 58 slides
│   ├── market_intelligence_data.json          # Macro benchmark rates & competitor intel
│   ├── audit_trail.json                       # Immutable frontline compliance log
│   ├── escalation_tickets.json                # RM escalation queue data
│   └── dispatch_log.json                      # Executive memo dispatch history
│
├── 📁 ui_v1/                          # Classic Cockpit Visual Modules (V1)
│   ├── executive_views.py             # Executive alert center & bi-weekly memo tab
│   ├── frontline_view.py              # Frontline relationship manager portal
│   ├── powerbi_analytics_hub.py       # 8-chart PowerBI analytics studio
│   └── icons.py                       # High-resolution SVG / Material symbol icons
│
├── 📁 ui_chat/                        # ChatGPT-Style Interface Components (V2)
│   ├── chat_components.py             # Header, starter cards & citation accordion
│   ├── chat_sidebar.py                # New chat CTA, mode switcher & telemetry
│   └── chat_styles.css                # Minimalist, luxury OpenAI/Claude aesthetic styling
│
├── 📁 docs/                           # Executive Presentations, Specs & Audit Reports
│   ├── SCOPE_OF_WORK_NATIONAL_BONDS.md
│   ├── UI_STRUCTURE_AND_AUDIT_REPORT.md
│   ├── national_bonds_h1_2026_ground_truth_report.md
│   ├── AI Enabled Product Management Transformation Roadmap GCCO.pptx
│   ├── National_Bonds_BiWeekly_Intelligence_Report_2024-06.pdf
│   ├── National_Bonds_GCCO_Escalation_Dossier_Booster_Sukuk.pdf
│   ├── National_Bonds_Certified_Circular_Booster_Plan.pdf
│   ├── Jawad Business Intelligence Quote.pdf
│   ├── Professional_Services_Quotation_Jawad_Ahmad.docx
│   ├── comprehensive_slide_audit.txt
│   ├── extracted_h1_financial_metrics.txt
│   ├── pptx_extracted.txt
│   ├── svg_extracted_text_data.md
│   └── reference_media/               # Reference captures & WhatsApp screenshots
│
└── 📁 scripts/                        # Data Extraction & Preparation Scripts
    ├── calibrate_national_bonds_data.py
    ├── prepare_data.py
    ├── parse_all_svgs.py
    ├── extract_financial_kpis.py
    ├── analyze_slides.py
    ├── generate_ground_truth_report.py
    ├── generate_quotation.py
    └── capture_ui_screenshots.py
```

---

## 🛡️ Non-Destructive Architecture Guarantee

* **Zero Breakage on V1:** [app.py](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/app.py) runs untouched.
* **Dual Path Resolution:** [backend/jd_engine.py](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/backend/jd_engine.py) dynamically checks both `data/` and the project root so scripts never fail with `FileNotFoundError`.
* **Shared Intelligence:** Both V1 and V2 query the exact same [JDAgent](file:///d:/Tools%20of%20Jawad/24-%20Data%20Analysis/backend/jd_engine.py) intelligence brain, ensuring total consistency across all figures and citations.
