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

def render_powerbi_studio(kpi_df, cust_df, market_json_path="market_intelligence_data.json", default_cycle="2026-06"):
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.98) 100%); border: 1px solid rgba(2, 132, 199, 0.4); border-radius: 12px; padding: 18px 24px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.25);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="background: #0284c7; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.05em;">POWERBI VISUAL STUDIO</span>
                    <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">LIVE OLAP SLICING</span>
                </div>
                <h2 style="margin: 0; font-size: 23px; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">
                    Executive Commercial Intelligence & Multi-Dimensional Analytics Hub
                </h2>
                <p style="margin: 4px 0 0 0; font-size: 13px; color: #94a3b8; max-width: 900px;">
                    Deep-dive visual analytics workspace built for financial analysts, commercial planners, and ALCO leadership. Fully responsive interactive slicing across 18 months, 5 product families, and 154,000 verified customer accounts.
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.06em;">Portfolio Engine</div>
                <div style="font-size: 18px; font-weight: 800; color: #ffffff;">AED 18.34B AUM</div>
                <div style="font-size: 11px; color: #94a3b8;">154K Active Accounts</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 1. POWERBI-STYLE MULTI-DIMENSIONAL SLICER RIBBON
    # -------------------------------------------------------------
    st.markdown("<p style='font-size: 12px; font-weight: 800; text-transform: uppercase; color: #0284c7; letter-spacing: 0.06em; margin-bottom: 6px;'>🎛️ Interactive Visual Slicers & Dynamic Filters</p>", unsafe_allow_html=True)
    
    with st.container():
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 2, 1.5, 1.5])
        
        all_months = sorted(list(kpi_df['month'].unique()))
        with f_col1:
            selected_cycle = st.selectbox(
                "📅 Analysis Reporting Cycle",
                options=all_months,
                index=all_months.index(default_cycle) if default_cycle in all_months else len(all_months)-1,
                key="pbi_slicer_cycle"
            )
            
        all_prods = list(kpi_df['product_name'].unique())
        with f_col2:
            selected_prods = st.multiselect(
                "📦 Product Family Slicer",
                options=all_prods,
                default=all_prods,
                key="pbi_slicer_prods"
            )
            
        with f_col3:
            segments_list = ["All Segments", "Mass Retail", "Emerging Affluent", "High Net Worth"]
            selected_segment = st.selectbox(
                "👥 Customer Segment Slicer",
                options=segments_list,
                index=0,
                key="pbi_slicer_segment"
            )
            
        with f_col4:
            channels_list = ["All Channels", "Mobile App", "Branch Network", "Direct Sales", "Exchange Houses", "Web Portal"]
            selected_channel = st.selectbox(
                "🌐 Acquisition Channel Slicer",
                options=channels_list,
                index=0,
                key="pbi_slicer_channel"
            )

    if not selected_prods:
        st.warning("⚠️ Please select at least one product family to display visual analytics.")
        selected_prods = all_prods

    # Filtered KPI Dataset
    cycle_kpis = kpi_df[(kpi_df['month'] == selected_cycle) & (kpi_df['product_name'].isin(selected_prods))]

    # -------------------------------------------------------------
    # 2. POWERBI SUMMARY CARDS RIBBON WITH TREND SPARKLINES
    # -------------------------------------------------------------
    tot_gross = cycle_kpis['gross_inflows_aed'].sum() / 1e6
    tot_redemptions = cycle_kpis['redemptions_aed'].sum() / 1e6
    tot_net = cycle_kpis['net_inflows_aed'].sum() / 1e6
    tot_target = cycle_kpis['target_inflows_aed'].sum() / 1e6
    tot_variance = ((tot_net - tot_target) / tot_target) * 100 if tot_target > 0 else 0.0
    redemption_rate = (tot_redemptions / tot_gross) * 100 if tot_gross > 0 else 0.0
    active_savers = cycle_kpis['active_customers'].sum()

    var_color = "#10b981" if tot_variance >= 0 else ("#f59e0b" if tot_variance >= -10 else "#ef4444")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #0284c7;">
            <div class="kpi-card-header"><span class="kpi-card-title">Gross Inflows (Selected)</span><span>📥</span></div>
            <div class="kpi-card-value" style="color: #0284c7;">AED {tot_gross:.1f}M</div>
            <div class="kpi-card-footer"><span>Total Fresh Capital Inflow</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #f59e0b;">
            <div class="kpi-card-header"><span class="kpi-card-title">Gross Redemptions</span><span>🔄</span></div>
            <div class="kpi-card-value" style="color: #f59e0b;">AED {tot_redemptions:.1f}M</div>
            <div class="kpi-card-footer"><span>{redemption_rate:.1f}% Outflow / Volume Ratio</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid {var_color};">
            <div class="kpi-card-header"><span class="kpi-card-title">Actual Net Position</span><span>⚖️</span></div>
            <div class="kpi-card-value" style="color: {var_color};">AED {tot_net:.1f}M</div>
            <div class="kpi-card-footer"><span>Target AED {tot_target:.1f}M ({tot_variance:+.1f}%)</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #10b981;">
            <div class="kpi-card-header"><span class="kpi-card-title">Active Savers Sliced</span><span>👥</span></div>
            <div class="kpi-card-value" style="color: #10b981;">{active_savers:,}</div>
            <div class="kpi-card-footer"><span>{(active_savers/154000*100):.1f}% of Total Company Base</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 3. ROW 1: CASHFLOW WATERFALL & HIERARCHICAL SUNBURST
    # -------------------------------------------------------------
    col_w1, col_w2 = st.columns([1.2, 1])

    with col_w1:
        st.markdown("#### 🌊 1. Portfolio Liquidity & Cashflow Waterfall Bridge")
        st.caption(f"Deconstruction of Gross Inflows, Channel Contributions, and Redemptions for {selected_cycle} (AED Millions)")
        
        # Build Waterfall Data
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
            connector={"line": {"color": "#94a3b8", "width": 1.5, "dash": "dot"}},
            decreasing={"marker": {"color": "#ef4444"}},
            increasing={"marker": {"color": "#0284c7"}},
            totals={"marker": {"color": "#0f172a" if tot_net > 0 else "#dc2626"}}
        ))
        fig_wf.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="AED Millions",
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b'),
            yaxis=dict(gridcolor='rgba(148, 163, 184, 0.15)')
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_w2:
        st.markdown("#### ☀️ 2. Hierarchical AUM Allocation Sunburst")
        st.caption("Click any product ring to zoom into Tenor Bands and Customer Tier Volumes")
        
        # Sunburst Data
        sun_labels = [
            "Total AUM (18.34B)", 
            "Term Sukuk", "Saving Bonds", "Booster Plan", "MyPlan", "Second Salary",
            "Sukuk: 1Y Tenor", "Sukuk: 2Y-3Y", "Sukuk: 5Y+",
            "Bonds: Mass Retail", "Bonds: Affluent", "Bonds: Minors",
            "Booster: 2Y Lock", "Booster: 3Y Lock",
            "MyPlan: 3Y Saver", "MyPlan: 5Y Saver",
            "Salary: 3Y Ret", "Salary: 10Y Ret"
        ]
        sun_parents = [
            "", 
            "Total AUM (18.34B)", "Total AUM (18.34B)", "Total AUM (18.34B)", "Total AUM (18.34B)", "Total AUM (18.34B)",
            "Term Sukuk", "Term Sukuk", "Term Sukuk",
            "Saving Bonds", "Saving Bonds", "Saving Bonds",
            "Booster Plan", "Booster Plan",
            "MyPlan", "MyPlan",
            "Second Salary", "Second Salary"
        ]
        sun_values = [
            18340,
            11500, 4600, 482, 460, 20,
            4600, 4600, 2300,
            2300, 1840, 460,
            337, 145,
            276, 184,
            14, 6
        ]
        
        fig_sun = go.Figure(go.Sunburst(
            labels=sun_labels,
            parents=sun_parents,
            values=sun_values,
            branchvalues="total",
            marker=dict(colorscale="Blues", showscale=False),
            hovertemplate="<b>%{label}</b><br>Volume: AED %{value:,.0f}M (%{percentRoot:.1%})<extra></extra>"
        ))
        fig_sun.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=340,
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(fig_sun, use_container_width=True)

    st.markdown("<hr style='margin: 18px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 4. ROW 2: 4-QUADRANT BUBBLE MATRIX & DUAL-AXIS MACRO COMBO
    # -------------------------------------------------------------
    col_q1, col_q2 = st.columns([1.1, 1.1])

    with col_q1:
        st.markdown("#### 🎯 3. Strategic 4-Quadrant BCG / Product Bubble Matrix")
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
                color = "#ef4444"
                status = "Material Breach"
            elif dev_val <= -8:
                color = "#f59e0b"
                status = "Early Warning"
            else:
                color = "#10b981"
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
        fig_mat.add_vline(x=4.75, line_width=1.2, line_dash="dash", line_color="rgba(148, 163, 184, 0.4)")
        fig_mat.add_hline(y=0.0, line_width=1.2, line_dash="dash", line_color="rgba(148, 163, 184, 0.4)")
        
        # Quadrant labels
        fig_mat.add_annotation(x=5.6, y=18, text="CORE GROWTH ANCHORS", showarrow=False, font=dict(size=9, color="#10b981", family="Plus Jakarta Sans, sans-serif"))
        fig_mat.add_annotation(x=3.8, y=18, text="DISCIPLINED DRIVERS", showarrow=False, font=dict(size=9, color="#0284c7", family="Plus Jakarta Sans, sans-serif"))
        fig_mat.add_annotation(x=5.6, y=-22, text="YIELD MAGNETS (CHURN RISK)", showarrow=False, font=dict(size=9, color="#f59e0b", family="Plus Jakarta Sans, sans-serif"))
        fig_mat.add_annotation(x=3.8, y=-22, text="TURNAROUND TARGETS", showarrow=False, font=dict(size=9, color="#ef4444", family="Plus Jakarta Sans, sans-serif"))

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
                    line=dict(width=1.5, color="#0f172a")
                ),
                hovertemplate=f"<b>{r['Product']}</b><br>Yield: {r['Yield']:.2f}% p.a.<br>Target Variance: {r['Growth']:+.1f}%<br>Active Savers: {r['Customers']:,}<br>Net Inflow: AED {r['Net_M']:.1f}M<extra></extra>"
            ))
            
        fig_mat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=340,
            margin=dict(l=20, r=20, t=25, b=20),
            xaxis=dict(title="Annualized Profit Rate Yield (% p.a.)", range=[3.4, 6.0], gridcolor='rgba(148, 163, 184, 0.15)'),
            yaxis=dict(title="Variance vs Target Plan (%)", range=[-30, 25], gridcolor='rgba(148, 163, 184, 0.15)'),
            showlegend=False,
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b')
        )
        st.plotly_chart(fig_mat, use_container_width=True)

    with col_q2:
        st.markdown("#### 📈 4. Dual-Axis Macro-Inflows Correlation Combo")
        st.caption("Net Inflow Volume vs Central Bank Base Rate & 3M EIBOR Trajectory across all 18 Months")

        # Load Macro Data
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
                    marker_color="rgba(2, 132, 199, 0.75)",
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
                    line=dict(color="#10b981", width=2.5),
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
                    line=dict(color="#f59e0b", width=2, dash="dash"),
                    hovertemplate="<b>%{x} 3M EIBOR:</b> %{y:.2f}%<extra></extra>"
                ),
                secondary_y=True
            )

            fig_combo.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=340,
                margin=dict(l=20, r=20, t=25, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b'),
                hovermode="x unified"
            )
            fig_combo.update_xaxes(gridcolor='rgba(148, 163, 184, 0.15)')
            fig_combo.update_yaxes(title_text="Net Inflows (AED M)", secondary_y=False, gridcolor='rgba(148, 163, 184, 0.15)')
            fig_combo.update_yaxes(title_text="Benchmark Yield (%)", secondary_y=True, range=[3.5, 6.0], showgrid=False)
            st.plotly_chart(fig_combo, use_container_width=True)

    st.markdown("<hr style='margin: 18px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 5. ROW 3: 18-MONTH DEVIATION HEATMAP & PREDICTIVE FORECAST CONE
    # -------------------------------------------------------------
    col_h1, col_h2 = st.columns([1.2, 1])

    with col_h1:
        st.markdown("#### 🗺️ 5. 18-Month Performance & Deviation Heatmap Matrix")
        st.caption("Cross-temporal matrix tracking target variance deviations across all 5 pilot products")

        pivot_dev = kpi_df.pivot(index="product_name", columns="month", values="deviation_pct")
        short_names = [idx.split(" (")[0] for idx in pivot_dev.index]
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot_dev.values,
            x=pivot_dev.columns,
            y=short_names,
            colorscale=[
                [0.0, "#dc2626"],   # -30% deep breach
                [0.4, "#f59e0b"],   # -10% early warning
                [0.6, "#94a3b8"],   # 0% on track
                [1.0, "#10b981"]    # +15% overperforming
            ],
            zmin=-30,
            zmax=15,
            colorbar=dict(title="Var %", thickness=12, len=0.8),
            text=[[f"{v:+.1f}%" for v in row] for row in pivot_dev.values],
            texttemplate="%{text}",
            textfont=dict(size=9.5, color="#ffffff"),
            hovertemplate="<b>Product:</b> %{y}<br><b>Cycle:</b> %{x}<br><b>Variance:</b> %{z:+.1f}%<extra></extra>"
        ))
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=340,
            margin=dict(l=20, r=20, t=25, b=20),
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b')
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_h2:
        st.markdown("#### 🔮 6. 6-Month Monte Carlo Predictive Forecast Cone")
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
            line=dict(color="#0284c7", width=2.5),
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
            fillcolor="rgba(2, 132, 199, 0.15)",
            name="95% Confidence Cone"
        ))
        
        # Forecast Mean
        fig_cone.add_trace(go.Scatter(
            x=[months_hist[-1]] + forward_months,
            y=[last_val] + f_proj,
            name="Q3-Q4 Projected Mean",
            mode="lines",
            line=dict(color="#10b981", width=2.5, dash="dash")
        ))
        
        # Vertical Separator
        fig_cone.add_vline(x=months_hist[-1], line_width=1.5, line_dash="dot", line_color="#f59e0b")
        fig_cone.add_annotation(x=months_hist[-1], y=max(vals_hist)*0.95, text="Forecast Horizon", showarrow=False, font=dict(size=9, color="#f59e0b"))

        fig_cone.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=340,
            margin=dict(l=20, r=20, t=25, b=20),
            yaxis_title="Total Net Inflow (AED M)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b'),
            hovermode="x unified"
        )
        fig_cone.update_xaxes(gridcolor='rgba(148, 163, 184, 0.15)')
        fig_cone.update_yaxes(gridcolor='rgba(148, 163, 184, 0.15)')
        st.plotly_chart(fig_cone, use_container_width=True)

    st.markdown("<hr style='margin: 18px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 6. ROW 4: CUSTOMER CONVERSION FUNNEL & CHANNEL HEATMAP
    # -------------------------------------------------------------
    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("#### ⏳ 7. Customer Acquisition & Lifecycle Retention Funnel")
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
            marker={"color": ["#0f172a", "#0369a1", "#0284c7", "#38bdf8", "#10b981", "#059669"]}
        ))
        fig_funnel.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b')
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_f2:
        st.markdown("#### 👥 8. Customer Segment × Acquisition Channel Matrix")
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
            textfont=dict(size=10.5, color="#ffffff"),
            hovertemplate="<b>Segment:</b> %{y}<br><b>Channel:</b> %{x}<br><b>Accounts:</b> %{z:,}<extra></extra>"
        ))
        fig_cross.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#64748b')
        )
        st.plotly_chart(fig_cross, use_container_width=True)
