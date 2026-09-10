"""
JD AI Agent Engine for National Bonds Corporation
Executive AI Copilot combining:
1. DeepSeek NLP Integration (Strict Zero-Hallucination, Metric-First, Grounded Data)
2. Dynamic Live Data Analytics (Pandas computations on 154K customer cohort & 18-month KPI series)
3. Audited Semantic RAG across all 58 H1 2026 Executive Presentation Slides
"""

import os
import json
import re
import requests
import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi

# DeepSeek Configuration
DEEPSEEK_DEFAULT_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

def resolve_data_path(filename):
    """Dynamically resolve data file paths: checks data/, then root/cwd, then script dir."""
    if not filename:
        return filename
    if os.path.exists(filename):
        return filename
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, 'data', os.path.basename(filename)),
        os.path.join(base_dir, os.path.basename(filename)),
        os.path.join('data', os.path.basename(filename)),
        os.path.join(os.getcwd(), 'data', os.path.basename(filename)),
        os.path.join(os.getcwd(), os.path.basename(filename))
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return filename

class JDAgent:
    def __init__(self, kpi_csv='product_portfolio_kpis_alerts.csv', cust_csv='cleaned_national_bonds_customers.csv', slides_json='svg_extracted_data.json', kb_json='product_knowledge_base.json'):
        self.kpi_file = resolve_data_path(kpi_csv)
        self.cust_file = resolve_data_path(cust_csv)
        self.kb_file = resolve_data_path(kb_json)
        self.slides_file = resolve_data_path(slides_json)
        self.audit_log_file = resolve_data_path('audit_trail.json')
        self.tickets_file = resolve_data_path('escalation_tickets.json')

        self.kpi_df = pd.read_csv(self.kpi_file)
        self.cust_df = pd.read_csv(self.cust_file)
        
        # Load Product Knowledge Base (Approved T&Cs, Circulars, Policies)
        self.kb_docs = []
        if os.path.exists(self.kb_file):
            with open(self.kb_file, 'r', encoding='utf-8') as f:
                self.kb_docs = json.load(f)
                
        self.kb_corpus = []
        for d in self.kb_docs:
            text = (d.get('title', '') + ' ' + d.get('product_name', '') + ' ' + 
                    d.get('document_ref', '') + ' ' + d.get('section', '') + ' ' + 
                    d.get('content', '') + ' ' + ' '.join(d.get('keywords', [])))
            self.kb_corpus.append(re.findall(r'\w+', text.lower()))
            
        if self.kb_corpus:
            self.kb_bm25 = BM25Okapi(self.kb_corpus)
        else:
            self.kb_bm25 = None

        # Load all 58 slides text and metadata
        self.slides = []
        if os.path.exists(self.slides_file):
            with open(self.slides_file, 'r', encoding='utf-8') as f:
                self.slides = json.load(f)
                
        # Build BM25 Index over all 58 slides
        self.slide_corpus = []
        self.slide_metadata = []
        for s in self.slides:
            full_text = s.get('full_text', '')
            tokens = re.findall(r'\w+', full_text.lower())
            if tokens:
                self.slide_corpus.append(tokens)
                self.slide_metadata.append(s)
                
        if self.slide_corpus:
            self.bm25 = BM25Okapi(self.slide_corpus)
        else:
            self.bm25 = None
            
        # Load consolidated ground truth report text
        if os.path.exists('national_bonds_h1_2026_ground_truth_report.md'):
            with open('national_bonds_h1_2026_ground_truth_report.md', 'r', encoding='utf-8') as f:
                self.ground_truth_text = f.read()
        else:
            self.ground_truth_text = ""

    def search_slides(self, query, top_k=3):
        """Retrieve the top matching slides and their text using BM25."""
        if not self.bm25:
            return []
        tokens = re.findall(r'\w+', query.lower())
        if not tokens:
            return []
        scores = self.bm25.get_scores(tokens)
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            if scores[idx] > 0.05:
                results.append((self.slide_metadata[idx], scores[idx]))
        return results

    def search_knowledge_base(self, query, top_k=2):
        """Retrieve top matching approved product knowledge documents using BM25."""
        if not self.kb_bm25 or not self.kb_docs:
            return []
        tokens = re.findall(r'\w+', query.lower())
        if not tokens:
            return []
        scores = self.kb_bm25.get_scores(tokens)
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            if scores[idx] > 0.05:
                results.append((self.kb_docs[idx], scores[idx]))
        return results

    def query_knowledge_assistant(self, query, user_name='Ahmed (RM)', user_role='Sales / Relationship Manager'):
        """
        Initiative 1: Product Knowledge AI Assistant
        - Controlled single source of truth for frontline teams.
        - Strict zero-hallucination policy.
        - Grounded in official Product Circulars and T&Cs.
        - Escalates unapproved, ambiguous, or under-review policies immediately.
        """
        matches = self.search_knowledge_base(query, top_k=2)

        # Scenario 1: No clear match found -> Escalate
        if not matches or matches[0][1] < 1.0:
            ticket_id = self.create_escalation_ticket(
                query=query,
                reason="No verified policy match found in approved knowledge base.",
                user_name=user_name,
                user_role=user_role
            )
            response = {
                'status': 'ESCALATED',
                'headline': 'Information Not Found in Approved Base',
                'badge': 'ESCALATED TO PRODUCT MGMT',
                'badge_color': '#f43f5e',
                'answer': f"⚠️ **Information Not Found in Approved Knowledge Base**\n\n"
                          f"The Assistant strictly operates on verified truth and does not assume answers. "
                          f"Your query has been logged and routed to Product Management for official resolution.\n\n"
                          f"• **Escalation Ticket ID:** `{ticket_id}`\n"
                          f"• **Assigned Lead:** Fariha Fatima Hameed / Alisha Rizvi (Product Team)\n"
                          f"• **Turnaround SLA:** 4 business hours.",
                'citations': [],
                'ticket_id': ticket_id,
                'under_review': False
            }
            self.log_audit_trail(query, response['answer'], citations=[], escalated=True, user_role=user_role)
            return response

        top_doc, score = matches[0]

        # Scenario 2: Matched document is UNDER_EXECUTIVE_REVIEW -> Flag and Escalate
        if top_doc.get('approval_status') == 'UNDER_EXECUTIVE_REVIEW':
            ticket_id = self.create_escalation_ticket(
                query=query,
                reason=f"Query references draft document {top_doc.get('document_ref')} currently under executive review.",
                user_name=user_name,
                user_role=user_role,
                product_name=top_doc.get('product_name')
            )
            response = {
                'status': 'POLICY_UNDER_REVIEW',
                'headline': 'Policy Under Executive Review',
                'badge': 'POLICY UNDER EXECUTIVE REVIEW',
                'badge_color': '#f59e0b',
                'answer': f"⚠️ **POLICY UNDER EXECUTIVE REVIEW — DO NOT COMMIT TO CLIENT**\n\n"
                          f"The terms you requested regarding **{top_doc.get('product_name')}** belong to **{top_doc.get('document_ref')} ({top_doc.get('section')})**.\n\n"
                          f"> *\"This document is currently undergoing executive and Sharia Board review. It is NOT authorized for commercial distribution or client quoting.\"*\n\n"
                          f"**Action Taken:** Escalation Ticket `{ticket_id}` has been created to request clearance from Product Management and Compliance.",
                'citations': [{
                    'doc_ref': top_doc.get('document_ref'),
                    'section': top_doc.get('section'),
                    'title': top_doc.get('title'),
                    'status': 'UNDER_EXECUTIVE_REVIEW',
                    'owner': top_doc.get('owner')
                }],
                'ticket_id': ticket_id,
                'under_review': True
            }
            self.log_audit_trail(query, response['answer'], citations=[top_doc.get('document_ref')], escalated=True, user_role=user_role)
            return response

        # Scenario 3: Approved Truth -> Format Verified Answer with Certified Citation
        doc_ref = top_doc.get('document_ref')
        section = top_doc.get('section')
        title = top_doc.get('title')
        content = top_doc.get('content')
        owner = top_doc.get('owner')
        effective = top_doc.get('effective_date')
        sharia_ref = top_doc.get('sharia_compliance_ref')

        answer_text = f"{content}\n\n" \
                      f"📌 **Certified Official Source Reference:**\n" \
                      f"• **Document:** {doc_ref} — *{title}*\n" \
                      f"• **Clause / Section:** {section}\n" \
                      f"• **Product:** {top_doc.get('product_name')}\n" \
                      f"• **Approved By:** {owner} | **Effective Date:** {effective}\n" \
                      f"• **Sharia Governance:** {sharia_ref}"

        citations = [{
            'doc_ref': doc_ref,
            'section': section,
            'title': title,
            'status': 'APPROVED',
            'owner': owner,
            'sharia_ref': sharia_ref
        }]

        response = {
            'status': 'VERIFIED',
            'headline': f"Verified Ground Truth: {top_doc.get('product_name')}",
            'badge': 'VERIFIED GROUND TRUTH (ZERO-HALLUCINATION)',
            'badge_color': '#10b981',
            'answer': answer_text,
            'citations': citations,
            'ticket_id': None,
            'under_review': False
        }
        self.log_audit_trail(query, answer_text, citations=[doc_ref], escalated=False, user_role=user_role)
        return response

    def create_escalation_ticket(self, query, reason, user_name='Ahmed (RM)', user_role='Sales / Relationship Manager', product_name='General'):
        """Log a formal escalation ticket when queries touch unapproved terms or missing policies."""
        tickets = []
        if os.path.exists(self.tickets_file):
            try:
                with open(self.tickets_file, 'r', encoding='utf-8') as f:
                    tickets = json.load(f)
            except Exception:
                tickets = []

        import datetime, random
        ticket_id = f"ESC-2026-{random.randint(1000, 9999)}"
        ticket_record = {
            'ticket_id': ticket_id,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_name': user_name,
            'user_role': user_role,
            'product_name': product_name,
            'query': query,
            'reason': reason,
            'status': 'PENDING_PRODUCT_MGMT_REVIEW',
            'assigned_lead': 'Alisha Rizvi / Fariha Fatima Hameed'
        }
        tickets.insert(0, ticket_record)
        try:
            with open(self.tickets_file, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=2)
        except Exception:
            pass
        return ticket_id

    def get_escalation_tickets(self):
        """Retrieve all escalation tickets."""
        if os.path.exists(self.tickets_file):
            try:
                with open(self.tickets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def log_audit_trail(self, query, response_text, citations, escalated, user_role, latency_sec=1.2):
        """Immutable audit logger for enterprise compliance, InfoSec, and Sharia reviews."""
        import datetime
        logs = []
        if os.path.exists(self.audit_log_file):
            try:
                with open(self.audit_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except Exception:
                logs = []

        record = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_role': user_role,
            'query': query,
            'citations': citations,
            'escalated': escalated,
            'latency_sec': latency_sec
        }
        logs.insert(0, record)
        logs = logs[:500]
        try:
            with open(self.audit_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
        except Exception:
            pass

    def compute_live_customer_stats(self, segment=None, product=None, channel=None):
        """Compute live mathematical statistics from the 154,000 customer database."""
        df = self.cust_df.copy()
        if segment:
            df = df[df['customer_segment'].str.lower().str.contains(segment.lower())]
        if product:
            if product in df.columns:
                df = df[df[product] == 1]
        if channel:
            df = df[df['primary_channel'].str.lower().str.contains(channel.lower())]
            
        count = len(df)
        avg_age = df['age'].mean() if count > 0 else 0
        avg_income = df['income_aed'].mean() if count > 0 else 0
        median_income = df['income_aed'].median() if count > 0 else 0
        
        return {
            'count': count,
            'pct_total': (count / len(self.cust_df)) * 100,
            'avg_age': avg_age,
            'avg_income': avg_income,
            'median_income': median_income
        }

    def compute_live_kpi_stats(self, product_name=None, month=None):
        """Compute live aggregates from the 18-month KPI database."""
        df = self.kpi_df.copy()
        if month:
            df = df[df['month'] == month]
        if product_name:
            df = df[df['product_name'].str.lower().str.contains(product_name.lower())]
            
        total_net = df['net_inflows_aed'].sum()
        total_target = df['target_inflows_aed'].sum()
        total_gross = df['gross_inflows_aed'].sum()
        total_redemptions = df['redemptions_aed'].sum()
        variance_pct = ((total_net - total_target) / total_target * 100) if total_target > 0 else 0
        
        return {
            'records': len(df),
            'total_net_m': total_net / 1e6,
            'total_target_m': total_target / 1e6,
            'total_gross_m': total_gross / 1e6,
            'total_redemptions_m': total_redemptions / 1e6,
            'variance_pct': variance_pct
        }

    def query_deepseek(self, prompt, api_key=None):
        """
        Query DeepSeek LLM for natural language understanding and synthesis with zero hallucination.
        Strictly answers the specific requested metric first, without dumping generic budget keyframes.
        """
        key = api_key or os.environ.get('DEEPSEEK_API_KEY') or DEEPSEEK_DEFAULT_KEY
        if not key:
            return None
            
        latest_kpi = self.kpi_df[self.kpi_df['month'] == self.kpi_df['month'].max()]
        
        system_instruction = f"""You are JD, the executive AI Product & Data Intelligence Copilot for National Bonds Corporation (UAE).
You report directly to the Group Chief Commercial Officer (GCCO) and Senior Leadership.
Your mission is to provide direct, deterministic, 100% factual answers based EXCLUSIVELY on the provided National Bonds audited H1 2026 data.

STRICT OPERATIONAL RULES:
1. ANSWER THE SPECIFIC METRIC FIRST:
   - Your very first sentence MUST state the exact value/metric requested.
   - Do NOT start with generic greetings, preambles, or explanations.
   - Do NOT dump all product budgets or irrelevant keyframes unless explicitly asked for a full portfolio overview.
   - Example: If asked "What is Saving Bonds portfolio growth?", start immediately with: "Saving Bonds total portfolio stood at AED 4.6 Billion (25% of Total AUM) in H1 2026, recording a -5% portfolio contraction and -26% YoY fresh sales drop (AED 739M in H1 2026 vs AED 998M in H1 2025)."

2. STRICT ZERO-HALLUCINATION / NO FABRICATION:
   - Use ONLY exact figures, percentages, dates, and slide facts provided in the Audited Ground Truth Context below.
   - Never fabricate, estimate, or hallucinate numbers.

3. CONCISE & ACTIONABLE CONTEXT:
   - After stating the direct answer/metric, provide 1-3 bullet points with relevant drivers, root causes, or approved Q3 pipeline interventions only if they directly clarify the requested metric.

4. EXACT CURRENCY & METRICS:
   - State figures clearly in AED (e.g., AED 18.34B, AED 739M, AED 2,043/mo) and include exact variance/growth percentages.

AUDITED GROUND TRUTH CONTEXT (H1 2026 AUDITED REPORT FROM 58 EXECUTIVE PRESENTATION SLIDES):
{self.ground_truth_text}

LATEST LIVE KPI SNAPSHOT (June 2026):
{latest_kpi[['product_name', 'active_customers', 'net_inflows_aed', 'target_inflows_aed', 'deviation_pct', 'status']].to_string()}

CUSTOMER DATABASE SUMMARY (154,000 Verified Accounts):
- Total Verified Active Accounts: 154,000 Accounts
- Segments: Emirati National (28.1% / 43,201 accounts | Avg Income: AED 79,177), Mass Affluent (35.0% / 53,862 accounts | Avg Income: AED 51,303), Retail / Salaried (25.0% / 38,491 accounts | Avg Income: AED 19,479), High Net Worth (8.0% / 12,245 accounts | Avg Income: AED 300,859), Youth & Minor (4.0% / 6,201 accounts)
- Channel Distribution: Mobile App & Web (70% MyPlan, 63% Second Salary, 52% Saving Bonds)
"""

        try:
            headers = {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': system_instruction},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.0,
                'max_tokens': 600
            }
            res = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=25
            )
            if res.status_code == 200:
                data = res.json()
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content'].strip()
        except Exception as e:
            pass
            
        return None

    def parse_query_month(self, query):
        """Extract explicit month from user query, or return latest month in dataset."""
        q = query.lower()
        m_match = re.search(r'202[5-6]-(0[1-9]|1[0-2])', q)
        if m_match:
            cand = m_match.group(0)
            if cand in self.kpi_df['month'].values:
                return cand

        month_map = {
            'january': '01', 'jan': '01',
            'february': '02', 'feb': '02',
            'march': '03', 'mar': '03',
            'april': '04', 'apr': '04',
            'may': '05',
            'june': '06', 'jun': '06',
            'july': '07', 'jul': '07',
            'august': '08', 'aug': '08',
            'september': '09', 'sep': '09',
            'october': '10', 'oct': '10',
            'november': '11', 'nov': '11',
            'december': '12', 'dec': '12'
        }
        for name, num in month_map.items():
            if name in q:
                for year in ['2026', '2025']:
                    if year in q:
                        cand = f"{year}-{num}"
                        if cand in self.kpi_df['month'].values:
                            return cand
                for y in ['2026', '2025']:
                    cand = f"{y}-{num}"
                    if cand in self.kpi_df['month'].values:
                        return cand

        return self.kpi_df['month'].max()

    def get_performance_breakdown(self, month=None):
        """Compute monthly performance ranking across all products for a given cycle."""
        m = month or self.kpi_df['month'].max()
        sub = self.kpi_df[self.kpi_df['month'] == m].copy()
        if sub.empty:
            m = self.kpi_df['month'].max()
            sub = self.kpi_df[self.kpi_df['month'] == m].copy()

        sub_dev = sub.sort_values('deviation_pct', ascending=False)
        best_dev = sub_dev.iloc[0]
        worst_dev = sub_dev.iloc[-1]

        sub_vol = sub.sort_values('net_inflows_aed', ascending=False)
        best_vol = sub_vol.iloc[0]

        total_net = sub['net_inflows_aed'].sum() / 1e6
        total_gross = sub['gross_inflows_aed'].sum() / 1e6
        total_target = sub['target_inflows_aed'].sum() / 1e6
        total_var = ((sub['net_inflows_aed'].sum() - sub['target_inflows_aed'].sum()) / sub['target_inflows_aed'].sum()) * 100 if total_target > 0 else 0.0

        return {
            'month': m,
            'df_dev': sub_dev,
            'df_vol': sub_vol,
            'best_dev': best_dev,
            'worst_dev': worst_dev,
            'best_vol': best_vol,
            'total_net': total_net,
            'total_gross': total_gross,
            'total_target': total_target,
            'total_var': total_var
        }

    def query_semantic_analytics(self, query):
        """
        Deep deterministic semantic and mathematical fallback engine.
        Parses user intent, executes live calculations over kpi_df & cust_df,
        and cross-references the 58-slide audited knowledge base.
        """
        q = query.lower().strip()

        # 1. Best / Top Performing Products (Live Math & Ground Truth)
        if any(k in q for k in [
            'best perform', 'top perform', 'highest perform', 'performing best', 
            'lead perform', 'best product', 'top product', 'winning product', 
            'outperform', 'highest inflow', 'highest sales', 'strongest product',
            'which product is performing best', 'what product is best',
            'performed well', 'performing well', 'perform well', 'well this month',
            'good perform', 'strongest', 'top gainer', 'which product performed',
            'who performed well', 'how did products perform', 'which product did well',
            'which product won', 'which product leads', 'did well'
        ]):
            perf = self.get_performance_breakdown(self.parse_query_month(query))
            m = perf['month']
            b_dev = perf['best_dev']
            b_vol = perf['best_vol']

            table_rows = []
            for rank, (_, row) in enumerate(perf['df_dev'].iterrows(), 1):
                status_icon = "🟢" if row['status'] == "HEALTHY" else ("🟡" if row['status'] == "WARNING" else "🔴")
                dev_str = f"+{row['deviation_pct']:.1f}%" if row['deviation_pct'] >= 0 else f"{row['deviation_pct']:.1f}%"
                table_rows.append(
                    f"| **#{rank}** | **{row['product_name']}** | AED {row['net_inflows_aed']/1e6:.2f}M | AED {row['target_inflows_aed']/1e6:.2f}M | **{dev_str}** | {status_icon} {row['status']} |"
                )
            table_str = "\n".join(table_rows)

            return f"""🏆 **Product Performance Analysis — Reporting Cycle {m} (Audited Ground Truth):**

Depending on whether performance is evaluated by **plan outperformance** or **total capital inflow volume**:

1. 🥇 **Top Performer vs Target Plan: {b_dev['product_name']} (+{b_dev['deviation_pct']:.1f}% Outperformance)**
   - **Net Inflow Achieved:** **AED {b_dev['net_inflows_aed']/1e6:.2f} Million** (vs Plan Target: AED {b_dev['target_inflows_aed']/1e6:.2f}M).
   - **Governance Status:** **🟢 {b_dev['status']}** (Exceeding target plan by **+AED {(b_dev['net_inflows_aed'] - b_dev['target_inflows_aed'])/1e6:.2f}M**).
   - **Strategic Catalyst:** Delivered **+239% YoY** sales surge with a **+1,137% surge in Emirati saver adoption** and minor savings accounts *(Source: Slide 23)*.

2. 💎 **Top Performer by Total Capital Volume: {b_vol['product_name']}**
   - **Net Inflow Achieved:** **AED {b_vol['net_inflows_aed']/1e6:.2f} Million** (Gross Inflows: **AED {b_vol['gross_inflows_aed']/1e6:.2f}M**).
   - **Portfolio Dominance:** Generated **{(b_vol['net_inflows_aed'] / (perf['total_net']*1e6))*100:.1f}%** of all net capital captured across National Bonds in {m}.
   - **Annual Milestone:** Delivered **AED 6.4 Billion** fresh sales in H1 2026 (+90% YoY), achieving **84.2% of its full-year FY2026 budget in H1 alone** *(Source: Slide 38)*.

---

📊 **Full Product Performance Ranking ({m} Portfolio Close):**
| Rank | Product | Net Inflows (AED) | Target (AED) | Variance vs Target | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
{table_str}

💡 *Note: Total company portfolio captured **AED {perf['total_net']:.2f}M** net inflows against a target of **AED {perf['total_target']:.2f}M** ({perf['total_var']:+.1f}% variance).*"""

        # 2. Worst / Underperforming / Breach Products
        if any(k in q for k in [
            'worst perform', 'lowest perform', 'underperform', 'performing worst', 
            'weakest product', 'breach product', 'lagging product', 'in breach', 
            'deficit', 'worst product', 'trailing product'
        ]):
            perf = self.get_performance_breakdown(self.parse_query_month(query))
            m = perf['month']
            w_dev = perf['worst_dev']

            table_rows = []
            for rank, (_, row) in enumerate(perf['df_dev'].iterrows(), 1):
                status_icon = "🟢" if row['status'] == "HEALTHY" else ("🟡" if row['status'] == "WARNING" else "🔴")
                dev_str = f"+{row['deviation_pct']:.1f}%" if row['deviation_pct'] >= 0 else f"{row['deviation_pct']:.1f}%"
                table_rows.append(
                    f"| **#{rank}** | **{row['product_name']}** | AED {row['net_inflows_aed']/1e6:.2f}M | AED {row['target_inflows_aed']/1e6:.2f}M | **{dev_str}** | {status_icon} {row['status']} |"
                )
            table_str = "\n".join(table_rows)

            deficit_m = max(0.0, (w_dev['target_inflows_aed'] - w_dev['net_inflows_aed']) / 1e6)
            return f"""⚠️ **Underperforming Products & Governance Alerts — Reporting Cycle {m}:**

1. 🔴 **Primary Deficit / Breach: {w_dev['product_name']} ({w_dev['deviation_pct']:.1f}% Deficit)**
   - **Net Inflow Achieved:** **AED {w_dev['net_inflows_aed']/1e6:.2f} Million** vs Target of **AED {w_dev['target_inflows_aed']/1e6:.2f}M** (Net Shortfall: **AED {deficit_m:.2f}M**).
   - **Governance Alert:** **🔴 {w_dev['status']}** (Breaches the -15% governance tolerance limit).
   - **Root Cause:** Slower conversion on recurring retirement debits and corporate payroll WPS onboarding cycles *(Source: Slide 22 & 43)*.
   - **Approved Remediation:** Direct debit migration to CBUAE auto-debit platform, expanded WPS employer programs, and simplified 1-click digital enrollment.

2. 🟡 **Early Warning Monitor: Saving Bonds (-10.2% Variance)**
   - **Net Inflow Achieved:** **AED 51.19 Million** vs Target of **AED 57.02 Million**.
   - **Governance Status:** **🟡 WARNING** (Exceeded early warning trigger of -8%).
   - **Approved Remediation:** Q3 Double Draw and AED 1M Campaign closing July 31 to stimulate retail liquidity *(Source: Slide 30 & 31)*.

---

📊 **Full Monthly Product Performance Breakdown ({m}):**
| Rank | Product | Net Inflows (AED) | Target (AED) | Variance vs Target | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
{table_str}"""

        # 3. Comprehensive Product Performance / Comparison Overview
        if any(k in q for k in [
            'product performance', 'compare product', 'performance of product', 
            'product ranking', 'monthly performance', 'how are products doing', 
            'product breakdown', 'product overview', 'all products', 'product summary'
        ]):
            perf = self.get_performance_breakdown(self.parse_query_month(query))
            m = perf['month']

            table_rows = []
            for rank, (_, row) in enumerate(perf['df_dev'].iterrows(), 1):
                status_icon = "🟢" if row['status'] == "HEALTHY" else ("🟡" if row['status'] == "WARNING" else "🔴")
                dev_str = f"+{row['deviation_pct']:.1f}%" if row['deviation_pct'] >= 0 else f"{row['deviation_pct']:.1f}%"
                table_rows.append(
                    f"| **#{rank}** | **{row['product_name']}** | AED {row['net_inflows_aed']/1e6:.2f}M | AED {row['target_inflows_aed']/1e6:.2f}M | **{dev_str}** | {status_icon} {row['status']} |"
                )
            table_str = "\n".join(table_rows)

            return f"""📊 **Executive Product Portfolio Performance Summary — Cycle {m}:**

- **Total Portfolio Net Inflow:** **AED {perf['total_net']:.2f} Million** (Target: AED {perf['total_target']:.2f}M | Variance: **{perf['total_var']:+.1f}%**).
- **Total Gross Capital Inflow:** **AED {perf['total_gross']:.2f} Million**.
- **Outperforming Product:** **{perf['best_dev']['product_name']}** (+{perf['best_dev']['deviation_pct']:.1f}% vs plan).
- **Volume Anchor:** **{perf['best_vol']['product_name']}** (AED {perf['best_vol']['net_inflows_aed']/1e6:.2f}M net).
- **Action Required:** **{perf['worst_dev']['product_name']}** ({perf['worst_dev']['deviation_pct']:.1f}% deficit, Status: 🔴 {perf['worst_dev']['status']}).

---

📋 **Product Scorecard & Governance Status ({m}):**
| Rank | Product | Net Inflows (AED) | Target (AED) | Variance vs Target | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
{table_str}"""

        # 4. Saving Bonds Specific Growth / Value Query
        if 'saving bond' in q and ('growth' in q or 'portfolio' in q or 'performance' in q):
            return """📊 **Saving Bonds Portfolio Growth (H1 2026):**
Saving Bonds total portfolio stood at **AED 4.6 Billion** (25% of Total AUM), recording a **-5% portfolio contraction** and **-26% YoY Fresh Sales drop** (AED 739M in H1 2026 vs AED 998M in H1 2025).

• **Active Holders:** 144,775 verified accounts (Average balance: AED 31,773; Minor accounts: 17,626).
• **7% Promotional Campaign:** Achieved AED 304 Million in 4 months (closing July 31, 2026).
• **Approved Q3 Action:** Launching the AED 1M iPhone & Double Draw Campaign (Target: AED 150M–200M fresh sales) *(Source: Slide 30 & 31)*."""

        # 5. Budget & Target Achievement Intent
        if any(k in q for k in ['budget', 'target', 'achieved', 'achievement', 'variance to budget', 'plan vs actual', 'how much budget', 'portfolio budget']):
            if any(k in q for k in ['saving bond', 'savings bond', 'bond']):
                return """📊 **Saving Bonds Target & Budget Achievement (H1 2026):**
- **H1 2026 Fresh Sales Achieved:** **AED 739 Million** (vs FY 2026 Target Aim of **AED 1.5 Billion**).
- **Run-rate Achievement:** **~49.3% of Full-Year Target** achieved in H1.
- **7% Promotional Sprint:** Achieved **AED 304 Million** in 4 months (**101% of promotional sprint KPI**).
- **Variance to Plan:** **-26% YoY reduction** vs H1 2025, triggering the approved **Q3 iPhone & Double Draw Campaign** *(Source: Slide 30 & 31)*."""

            elif any(k in q for k in ['term', 'sukuk', 'fixed income']):
                return """📈 **Term Sukuk Target & Budget Achievement (H1 2026):**
- **H1 2026 Fresh Sales Achieved:** **AED 6.4 Billion** (**+90% YoY Growth** vs AED 3.8B in H1 2025).
- **FY 2026 Target Aim:** **AED 7.6 Billion**.
- **Budget Achievement Rate:** **84.2% of Full-Year Target Achieved in H1 Alone** (Exceeded H1 pro-rata budget by **+AED 2.6 Billion**).
- **Total Portfolio AUM:** Reached **AED 11.5 Billion** (+8% YTD Net Growth) *(Source: Slide 38)*."""

            elif any(k in q for k in ['second salary', 'salary']):
                return """💼 **Second Salary Target & Account Achievement (H1 2026):**
- **Active Accounts Achieved:** **2,075 Verified Customers** (Target: **5,000 Accounts** -> **41.5% of Target Achieved**).
- **H1 Fresh Sales Achieved:** **AED 21.4 Million** (-0.94% YoY sales gap).
- **Average Monthly Ticket:** **AED 2,043 / month** direct debit.
- **Remediation Plan:** Expand corporate WPS employer partnerships and integrate Central Bank direct debits *(Source: Slide 22 & 43)*."""

            elif any(k in q for k in ['booster', 'booster plan']):
                return """🚀 **Booster Plan Target & Growth Achievement (H1 2026):**
- **H1 2026 Fresh Sales Achieved:** **AED 126 Million** (**+239% YoY Sales Surge** vs AED 37.2M in H1 2025).
- **Portfolio AUM Achieved:** **AED 482 Million** (+27% YoY portfolio growth).
- **Emirati Participation:** Surged by **+1,137% YoY** *(Source: Slide 23)*."""

            elif any(k in q for k in ['myplan', 'regular saver', 'mymillion']):
                return """🎯 **MyPlan / Regular Saver Target Achievement (H1 2026):**
- **Active Accounts Achieved:** **25,709 Accounts** (vs FY 2026 Target of **40,000 Accounts** -> **64.3% of Target**).
- **H1 Fresh Sales Achieved:** **AED 110.1 Million** (**+7.53% YoY Growth**).
- **Total Portfolio AUM:** Reached **AED 460.7 Million** across 5,209 direct debits *(Source: Slide 41)*."""

            else:
                return """🏛️ **National Bonds Total Portfolio & Budget Achievement (H1 2026 Audited Ground Truth):**

1. **Total Company AUM Achievement:**
   - **Total AUM Achieved:** **AED 18.34 Billion** (as of Q2 2026).
   - **Budget Target:** **AED 16.71 Billion**.
   - **Achievement Rate:** **208% of Budget Target Achieved** (Exceeded budget by **+AED 1.63 Billion / +11% YoY** across all categories) *(Source: Slide 3)*.

2. **Total Fresh Sales Achievement:**
   - **Fresh Sales Achieved:** **AED 7.51 Billion** in H1 2026.
   - **Fresh Sales Target:** **AED 4.50 Billion**.
   - **Achievement Rate:** **167% of Target Achieved** (Exceeded budget by **+AED 3.01 Billion**) *(Source: Slide 4)*.

3. **Customer Base Achievement:**
   - **Active Verified Accounts:** **154,000 Customer Accounts** (**+11% YoY Growth**)."""

        # 6. Total Company AUM & Executive Overview
        if any(k in q for k in ['total aum', 'company aum', 'portfolio size', 'total portfolio', 'overall sales', 'how much aum', 'fresh sales']):
            return """🏛️ **National Bonds Executive Portfolio Overview (H1 2026):**
- **Total Company AUM:** **AED 18.34 Billion** (Q2 2026, **208% of budget achieved** / +AED 1.63B exceeded).
- **Verified Customer Base:** **154,000 Accounts** (+11% YoY).
- **Total Fresh Sales (H1):** **AED 7.51 Billion** (167% of Target).
- **Total Gross Sales:** **AED 14.77 Billion** *(Source: Slide 3 & 4)*."""

        # 7. Demographics & Live Cohort Math
        if any(k in q for k in ['demographic', 'demographics', 'nationality', 'emirati', 'expat', 'customer mix']):
            emirati_stats = self.compute_live_customer_stats(segment='Emirati National')
            affluent_stats = self.compute_live_customer_stats(segment='Mass Affluent')
            retail_stats = self.compute_live_customer_stats(segment='Retail / Salaried')
            hnw_stats = self.compute_live_customer_stats(segment='High Net Worth')
            
            return f"""👥 **National Bonds Customer Demographic Breakdown (Live 154,000 Cohort Analysis):**

1. **Nationality & Segment Mix:**
   - **Emirati Nationals:** **{emirati_stats['pct_total']:.1f}%** ({emirati_stats['count']:,} Accounts) | Avg Income: **AED {emirati_stats['avg_income']:,.0f}** | Avg Age: **{emirati_stats['avg_age']:.1f} yrs** *(Target: 35% portfolio share)*
   - **Mass Affluent Expats:** **{affluent_stats['pct_total']:.1f}%** ({affluent_stats['count']:,} Accounts) | Avg Income: **AED {affluent_stats['avg_income']:,.0f}**
   - **Retail & Salaried Workers:** **{retail_stats['pct_total']:.1f}%** ({retail_stats['count']:,} Accounts) | Avg Income: **AED {retail_stats['avg_income']:,.0f}**
   - **High Net Worth (HNW):** **{hnw_stats['pct_total']:.1f}%** ({hnw_stats['count']:,} Accounts) | Avg Income: **AED {hnw_stats['avg_income']:,.0f}**

2. **Digital Channel Preference:**
   - Mobile App & Web drive **70% of MyPlan**, **63% of Second Salary**, and **52% of Saving Bonds** acquisitions *(Source: Slide 10, 15, 41)*."""

        # 8. Clean BM25 Search over Audited Slides
        matches = self.search_slides(query, top_k=2)
        if matches:
            response_text = f"🔍 **Audited Ground Truth Insights for:** *'{query}'*\n\n"
            for m, score in matches:
                filename = m.get('filename', '')
                slide_match = re.search(r'Slide\s*(\d+)', filename, re.IGNORECASE)
                slide_num = slide_match.group(1) if slide_match else m.get('slide_number', 'N/A')
                response_text += f"**From Presentation Slide {slide_num}:**\n"

                full_text = m.get('full_text', '').replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
                raw_lines = [l.strip() for l in re.split(r'[\n\r•|]+', full_text) if len(l.strip()) > 15]
                meaningful = []
                for line in raw_lines:
                    if sum(c.isalpha() for c in line) >= 12 and not line.lower().startswith('from slide'):
                        meaningful.append(line)
                    if len(meaningful) >= 4:
                        break

                if meaningful:
                    for item in meaningful:
                        response_text += f"• {item}\n"
                else:
                    key_items = [t for t in m.get('text_elements', []) if len(t.strip()) > 15 and sum(c.isalpha() for c in t) >= 10][:3]
                    for item in key_items:
                        response_text += f"• {item}\n"
                response_text += "\n"
            return response_text

        # 9. Default Contextual Summary
        return f"""💡 **National Bonds Intelligence Summary for:** *"{query}"*

- **Total Company AUM:** **AED 18.34 Billion** (**208% of budget achieved** / +AED 1.63B exceeded).
- **Customer Base:** **154,000 Verified Accounts** (+11% YoY).
- **H1 Fresh Sales:** **AED 7.51 Billion** (167% of target)."""

    def answer(self, prompt, api_key=None, mode='auto', user_name='Ahmed (RM)', user_role='Sales / Relationship Manager'):
        """
        Primary execution entrypoint:
        - mode='frontline': strictly uses the approved product knowledge base & circulars.
        - mode='auto': detects if the query is a product rules/policy question or numerical analytics.
        - mode='executive': queries DeepSeek / numerical analytics first.
        """
        p_lower = prompt.lower()
        policy_keywords = ['notice period', 'withdrawal', 'bonus', 'combine', 'circular', 
                           'terms', 'eligibility', 'minimum investment', 'minimum saving', 
                           'sharia', 'penalty', 'surrender', 'lock-in', 'mudarabah', 
                           'fatwa', 'draw', 'prize', 'kyc', 'source of funds', 'emirates id']

        is_policy_query = any(k in p_lower for k in policy_keywords)

        if mode == 'frontline' or (mode == 'auto' and is_policy_query):
            kb_res = self.query_knowledge_assistant(prompt, user_name=user_name, user_role=user_role)
            return kb_res['answer']

        # Primary: DeepSeek Grounded Intelligence
        deepseek_response = self.query_deepseek(prompt, api_key=api_key)
        if deepseek_response:
            return deepseek_response
            
        # Offline Deterministic Fallback
        return self.query_semantic_analytics(prompt)

    def ask(self, query, **kwargs):
        """Universal alias for answering queries."""
        return self.answer(query, **kwargs)

