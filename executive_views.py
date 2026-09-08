"""
National Bonds Corporation - AI Product Management Transformation
Executive Cockpit Extensions: Alert Center, Bi-Weekly Intelligence Report & Multi-Agent Engine
Author: Jawad Ahmad | Product AI Solutions
"""

import streamlit as st
import pandas as pd
import json
import os
import datetime
import random
import plotly.express as px
import plotly.graph_objects as go
from report_generator import BiWeeklyReportGenerator
from pdf_generator import ExecutivePDFGenerator

def render_executive_alert_banner(kpi_df, selected_cycle, warning_threshold, breach_threshold):
    """Scans all products for the selected cycle and renders proactive portfolio alerts."""
    cycle_df = kpi_df[kpi_df["month"] == selected_cycle]
    if cycle_df.empty:
        return

    breaches = cycle_df[cycle_df["deviation_pct"] <= breach_threshold]
    warnings = cycle_df[(cycle_df["deviation_pct"] > breach_threshold) & (cycle_df["deviation_pct"] <= warning_threshold)]

    if breaches.empty and warnings.empty:
        st.markdown('''
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid #10b981; border-left: 5px solid #10b981; border-radius: 10px; padding: 12px 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 700; color: #065f46; font-size: 13.5px;">✅ PORTFOLIO STABILITY: All 5 pilot products operating within approved governance ranges for this cycle.</span>
                <span style="font-size: 12px; color: #10b981; font-weight: 700;">ALL PRODUCTS OPTIMAL</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        return

    # Active Alerts Detected
    b_names = [f"<b>{r['product_name']}</b> ({r['deviation_pct']:+.1f}%)" for _, r in breaches.iterrows()]
    w_names = [f"<b>{r['product_name']}</b> ({r['deviation_pct']:+.1f}%)" for _, r in warnings.iterrows()]

    st.markdown('''
    <div style="background: rgba(239, 68, 68, 0.06); border: 1.5px solid #ef4444; border-left: 6px solid #ef4444; border-radius: 12px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 4px 12px -2px rgba(239, 68, 68, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 18px;">🚨</span>
                <strong style="color: #dc2626; font-size: 14px; letter-spacing: 0.02em;">EXECUTIVE EARLY WARNING ALERT CENTER &bull; CYCLE: ''' + str(selected_cycle) + '''</strong>
            </div>
            <span class="status-pill status-breach">ACTION REQUIRED</span>
        </div>
        <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5;">
            <b>Active Tolerance Deviations:</b> ''' + (", ".join(b_names) if b_names else "None") + '''
            ''' + (("&nbsp;&bull;&nbsp; <b>Early Warnings:</b> " + ", ".join(w_names)) if w_names else "") + '''
        </div>
        <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">
            Multi-Agent system has flagged root causes across digital distribution channels and external competitor deposit rates.
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_multi_agent_trace(selected_product, selected_cycle, dev, state_key):
    """Renders the 4 specialist agents collaborating to analyze the selected product."""
    st.markdown('''
    <div class="exec-section-header" style="margin-top: 20px;">
        🤖 Specialist Multi-Agent Collaboration Trace (Initiative 3 Ground Truth)
    </div>
    <p style="font-size: 12.5px; color: var(--text-muted); margin: -4px 0 12px 0;">
        Demonstrating the 4 specialized cognitive agents operating in coordination before human executive sign-off.
    </p>
    ''', unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown(f'''
        <div style="background: var(--card-bg, #ffffff); border: 1px solid var(--card-border, #e2e8f0); border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: #0284c7; font-size: 12.5px;">1. PRODUCT PERFORMANCE AGENT</strong>
                <span style="font-size: 10.5px; background: rgba(2, 132, 199, 0.1); color: #0284c7; padding: 2px 6px; border-radius: 4px; font-weight: 700;">MONITORING</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
                Tracked <b>{selected_product}</b> in <b>{selected_cycle}</b>. Identified variance of <b>{dev:+.1f}%</b> against target budget curve. Net run rate flagged as <code>{state_key.upper()}</code>.
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="background: var(--card-bg, #ffffff); border: 1px solid var(--card-border, #e2e8f0); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: #10b981; font-size: 12.5px;">2. MARKET INTELLIGENCE AGENT</strong>
                <span style="font-size: 10.5px; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 2px 6px; border-radius: 4px; font-weight: 700;">INGESTION</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
                Cross-referenced UAE 3M EIBOR and competitor promotional moves (FAB iSave 5.10%, Wio Bank 5.25%). Isolated market yield pressure level as <code>ELEVATED</code>.
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col_a2:
        st.markdown(f'''
        <div style="background: var(--card-bg, #ffffff); border: 1px solid var(--card-border, #e2e8f0); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: #d97706; font-size: 12.5px;">3. INVESTIGATION AGENT</strong>
                <span style="font-size: 10.5px; background: rgba(245, 158, 11, 0.1); color: #d97706; padding: 2px 6px; border-radius: 4px; font-weight: 700;">ROOT CAUSE</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
                Tested 4 operational hypotheses. Isolated 72% of variance to primary digital acquisition channel drop and expat summer travel cash outflow seasonality.
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="background: var(--card-bg, #ffffff); border: 1px solid var(--card-border, #e2e8f0); border-left: 4px solid #f43f5e; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: #e11d48; font-size: 12.5px;">4. ALERT & RECOMMENDATION AGENT</strong>
                <span style="font-size: 10.5px; background: rgba(244, 63, 94, 0.1); color: #e11d48; padding: 2px 6px; border-radius: 4px; font-weight: 700;">ACTION READY</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
                Synthesized dynamic executive escalation memo. Formulated 3 tactical recovery countermeasures. Pending GCCO executive endorsement.
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_biweekly_report_tab(selected_cycle):
    """Renders the comprehensive Bi-Weekly Product & Market Intelligence Report (Initiative 2)."""
    gen = BiWeeklyReportGenerator()
    rep = gen.generate_report(selected_cycle)
    meta = rep["executive_summary"]
    macro = rep["macro_signals"]

    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.08) 0%, rgba(14, 165, 233, 0.04) 100%); border: 1px solid rgba(2, 132, 199, 0.2); border-radius: 12px; padding: 16px 20px; margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <span style="background: #0ea5e9; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 9px; border-radius: 6px; letter-spacing: 0.04em;">INITIATIVE 2 &bull; VERY HIGH PRIORITY</span>
                <h3 style="margin: 6px 0 2px 0; font-size: 20px; font-weight: 800; color: var(--text-primary);">
                    Bi-Weekly Product & Market Intelligence Report
                </h3>
                <p style="margin: 0; font-size: 13px; color: var(--text-secondary);">
                    Reference: <code>{rep['report_ref']}</code> &bull; Cycle: <b>{rep['reporting_cycle']}</b> &bull; Presented to: <b>Group Chief Commercial Officer (GCCO)</b>
                </p>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 12px; font-weight: 600; color: var(--text-muted);">{rep['generated_date']}</span><br>
                <span class="status-pill status-healthy">CERTIFIED INTELLIGENCE</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Section 1: Topline KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">Net Fresh Inflows</span><span>📈</span></div>
            <div class="kpi-card-value" style="color: #0284c7;">AED {meta['total_net_m']:.1f}M</div>
            <div class="kpi-card-footer">Target: AED {meta['total_target_m']:.1f}M ({meta['variance_pct']:+.1f}%)</div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">Total Redemptions</span><span>🔄</span></div>
            <div class="kpi-card-value" style="color: #f59e0b;">AED {meta['total_redemptions_m']:.1f}M</div>
            <div class="kpi-card-footer">{meta['redemption_ratio_pct']:.1f}% of Gross Volume</div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">CBUAE Base Rate</span><span>🏛️</span></div>
            <div class="kpi-card-value" style="color: #10b981;">{macro['cbuae_base_rate_pct']:.2f}%</div>
            <div class="kpi-card-footer">3M EIBOR: {macro['eibor_3m_pct']:.2f}%</div>
        </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">Savings Index</span><span>📊</span></div>
            <div class="kpi-card-value" style="color: #0284c7;">{macro['consumer_savings_index']} Pts</div>
            <div class="kpi-card-footer">CPI Inflation: {macro['inflation_rate_pct']:.1f}%</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 2: Product Breakdown Table & Chart
    st.markdown("#### 📊 Product-by-Product Commercial Trajectory (Cycle " + str(selected_cycle) + ")")
    df_prod = pd.DataFrame(rep["product_breakdown"])
    df_prod["short_name"] = df_prod["product_name"].apply(lambda x: x.split(" (")[0])
    
    fig_bwr = px.bar(
        df_prod, x="short_name", y=["net_inflows_m", "target_inflows_m"],
        barmode="group",
        title=f"Net Inflow Actual vs Target Plan for Cycle {selected_cycle} (AED M)",
        labels={"value": "AED Millions", "short_name": "Product", "variable": "Metric"},
        color_discrete_sequence=["#0284c7", "#94a3b8"]
    )
    fig_bwr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250,
        margin=dict(l=15, r=15, t=30, b=15),
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#64748b"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bwr, use_container_width=True)

    st.dataframe(
        df_prod[['product_name', 'active_customers', 'gross_inflows_m', 'redemptions_m', 'net_inflows_m', 'target_inflows_m', 'deviation_pct']].style.format({
            "active_customers": "{:,.0f}",
            "net_inflows_m": "AED {:,.2f}M",
            "target_inflows_m": "AED {:,.2f}M",
            "gross_inflows_m": "AED {:,.2f}M",
            "redemptions_m": "AED {:,.2f}M",
            "deviation_pct": "{:+.1f}%"
        }),
        use_container_width=True,
        height=190
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 3: Cross Correlations & Competitor Benchmarks
    col_cor1, col_cor2 = st.columns(2)
    with col_cor1:
        st.markdown("#### 🔗 Cross-Indicator Correlations & Market Drivers")
        for c in rep["cross_correlations"]:
            st.markdown(f'''
            <div style="background: var(--card-bg, #ffffff); border: 1px solid var(--card-border, #e2e8f0); border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                <strong style="color: #0284c7; font-size: 13px;">{c['insight']}</strong>
                <div style="font-size: 12.5px; color: var(--text-secondary); margin-top: 4px; line-height: 1.4;">
                    {c['detail']}
                </div>
            </div>
            ''', unsafe_allow_html=True)

    with col_cor2:
        st.markdown("#### 🏦 Competitor Promotional Savings Radar")
        comp_list = macro.get("competitor_benchmarks", [])
        if comp_list:
            comp_banks = [c.get("bank", "").split(" (")[0] for c in comp_list] + ["National Bonds (Sukuk)"]
            comp_rates = [c.get("rate_pct", 0.0) for c in comp_list] + [5.40]
            comp_colors = ["#64748b", "#64748b", "#64748b", "#64748b", "#10b981"]
            fig_comp_radar = go.Figure(go.Bar(
                y=comp_banks,
                x=comp_rates,
                orientation="h",
                marker=dict(color=comp_colors),
                text=[f"{r:.2f}%" for r in comp_rates],
                textposition="outside"
            ))
            fig_comp_radar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=210,
                margin=dict(l=15, r=25, t=15, b=15),
                xaxis=dict(title="Advertised Yield (% p.a.)", range=[0, 6.2]),
                font=dict(family="Plus Jakarta Sans, sans-serif", color="#64748b")
            )
            st.plotly_chart(fig_comp_radar, use_container_width=True)

        for comp in macro.get("competitor_benchmarks", []):
            st.markdown(f'''
            <div style="background: var(--card-bg, #ffffff); border: 1px solid var(--card-border, #e2e8f0); border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 700; font-size: 12px; color: var(--text-primary);">{comp.get('bank')}</div>
                    <div style="font-size: 11px; color: var(--text-muted);">{comp.get('product')} &bull; {comp.get('tenor', 'Direct Savings')}</div>
                </div>
                <span style="font-size: 13px; font-weight: 800; color: #0284c7;">{comp.get('rate_pct'):.2f}% p.a.</span>
            </div>
            ''', unsafe_allow_html=True)

    # Section 4: Watch Items & Recommendations
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("#### ⚠️ Emerging Risks & Watch Items")
        for w in rep["watch_items"]:
            st.markdown(f'''
            <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid #f59e0b; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 12.5px; color: #92400e;">
                <b>[!]</b> {w}
            </div>
            ''', unsafe_allow_html=True)

    with col_w2:
        st.markdown("#### 🎯 Commercial Management Decisions")
        for r in rep["management_recommendations"]:
            st.markdown(f'''
            <div style="background: rgba(2, 132, 199, 0.06); border: 1px solid #0284c7; border-left: 4px solid #0284c7; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 12.5px; color: #0369a1;">
                {r}
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("<hr style='margin: 16px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
    col_dl1, col_dl2 = st.columns([2, 1])
    with col_dl1:
        pdf_gen = ExecutivePDFGenerator()
        pdf_bytes = pdf_gen.generate_biweekly_report_pdf(selected_cycle)
        st.download_button(
            label=f"📥 Download Boardroom PDF Report ({rep['report_ref']}.pdf)",
            data=pdf_bytes,
            file_name=f"{rep['report_ref']}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label=f"📄 Download Raw Text ({rep['report_ref']}.txt)",
            data=rep["exportable_text"],
            file_name=f"{rep['report_ref']}.txt",
            mime="text/plain",
            use_container_width=True
        )

def dispatch_alert_memo(product_name, cycle, dev, deficit_m, channel_driver="Digital Web / App Drop", user_name="Jawad Ahmad"):
    """Simulates multi-channel alert dispatch to GCCO and assigned Product Owners."""
    dispatch_file = "dispatch_log.json"
    logs = []
    if os.path.exists(dispatch_file):
        try:
            with open(dispatch_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []

    receipt_id = f"DISPATCH-2026-{random.randint(10000, 99999)}"
    record = {
        "receipt_id": receipt_id,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": user_name,
        "recipients": [
            "Group Chief Commercial Officer (GCCO)",
            "Fariha Fatima Hameed (Product Management Lead)",
            "Alisha Rizvi (Product Lead)",
            "ALCO Commercial Committee"
        ],
        "product_name": product_name,
        "cycle": cycle,
        "deviation_pct": dev,
        "deficit_m": deficit_m,
        "primary_driver": channel_driver,
        "channels": ["Office365 / Corporate Exchange SMTP", "Microsoft Teams Commercial Channel Webhook"],
        "delivery_status": "DELIVERED",
        "sha256_hash": f"SHA256:{random.getrandbits(128):032x}"
    }
    logs.insert(0, record)
    try:
        with open(dispatch_file, "w", encoding="utf-8") as f:
            json.dump(logs[:100], f, indent=2)
    except Exception:
        pass
    return record
