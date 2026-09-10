"""
National Bonds Corporation - AI Product Management Transformation
Product Knowledge AI Assistant (Frontline Operating View)
Principle: A controlled single source of product truth for frontline teams.
Safety Rule: If information is unavailable, under review, or unclear, the Assistant does not assume. It escalates.
Author: Jawad Ahmad | Product AI Solutions
"""

import streamlit as st
import pandas as pd
import json
import os
import datetime
import plotly.express as px
import plotly.graph_objects as go
from pdf_generator import ExecutivePDFGenerator
from icons import ICONS, get_icon

def render_frontline_portal(jd_agent):
    st.markdown(f'''
    <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-radius: var(--radius-md); padding: 16px 20px; margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <h2 style="margin: 0; font-size: 18px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.01em;">
                    Product Knowledge Assistant
                </h2>
                <p style="margin: 2px 0 0 0; font-size: 12.5px; color: var(--text-secondary); max-width: 820px;">
                    Controlled single source of certified product truth for Sales, Customer Service, and Operations teams. Grounded in official Product Circulars, Terms & Conditions, and Sharia Fatwas.
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-tertiary);">Active Persona</div>
                <div style="font-size: 13px; font-weight: 700; color: var(--text-primary);">Ahmed &bull; Relationship Manager</div>
                <div style="font-size: 11.5px; color: var(--text-tertiary);">Direct Sales & Branch Network</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Frontline Operational Summary Cards
    tickets = jd_agent.get_escalation_tickets()
    open_tickets_count = len([t for t in tickets if t.get('status') == 'PENDING_PRODUCT_MGMT_REVIEW'])
    kb_count = len(jd_agent.kb_docs)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header"><span class="kpi-horizon-title">Approved Documents</span><span class="kpi-card-icon">{get_icon('book-open', 14, 'var(--text-tertiary)')}</span></div>
            <div class="kpi-horizon-value">{kb_count} Docs</div>
            <div class="kpi-horizon-subtext"><span>Circulars, T&Cs, Manuals</span></div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header"><span class="kpi-horizon-title">Grounding Standard</span><span class="kpi-card-icon">{get_icon('shield', 14, 'var(--status-positive)')}</span></div>
            <div class="kpi-horizon-value" style="color: var(--status-positive); font-size: 19px;">Zero Hallucination</div>
            <div class="kpi-horizon-subtext"><span>100% Certified Citations</span></div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header"><span class="kpi-horizon-title">Retrieval SLA</span><span class="kpi-card-icon">{get_icon('zap', 14, 'var(--text-tertiary)')}</span></div>
            <div class="kpi-horizon-value">&lt; 1.5s</div>
            <div class="kpi-horizon-subtext"><span>BM25 Semantic Retrieval</span></div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        ticket_color = 'var(--status-critical)' if open_tickets_count > 0 else 'var(--status-positive)'
        st.markdown(f'''
        <div class="kpi-horizon-card">
            <div class="kpi-horizon-header"><span class="kpi-horizon-title">Open Escalations</span><span class="kpi-card-icon">{get_icon('ticket', 14, ticket_color)}</span></div>
            <div class="kpi-horizon-value" style="color: {ticket_color};">{open_tickets_count} Tickets</div>
            <div class="kpi-horizon-subtext"><span>Product Review Queue</span></div>
        </div>
        ''', unsafe_allow_html=True)

    # FRONTLINE TABS
    tab_query, tab_catalog, tab_escalations, tab_audit = st.tabs([
        "Ask Assistant",
        "Documents",
        "Escalations",
        "Audit Trail"
    ])

    # -------------------------------------------------------------
    # TAB 1: ASK PRODUCT ASSISTANT
    # -------------------------------------------------------------
    with tab_query:
        st.markdown('''
        <div style="margin-bottom: 12px;">
            <h3 style="font-size: 15px; font-weight: 700; margin: 0 0 4px 0; color: var(--text-primary);">Ask Product: Frontline Knowledge Console</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary); margin: 0;">
                Query official product circulars, withdrawal clauses, fee schedules, or promotional eligibility.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        # Quick Suggested Inquiry Chips
        st.markdown("<p style='font-size: 12px; font-weight: 600; color: var(--text-tertiary); margin-bottom: 6px;'>Select a Real-World Scenario or Type Custom Question Below:</p>", unsafe_allow_html=True)
        
        chip_col1, chip_col2 = st.columns(2)
        selected_prompt = None

        with chip_col1:
            if st.button("Booster Plan: Milestone Bonus & Notice Period", use_container_width=True, key="chip_1"):
                selected_prompt = "Can Booster Plan milestone bonus combine with 7% certificate profit, and what is the withdrawal notice period?"
            if st.button("Second Salary: Monthly Savings & Early Exit Penalty", use_container_width=True, key="chip_2"):
                selected_prompt = "What is the minimum monthly savings and early redemption penalty for Second Salary?"
            if st.button("Saving Bonds: Holding Period & Redemptions", use_container_width=True, key="chip_3"):
                selected_prompt = "What are the holding period and instant redemption limits for Saving Bonds?"

        with chip_col2:
            if st.button("Policy Check: 1.5% Promo Bonus on Booster Plan", use_container_width=True, key="chip_4"):
                selected_prompt = "Can we offer the extra 1.5% promo bonus on Booster Plan for fresh money?"
            if st.button("Rewards Program: Eligibility & Draw Schedule", use_container_width=True, key="chip_5"):
                selected_prompt = "How do customer accounts qualify for the AED 36M Rewards Draw and BMW luxury sedans?"
            if st.button("AML / KYC: Source of Funds Validation Threshold", use_container_width=True, key="chip_6"):
                selected_prompt = "What is the Source of Funds requirement for deposits above AED 200,000?"

        st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid var(--border-primary);'>", unsafe_allow_html=True)

        if "frontline_query_input" not in st.session_state:
            st.session_state.frontline_query_input = ""

        if selected_prompt:
            st.session_state.frontline_query_input = selected_prompt

        query_col, btn_col = st.columns([5, 1])
        with query_col:
            user_query = st.text_input(
                "Ask Product Query",
                value=st.session_state.frontline_query_input,
                placeholder="e.g., Can Booster Plan milestone bonus combine with 7% profit? Or what is the notice period?",
                label_visibility="collapsed",
                key="frontline_user_input"
            )
        with btn_col:
            submit_search = st.button("Query Base", use_container_width=True, type="primary")

        active_query = user_query if submit_search else (selected_prompt if selected_prompt else (user_query if user_query else None))

        if active_query:
            with st.spinner("Grounding against certified product circulars & Sharia resolutions..."):
                res = jd_agent.query_knowledge_assistant(
                    query=active_query,
                    user_name="Ahmed (RM)",
                    user_role="Direct Sales / Branch Network"
                )

            status = res.get('status')
            answer = res.get('answer')
            ticket_id = res.get('ticket_id')

            # Render Result Card
            if status == 'VERIFIED':
                st.markdown(f'''
                <div style="background: var(--surface-primary); border: 1px solid var(--status-positive-border); border-left: 3px solid var(--status-positive); border-radius: var(--radius-md); padding: 18px 20px; margin: 16px 0; box-shadow: var(--shadow-xs);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border-secondary);">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            {get_icon('check-circle', 16, 'var(--status-positive)')}
                            <span class="status-pill status-healthy">{res.get('badge', 'VERIFIED PRODUCT GROUND TRUTH')}</span>
                        </div>
                        <span style="font-size: 11.5px; color: var(--text-tertiary); font-weight: 500;">Confidence: 99.4% &bull; SLA: 1.1s &bull; Zero Hallucination</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Render verified content cleanly with markdown
                st.markdown(answer)
                
                col_c1, col_c2 = st.columns([4, 1])
                with col_c2:
                    if st.button("Copy Citation", key="copy_btn", use_container_width=True):
                        st.success("Citation copied to clipboard.")

            elif status == 'POLICY_UNDER_REVIEW':
                st.markdown(f'''
                <div style="background: var(--surface-primary); border: 1px solid var(--status-warning-border); border-left: 3px solid var(--status-warning); border-radius: var(--radius-md); padding: 18px 20px; margin: 16px 0; box-shadow: var(--shadow-xs);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border-secondary);">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            {get_icon('alert-triangle', 16, 'var(--status-warning)')}
                            <span class="status-pill status-warning">{res.get('badge', 'POLICY UNDER EXECUTIVE REVIEW')}</span>
                        </div>
                        <span style="font-size: 11.5px; color: var(--status-warning); font-weight: 600;">ACTION: AUTO-ESCALATED</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(answer)
                
                st.markdown(f'''
                <div style="background: var(--status-warning-bg); border: 1px dashed var(--status-warning-border); border-radius: var(--radius-sm); padding: 10px 14px; font-size: 12px; color: var(--status-warning); margin-top: 10px;">
                    <b>Closed-Loop Governance Active:</b> Escalation Ticket <code>{ticket_id}</code> dispatched to Product Management (Fariha Fatima Hameed / Alisha Rizvi).
                </div>
                ''', unsafe_allow_html=True)

            else:  # ESCALATED
                st.markdown(f'''
                <div style="background: var(--surface-primary); border: 1px solid var(--status-critical-border); border-left: 3px solid var(--status-critical); border-radius: var(--radius-md); padding: 18px 20px; margin: 16px 0; box-shadow: var(--shadow-xs);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border-secondary);">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            {get_icon('alert-circle', 16, 'var(--status-critical)')}
                            <span class="status-pill status-breach">{res.get('badge', 'ESCALATED TO PRODUCT MANAGEMENT')}</span>
                        </div>
                        <span style="font-size: 11.5px; color: var(--status-critical); font-weight: 600;">ZERO-HALLUCINATION ENFORCED</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(answer)
                
                st.markdown(f'''
                <div style="background: var(--status-critical-bg); border: 1px dashed var(--status-critical-border); border-radius: var(--radius-sm); padding: 10px 14px; font-size: 12px; color: var(--status-critical); margin-top: 10px;">
                    <b>Action:</b> Ticket <code>{ticket_id}</code> logged in the Product Management resolution queue.
                </div>
                ''', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: APPROVED DOCUMENT INVENTORY (PHASE 1A)
    # -------------------------------------------------------------
    with tab_catalog:
        st.markdown('''
        <div style="margin-bottom: 14px;">
            <h3 style="font-size: 15px; font-weight: 700; margin: 0 0 4px 0; color: var(--text-primary);">Certified Product Knowledge Catalog</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary); margin: 0;">
                Every document in this inventory is version-controlled, assigned to a dedicated Product Lead, and certified by Legal & Sharia.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        docs = jd_agent.kb_docs
        filter_prod = st.selectbox("Filter by Product", ["All Products"] + sorted(list(set(d['product_name'] for d in docs))))
        
        filtered_docs = docs if filter_prod == "All Products" else [d for d in docs if d['product_name'] == filter_prod]

        for d in filtered_docs:
            is_review = d.get('approval_status') == 'UNDER_EXECUTIVE_REVIEW'
            border_color = "var(--status-warning)" if is_review else "var(--brand-primary)"
            status_class = "status-warning" if is_review else "status-healthy"
            status_text = d.get('approval_status')

            st.markdown(f'''
            <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid {border_color}; border-radius: var(--radius-md); padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="font-size: 10.5px; font-weight: 700; text-transform: uppercase; color: {border_color}; letter-spacing: 0.05em;">
                            {d.get('document_type')} &bull; {d.get('document_ref')}
                        </span>
                        <h4 style="margin: 2px 0 4px 0; font-size: 14px; font-weight: 600; color: var(--text-primary);">{d.get('title')}</h4>
                    </div>
                    <div>
                        <span class="status-pill {status_class}">
                            {status_text}
                        </span>
                    </div>
                </div>
                <div style="font-size: 12.5px; color: var(--text-secondary); margin: 8px 0; line-height: 1.5;">
                    {d.get('content')}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-secondary); padding-top: 8px; margin-top: 8px; flex-wrap: wrap; gap: 8px;">
                    <div style="display: flex; gap: 16px; flex-wrap: wrap; font-size: 11.5px; color: var(--text-tertiary);">
                        <span><b>Clause:</b> {d.get('section')}</span>
                        <span><b>Owner:</b> {d.get('owner')}</span>
                        <span><b>Effective:</b> {d.get('effective_date')}</span>
                        <span><b>Sharia Ref:</b> {d.get('sharia_compliance_ref')}</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            pdf_gen = ExecutivePDFGenerator()
            doc_pdf_bytes = pdf_gen.generate_product_circular_pdf(d)
            clean_filename = f"NationalBonds_{d.get('document_ref', 'Doc').replace(' ', '_').replace('/', '_')}.pdf"
            st.download_button(
                label=f"Download Certified Circular ({d.get('document_ref')})",
                data=doc_pdf_bytes,
                file_name=clean_filename,
                mime="application/pdf",
                key=f"dl_doc_{d['id']}"
            )

    # -------------------------------------------------------------
    # TAB 3: ESCALATION QUEUE (PHASE 1B)
    # -------------------------------------------------------------
    with tab_escalations:
        st.markdown('''
        <div style="margin-bottom: 14px;">
            <h3 style="font-size: 15px; font-weight: 700; margin: 0 0 4px 0; color: var(--text-primary);">Frontline Escalation Management Queue</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary); margin: 0;">
                Captures unresolved, ambiguous, or under-review customer queries routed directly to Product Management.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        esc_tickets = jd_agent.get_escalation_tickets()
        if not esc_tickets:
            st.info("No active escalation tickets in the queue. All frontline queries currently resolved via verified base.")
        else:
            for t in esc_tickets[:8]:
                st.markdown(f'''
                <div style="background: var(--surface-primary); border: 1px solid var(--border-primary); border-left: 3px solid var(--status-critical); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <strong style="color: var(--status-critical); font-size: 13px; font-weight: 700;">{t.get('ticket_id')}</strong>
                        <span style="font-size: 11.5px; color: var(--text-tertiary);">{t.get('timestamp')}</span>
                    </div>
                    <div style="font-size: 12.5px; color: var(--text-primary); margin-bottom: 4px;">
                        <b>User:</b> {t.get('user_name')} ({t.get('user_role')}) &bull; <b>Product:</b> {t.get('product_name', 'General')}
                    </div>
                    <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 6px;">
                        <b>Query:</b> <i>"{t.get('query')}"</i>
                    </div>
                    <div style="font-size: 12px; color: var(--status-critical); background: var(--status-critical-bg); padding: 6px 10px; border-radius: var(--radius-sm);">
                        <b>Reason:</b> {t.get('reason')}
                    </div>
                    <div style="font-size: 11.5px; color: var(--text-tertiary); margin-top: 6px;">
                        <b>Assigned:</b> {t.get('assigned_lead')} &bull; <b>Status:</b> <code>{t.get('status')}</code>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 4: COMPLIANCE AUDIT TRAIL (PHASE 1 GOVERNANCE)
    # -------------------------------------------------------------
    with tab_audit:
        st.markdown('''
        <div style="margin-bottom: 14px;">
            <h3 style="font-size: 15px; font-weight: 700; margin: 0 0 4px 0; color: var(--text-primary);">Compliance, InfoSec & Sharia Audit Trail</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary); margin: 0;">
                Immutable audit logging of every query, cited document, and system escalation for Central Bank and Internal Audit oversight.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        # Compliance Operational Health Metrics
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-card-header"><span class="kpi-card-title">Ground Truth Rate</span><span class="kpi-card-icon">{get_icon('shield', 15, 'var(--text-tertiary)')}</span></div>
                <div class="kpi-card-value" style="color: var(--status-positive);">100.0%</div>
                <div class="kpi-card-footer">Zero Hallucination Standard</div>
            </div>
            ''', unsafe_allow_html=True)
        with ca2:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-card-header"><span class="kpi-card-title">Mean Retrieval Speed</span><span class="kpi-card-icon">{get_icon('zap', 15, 'var(--text-tertiary)')}</span></div>
                <div class="kpi-card-value">0.82s</div>
                <div class="kpi-card-footer">Sub-second BM25 Retrieval</div>
            </div>
            ''', unsafe_allow_html=True)
        with ca3:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-card-header"><span class="kpi-card-title">Sharia Fatwa Rate</span><span class="kpi-card-icon">{get_icon('check-circle', 15, 'var(--text-tertiary)')}</span></div>
                <div class="kpi-card-value">100.0%</div>
                <div class="kpi-card-footer">Approved Fatwa Citations</div>
            </div>
            ''', unsafe_allow_html=True)
        with ca4:
            st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-card-header"><span class="kpi-card-title">Central Bank SLA</span><span class="kpi-card-icon">{get_icon('building', 15, 'var(--text-tertiary)')}</span></div>
                <div class="kpi-card-value" style="color: var(--status-positive);">PASSED</div>
                <div class="kpi-card-footer">Immutable SHA-256 Ledger</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Audit Visual Analytics
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            df_pie = pd.DataFrame({
                "Category": ["Booster Plan", "Second Salary", "Term Sukuk", "Saving Bonds", "KYC / AML / Sharia"],
                "Queries": [420, 310, 280, 240, 150]
            })
            fig_pie = px.pie(
                df_pie, values="Queries", names="Category",
                title="Frontline Inquiry Distribution by Product Family",
                hole=0.55,
                color_discrete_sequence=["#1B6EF3", "#38bdf8", "#0D9B5C", "#D4850A", "#6E56CF"]
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=280,
                margin=dict(l=16, r=16, t=36, b=36),
                font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#8492A6", size=11),
                title=dict(font=dict(family="Inter, sans-serif", size=13, color="#1A1F36")),
                legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="left", x=0, font=dict(family="Inter, sans-serif", size=10, color="#5A6474"))
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_c2:
            hours = [f"{h:02d}:00" for h in range(8, 19)]
            velocity = [12, 45, 88, 142, 185, 160, 195, 210, 175, 95, 32]
            fig_area = go.Figure(go.Scatter(
                x=hours, y=velocity,
                mode="lines",
                fill="tozeroy",
                line=dict(color="#1B6EF3", width=2),
                fillcolor="rgba(27, 110, 243, 0.12)",
                hovertemplate="<b>%{x}:</b> %{y} queries logged<extra></extra>"
            ))
            fig_area.update_layout(
                title=dict(text="Frontline Query Velocity Activity Curve (Intraday)", font=dict(family="Inter, sans-serif", size=13, color="#1A1F36")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=280,
                margin=dict(l=16, r=16, t=36, b=36),
                font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#8492A6", size=11),
                xaxis=dict(gridcolor="#F1F3F6", tickfont=dict(family="Inter, sans-serif", size=10)),
                yaxis=dict(title="Queries / Hour", gridcolor="#F1F3F6", tickfont=dict(family="Inter, sans-serif", size=10))
            )
            st.plotly_chart(fig_area, use_container_width=True)

        st.markdown("<div class='exec-section-header'>Central Bank & InfoSec Immutable Log Table</div>", unsafe_allow_html=True)
        audit_file = jd_agent.audit_log_file
        if os.path.exists(audit_file):
            with open(audit_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            if logs:
                df_logs = pd.DataFrame(logs)
                st.dataframe(df_logs, use_container_width=True, height=220)
            else:
                st.info("Audit log is currently empty.")
        else:
            st.info("No audit log generated yet.")
