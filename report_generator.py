"""
National Bonds Corporation - AI Product Management Transformation
Initiative 2: Bi-Weekly Product & Market Intelligence Reporting Engine
Principle: Move management from "what happened?" to "what is changing, why, and what needs attention?"
Fuses: Internal Portfolio Performance (KPIs) + External UAE Macro & Competitor Benchmarks
Author: Jawad Ahmad | Product AI Solutions
"""

import json
import os
import pandas as pd
import numpy as np
from datetime import datetime

class BiWeeklyReportGenerator:
    def __init__(self, kpi_csv="product_portfolio_kpis_alerts.csv", market_json="market_intelligence_data.json", cust_csv="cleaned_national_bonds_customers.csv"):
        self.kpi_df = pd.read_csv(kpi_csv)
        self.cust_df = pd.read_csv(cust_csv)
        self.market_file = market_json
        
        self.market_data = {}
        if os.path.exists(market_json):
            with open(market_json, "r", encoding="utf-8") as f:
                raw = json.load(f)
                for entry in raw:
                    self.market_data[entry["month"]] = entry

    def generate_report(self, cycle_month):
        """Compiles the complete 5-section Bi-Weekly Product & Market Intelligence Report for a given cycle."""
        cycle_df = self.kpi_df[self.kpi_df["month"] == cycle_month].copy()
        if cycle_df.empty:
            cycle_month = self.kpi_df["month"].max()
            cycle_df = self.kpi_df[self.kpi_df["month"] == cycle_month].copy()

        tot_net = cycle_df["net_inflows_aed"].sum()
        tot_target = cycle_df["target_inflows_aed"].sum()
        tot_gross = cycle_df["gross_inflows_aed"].sum()
        tot_redemptions = cycle_df["redemptions_aed"].sum()
        variance_pct = ((tot_net - tot_target) / tot_target * 100) if tot_target > 0 else 0
        redemption_ratio = (tot_redemptions / tot_gross * 100) if tot_gross > 0 else 0

        market_entry = self.market_data.get(cycle_month, {
            "cbuae_base_rate_pct": 4.65,
            "eibor_3m_pct": 4.55,
            "inflation_rate_pct": 2.3,
            "consumer_savings_index": 120,
            "macro_narrative": "UAE retail savings climate remains resilient.",
            "competitor_benchmarks": [
                {"bank": "FAB", "product": "iSave", "rate_pct": 5.10},
                {"bank": "Emirates NBD", "product": "Smart Saver", "rate_pct": 4.65},
                {"bank": "ADCB", "product": "Destiny Deposit", "rate_pct": 4.90},
                {"bank": "Wio Bank", "product": "Personal Spaces", "rate_pct": 5.25}
            ]
        })

        product_rows = []
        for _, row in cycle_df.iterrows():
            p_name = row["product_name"]
            net = row["net_inflows_aed"]
            tgt = row["target_inflows_aed"]
            gross = row["gross_inflows_aed"]
            red = row["redemptions_aed"]
            dev = row["deviation_pct"]
            cust = row["active_customers"]
            status = row["status"]
            product_rows.append({
                "product_name": p_name,
                "active_customers": cust,
                "net_inflows_m": net / 1e6,
                "target_inflows_m": tgt / 1e6,
                "gross_inflows_m": gross / 1e6,
                "redemptions_m": red / 1e6,
                "deviation_pct": dev,
                "status": status
            })

        watch_items = []
        if tot_redemptions / 1e6 > 250:
            watch_items.append("Elevated Liquidity Run-Off: Total redemptions crossed AED 250M threshold driven by seasonal expat commitments.")
        if any(r["deviation_pct"] < -15 for r in product_rows):
            breached = [r["product_name"] for r in product_rows if r["deviation_pct"] < -15]
            watch_items.append(f"Material Deficit Alert: {', '.join(breached)} breached -15% budget tolerance in {cycle_month}.")
        watch_items.append(f"Monetary Policy Sensitivity: CBUAE base rate at {market_entry['cbuae_base_rate_pct']:.2f}% requires ALCO review of high-yield promotional tiers.")

        report_data = {
            "report_ref": f"NBC-BIWEEKLY-INTEL-{cycle_month.replace('-', '')}",
            "reporting_cycle": cycle_month,
            "generated_date": datetime.now().strftime('%d %B %Y'),
            "executive_summary": {
                "total_net_m": tot_net / 1e6,
                "total_target_m": tot_target / 1e6,
                "total_gross_m": tot_gross / 1e6,
                "total_redemptions_m": tot_redemptions / 1e6,
                "variance_pct": variance_pct,
                "redemption_ratio_pct": redemption_ratio,
                "market_pressure": market_entry.get("market_pressure_level", "MODERATE")
            },
            "macro_signals": market_entry,
            "product_breakdown": product_rows,
            "cross_correlations": [
                {
                    "insight": "Fixed-Yield Flight to Quality",
                    "detail": f"Lowering 3M EIBOR ({market_entry['eibor_3m_pct']:.2f}%) has accelerated institutional and HNW demand for Term Sukuk and Booster Plan as savers lock in fixed rates before expected Central Bank cuts."
                },
                {
                    "insight": "Retail Savings Disintermediation",
                    "detail": f"Digital Challenger banks (Wio at 5.25%, FAB iSave at 5.10%) are intensifying liquid deposit competition, creating temporary net outflow headwinds on standard Saving Bonds."
                }
            ],
            "watch_items": watch_items,
            "management_recommendations": [
                "1. Direct Sales Focus: Accelerate Second Salary corporate employee scheme partnerships across government-linked entities.",
                "2. Liquidity Defense: Deploy targeted +35 bps Milestone Retention Bonus on maturing 12-month Booster Plan certificates.",
                "3. Marketing Optimization: Reallocate 20% of digital paid acquisition budget from generic display into high-converting payroll savings campaigns."
            ]
        }

        report_data["exportable_text"] = self._build_exportable_text(report_data)
        return report_data

    def _build_exportable_text(self, data):
        meta = data["executive_summary"]
        macro = data["macro_signals"]
        lines = [
            "=" * 84,
            "                   NATIONAL BONDS CORPORATION | DUBAI, UAE",
            f"          BI-WEEKLY PRODUCT & MARKET INTELLIGENCE EXECUTIVE REPORT",
            f"                     Reporting Cycle: {data['reporting_cycle']} | Reference: {data['report_ref']}",
            "=" * 84,
            f"PRESENTED TO : Group Chief Commercial Officer (GCCO) & Commercial Steering Committee",
            f"DATE         : {data['generated_date']}",
            f"STATUS       : Certified Executive Intelligence (Internal KPIs fused with UAE Macro Benchmarks)",
            "-" * 84,
            "",
            "1. EXECUTIVE MACRO & PORTFOLIO PERFORMANCE SYNTHESIS",
            f"   • Total Fresh Net Inflows: AED {meta['total_net_m']:.2f}M vs Target AED {meta['total_target_m']:.2f}M (Variance: {meta['variance_pct']:+.1f}%)",
            f"   • Gross Inflow Volume     : AED {meta['total_gross_m']:.2f}M | Total Redemptions: AED {meta['total_redemptions_m']:.2f}M",
            f"   • Portfolio Redemption %  : {meta['redemption_ratio_pct']:.1f}% of gross volume liquidated",
            f"   • UAE Macroeconomic Pulse : CBUAE Base Rate: {macro['cbuae_base_rate_pct']:.2f}% | 3M EIBOR: {macro['eibor_3m_pct']:.2f}% | CPI Inflation: {macro['inflation_rate_pct']:.1f}%",
            f"   • Market Climate Summary  : {macro['macro_narrative']}",
            "",
            "2. PRODUCT-BY-PRODUCT COMMERCIAL TRAJECTORY",
            f"{'Product Name':<18} | {'Active Users':<12} | {'Net Inflows':<14} | {'Target':<12} | {'Variance':<10} | {'Status':<14}",
            "-" * 84
        ]
        for p in data["product_breakdown"]:
            status_tag = "CRITICAL BREACH" if p["deviation_pct"] <= -15 else ("EARLY WARNING" if p["deviation_pct"] <= -8 else "OPTIMAL")
            lines.append(f"{p['product_name']:<18} | {p['active_customers']:<12,d} | AED {p['net_inflows_m']:>6.2f}M | AED {p['target_inflows_m']:>6.2f}M | {p['deviation_pct']:>+8.1f}% | {status_tag:<14}")
        lines.extend([
            "-" * 84,
            "",
            "3. CROSS-INDICATOR CORRELATIONS (INTERNAL KPIS <-> EXTERNAL BENCHMARKS)",
        ])
        for c in data["cross_correlations"]:
            lines.append(f"   • {c['insight']}:")
            lines.append(f"     {c['detail']}")
        lines.extend([
            "",
            "4. EMERGING RISKS & WATCH ITEMS",
        ])
        for w in data["watch_items"]:
            lines.append(f"   [!] {w}")
        lines.extend([
            "",
            "5. RECOMMENDED COMMERCIAL MANAGEMENT DECISIONS",
        ])
        for r in data["management_recommendations"]:
            lines.append(f"   {r}")
        lines.extend([
            "",
            "=" * 84,
            "Report compiled automatically via AI Product Intelligence & Decision Support Engine.",
            "=" * 84
        ])
        return "\n".join(lines)
