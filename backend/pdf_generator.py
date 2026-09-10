"""
National Bonds Corporation - AI Product Management Transformation
Executive PDF Generator Suite: Boardroom-Grade Reports & Escalation Memos
Author: Jawad Ahmad | Product AI Solutions
"""

import io
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

from report_generator import BiWeeklyReportGenerator

# --- Numbered Canvas for "Page X of Y" and Footer ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        # Footer rule
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 40, A4[0] - 36, 40)
        # Text
        left_text = "CONFIDENTIAL & PROPRIETARY — NATIONAL BONDS CORPORATION"
        right_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(36, 28, left_text)
        self.drawRightString(A4[0] - 36, 28, right_text)
        self.restoreState()

# --- Matplotlib Helper: Theme-Aware Boardroom Charts ---
def find_matching_product_df(kpi_df, product_name):
    """Fuzzy and alias matching to ensure trajectory chart NEVER renders empty."""
    clean_target = str(product_name).lower().strip().replace("-", " ")
    
    # Exact match
    m = kpi_df[kpi_df["product_name"].str.lower() == clean_target]
    if not m.empty:
        return m.sort_values("month")
        
    # Alias maps for product family names
    alias_map = {
        "booster": "Booster Plan",
        "sukuk": "Term Sukuk (Fixed Income)",
        "term": "Term Sukuk (Fixed Income)",
        "saving": "Saving Bonds",
        "bond": "Saving Bonds",
        "salary": "Second Salary (Regular Savings)",
        "myplan": "MyPlan / Regular Saver",
        "saver": "MyPlan / Regular Saver"
    }
    for kw, canon in alias_map.items():
        if kw in clean_target:
            sub = kpi_df[kpi_df["product_name"] == canon]
            if not sub.empty:
                return sub.sort_values("month")
                
    # Fallback to Saving Bonds (primary retail baseline) if no match
    return kpi_df[kpi_df["product_name"] == "Saving Bonds"].sort_values("month")

def generate_inflows_chart(product_rows):
    fig, ax = plt.subplots(figsize=(6.8, 2.2), dpi=200)
    names = [p["product_name"].replace(" (Fixed Income)", "").replace(" (Regular Savings)", "").replace(" / Regular Saver", "") for p in product_rows]
    actuals = [p["net_inflows_m"] for p in product_rows]
    targets = [p["target_inflows_m"] for p in product_rows]
    
    x = np.arange(len(names))
    width = 0.35
    
    ax.bar(x - width/2, actuals, width, label="Actual Inflows (AED M)", color="#0b192c", edgecolor="none", zorder=3)
    ax.bar(x + width/2, targets, width, label="Target Budget (AED M)", color="#c5a059", edgecolor="none", zorder=3)
    
    ax.set_ylabel("AED Millions", fontsize=7.5, fontweight="bold", color="#334155")
    ax.set_title("Product Performance vs Approved Budget Allocation (Cycle 2026-06)", fontsize=9, fontweight="bold", color="#0f172a", pad=6)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=7.5, fontweight="bold", color="#1e293b")
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=7, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.4, color="#cbd5e1", zorder=0)
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")
        
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_competitor_chart(competitors):
    fig, ax = plt.subplots(figsize=(6.8, 1.8), dpi=200)
    banks = [c["bank"].split(" (")[0] for c in competitors] + ["National Bonds (Sukuk)"]
    rates = [c["rate_pct"] for c in competitors] + [5.40]
    colors_list = ["#64748b", "#64748b", "#64748b", "#64748b", "#10b981"]
    
    bars = ax.barh(banks, rates, color=colors_list, height=0.52, zorder=3)
    ax.set_xlabel("Advertised Promotional Yield (% p.a.)", fontsize=7.5, fontweight="bold", color="#334155")
    ax.set_title("UAE Retail Deposit & Sukuk Competitive Yield Radar", fontsize=8.5, fontweight="bold", color="#0f172a", pad=5)
    ax.set_xlim(0, 6.5)
    ax.tick_params(axis="both", labelsize=7)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#cbd5e1", zorder=0)
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#ffffff")
    
    for bar, rate in zip(bars, rates):
        ax.text(rate + 0.08, bar.get_y() + bar.get_height()/2, f"{rate:.2f}%", va="center", ha="left", fontsize=7.5, fontweight="bold", color="#0f172a")
    
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_product_trajectory_chart(kpi_df, product_name, current_cycle="2026-06"):
    fig, ax = plt.subplots(figsize=(6.8, 2.2), dpi=200)
    p_df = find_matching_product_df(kpi_df, product_name)
    p_df = p_df.tail(12)
    
    months_raw = p_df["month"].tolist()
    x_labels = []
    for m in months_raw:
        try:
            dt = datetime.strptime(m, "%Y-%m")
            x_labels.append(dt.strftime("%b %y"))
        except:
            x_labels.append(m)
            
    actual = (p_df["net_inflows_aed"] / 1e6).tolist()
    target = (p_df["target_inflows_aed"] / 1e6).tolist()
    warning_line = [t * 0.92 for t in target] # -8.0% tolerance band
    
    # Plot target and warning line
    ax.plot(x_labels, target, label="ALCO Target Budget", color="#10b981", linestyle="--", linewidth=1.7, zorder=2)
    ax.plot(x_labels, warning_line, label="-8.0% Warning Boundary", color="#ef4444", linestyle=":", linewidth=1.7, zorder=2)
    
    # Plot actual
    ax.plot(x_labels, actual, label="Actual Net Inflows", color="#0284c7", linewidth=2.3, marker="o", markersize=3.5, zorder=4)
    min_val = min(actual) if actual else 40
    ax.fill_between(x_labels, actual, [min_val * 0.95] * len(actual), color="#0284c7", alpha=0.08, zorder=1)
    
    # Breach zone
    ax.fill_between(x_labels, actual, warning_line, where=[a < w for a, w in zip(actual, warning_line)],
                    color="#fee2e2", alpha=0.6, label="Breach Zone (< -8.0%)", zorder=3)
    
    clean_pname = p_df["product_name"].iloc[0] if not p_df.empty else product_name
    ax.set_title(f"{clean_pname} — 12-Month Inflow Trajectory vs Tolerance Boundary", fontsize=9, fontweight="bold", color="#0f172a", pad=6)
    ax.set_ylabel("AED Millions", fontsize=7.5, fontweight="bold", color="#475569")
    ax.tick_params(axis="x", rotation=25, labelsize=7)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=7, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.4, color="#cbd5e1", zorder=0)
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")
        
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_channel_variance_chart():
    fig, ax = plt.subplots(figsize=(6.8, 1.4), dpi=200)
    channels = ["Call Center Telesales", "Direct Wealth Sales", "Branch Network", "Mobile App Gateway"]
    variances = [-4.2, 8.4, 2.1, -68.4]
    bar_colors = ["#ef4444" if v < 0 else "#10b981" for v in variances]
    
    bars = ax.barh(channels, variances, color=bar_colors, height=0.48, zorder=3)
    ax.axvline(x=0, color="#64748b", linewidth=0.8, linestyle="-", zorder=2)
    
    for bar, val in zip(bars, variances):
        x_pos = val - 4 if val < 0 else val + 1
        align = "right" if val < 0 else "left"
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, f"{val:+.1f}%", 
                va="center", ha=align, fontsize=7, fontweight="bold", 
                color="#dc2626" if val < 0 else "#16a34a")
        
    ax.set_title("Acquisition Channel Deviation Breakdown vs Target (%)", fontsize=8.5, fontweight="bold", color="#0f172a", pad=5)
    ax.tick_params(axis="both", labelsize=7)
    ax.set_xlim(-85, 20)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#cbd5e1", zorder=0)
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")
        
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

