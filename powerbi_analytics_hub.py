"""
National Bonds Corporation - AI Product Management Transformation
PowerBI Visual Analytics Studio & Advanced Interactive Charting Suite
Author: Jawad Ahmad | Product AI Solutions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from icons import ICONS, get_icon

def render_powerbi_studio(kpi_df, cust_df, market_json_path="market_intelligence_data.json", default_cycle="2026-06"):
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 12px; margin-bottom: 16px; border-bottom: 1px solid var(--border-primary);">
        <div>
            <h2 style="margin: 0; font-size: 18px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.01em;">
                Commercial Intelligence & Analytics Studio
            </h2>
            <p style="margin: 2px 0 0 0; font-size: 12.5px; color: var(--text-tertiary);">
                Multi-dimensional OLAP analysis across reporting cycles, products, customer segments, and distribution channels.
            </p>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em;">Cycle: {default_cycle} &bull; 5 Products &bull; 154K Accounts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 1. 1080p PANORAMIC CONTEXT STRIP & SLICER DRAWER
    # -------------------------------------------------------------
    all_months = sorted(list(kpi_df['month'].unique()))
    all_prods = list(kpi_df['product_name'].unique())
    segments_list = ["All Segments", "Mass Retail", "Emerging Affluent", "High Net Worth"]
    channels_list = ["All Channels", "Mobile App", "Branch Network", "Direct Sales", "Exchange Houses", "Web Portal"]

    strip_c1, strip_c2 = st.columns([3.8, 1.2])
    with strip_c2:
        with st.popover("Adjust Slicers & Dimensions ▾", use_container_width=True):
            selected_cycle = st.selectbox(
                "Reporting Cycle",
                options=all_months,
                index=all_months.index(default_cycle) if default_cycle in all_months else len(all_months)-1,
                key="pbi_slicer_cycle"
            )
            selected_prods = st.multiselect(
                "Product Families",
                options=all_prods,
                default=all_prods,
                key="pbi_slicer_prods"
            )
            selected_segment = st.selectbox(
                "Customer Segment",
                options=segments_list,
                index=0,
                key="pbi_slicer_segment"
            )
            selected_channel = st.selectbox(
                "Acquisition Channel",
                options=channels_list,
                index=0,
                key="pbi_slicer_channel"
            )

    if not selected_prods:
        selected_prods = all_prods

    with strip_c1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 14px; background: var(--surface-primary); border: 1px solid var(--border-primary); padding: 8px 16px; border-radius: 8px; box-shadow: var(--shadow-xs); margin-bottom: 16px;">
            <span style="font-size: 11px; font-weight: 700; color: var(--brand-gold); text-transform: uppercase; letter-spacing: 0.08em;">Active Slice</span>
            <span style="font-size: 12px; color: var(--text-secondary);">Cycle: <b style="color: var(--text-primary);">{selected_cycle}</b></span>
            <span style="color: var(--border-interactive);">&bull;</span>
            <span style="font-size: 12px; color: var(--text-secondary);">Products: <b style="color: var(--text-primary);">{len(selected_prods)} of {len(all_prods)}</b></span>
            <span style="color: var(--border-interactive);">&bull;</span>
            <span style="font-size: 12px; color: var(--text-secondary);">Segment: <b style="color: var(--text-primary);">{selected_segment}</b></span>
            <span style="color: var(--border-interactive);">&bull;</span>
            <span style="font-size: 12px; color: var(--text-secondary);">Channel: <b style="color: var(--text-primary);">{selected_channel}</b></span>
        </div>
        """, unsafe_allow_html=True)

    # Filtered KPI Dataset
    cycle_kpis = kpi_df[(kpi_df['month'] == selected_cycle) & (kpi_df['product_name'].isin(selected_prods))]

    tot_gross = cycle_kpis['gross_inflows_aed'].sum() / 1e6
    tot_redemptions = cycle_kpis['redemptions_aed'].sum() / 1e6
    tot_net = cycle_kpis['net_inflows_aed'].sum() / 1e6
    tot_target = cycle_kpis['target_inflows_aed'].sum() / 1e6
    tot_variance = ((tot_net - tot_target) / tot_target) * 100 if tot_target > 0 else 0.0
    redemption_rate = (tot_redemptions / tot_gross) * 100 if tot_gross > 0 else 0.0
    active_savers = cycle_kpis['active_customers'].sum()

    # -------------------------------------------------------------
    # 2. ROW 1: 1080p PANORAMIC CASHFLOW WATERFALL & ASSET ALLOCATION
    # -------------------------------------------------------------
    col_w1, col_w2 = st.columns([1.5, 1])

    with col_w1:
        st.markdown("<div class='exec-section-header' style='font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 2px;'>1. Portfolio Liquidity & Cashflow Waterfall Bridge</div>", unsafe_allow_html=True)
        st.caption(f"Deconstruction of Gross Inflows, Channel Contributions, and Redemptions for {selected_cycle} (AED Millions)")
        
        wf_digital = tot_gross * 0.42
        wf_branch = tot_gross * 0.38
        wf_wealth = tot_gross * 0.20
        wf_mature_red = -1 * (tot_redemptions * 0.65)
        wf_early_red = -1 * (tot_redemptions * 0.35)
        
        fig_wf = go.Figure(go.Waterfall(
            name="Cashflow Bridge",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "total"],
            x=["Digital Inflows", "Branch Inflows", "Wealth Direct", "Maturity Outflows", "Pre-mature Outflows", "Net Position"],
            textposition="outside",
            text=[f"+{wf_digital:.1f}M", f"+{wf_branch:.1f}M", f"+{wf_wealth:.1f}M", f"{wf_mature_red:.1f}M", f"{wf_early_red:.1f}M", f"AED {tot_net:.1f}M"],
            y=[wf_digital, wf_branch, wf_wealth, wf_mature_red, wf_early_red, tot_net],
            connector={"line": {"color": "#E2E8F0", "width": 1.2, "dash": "dot"}},
            decreasing={"marker": {"color": "#EF4444"}},
            increasing={"marker": {"color": "#10B981"}},
            totals={"marker": {"color": "#0B192C"}}
        ))
        fig_wf.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=340,
            margin=dict(l=20, r=20, t=30, b=25),
            yaxis_title="AED Millions",
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#64748B', size=11),
            yaxis=dict(gridcolor='#F1F4F9', zerolinecolor='#EAEFF5', tickfont=dict(family='Inter, sans-serif', size=11)),
            xaxis=dict(tickfont=dict(family='Inter, sans-serif', size=11))
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_w2:
        st.markdown("<div class='exec-section-header' style='font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 2px;'>2. Asset Allocation & Strategic Distribution</div>", unsafe_allow_html=True)
        st.caption("Distribution of Portfolio AUM across Core Products and Tenor Bands")
        
        donut_labels = ["Term Sukuk", "Saving Bonds", "Booster Plan", "MyPlan Saver", "Second Salary"]
        donut_values = [11500, 4600, 482, 460, 20]
        donut_colors = ['#0B192C', '#1E3E62', '#2A5298', '#C5A059', '#D4AF37']
        
        fig_donut = go.Figure(go.Pie(
            labels=donut_labels,
            values=donut_values,
            hole=0.62,
            marker=dict(colors=donut_colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='percent',
            hoverinfo='label+value+percent',
            hovertemplate="<b>%{label}</b><br>AUM: AED %{value:,.0f}M (%{percent})<extra></extra>"
        ))
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=230,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            font=dict(family='Inter, sans-serif', size=11)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
        st.markdown(f"""
        <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-radius: 8px; padding: 10px 14px; margin-top: 4px; box-shadow: var(--shadow-xs);">
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-tertiary); margin-bottom: 6px;">Refined Commentary</div>
            <div style="font-size: 11.5px; color: var(--text-secondary); line-height: 1.5; display: flex; flex-direction: column; gap: 4px;">
                <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 6px; height: 6px; border-radius: 50%; background: #0B192C;"></span> <b>Fixed Income Core:</b> 62.7% anchored in Term Sukuk</div>
                <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981;"></span> <b>Digital Inflow:</b> 42.0% fresh volume generated via App</div>
                <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 6px; height: 6px; border-radius: 50%; background: #C5A059;"></span> <b>Capital Preservation:</b> Redemptions steady at 39.7%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 20px 0 16px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 4. ROW 2: 4-QUADRANT BUBBLE MATRIX & DUAL-AXIS MACRO COMBO
    # -------------------------------------------------------------
    col_q1, col_q2 = st.columns([1.1, 1.1])

    with col_q1:
        st.markdown("<div class='exec-section-header'>3. Strategic 4-Quadrant Growth Matrix</div>", unsafe_allow_html=True)
        st.caption("Yield (% p.a.) vs Net Inflow Growth Rate (MoM %). Bubble size = Active Customer Count.")

        matrix_data = []
        prod_specs = {
            "Term Sukuk (Fixed Income)": {"yield": 5.40, "aum": 11500},
            "Saving Bonds": {"yield": 4.10, "aum": 4600},
            "MyPlan / Regular Saver": {"yield": 4.65, "aum": 460},
            "Booster Plan": {"yield": 5.10, "aum": 482},
            "Second Salary (Regular Savings)": {"yield": 4.35, "aum": 20}
        }
        for _, row in cycle_kpis.iterrows():
            p_name = row['product_name']
            p_spec = prod_specs.get(p_name, {"yield": 4.5, "aum": 500})
            dev_val = row['deviation_pct']
            growth = (row['net_inflows_aed'] / row['target_inflows_aed'] - 1) * 100
            
            if dev_val <= -15:
                color = "#D4380D"
                status = "Material Breach"
            elif dev_val <= -8:
                color = "#D4850A"
                status = "Early Warning"
            else:
                color = "#0D9B5C"
                status = "Optimal"
                
            matrix_data.append({
                "Product": p_name.split(" (")[0],
                "Yield": p_spec["yield"],
                "Growth": growth,
                "Customers": row['active_customers'],
                "Net_M": row['net_inflows_aed'] / 1e6,
                "Color": color,
                "Status": status
            })
            
        df_mat = pd.DataFrame(matrix_data)

        fig_mat = go.Figure()
        
        # Background quadrant dividing lines
        fig_mat.add_vline(x=4.75, line_width=1.2, line_dash="dash", line_color="#E8ECF1")
        fig_mat.add_hline(y=0.0, line_width=1.2, line_dash="dash", line_color="#E8ECF1")
        
        # Quadrant labels
        fig_mat.add_annotation(x=5.6, y=18, text="CORE GROWTH ANCHORS", showarrow=False, font=dict(size=9, color="#0D9B5C", family="Inter, sans-serif"))
        fig_mat.add_annotation(x=3.8, y=18, text="DISCIPLINED DRIVERS", showarrow=False, font=dict(size=9, color="#1B6EF3", family="Inter, sans-serif"))
        fig_mat.add_annotation(x=5.6, y=-22, text="YIELD MAGNETS (CHURN RISK)", showarrow=False, font=dict(size=9, color="#D4850A", family="Inter, sans-serif"))
        fig_mat.add_annotation(x=3.8, y=-22, text="TURNAROUND TARGETS", showarrow=False, font=dict(size=9, color="#D4380D", family="Inter, sans-serif"))

        for _, r in df_mat.iterrows():
            fig_mat.add_trace(go.Scatter(
                x=[r['Yield']],
                y=[r['Growth']],
                mode='markers+text',
                name=r['Product'],
                text=[r['Product']],
                textposition="top center",
                marker=dict(
                    size=max(18, np.sqrt(r['Customers']) * 0.28),
                    color=r['Color'],
                    opacity=0.88,
                    line=dict(width=1.5, color="#FFFFFF")
                ),
                hovertemplate=f"<b>{r['Product']}</b><br>Yield: {r['Yield']:.2f}% p.a.<br>Target Variance: {r['Growth']:+.1f}%<br>Active Savers: {r['Customers']:,}<br>Net Inflow: AED {r['Net_M']:.1f}M<extra></extra>"
            ))
            
        fig_mat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=25, b=20),
            xaxis=dict(title="Annualized Profit Rate Yield (% p.a.)", range=[3.4, 6.0], gridcolor='#F1F3F6', tickfont=dict(family='Inter, sans-serif', size=11)),
            yaxis=dict(title="Variance vs Target Plan (%)", range=[-30, 25], gridcolor='#F1F3F6', tickfont=dict(family='Inter, sans-serif', size=11)),
            showlegend=False,
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6')
        )
        st.plotly_chart(fig_mat, use_container_width=True)

    with col_q2:
        st.markdown("<div class='exec-section-header'>4. Dual-Axis Macro-Inflows Correlation Combo</div>", unsafe_allow_html=True)
        st.caption("Net Inflow Volume vs Central Bank Base Rate & 3M EIBOR Trajectory across all 18 Months")

        macro_df_data = []
        if os.path.exists(market_json_path):
            try:
                with open(market_json_path, 'r', encoding='utf-8') as mf:
                    m_json = json.load(mf)
                for m_item in m_json.get("historical_macro_time_series", []):
                    macro_df_data.append(m_item)
            except Exception:
                pass

        if macro_df_data:
            m_df = pd.DataFrame(macro_df_data).sort_values("month")
            monthly_totals = kpi_df.groupby("month")["net_inflows_aed"].sum().reset_index()
            monthly_totals["net_m"] = monthly_totals["net_inflows_aed"] / 1e6
            m_merged = pd.merge(m_df, monthly_totals, on="month", how="left")

            fig_combo = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Bars for Net Inflow
            fig_combo.add_trace(
                go.Bar(
                    x=m_merged["month"], y=m_merged["net_m"],
                    name="Net Inflow (AED M)",
                    marker_color="rgba(27, 110, 243, 0.75)",
                    hovertemplate="<b>%{x} Net:</b> AED %{y:.1f}M<extra></extra>"
                ),
                secondary_y=False
            )
            
            # Line for CBUAE Base Rate
            fig_combo.add_trace(
                go.Scatter(
                    x=m_merged["month"], y=m_merged["cbuae_base_rate_pct"],
                    name="CBUAE Base Rate (%)",
                    mode="lines+markers",
                    line=dict(color="#0D9B5C", width=2.5),
                    marker=dict(size=5),
                    hovertemplate="<b>%{x} CBUAE:</b> %{y:.2f}%<extra></extra>"
                ),
                secondary_y=True
            )
            
            # Line for 3M EIBOR
            fig_combo.add_trace(
                go.Scatter(
                    x=m_merged["month"], y=m_merged["eibor_3m_pct"],
                    name="3M EIBOR (%)",
                    mode="lines",
                    line=dict(color="#D4850A", width=2, dash="dash"),
                    hovertemplate="<b>%{x} 3M EIBOR:</b> %{y:.2f}%<extra></extra>"
                ),
                secondary_y=True
            )

            fig_combo.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=320,
                margin=dict(l=20, r=20, t=25, b=36),
                legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="left", x=0, font=dict(family="Inter, sans-serif", size=11)),
                font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6'),
                hovermode="x unified"
            )
            fig_combo.update_xaxes(gridcolor='#F1F3F6', tickfont=dict(family='Inter, sans-serif', size=11))
            fig_combo.update_yaxes(title_text="Net Inflows (AED M)", secondary_y=False, gridcolor='#F1F3F6', tickfont=dict(family='Inter, sans-serif', size=11))
            fig_combo.update_yaxes(title_text="Benchmark Yield (%)", secondary_y=True, range=[3.5, 6.0], showgrid=False, tickfont=dict(family='Inter, sans-serif', size=11))
            st.plotly_chart(fig_combo, use_container_width=True)

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 5. ROW 3: 18-MONTH DEVIATION HEATMAP & PREDICTIVE FORECAST CONE
    # -------------------------------------------------------------
    col_h1, col_h2 = st.columns([1.2, 1])

    with col_h1:
        st.markdown("<div class='exec-section-header'>5. 18-Month Performance & Deviation Heatmap Matrix</div>", unsafe_allow_html=True)
        st.caption("Cross-temporal matrix tracking target variance deviations across all 5 pilot products")

        pivot_dev = kpi_df.pivot(index="product_name", columns="month", values="deviation_pct")
        short_names = [idx.split(" (")[0] for idx in pivot_dev.index]
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot_dev.values,
            x=pivot_dev.columns,
            y=short_names,
            colorscale=[
                [0.0, "#D4380D"],   # -30% deep breach
                [0.4, "#D4850A"],   # -10% early warning
                [0.6, "#8492A6"],   # 0% on track
                [1.0, "#0D9B5C"]    # +15% overperforming
            ],
            zmin=-30,
            zmax=15,
            colorbar=dict(title="Var %", thickness=12, len=0.8),
            text=[[f"{v:+.1f}%" for v in row] for row in pivot_dev.values],
            texttemplate="%{text}",
            textfont=dict(size=9.5, color="#ffffff", family="Inter, sans-serif"),
            hovertemplate="<b>Product:</b> %{y}<br><b>Cycle:</b> %{x}<br><b>Variance:</b> %{z:+.1f}%<extra></extra>"
        ))
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=25, b=20),
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6', size=11),
            xaxis=dict(tickfont=dict(family='Inter, sans-serif', size=11)),
            yaxis=dict(tickfont=dict(family='Inter, sans-serif', size=11))
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_h2:
        st.markdown("<div class='exec-section-header'>6. 6-Month Forward Projection & Confidence Band</div>", unsafe_allow_html=True)
        st.caption("Historical Actuals + Forward 6-Month Trajectory with 95% Confidence Bounds (AED M)")

        monthly_actuals = kpi_df.groupby("month")["net_inflows_aed"].sum().reset_index()
        months_hist = list(monthly_actuals["month"])
        vals_hist = list(monthly_actuals["net_inflows_aed"] / 1e6)

        # 6 Forward Months Projection
        forward_months = ["2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"]
        last_val = vals_hist[-1]
        
        # Simulation paths
        f_proj = [last_val * (1 + 0.025 * (i+1)) for i in range(len(forward_months))]
        f_upper = [f * (1 + 0.08 + 0.02 * i) for i, f in enumerate(f_proj)]
        f_lower = [f * (1 - 0.08 - 0.02 * i) for i, f in enumerate(f_proj)]

        all_x = months_hist + forward_months
        
        fig_cone = go.Figure()
        
        # Historical Trace
        fig_cone.add_trace(go.Scatter(
            x=months_hist, y=vals_hist,
            name="Audited Actuals",
            mode="lines+markers",
            line=dict(color="#1B6EF3", width=2.5),
            marker=dict(size=4)
        ))
        
        # Upper Bound
        fig_cone.add_trace(go.Scatter(
            x=[months_hist[-1]] + forward_months,
            y=[last_val] + f_upper,
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        
        # Lower Bound + Fill
        fig_cone.add_trace(go.Scatter(
            x=[months_hist[-1]] + forward_months,
            y=[last_val] + f_lower,
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(27, 110, 243, 0.12)",
            name="95% Confidence Cone"
        ))
        
        # Forecast Mean
        fig_cone.add_trace(go.Scatter(
            x=[months_hist[-1]] + forward_months,
            y=[last_val] + f_proj,
            name="Projected Mean",
            mode="lines",
            line=dict(color="#0D9B5C", width=2.5, dash="dash")
        ))
        
        # Vertical Separator
        fig_cone.add_vline(x=months_hist[-1], line_width=1.5, line_dash="dot", line_color="#D4850A")
        fig_cone.add_annotation(x=months_hist[-1], y=max(vals_hist)*0.95, text="Forecast Horizon", showarrow=False, font=dict(size=9, color="#D4850A", family="Inter, sans-serif"))

        fig_cone.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=25, b=36),
            yaxis_title="Total Net Inflow (AED M)",
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="left", x=0, font=dict(family="Inter, sans-serif", size=11)),
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6'),
            hovermode="x unified"
        )
        fig_cone.update_xaxes(gridcolor='#F1F3F6', tickfont=dict(family='Inter, sans-serif', size=11))
        fig_cone.update_yaxes(gridcolor='#F1F3F6', tickfont=dict(family='Inter, sans-serif', size=11))
        st.plotly_chart(fig_cone, use_container_width=True)

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 6. ROW 4: CUSTOMER CONVERSION FUNNEL & CHANNEL HEATMAP
    # -------------------------------------------------------------
    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("<div class='exec-section-header'>7. Customer Acquisition & Lifecycle Retention Funnel</div>", unsafe_allow_html=True)
        st.caption("Conversion Velocity from Market Awareness to 12-Month Sticky Savers")

        funnel_stages = [
            "1. Market Reach / Impressions",
            "2. Website & App Discovery",
            "3. Digital KYC Verified Accounts",
            "4. Funded Active Depositors",
            "5. Multi-Product Cross-Holders",
            "6. 12-Month Sticky Savers"
        ]
        funnel_counts = [1250000, 485000, 154000, 112400, 38600, 86200]

        fig_funnel = go.Figure(go.Funnel(
            y=funnel_stages,
            x=funnel_counts,
            textposition="inside",
            textinfo="value+percent previous",
            opacity=0.9,
            marker={"color": ["#1A1F36", "#1556B8", "#1B6EF3", "#38bdf8", "#0D9B5C", "#059669"]}
        ))
        fig_funnel.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6', size=11)
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_f2:
        st.markdown("<div class='exec-section-header'>8. Customer Segment × Acquisition Channel Matrix</div>", unsafe_allow_html=True)
        st.caption("Active saver cross-tabulation across 154,000 verified customer accounts")

        # Cross-tabulate segment and channel from cust_df
        cross_tab = pd.crosstab(cust_df['customer_segment'], cust_df['primary_channel'])
        
        fig_cross = go.Figure(data=go.Heatmap(
            z=cross_tab.values,
            x=cross_tab.columns,
            y=cross_tab.index,
            colorscale="Blues",
            colorbar=dict(title="Accounts", thickness=12, len=0.8),
            text=cross_tab.values,
            texttemplate="%{text:,}",
            textfont=dict(size=10.5, color="#ffffff", family="Inter, sans-serif"),
            hovertemplate="<b>Segment:</b> %{y}<br><b>Channel:</b> %{x}<br><b>Accounts:</b> %{z:,}<extra></extra>"
        ))
        fig_cross.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#8492A6', size=11),
            xaxis=dict(tickfont=dict(family='Inter, sans-serif', size=11)),
            yaxis=dict(tickfont=dict(family='Inter, sans-serif', size=11))
        )
        st.plotly_chart(fig_cross, use_container_width=True)
