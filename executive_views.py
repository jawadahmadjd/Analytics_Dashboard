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
from icons import ICONS, get_icon

def render_executive_alert_banner(kpi_df, selected_cycle, warning_threshold, breach_threshold):
    """Scans all products for the selected cycle and renders proactive portfolio alerts."""
    cycle_df = kpi_df[kpi_df["month"] == selected_cycle]
    if cycle_df.empty:
        return

    breaches = cycle_df[cycle_df["deviation_pct"] <= breach_threshold]
    warnings = cycle_df[(cycle_df["deviation_pct"] > breach_threshold) & (cycle_df["deviation_pct"] <= warning_threshold)]

    if breaches.empty and warnings.empty:
        st.markdown(f'''
        <div style="background: var(--status-positive-bg); border: 1px solid var(--status-positive-border); border-left: 3px solid var(--status-positive); border-radius: var(--radius-sm); padding: 10px 16px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    {get_icon('check-circle', 15, 'var(--status-positive)')}
                    <span style="font-weight: 600; color: var(--status-positive); font-size: 13px;">Portfolio Stability: All 5 pilot products operating within approved governance ranges for cycle {selected_cycle}.</span>
                </div>
                <span class="status-pill status-healthy" style="font-size: 11px;">OPTIMAL</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        return

    # Active Alerts Detected
    b_names = [f"<b>{r['product_name']}</b> ({r['deviation_pct']:+.1f}%)" for _, r in breaches.iterrows()]
    w_names = [f"<b>{r['product_name']}</b> ({r['deviation_pct']:+.1f}%)" for _, r in warnings.iterrows()]

    if not breaches.empty:
        st.markdown(f'''
        <div style="background: var(--status-critical-bg); border: 1px solid var(--status-critical-border); border-left: 3px solid var(--status-critical); border-radius: var(--radius-sm); padding: 12px 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    {get_icon('alert-circle', 15, 'var(--status-critical)')}
                    <strong style="color: var(--status-critical); font-size: 13px; font-weight: 700;">Active Tolerance Deviations &mdash; Cycle {selected_cycle}</strong>
                </div>
                <span class="status-pill status-breach">ACTION REQUIRED</span>
            </div>
            <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                <span style="color: var(--text-secondary);">Deviations:</span> {", ".join(b_names) if b_names else "None"}
                {("&nbsp;&bull;&nbsp; <span style='color: var(--text-secondary);'>Early Warnings:</span> " + ", ".join(w_names)) if w_names else ""}
            </div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 4px;">
                Multi-agent cognitive engine flagged root causes across digital distribution drop and competitor deposit yields.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div style="background: var(--status-warning-bg); border: 1px solid var(--status-warning-border); border-left: 3px solid var(--status-warning); border-radius: var(--radius-sm); padding: 12px 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    {get_icon('alert-triangle', 15, 'var(--status-warning)')}
                    <strong style="color: var(--status-warning); font-size: 13px; font-weight: 700;">Early Warning Notice &mdash; Cycle {selected_cycle}</strong>
                </div>
                <span class="status-pill status-warning">MONITORING</span>
            </div>
            <div style="font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                <span style="color: var(--text-secondary);">Watchlist Products:</span> {", ".join(w_names)}
            </div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 4px;">
                Performance trajectory soft; operating within buffer but approaching governance boundaries.
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_multi_agent_trace(selected_product, selected_cycle, dev, state_key):
    """Renders the 4 specialist agents collaborating to analyze the selected product."""
    st.markdown('''
    <div class="exec-section-header" style="margin-top: 18px;">
        Specialist Multi-Agent Collaboration Trace
    </div>
    <p style="font-size: 12px; color: var(--text-tertiary); margin: -4px 0 12px 0;">
        Specialized cognitive agents operating in coordination prior to executive commercial dispatch.
    </p>
    ''', unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown(f'''
        <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid var(--brand-primary); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: var(--text-primary); font-size: 12px; font-weight: 600;">1. Product Performance Agent</strong>
                <span style="font-size: 10.5px; background: var(--surface-tertiary); color: var(--brand-text); padding: 2px 6px; border-radius: 4px; font-weight: 600;">MONITORING</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.45;">
                Tracked <b>{selected_product}</b> in <b>{selected_cycle}</b>. Identified variance of <b>{dev:+.1f}%</b> against target budget curve. Net run rate flagged as <code>{state_key.upper()}</code>.
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid var(--status-positive); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: var(--text-primary); font-size: 12px; font-weight: 600;">2. Market Intelligence Agent</strong>
                <span style="font-size: 10.5px; background: var(--status-positive-bg); color: var(--status-positive); padding: 2px 6px; border-radius: 4px; font-weight: 600;">INGESTION</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.45;">
                Cross-referenced UAE 3M EIBOR and competitor promotional moves (FAB iSave 5.10%, Wio Bank 5.25%). Isolated market yield pressure level as <code>ELEVATED</code>.
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col_a2:
        st.markdown(f'''
        <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid var(--status-warning); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: var(--text-primary); font-size: 12px; font-weight: 600;">3. Investigation Agent</strong>
                <span style="font-size: 10.5px; background: var(--status-warning-bg); color: var(--status-warning); padding: 2px 6px; border-radius: 4px; font-weight: 600;">ROOT CAUSE</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.45;">
                Tested 4 operational hypotheses. Isolated 72% of variance to primary digital acquisition channel drop and expat summer travel cash outflow seasonality.
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid var(--status-critical); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <strong style="color: var(--text-primary); font-size: 12px; font-weight: 600;">4. Alert & Recommendation Agent</strong>
                <span style="font-size: 10.5px; background: var(--status-critical-bg); color: var(--status-critical); padding: 2px 6px; border-radius: 4px; font-weight: 600;">ACTION READY</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.45;">
                Synthesized dynamic executive escalation memo. Formulated 3 tactical recovery countermeasures. Pending GCCO executive endorsement.
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_biweekly_report_tab(selected_cycle):
    """Renders the comprehensive Bi-Weekly Product & Market Intelligence Report."""
    gen = BiWeeklyReportGenerator()
    rep = gen.generate_report(selected_cycle)
    meta = rep["executive_summary"]
    macro = rep["macro_signals"]

    st.markdown(f'''
    <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-radius: var(--radius-md); padding: 16px 20px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.01em;">
                    Bi-Weekly Product & Market Intelligence Report
                </h3>
                <p style="margin: 4px 0 0 0; font-size: 13px; color: var(--text-secondary);">
                    Reference: <code style="font-family: 'JetBrains Mono', monospace; font-size: 12px;">{rep['report_ref']}</code> &bull; Cycle: <b>{rep['reporting_cycle']}</b> &bull; Addressed to: <b>Group Chief Commercial Officer (GCCO)</b>
                </p>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 12px; font-weight: 500; color: var(--text-tertiary);">{rep['generated_date']}</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Section 1: Topline KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">Net Fresh Inflows</span><span class="kpi-card-icon">{get_icon('trending-up', 15, 'var(--text-tertiary)')}</span></div>
            <div class="kpi-card-value">AED {meta['total_net_m']:.1f}M</div>
            <div class="kpi-card-footer">Target: AED {meta['total_target_m']:.1f}M ({meta['variance_pct']:+.1f}%)</div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">Total Redemptions</span><span class="kpi-card-icon">{get_icon('refresh', 15, 'var(--text-tertiary)')}</span></div>
            <div class="kpi-card-value">AED {meta['total_redemptions_m']:.1f}M</div>
            <div class="kpi-card-footer">{meta['redemption_ratio_pct']:.1f}% of Gross Volume</div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">CBUAE Base Rate</span><span class="kpi-card-icon">{get_icon('shield', 15, 'var(--text-tertiary)')}</span></div>
            <div class="kpi-card-value">{macro['cbuae_base_rate_pct']:.2f}%</div>
            <div class="kpi-card-footer">3M EIBOR: {macro['eibor_3m_pct']:.2f}%</div>
        </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-card-header"><span class="kpi-card-title">Savings Index</span><span class="kpi-card-icon">{get_icon('bar-chart', 15, 'var(--text-tertiary)')}</span></div>
            <div class="kpi-card-value">{macro['consumer_savings_index']} Pts</div>
            <div class="kpi-card-footer">CPI Inflation: {macro['inflation_rate_pct']:.1f}%</div>
        </div>
        ''', unsafe_allow_html=True)

    # Section 2: Product Breakdown Table & Chart
    st.markdown("<div class='exec-section-header'>Product Commercial Trajectory (Cycle " + str(selected_cycle) + ")</div>", unsafe_allow_html=True)
    df_prod = pd.DataFrame(rep["product_breakdown"])
    df_prod["short_name"] = df_prod["product_name"].apply(lambda x: x.split(" (")[0])
    
    fig_bwr = px.bar(
        df_prod, x="short_name", y=["net_inflows_m", "target_inflows_m"],
        barmode="group",
        title=f"Net Inflow Actual vs Target Plan for Cycle {selected_cycle} (AED M)",
        labels={"value": "AED Millions", "short_name": "Product", "variable": "Metric"},
        color_discrete_sequence=["#1B6EF3", "#8492A6"]
    )
    fig_bwr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=16, r=16, t=36, b=36),
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#8492A6", size=11),
        title=dict(font=dict(family="Inter, sans-serif", size=13, color="#1A1F36")),
        xaxis=dict(gridcolor="#F1F3F6", tickfont=dict(family="Inter, sans-serif", size=11)),
        yaxis=dict(gridcolor="#F1F3F6", tickfont=dict(family="Inter, sans-serif", size=11)),
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="left", x=0, font=dict(family="Inter, sans-serif", size=11))
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

    # Section 3: Cross Correlations & Competitor Benchmarks
    col_cor1, col_cor2 = st.columns(2)
    with col_cor1:
        st.markdown("<div class='exec-section-header'>Cross-Indicator Correlations & Market Drivers</div>", unsafe_allow_html=True)
        for c in rep["cross_correlations"]:
            st.markdown(f'''
            <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid var(--brand-primary); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 8px;">
                <strong style="color: var(--text-primary); font-size: 12.5px;">{c['insight']}</strong>
                <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px; line-height: 1.45;">
                    {c['detail']}
                </div>
            </div>
            ''', unsafe_allow_html=True)

    with col_cor2:
        st.markdown("<div class='exec-section-header'>Competitor Promotional Savings Radar</div>", unsafe_allow_html=True)
        comp_list = macro.get("competitor_benchmarks", [])
        if comp_list:
            comp_banks = [c.get("bank", "").split(" (")[0] for c in comp_list] + ["National Bonds (Sukuk)"]
            comp_rates = [c.get("rate_pct", 0.0) for c in comp_list] + [5.40]
            comp_colors = ["#8492A6", "#8492A6", "#8492A6", "#8492A6", "#0D9B5C"]
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
                margin=dict(l=16, r=25, t=16, b=16),
                xaxis=dict(title="Advertised Yield (% p.a.)", range=[0, 6.2], gridcolor="#F1F3F6", tickfont=dict(family="Inter, sans-serif", size=11)),
                yaxis=dict(tickfont=dict(family="Inter, sans-serif", size=11)),
                font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#8492A6")
            )
            st.plotly_chart(fig_comp_radar, use_container_width=True)

        for comp in macro.get("competitor_benchmarks", []):
            st.markdown(f'''
            <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-radius: var(--radius-sm); padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; font-size: 12px; color: var(--text-primary);">{comp.get('bank')}</div>
                    <div style="font-size: 11px; color: var(--text-tertiary);">{comp.get('product')} &bull; {comp.get('tenor', 'Direct Savings')}</div>
                </div>
                <span style="font-size: 13px; font-weight: 700; color: var(--brand-primary); font-variant-numeric: tabular-nums;">{comp.get('rate_pct'):.2f}% p.a.</span>
            </div>
            ''', unsafe_allow_html=True)

    # Section 4: Watch Items & Recommendations
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("<div class='exec-section-header'>Emerging Risks & Watch Items</div>", unsafe_allow_html=True)
        for w in rep["watch_items"]:
            st.markdown(f'''
            <div style="background: var(--status-warning-bg); border: 1px solid var(--status-warning-border); border-left: 3px solid var(--status-warning); border-radius: var(--radius-sm); padding: 10px 14px; margin-bottom: 8px; font-size: 12.5px; color: var(--status-warning);">
                <b>[Watch]</b> {w}
            </div>
            ''', unsafe_allow_html=True)

    with col_w2:
        st.markdown("<div class='exec-section-header'>Commercial Management Decisions</div>", unsafe_allow_html=True)
        for r in rep["management_recommendations"]:
            st.markdown(f'''
            <div style="background: var(--brand-subtle); border: 1px solid var(--border-primary); border-left: 3px solid var(--brand-primary); border-radius: var(--radius-sm); padding: 10px 14px; margin-bottom: 8px; font-size: 12.5px; color: var(--brand-text);">
                {r}
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)
    col_dl1, col_dl2 = st.columns([2, 1])
    with col_dl1:
        pdf_gen = ExecutivePDFGenerator()
        pdf_bytes = pdf_gen.generate_biweekly_report_pdf(selected_cycle)
        st.download_button(
            label=f"Download Executive PDF Report ({rep['report_ref']}.pdf)",
            data=pdf_bytes,
            file_name=f"{rep['report_ref']}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label=f"Download Raw Text Summary ({rep['report_ref']}.txt)",
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