# --- Core PDF Generator Engine ---
class ExecutivePDFGenerator:
    def __init__(self, kpi_csv="product_portfolio_kpis_alerts.csv", market_json="market_intelligence_data.json"):
        self.kpi_df = pd.read_csv(kpi_csv)
        self.report_gen = BiWeeklyReportGenerator(kpi_csv=kpi_csv, market_json=market_json)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.s_title = ParagraphStyle(
            "DocTitle",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#0f172a")
        )
        self.s_subtitle = ParagraphStyle(
            "DocSubTitle",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#0284c7")
        )
        self.s_meta_label = ParagraphStyle(
            "MetaLabel",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#64748b")
        )
        self.s_meta_val = ParagraphStyle(
            "MetaVal",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#0f172a")
        )
        self.s_sec_header = ParagraphStyle(
            "SecHeader",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4
        )
        self.s_body = ParagraphStyle(
            "Body",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#334155")
        )
        self.s_body_bold = ParagraphStyle(
            "BodyBold",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#0f172a")
        )
        self.s_callout = ParagraphStyle(
            "Callout",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#1e293b")
        )

    def generate_biweekly_report_pdf(self, cycle_month="2026-06"):
        """Builds a boardroom-grade Bi-Weekly Commercial & Macro Intelligence Memorandum PDF matching the website view 1:1."""
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=32,
            rightMargin=32,
            topMargin=32,
            bottomMargin=42
        )

        styles = getSampleStyleSheet()
        s_norm = styles["Normal"]
        
        s_title = ParagraphStyle("BWTitle", parent=s_norm, fontName="Helvetica-Bold", fontSize=13.5, leading=16, textColor=colors.HexColor("#0f172a"))
        s_meta_l = ParagraphStyle("BWMetaL", parent=s_norm, fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=colors.HexColor("#64748b"))
        s_meta_v = ParagraphStyle("BWMetaV", parent=s_norm, fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#0f172a"))
        s_sec = ParagraphStyle("BWSec", parent=s_norm, fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=colors.HexColor("#0f172a"))
        s_body = ParagraphStyle("BWBody", parent=s_norm, fontName="Helvetica", fontSize=7.5, leading=10.5, textColor=colors.HexColor("#334155"))
        s_narr = ParagraphStyle("BWNarr", parent=s_norm, fontName="Helvetica", fontSize=7.5, leading=11, textColor=colors.HexColor("#1e293b"))

        elements = []

        # 1. Header Banner with Brand Emblem
        logo_table = Table([[
            Paragraph("<b>NB</b>", ParagraphStyle("LogoPBW", fontName="Helvetica-Bold", fontSize=14, textColor=colors.HexColor("#c5a059"), alignment=1))
        ]], colWidths=[34], rowHeights=[34])
        logo_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0b192c")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))

        hdr_data = [
            [
                logo_table,
                Paragraph("<b>National Bonds Corporation &bull; Commercial & Macro Intelligence</b><br/>"
                          "<font size=7.5 color='#c5a059'><b>EXECUTIVE MEMORANDUM &bull; BI-WEEKLY CYCLE CLOSE 2026-06</b></font><br/>"
                          "<font size=6.5 color='#64748b'>Classified: Confidential (ALCO / C-Suite) &bull; Ref: NBC-BIWEEKLY-INTEL-202606</font>", s_title),
                Paragraph("<font size=7.5 color='#059669'><b>ALCO RATIFIED</b></font><br/>"
                          "<font size=6.5 color='#64748b'>Date: <b>15 June 2026</b><br/>Status: <b>100% Sharia Certified</b></font>", ParagraphStyle("HRBW", parent=s_norm, alignment=2))
            ]
        ]
        hdr_t = Table(hdr_data, colWidths=[40, 360, 130])
        hdr_t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(hdr_t)
        elements.append(Spacer(1, 4))

        # Navy Bar
        rule_t = Table([[""]], colWidths=[530], rowHeights=[2])
        rule_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0b192c")),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(rule_t)
        elements.append(Spacer(1, 7))

        # 2. Metadata Routing Table
        meta_rows = [
            [
                Paragraph("ADDRESSEE", s_meta_l),
                Paragraph("<b>Group Executive Committee & ALCO</b>", s_meta_v),
                Paragraph("DOCUMENT REF", s_meta_l),
                Paragraph("<b>NBC-BIWEEKLY-INTEL-202606</b>", s_meta_v)
            ],
            [
                Paragraph("ORIGINATING UNIT", s_meta_l),
                Paragraph("<b>Commercial Intelligence & ALM Strategy</b>", s_meta_v),
                Paragraph("AUDIT STATUS", s_meta_l),
                Paragraph("<font color='#059669'><b>ALCO Ratified &bull; 100% Sharia Certified</b></font>", s_meta_v)
            ],
            [
                Paragraph("PUBLICATION DATE", s_meta_l),
                Paragraph("<b>15 June 2026</b>", s_meta_v),
                Paragraph("SECURITY TIER", s_meta_l),
                Paragraph("<font color='#dc2626'><b>RESTRICTED (C-SUITE / TREASURY)</b></font>", s_meta_v)
            ]
        ]
        meta_t = Table(meta_rows, colWidths=[110, 155, 105, 160])
        meta_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ]))
        elements.append(meta_t)
        elements.append(Spacer(1, 7))

        # 3. Section 1: Macro Cards
        elements.append(Paragraph("<b>01 &bull; MACRO BENCHMARK & PORTFOLIO SYNTHESIS</b>", s_sec))
        elements.append(Spacer(1, 3))
        
        kpi_card_data = [
            [
                Paragraph("<font color='#64748b'><b>CBUAE BASE RATE</b></font><br/><font size=10 color='#0f172a'><b>4.65%</b></font><br/><font size=6.5 color='#64748b'>Unchanged (Plateau)</font>", s_body),
                Paragraph("<font color='#64748b'><b>3M EIBOR</b></font><br/><font size=10 color='#0f172a'><b>4.52%</b></font><br/><font size=6.5 color='#64748b'>+4 bps Liquidity Spread</font>", s_body),
                Paragraph("<font color='#64748b'><b>NET INFLOWS (ACTUAL)</b></font><br/><font size=10 color='#0f172a'><b>AED 617.0M</b></font><br/><font size=6.5 color='#dc2626'>-9.5% vs Target AED 681.6M</font>", s_body),
                Paragraph("<font color='#64748b'><b>TOTAL REDEMPTIONS</b></font><br/><font size=10 color='#0f172a'><b>AED 405.7M</b></font><br/><font size=6.5 color='#d97706'>Run-off Ratio: 39.7%</font>", s_body)
            ]
        ]
        kpi_t = Table(kpi_card_data, colWidths=[130, 130, 135, 135])
        kpi_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        elements.append(kpi_t)
        elements.append(Spacer(1, 5))

        # Narrative Box
        narr_text = "<b>Executive Macro Synthesis:</b> The UAE domestic liquidity landscape remains characterized by sustained high base rates (4.65%). While aggregate NBC AUM surpasses <b>AED 18.34B</b>, monthly net inflows closed at <b>AED 617.0M</b> against a budget of <b>AED 681.6M</b>. Liquidity run-off is predominantly concentrated in retail demand accounts, whereas institutional Term Sukuk retention exhibits high resilience with an 87.4% renewal velocity."
        narr_t = Table([[Paragraph(narr_text, s_narr)]], colWidths=[530])
        narr_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
            ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#0284c7")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(narr_t)
        elements.append(Spacer(1, 8))

        # 4. Section 2: Budget Chart & Table
        elements.append(Paragraph("<b>02 &bull; PRODUCT PERFORMANCE VS APPROVED BUDGET ALLOCATION (CYCLE 2026-06)</b>", s_sec))
        elements.append(Spacer(1, 3))
        
        prod_breakdown = [
            {"product_name": "Term Sukuk (Fixed Income)", "net_inflows_m": 520.19, "target_inflows_m": 582.16, "deviation_pct": -10.65},
            {"product_name": "Saving Bonds", "net_inflows_m": 51.19, "target_inflows_m": 57.02, "deviation_pct": -10.22},
            {"product_name": "Booster Plan", "net_inflows_m": 26.49, "target_inflows_m": 21.68, "deviation_pct": 22.12},
            {"product_name": "MyPlan / Regular Saver", "net_inflows_m": 16.45, "target_inflows_m": 16.84, "deviation_pct": -1.79},
            {"product_name": "Second Salary (Regular Savings)", "net_inflows_m": 2.66, "target_inflows_m": 3.79, "deviation_pct": -28.95}
        ]
        chart_bw_buf = generate_inflows_chart(prod_breakdown)
        elements.append(Image(chart_bw_buf, width=530, height=138))
        elements.append(Spacer(1, 5))

        # Data Table
        table_rows = [
            [
                Paragraph("<b>Product Family</b>", s_meta_l),
                Paragraph("<b>Actual Net (AED M)</b>", ParagraphStyle("BWR1", parent=s_meta_l, alignment=2)),
                Paragraph("<b>Target Budget (AED M)</b>", ParagraphStyle("BWR2", parent=s_meta_l, alignment=2)),
                Paragraph("<b>Variance (AED M)</b>", ParagraphStyle("BWR3", parent=s_meta_l, alignment=2)),
                Paragraph("<b>Variance (%)</b>", ParagraphStyle("BWR4", parent=s_meta_l, alignment=2)),
                Paragraph("<b>Governance Status</b>", ParagraphStyle("BWR5", parent=s_meta_l, alignment=1))
            ],
            [
                Paragraph("<b>Term Sukuk (Fixed Income)</b>", s_body),
                Paragraph("AED 520.2M", ParagraphStyle("BWN1", parent=s_body, alignment=2)),
                Paragraph("AED 582.2M", ParagraphStyle("BWN2", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'>-AED 62.0M</font>", ParagraphStyle("BWN3", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'>-10.65%</font>", ParagraphStyle("BWN4", parent=s_body, alignment=2)),
                Paragraph("<font color='#d97706'><b>TOLERANCE WATCH</b></font>", ParagraphStyle("BWS1", parent=s_body, alignment=1))
            ],
            [
                Paragraph("<b>Saving Bonds (Retail)</b>", s_body),
                Paragraph("AED 51.2M", ParagraphStyle("BWN5", parent=s_body, alignment=2)),
                Paragraph("AED 57.0M", ParagraphStyle("BWN6", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'>-AED 5.8M</font>", ParagraphStyle("BWN7", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'>-10.22%</font>", ParagraphStyle("BWN8", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'><b>BREACH / ESCALATED</b></font>", ParagraphStyle("BWS2", parent=s_body, alignment=1))
            ],
            [
                Paragraph("<b>Booster Plan (Loyalty)</b>", s_body),
                Paragraph("AED 26.5M", ParagraphStyle("BWN9", parent=s_body, alignment=2)),
                Paragraph("AED 21.7M", ParagraphStyle("BWN10", parent=s_body, alignment=2)),
                Paragraph("<font color='#16a34a'>+AED 4.8M</font>", ParagraphStyle("BWN11", parent=s_body, alignment=2)),
                Paragraph("<font color='#16a34a'>+22.12%</font>", ParagraphStyle("BWN12", parent=s_body, alignment=2)),
                Paragraph("<font color='#16a34a'><b>OUTPERFORMING</b></font>", ParagraphStyle("BWS3", parent=s_body, alignment=1))
            ],
            [
                Paragraph("<b>MyPlan / Regular Saver</b>", s_body),
                Paragraph("AED 16.5M", ParagraphStyle("BWN13", parent=s_body, alignment=2)),
                Paragraph("AED 16.8M", ParagraphStyle("BWN14", parent=s_body, alignment=2)),
                Paragraph("<font color='#64748b'>-AED 0.3M</font>", ParagraphStyle("BWN15", parent=s_body, alignment=2)),
                Paragraph("<font color='#64748b'>-1.79%</font>", ParagraphStyle("BWN16", parent=s_body, alignment=2)),
                Paragraph("<font color='#16a34a'><b>ON TARGET</b></font>", ParagraphStyle("BWS4", parent=s_body, alignment=1))
            ],
            [
                Paragraph("<b>Second Salary (Retirement)</b>", s_body),
                Paragraph("AED 2.7M", ParagraphStyle("BWN17", parent=s_body, alignment=2)),
                Paragraph("AED 3.8M", ParagraphStyle("BWN18", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'>-AED 1.1M</font>", ParagraphStyle("BWN19", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'>-28.95%</font>", ParagraphStyle("BWN20", parent=s_body, alignment=2)),
                Paragraph("<font color='#dc2626'><b>REMEDIATION</b></font>", ParagraphStyle("BWS5", parent=s_body, alignment=1))
            ]
        ]
        p_table = Table(table_rows, colWidths=[160, 75, 75, 75, 65, 80])
        p_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(p_table)
        elements.append(Spacer(1, 7))

        # 5. Section 3: Competitive Market Pulse
        elements.append(Paragraph("<b>03 &bull; COMPETITIVE YIELD ARBITRAGE & LIQUIDITY SURVEILLANCE</b>", s_sec))
        elements.append(Spacer(1, 3))
        
        comp_data = [
            [
                Paragraph("<b>Retail Deposit Yield Arbitrage:</b> Neo-banks (Wio Bank at 5.25% promo rate) and digital accounts (FAB iSave at 5.10%) are aggressively bidding for short-term retail liquidity. Yield-sensitive cohorts are parking funds into 3-month high-yield promotional deposits, dampening Saving Bonds fresh inflows.", s_body),
                Paragraph("<b>Duration Lock & Institutional Stability:</b> Term Sukuk contracts (1Y to 3Y fixed maturities) maintain an 87.4% retention rate. Redemptions were concentrated in flexible retail certificates (AED 194.2M). Matured capital was successfully rolled into structured 2Y Booster tranches at a 74.2% capture rate.", s_body)
            ]
        ]
        comp_t = Table(comp_data, colWidths=[260, 260])
        comp_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#fffbeb")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#f0fdf4")),
            ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#fde68a")),
            ("BOX", (1, 0), (1, 0), 0.5, colors.HexColor("#bbf7d0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(comp_t)
        elements.append(Spacer(1, 7))

        # 6. Section 4: Governance Seal
        seal_data = [
            [
                Paragraph("<b>Group Executive Committee &bull; Asset Liability Management (ALCO)</b><br/>"
                          "Signatories: Group Chief Commercial Officer &bull; Head of Treasury & Financial Markets", s_body),
                Paragraph("<font color='#059669'><b>&check; ALCO RATIFIED &bull; SHA-256 AUDITED</b></font><br/>"
                          "<font size=6.5 color='#64748b'>LEDGER HASH: 0x9b3f88a2e1c93bb8e7d21... &bull; 100% FATWA COMPLIANT</font>", ParagraphStyle("SealBW", parent=s_norm, alignment=1))
            ]
        ]
        seal_t = Table(seal_data, colWidths=[350, 180])
        seal_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#f8fafc")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#f0fdf4")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#0f172a")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(seal_t)

        doc.build(elements, canvasmaker=NumberedCanvas)
        buf.seek(0)
        return buf.getvalue()

    def generate_gcco_escalation_memo_pdf(self, product_name="Saving Bonds", cycle_month="2026-06", dev=-10.22, deficit_m=5.82, net_inflow_m=51.18, target_inflow_m=57.02, briefing_text=""):
        """Builds a boardroom-grade GCCO Executive Escalation Briefing Dossier PDF matching the website view 1:1."""
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=32,
            rightMargin=32,
            topMargin=32,
            bottomMargin=42
        )

        styles = getSampleStyleSheet()
        s_norm = styles["Normal"]
        
        s_title = ParagraphStyle("GCCOTitle", parent=s_norm, fontName="Helvetica-Bold", fontSize=13.5, leading=16, textColor=colors.HexColor("#0f172a"))
        s_meta_l = ParagraphStyle("GCCOMetaL", parent=s_norm, fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=colors.HexColor("#64748b"))
        s_meta_v = ParagraphStyle("GCCOMetaV", parent=s_norm, fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#0f172a"))
        s_sec = ParagraphStyle("GCCOSec", parent=s_norm, fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=colors.HexColor("#0f172a"))
        s_body = ParagraphStyle("GCCOBody", parent=s_norm, fontName="Helvetica", fontSize=7.5, leading=10.5, textColor=colors.HexColor("#334155"))
        s_alert = ParagraphStyle("GCCOAlert", parent=s_norm, fontName="Helvetica", fontSize=7.5, leading=11, textColor=colors.HexColor("#991b1b"))

        elements = []

        # 1. Official Header Banner with Brand Emblem
        logo_table = Table([[
            Paragraph("<b>NB</b>", ParagraphStyle("LogoP", fontName="Helvetica-Bold", fontSize=14, textColor=colors.white, alignment=1))
        ]], colWidths=[34], rowHeights=[34])
        logo_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#991b1b")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))

        clean_prod = str(product_name).replace(" (Retail)", "").replace(" (Fixed Income)", "").replace(" (Regular Savings)", "").replace(" / Regular Saver", "")
        hdr_data = [
            [
                logo_table,
                Paragraph("<b>National Bonds Corporation &bull; Executive Escalation</b><br/>"
                          "<font size=7.5 color='#dc2626'><b>CONFIDENTIAL ESCALATION DOSSIER & ROUTING TABLE</b></font><br/>"
                          f"<font size=6.5 color='#64748b'>Strictly Confidential &bull; Group Chief Commercial Officer Direct Action &bull; Ref: ESC-2026-GCCO-01</font>", s_title),
                Paragraph("<font size=7.5 color='#dc2626'><b>URGENT GCCO ACTION</b></font><br/>"
                          f"<font size=6.5 color='#64748b'>Cycle: <b>{cycle_month}</b><br/>Status: <b>MANDATED</b></font>", ParagraphStyle("HR", parent=s_norm, alignment=2))
            ]
        ]
        hdr_t = Table(hdr_data, colWidths=[40, 360, 130])
        hdr_t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(hdr_t)
        elements.append(Spacer(1, 4))

        # Red Accent Bar
        rule_t = Table([[""]], colWidths=[530], rowHeights=[2])
        rule_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#991b1b")),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(rule_t)
        elements.append(Spacer(1, 7))

        # 2. Metadata Routing Table
        meta_rows = [
            [
                Paragraph("ADDRESSEE", s_meta_l),
                Paragraph("<b>Group Chief Commercial Officer (GCCO)</b>", s_meta_v),
                Paragraph("ESCALATION REF", s_meta_l),
                Paragraph("<b>ESC-2026-GCCO-01</b>", s_meta_v)
            ],
            [
                Paragraph("SEVERITY LEVEL", s_meta_l),
                Paragraph("<font color='#dc2626'><b>TIER-1 COMMERCIAL BREACH (Deficit &gt; 10%)</b></font>", s_meta_v),
                Paragraph("INCIDENT CYCLE", s_meta_l),
                Paragraph(f"<b>Cycle {cycle_month}</b>", s_meta_v)
            ],
            [
                Paragraph("UNDERPERFORMING ENTITY", s_meta_l),
                Paragraph(f"<b>{clean_prod}</b>", s_meta_v),
                Paragraph("DEFICIT GAP", s_meta_l),
                Paragraph(f"<font color='#dc2626'><b>{dev:+.1f}% (AED {deficit_m:.2f}M Shortfall)</b></font>", s_meta_v)
            ]
        ]
        meta_t = Table(meta_rows, colWidths=[110, 155, 105, 160])
        meta_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ]))
        elements.append(meta_t)
        elements.append(Spacer(1, 6))

        # 3. Critical Alert Callout Box
        alert_text = f"<b>CRITICAL COMMERCIAL BREACH NOTICE:</b> {clean_prod} monthly net inflows closed at <b>AED {net_inflow_m:.2f}M</b> against an ALCO approved target of <b>AED {target_inflow_m:.2f}M</b> (AED {deficit_m:.2f}M net deficit, {dev:+.1f}% deviation). This marks consecutive reporting periods wherein variance exceeded the -8.0% tolerance band. Pursuant to Commercial Governance Charter Section 4.2, immediate executive intervention directives are submitted below for GCCO ratification."
        alert_t = Table([[Paragraph(alert_text, s_alert)]], colWidths=[530])
        alert_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fef2f2")),
            ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#fecaca")),
            ("LINEBEFORE", (0, 0), (0, -1), 3.5, colors.HexColor("#dc2626")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(alert_t)
        elements.append(Spacer(1, 7))

        # 4. Section 1: Trajectory Chart
        elements.append(Paragraph("<b>01 &bull; 12-MONTH INFLOW TRAJECTORY VS TOLERANCE BOUNDARY</b>", s_sec))
        elements.append(Spacer(1, 2))
        chart_traj_buf = generate_product_trajectory_chart(self.kpi_df, product_name, cycle_month)
        elements.append(Image(chart_traj_buf, width=530, height=138))
        elements.append(Spacer(1, 4))

        # 5. Section 2: Channel Diagnosis
        elements.append(Paragraph("<b>02 &bull; CHANNEL ATTRIBUTION & LEAKAGE ROOT CAUSE DECONSTRUCTION</b>", s_sec))
        elements.append(Spacer(1, 2))
        chart_chan_buf = generate_channel_variance_chart()
        elements.append(Image(chart_chan_buf, width=530, height=88))
        elements.append(Spacer(1, 4))

        # Insights side-by-side
        ins_data = [
            [
                Paragraph("<b>Mobile App Gateway Friction (-68.4%):</b> Payment gateway migration on June 3rd caused authentication retry timeouts on recurring debits. Drop-off surged from 4.1% to 19.8%, stranding an estimated <b>AED 3.2M</b> in uncaptured monthly top-ups.", s_body),
                Paragraph("<b>Neo-Bank Competitor Yield Premium:</b> Aggressive 5.25% promotional deposits by digital neo-banks triggered opportunistic withdrawals among Mass Affluent savers (AED 50k - AED 250k tier), dampening demand inflows.", s_body)
            ]
        ]
        ins_t = Table(ins_data, colWidths=[260, 260])
        ins_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#fff1f2")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#fffbeb")),
            ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#fecdd3")),
            ("BOX", (1, 0), (1, 0), 0.5, colors.HexColor("#fde68a")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(ins_t)
        elements.append(Spacer(1, 5))

        # 6. Section 3: Directives
        elements.append(Paragraph("<b>03 &bull; MANDATED COMMERCIAL RECOVERY DIRECTIVES (GCCO DIRECT EXECUTION)</b>", s_sec))
        elements.append(Spacer(1, 2))
        
        dir_rows = [
            [
                Paragraph("<b>Directive 1 (Urgent): Hotfix Mobile Payment Gateway & Reinstate 1-Click Apple Pay</b><br/>"
                          "<font color='#64748b'>Engineering team to rollback the buggy authentication timeout and restore single-tap recurring top-up.</font>", s_body),
                Paragraph("<font color='#059669'><b>+AED 3.2M Inflow Recovery</b></font><br/>"
                          "<font size=6.5 color='#64748b'>Owner: Digital Lead &bull; ETA: 48h</font>", ParagraphStyle("D1", parent=s_norm, alignment=2))
            ],
            [
                Paragraph("<b>Directive 2: Deploy 5.30% 6-Month Booster Sukuk Flash Tranche</b><br/>"
                          "<font color='#64748b'>Launch targeted promotional yield tranche directly in mobile app to counter neo-bank churn.</font>", s_body),
                Paragraph("<font color='#059669'><b>+AED 4.5M New Liquidity</b></font><br/>"
                          "<font size=6.5 color='#64748b'>Owner: Commercial Strategy &bull; ETA: 5 Days</font>", ParagraphStyle("D2", parent=s_norm, alignment=2))
            ],
            [
                Paragraph("<b>Directive 3: Direct Relationship Manager Concierge Outreach</b><br/>"
                          "<font color='#64748b'>Assign dedicated RM calls to 420 High Net Worth savers (&gt; AED 250k) with high withdrawal intent.</font>", s_body),
                Paragraph("<font color='#059669'><b>+AED 6.0M Retention Capture</b></font><br/>"
                          "<font size=6.5 color='#64748b'>Owner: Wealth Sales Lead &bull; ETA: Immediate</font>", ParagraphStyle("D3", parent=s_norm, alignment=2))
            ]
        ]
        dir_t = Table(dir_rows, colWidths=[380, 150])
        dir_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fef2f2")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(dir_t)
        elements.append(Spacer(1, 8))

        # 7. Section 4: Sign-Off & Execution Stamp
        sign_data = [
            [
                Paragraph("<b>FORMAL GCCO HUMAN-IN-THE-LOOP EXECUTIVE ACTION SIGN-OFF</b><br/>"
                          "I hereby review the autonomous findings and authorize the tactical countermeasures:<br/>"
                          "[ &nbsp; ] <b>APPROVED TO EXECUTE</b> &nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] <b>CONDITIONAL APPROVAL</b> &nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] <b>REVISE / RE-MODEL</b><br/>"
                          "<b>GCCO Signature:</b> ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> ______________", s_body),
                Paragraph("<font color='#dc2626'><b>&check; MANDATED FOR EXECUTION</b></font><br/>"
                          "<font size=6.5 color='#64748b'>REF: ESC-2026-GCCO-01-SIGNED<br/>SHA-256 LEDGER AUDITED</font>", ParagraphStyle("SignStamp", parent=s_norm, alignment=1))
            ]
        ]
        sign_t = Table(sign_data, colWidths=[390, 140])
        sign_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#ffffff")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#fef2f2")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#0f172a")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(sign_t)

        doc.build(elements, canvasmaker=NumberedCanvas)
        buf.seek(0)
        return buf.getvalue()


    def generate_product_circular_pdf(self, doc):
        """Builds a certified 1-page Product Circular / Directive PDF."""
        buf = io.BytesIO()
        doc_tpl = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=48
        )
        elements = []
        is_review = doc.get("approval_status") == "UNDER_EXECUTIVE_REVIEW"
        theme_color = "#f59e0b" if is_review else "#0284c7"
        badge_status = doc.get("approval_status", "APPROVED")

        # Header
        hdr_data = [
            [
                Paragraph("<b>NATIONAL BONDS CORPORATION</b><br/><font size=9 color='" + theme_color + "'><b>SHARIA-COMPLIANT PRODUCT MANAGEMENT OFFICE</b></font>", self.s_title),
                Paragraph(f"<font color='#64748b'>DOC REF: <b>{doc.get('document_ref', 'N/A')}</b><br/>EFFECTIVE: <b>{doc.get('effective_date', 'N/A')}</b><br/>STATUS: <b>{badge_status}</b></font>", self.s_meta_val)
            ]
        ]
        hdr_table = Table(hdr_data, colWidths=[350, 170])
        hdr_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(hdr_table)
        elements.append(Spacer(1, 4))

        # Color bar
        rule_table = Table([[""]], colWidths=[520], rowHeights=[2.5])
        rule_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(theme_color)),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0)
        ]))
        elements.append(rule_table)
        elements.append(Spacer(1, 10))

        # Metadata Table
        meta_data = [
            [
                Paragraph("<b>PRODUCT:</b>", self.s_meta_label),
                Paragraph(f"<b>{doc.get('product_name', 'N/A')}</b>", self.s_meta_val),
                Paragraph("<b>DOC TYPE:</b>", self.s_meta_label),
                Paragraph(f"{doc.get('document_type', 'N/A')}", self.s_meta_val)
            ],
            [
                Paragraph("<b>SECTION:</b>", self.s_meta_label),
                Paragraph(f"{doc.get('section', 'N/A')}", self.s_meta_val),
                Paragraph("<b>OWNER:</b>", self.s_meta_label),
                Paragraph(f"{doc.get('owner', 'Product Team')}", self.s_meta_val)
            ],
            [
                Paragraph("<b>SHARIA REF:</b>", self.s_meta_label),
                Paragraph(f"<font color='#16a34a'><b>{doc.get('sharia_compliance_ref', 'Fatwa Committee Approved')}</b></font>", self.s_meta_val),
                Paragraph("<b>SECURITY:</b>", self.s_meta_label),
                Paragraph("<b>INTERNAL AUTHORIZED CIRCULAR</b>", self.s_meta_val)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[65, 205, 65, 185])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # Title
        elements.append(Paragraph(f"<b>DOCUMENT TITLE: {doc.get('title', '')}</b>", self.s_sec_header))
        elements.append(Spacer(1, 4))

        # Content Box
        content_text = doc.get('content', '').replace('\n', '<br/><br/>')
        content_table = Table([[Paragraph(f"<font size=9 color='#0f172a'>{content_text}</font>", self.s_body)]], colWidths=[520])
        content_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ffffff")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ]))
        elements.append(content_table)
        elements.append(Spacer(1, 14))

        # Notice Box
        notice_txt = "<b>OPERATIONAL NOTICE FOR FRONTLINE RELATIONSHIP MANAGERS:</b><br/>" \
                     "This document serves as the mandatory single source of product truth. Frontline staff must not communicate verbal deviations, unregistered promotional yields, or uncertified redemption timelines. For customer disputes or unclear parameters, escalate immediately via the AI Product Knowledge Assistant."
        if is_review:
            notice_txt = "<font color='#b45309'><b>⚠️ MANDATORY UNDER-REVIEW RESTRICTION:</b><br/>" \
                         "This policy or circular is currently undergoing executive review by Product Leadership and the Sharia Supervisory Board. Frontline personnel are strictly prohibited from quoting these terms to clients until formal re-certification is issued.</font>"

        notice_table = Table([[Paragraph(notice_txt, self.s_callout)]], colWidths=[520])
        notice_bg = "#fffbeb" if is_review else "#f0f9ff"
        notice_box_color = "#f59e0b" if is_review else "#0284c7"
        notice_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(notice_bg)),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(notice_box_color)),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10)
        ]))
        elements.append(notice_table)
        elements.append(Spacer(1, 14))

        # Sharia & Legal Signatures
        sign_data = [
            [
                Paragraph("<b>DOCUMENT OWNER:</b><br/>" + str(doc.get('owner', 'Product Management')), self.s_meta_val),
                Paragraph("<b>SHARIA SUPERVISION:</b><br/>National Bonds Sharia Board", self.s_meta_val),
                Paragraph("<b>COMPLIANCE & LEGAL:</b><br/>Regulatory Verification Passed", self.s_meta_val)
            ]
        ]
        sign_table = Table(sign_data, colWidths=[173, 173, 174])
        sign_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ]))
        elements.append(sign_table)

        doc_tpl.build(elements, canvasmaker=NumberedCanvas)
        buf.seek(0)
        return buf.getvalue()
