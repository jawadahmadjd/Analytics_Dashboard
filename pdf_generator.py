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

# --- Matplotlib Helper: Theme-Aware Charts ---
def generate_inflows_chart(product_rows):
    fig, ax = plt.subplots(figsize=(6.5, 2.6), dpi=180)
    names = [p["product_name"].split(" (")[0] for p in product_rows]
    actuals = [p["net_inflows_m"] for p in product_rows]
    targets = [p["target_inflows_m"] for p in product_rows]
    
    x = np.arange(len(names))
    width = 0.35
    
    ax.bar(x - width/2, actuals, width, label="Actual Net (AED M)", color="#0284c7", edgecolor="none", zorder=3)
    ax.bar(x + width/2, targets, width, label="Target Budget (AED M)", color="#94a3b8", edgecolor="none", zorder=3)
    
    ax.set_ylabel("AED Millions", fontsize=8, fontweight="bold", color="#334155")
    ax.set_title("Product Net Inflow Performance vs Budget Target Plan", fontsize=10, fontweight="bold", color="#0f172a", pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8, fontweight="bold", color="#1e293b")
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=8, loc="upper right")
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
    fig, ax = plt.subplots(figsize=(6.5, 2.2), dpi=180)
    banks = [c["bank"].split(" (")[0] for c in competitors] + ["National Bonds (Sukuk)"]
    rates = [c["rate_pct"] for c in competitors] + [5.40]
    colors_list = ["#64748b", "#64748b", "#64748b", "#64748b", "#10b981"]
    
    bars = ax.barh(banks, rates, color=colors_list, height=0.55, zorder=3)
    ax.set_xlabel("Anticipated / Advertised Yield (% p.a.)", fontsize=8, fontweight="bold", color="#334155")
    ax.set_title("UAE Retail Deposit & Sukuk Competitive Yield Radar", fontsize=10, fontweight="bold", color="#0f172a", pad=6)
    ax.set_xlim(0, 6.5)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#cbd5e1", zorder=0)
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#ffffff")
    
    for bar, rate in zip(bars, rates):
        ax.text(rate + 0.08, bar.get_y() + bar.get_height()/2, f"{rate:.2f}%", va="center", ha="left", fontsize=8, fontweight="bold", color="#0f172a")
    
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_product_trajectory_chart(kpi_df, product_name, current_cycle):
    fig, ax = plt.subplots(figsize=(6.5, 2.6), dpi=180)
    p_df = kpi_df[kpi_df["product_name"] == product_name].sort_values("month")
    
    x = p_df["month"].tolist()
    actual = (p_df["net_inflows_aed"] / 1e6).tolist()
    target = (p_df["target_inflows_aed"] / 1e6).tolist()
    
    ax.plot(x, target, label="Budget Plan Target", color="#94a3b8", linestyle="--", linewidth=1.8, zorder=2)
    ax.plot(x, actual, label="Actual Net Inflows", color="#0284c7", linewidth=2.5, marker="o", markersize=4, zorder=4)
    ax.fill_between(x, actual, target, where=[a < t for a, t in zip(actual, target)], color="#fecaca", alpha=0.4, label="Underperformance Gap", zorder=1)
    
    if current_cycle in x:
        idx = x.index(current_cycle)
        ax.axvline(x=idx, color="#f59e0b", linestyle=":", linewidth=2, label=f"Reporting Cycle ({current_cycle})")
    
    ax.set_ylabel("AED Millions", fontsize=8, fontweight="bold", color="#334155")
    ax.set_title(f"{product_name} — 18-Month Performance Trajectory vs Target Plan", fontsize=10, fontweight="bold", color="#0f172a", pad=8)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.tick_params(axis="y", labelsize=8)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=7.5, loc="upper right")
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

    def generate_biweekly_report_pdf(self, cycle_month):
        """Builds a beautiful 3-page Bi-Weekly Intelligence Report PDF."""
        data = self.report_gen.generate_report(cycle_month)
        meta = data["executive_summary"]
        macro = data["macro_signals"]

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=48
        )

        elements = []

        # --- TOP HEADER BANNER ---
        hdr_data = [
            [
                Paragraph("<b>NATIONAL BONDS CORPORATION</b><br/><font size=9 color='#0284c7'><b>AI-ENABLED PRODUCT MANAGEMENT TRANSFORMATION</b></font>", self.s_title),
                Paragraph(f"<font color='#64748b'>DATE: <b>{data['generated_date']}</b><br/>REF: <b>{data['report_ref']}</b><br/>STATUS: <font color='#10b981'><b>CERTIFIED</b></font></font>", self.s_meta_val)
            ]
        ]
        hdr_table = Table(hdr_data, colWidths=[360, 160])
        hdr_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(hdr_table)
        elements.append(Spacer(1, 4))

        # Sub-banner rule
        rule_table = Table([[""]], colWidths=[520], rowHeights=[2.5])
        rule_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0284c7")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0)
        ]))
        elements.append(rule_table)
        elements.append(Spacer(1, 10))

        # Transmittal Metadata Box
        trans_data = [
            [
                Paragraph("<b>TO:</b>", self.s_meta_label),
                Paragraph("Group Chief Commercial Officer (GCCO) & Steering Committee", self.s_meta_val),
                Paragraph("<b>CYCLE:</b>", self.s_meta_label),
                Paragraph(f"<b>{data['reporting_cycle']}</b>", self.s_meta_val)
            ],
            [
                Paragraph("<b>FROM:</b>", self.s_meta_label),
                Paragraph("AI Product Intelligence & Early Warning Engine", self.s_meta_val),
                Paragraph("<b>SECURITY:</b>", self.s_meta_label),
                Paragraph("<font color='#dc2626'><b>COMMERCIAL-IN-CONFIDENCE</b></font>", self.s_meta_val)
            ]
        ]
        trans_table = Table(trans_data, colWidths=[45, 235, 60, 180])
        trans_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ]))
        elements.append(trans_table)
        elements.append(Spacer(1, 12))

        # --- SECTION 1: EXECUTIVE MACRO & PORTFOLIO PERFORMANCE ---
        elements.append(Paragraph("1. EXECUTIVE MACRO & PORTFOLIO PERFORMANCE SYNTHESIS", self.s_sec_header))
        
        kpi_card_data = [
            [
                Paragraph(f"<font color='#64748b'>NET INFLOWS</font><br/><b>AED {meta['total_net_m']:.1f}M</b><br/><font color='#dc2626'>Target: AED {meta['total_target_m']:.1f}M ({meta['variance_pct']:+.1f}%)</font>", self.s_callout),
                Paragraph(f"<font color='#64748b'>TOTAL REDEMPTIONS</font><br/><b>AED {meta['total_redemptions_m']:.1f}M</b><br/><font color='#f59e0b'>{meta['redemption_ratio_pct']:.1f}% of Gross Volume</font>", self.s_callout),
                Paragraph(f"<font color='#64748b'>CBUAE BASE RATE</font><br/><b>{macro['cbuae_base_rate_pct']:.2f}%</b><br/><font color='#10b981'>3M EIBOR: {macro['eibor_3m_pct']:.2f}%</font>", self.s_callout),
                Paragraph(f"<font color='#64748b'>SAVINGS INDEX</font><br/><b>{macro['consumer_savings_index']} Pts</b><br/><font color='#0284c7'>CPI Inflation: {macro['inflation_rate_pct']:.1f}%</font>", self.s_callout)
            ]
        ]
        kpi_table = Table(kpi_card_data, colWidths=[130, 130, 130, 130])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 8))

        elements.append(Paragraph(f"<b>Market Pulse:</b> {macro['macro_narrative']}", self.s_body))
        elements.append(Spacer(1, 10))

        # Inflows Chart
        chart_inflows = generate_inflows_chart(data["product_breakdown"])
        elements.append(Image(chart_inflows, width=520, height=208))
        elements.append(Spacer(1, 14))

        # --- SECTION 2: PRODUCT BREAKDOWN TABLE ---
        elements.append(Paragraph("2. PRODUCT-BY-PRODUCT COMMERCIAL TRAJECTORY", self.s_sec_header))
        
        prod_table_data = [
            [
                Paragraph("<b>Product Name</b>", self.s_meta_label),
                Paragraph("<b>Active Savers</b>", self.s_meta_label),
                Paragraph("<b>Net Inflows</b>", self.s_meta_label),
                Paragraph("<b>Target Plan</b>", self.s_meta_label),
                Paragraph("<b>Variance</b>", self.s_meta_label),
                Paragraph("<b>Health Status</b>", self.s_meta_label)
            ]
        ]
        for p in data["product_breakdown"]:
            dev = p["deviation_pct"]
            if dev <= -15:
                s_color = "#dc2626"
                s_txt = "CRITICAL BREACH"
            elif dev <= -8:
                s_color = "#d97706"
                s_txt = "EARLY WARNING"
            else:
                s_color = "#16a34a"
                s_txt = "OPTIMAL"
            
            prod_table_data.append([
                Paragraph(f"<b>{p['product_name']}</b>", self.s_body),
                Paragraph(f"{p['active_customers']:,}", self.s_body),
                Paragraph(f"AED {p['net_inflows_m']:.2f}M", self.s_body),
                Paragraph(f"AED {p['target_inflows_m']:.2f}M", self.s_body),
                Paragraph(f"<font color='{s_color}'><b>{dev:+.1f}%</b></font>", self.s_body),
                Paragraph(f"<font color='{s_color}'><b>{s_txt}</b></font>", self.s_body)
            ])

        p_table = Table(prod_table_data, colWidths=[140, 75, 75, 75, 65, 90])
        p_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ]))
        elements.append(p_table)
        elements.append(Spacer(1, 14))

        # --- PAGE BREAK FOR REPORT PAGES 2 & 3 ---
        elements.append(PageBreak())

        # --- SECTION 3: CROSS-INDICATOR CORRELATIONS & COMPETITORS ---
        elements.append(Paragraph("3. CROSS-INDICATOR CORRELATIONS & COMPETITIVE DYNAMICS", self.s_sec_header))
        for c in data["cross_correlations"]:
            c_table_data = [[
                Paragraph(f"<b>{c['insight']}</b><br/>{c['detail']}", self.s_callout)
            ]]
            ct = Table(c_table_data, colWidths=[520])
            ct.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f9ff")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#0284c7")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
            ]))
            elements.append(ct)
            elements.append(Spacer(1, 6))

        elements.append(Spacer(1, 6))
        chart_comp = generate_competitor_chart(macro.get("competitor_benchmarks", []))
        elements.append(Image(chart_comp, width=520, height=176))
        elements.append(Spacer(1, 14))

        # --- SECTION 4 & 5: RISKS, WATCH ITEMS & ALCO DECISIONS ---
        elements.append(Paragraph("4. EMERGING RISKS & WATCH ITEMS", self.s_sec_header))
        for w in data["watch_items"]:
            w_box = Table([[Paragraph(f"<font color='#b45309'><b>[!] ALERT:</b> {w}</font>", self.s_callout)]], colWidths=[520])
            w_box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fffbeb")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#f59e0b")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
            ]))
            elements.append(w_box)
            elements.append(Spacer(1, 4))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph("5. RECOMMENDED COMMERCIAL MANAGEMENT DECISIONS", self.s_sec_header))
        for r in data["management_recommendations"]:
            r_box = Table([[Paragraph(f"<font color='#0369a1'><b>&bull;</b> {r}</font>", self.s_body)]], colWidths=[520])
            r_box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
            ]))
            elements.append(r_box)
            elements.append(Spacer(1, 4))

        elements.append(Spacer(1, 14))

        # Formal Sign-Off Footer Table
        sign_data = [
            [
                Paragraph("<b>PREPARED BY:</b><br/>Fariha Fatima Hameed<br/>Product Management Lead", self.s_meta_val),
                Paragraph("<b>REVIEWED BY:</b><br/>Jawad Ahmad<br/>Lead AI Solutions Architect", self.s_meta_val),
                Paragraph("<b>EXECUTIVE ENDORSEMENT:</b><br/>Office of the GCCO<br/>National Bonds Corporation", self.s_meta_val)
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

        doc.build(elements, canvasmaker=NumberedCanvas)
        buf.seek(0)
        return buf.getvalue()

    def generate_gcco_escalation_memo_pdf(self, product_name, cycle_month, dev, deficit_m, net_inflow_m, target_inflow_m, briefing_text):
        """Builds a beautiful 2-page GCCO Executive Escalation Briefing Memo PDF."""
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=48
        )

        elements = []

        # Header Banner
        hdr_data = [
            [
                Paragraph("<b>NATIONAL BONDS CORPORATION</b><br/><font size=9 color='#dc2626'><b>EXECUTIVE PRODUCT ESCALATION DOSSIER</b></font>", self.s_title),
                Paragraph(f"<font color='#64748b'>DATE: <b>{datetime.now().strftime('%d %B %Y')}</b><br/>CYCLE: <b>{cycle_month}</b><br/>STATUS: <font color='#dc2626'><b>GOVERNANCE ESCALATION</b></font></font>", self.s_meta_val)
            ]
        ]
        hdr_table = Table(hdr_data, colWidths=[360, 160])
        hdr_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ]))
        elements.append(hdr_table)
        elements.append(Spacer(1, 4))

        # Red Rule
        rule_table = Table([[""]], colWidths=[520], rowHeights=[2.5])
        rule_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#dc2626")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0)
        ]))
        elements.append(rule_table)
        elements.append(Spacer(1, 10))

        # Memo Metadata Box
        memo_data = [
            [
                Paragraph("<b>TO:</b>", self.s_meta_label),
                Paragraph("Group Chief Commercial Officer (GCCO)", self.s_meta_val),
                Paragraph("<b>PRODUCT:</b>", self.s_meta_label),
                Paragraph(f"<b>{product_name}</b>", self.s_meta_val)
            ],
            [
                Paragraph("<b>FROM:</b>", self.s_meta_label),
                Paragraph("AI Product Intelligence & Early Warning System", self.s_meta_val),
                Paragraph("<b>DEFICIT GAP:</b>", self.s_meta_label),
                Paragraph(f"<font color='#dc2626'><b>{dev:+.1f}% (AED {deficit_m:.2f}M)</b></font>", self.s_meta_val)
            ],
            [
                Paragraph("<b>ACTUAL NET:</b>", self.s_meta_label),
                Paragraph(f"AED {net_inflow_m:.2f}M (Target: AED {target_inflow_m:.2f}M)", self.s_meta_val),
                Paragraph("<b>ACTION REQUIRED:</b>", self.s_meta_label),
                Paragraph("<b>ALCO & GCCO Commercial Endorsement</b>", self.s_meta_val)
            ]
        ]
        memo_table = Table(memo_data, colWidths=[45, 225, 75, 175])
        memo_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5)
        ]))
        elements.append(memo_table)
        elements.append(Spacer(1, 10))

        # Trajectory Chart
        elements.append(Paragraph("1. HISTORICAL 18-MONTH PERFORMANCE TRAJECTORY", self.s_sec_header))
        chart_traj = generate_product_trajectory_chart(self.kpi_df, product_name, cycle_month)
        elements.append(Image(chart_traj, width=520, height=208))
        elements.append(Spacer(1, 12))

        # Executive Briefing Commentary
        elements.append(Paragraph("2. ROOT-CAUSE INVESTIGATION & TACTICAL ANALYSIS", self.s_sec_header))
        # Format briefing text paragraphs
        for line in briefing_text.split("\n"):
            if line.strip():
                if line.startswith("="):
                    continue
                elif line.startswith("SECTION") or line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
                    elements.append(Paragraph(f"<b>{line.strip()}</b>", self.s_body_bold))
                elif line.startswith("-") or line.startswith("*") or line.startswith("•"):
                    elements.append(Paragraph(f"&bull; {line.strip()[1:].strip()}", self.s_body))
                else:
                    elements.append(Paragraph(line.strip(), self.s_body))
                elements.append(Spacer(1, 2))

        elements.append(Spacer(1, 14))

        # Human in the loop decision box
        dec_data = [
            [Paragraph("<b>FORMAL GCCO HUMAN-IN-THE-LOOP EXECUTIVE ACTION SIGN-OFF</b>", self.s_body_bold)],
            [Paragraph("I hereby review the autonomous findings and authorize the tactical countermeasures:<br/><br/>[ &nbsp; ] <b>APPROVED TO EXECUTE</b> &nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] <b>CONDITIONAL APPROVAL</b> &nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] <b>REVISE / RE-MODEL</b><br/><br/><b>GCCO Signature:</b> ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> ______________", self.s_body)]
        ]
        dec_table = Table(dec_data, colWidths=[520])
        dec_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#ffffff")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#0f172a")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
        ]))
        elements.append(dec_table)

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
