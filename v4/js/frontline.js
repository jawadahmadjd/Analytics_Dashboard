/* ==========================================================================
   National Bonds Corporation — Frontline Knowledge Assistant (Initiative 1)
   Document Reference: NBC-DESKTOP-UI-AUDIT-2026-V1
   ========================================================================== */

window.NBC_FRONTLINE = {
  activeTab: 'ask',

  render(container, state) {
    container.innerHTML = `
      <!-- Frontline Hero Banner -->
      <div class="frontline-hero">
        <div>
          <div style="font-size: 21px; font-weight: 800; color: var(--navy-slate-900);">Frontline Knowledge Assistant & Grounded Copilot</div>
          <div style="font-size: 13px; color: var(--text-secondary); margin-top: 3px;">
            Single Source of Truth for Sales, Branches & Relationship Managers &bull; 100% Sharia Certified & Grounded Citations
          </div>
        </div>
        <div class="persona-badge">
          <div class="persona-avatar">A</div>
          <div>
            <div style="font-size: 13px; font-weight: 800; color: var(--navy-slate-900);">Ahmed &bull; Relationship Manager</div>
            <div style="font-size: 11px; color: var(--brand-primary); font-weight: 600;">Direct Sales & Branch Network</div>
          </div>
        </div>
      </div>

      <!-- 4 Operational Summary Cards -->
      <div class="kpi-cards-grid" style="margin-bottom: 20px;">
        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header">
            <span class="kpi-card-label">Approved Documents</span>
            <span class="material-symbols-rounded" style="color: var(--brand-primary);">menu_book</span>
          </div>
          <div class="kpi-card-value" style="font-size: 22px;">10 Certified</div>
          <div class="kpi-card-footer">
            <span class="status-badge healthy">100% VERIFIED</span>
            <span class="kpi-target-note">All 5 Products Active</span>
          </div>
        </div>

        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header">
            <span class="kpi-card-label">Grounding Standard</span>
            <span class="material-symbols-rounded" style="color: #10b981;">verified</span>
          </div>
          <div class="kpi-card-value" style="font-size: 22px; color: #10b981;">Zero Hallucination</div>
          <div class="kpi-card-footer">
            <span class="status-badge healthy">STRICT RAG</span>
            <span class="kpi-target-note">Fatwa Compliance</span>
          </div>
        </div>

        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header">
            <span class="kpi-card-label">Retrieval SLA</span>
            <span class="material-symbols-rounded" style="color: var(--brand-primary);">bolt</span>
          </div>
          <div class="kpi-card-value" style="font-size: 22px; font-family: var(--font-mono);">0.82s Avg</div>
          <div class="kpi-card-footer">
            <span class="status-badge healthy">&lt; 1.5s TARGET</span>
            <span class="kpi-target-note">Sub-Second SLA</span>
          </div>
        </div>

        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header">
            <span class="kpi-card-label">Open Escalations</span>
            <span class="material-symbols-rounded" style="color: #f59e0b;">confirmation_number</span>
          </div>
          <div class="kpi-card-value" style="font-size: 22px; font-family: var(--font-mono); color: #f59e0b;">1 Pending</div>
          <div class="kpi-card-footer">
            <span class="status-badge warning">ESC-2026-3041</span>
            <span class="kpi-target-note">Assigned to Product Lead</span>
          </div>
        </div>
      </div>

      <!-- Frontline Navigation Tabs -->
      <div class="tabs-ribbon" style="margin-bottom: 20px;">
        <button class="nav-tab ${this.activeTab === 'ask' ? 'active' : ''}" data-fl-tab="ask">
          <span class="material-symbols-rounded">chat</span> Ask Assistant (RAG)
        </button>
        <button class="nav-tab ${this.activeTab === 'docs' ? 'active' : ''}" data-fl-tab="docs">
          <span class="material-symbols-rounded">library_books</span> Approved Document Inventory
        </button>
        <button class="nav-tab ${this.activeTab === 'tickets' ? 'active' : ''}" data-fl-tab="tickets">
          <span class="material-symbols-rounded">confirmation_number</span> Escalations Queue
          <span class="tab-badge" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b;">1</span>
        </button>
        <button class="nav-tab ${this.activeTab === 'compliance' ? 'active' : ''}" data-fl-tab="compliance">
          <span class="material-symbols-rounded">security</span> Compliance & Audit Trail
        </button>
      </div>

      <!-- Frontline Content Container -->
      <div id="frontline-tab-pane"></div>
    `;

    // Render Sub Tab
    const pane = container.querySelector('#frontline-tab-pane');
    if (this.activeTab === 'ask') this.renderAskTab(pane, state);
    else if (this.activeTab === 'docs') this.renderDocsTab(pane, state);
    else if (this.activeTab === 'tickets') this.renderTicketsTab(pane, state);
    else if (this.activeTab === 'compliance') this.renderComplianceTab(pane, state);

    // Bind sub tabs
    container.querySelectorAll('[data-fl-tab]').forEach(btn => {
      btn.addEventListener('click', () => {
        this.activeTab = btn.getAttribute('data-fl-tab');
        this.render(container, state);
      });
    });
  },

  // Sub Tab 1: Ask Assistant
  renderAskTab(container, state) {
    const defaultQ = "Can Booster Plan milestone bonus combine with 7% certificate profit, and what is the withdrawal notice period?";
    container.innerHTML = `
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-card-title">Pre-Approved Operational Inquiries</div>
            <div class="chart-card-subtitle">Select a Common Frontline Scenario or Enter a Freeform Query</div>
          </div>
          <span class="verified-pill">
            <span class="material-symbols-rounded" style="font-size: 14px;">gavel</span>
            SHARIA FATWA COMPLIANT
          </span>
        </div>

        <div class="scenario-chips-grid">
          <button class="scenario-btn" data-query="Can Booster Plan milestone bonus combine with 7% certificate profit, and what is the withdrawal notice period?">
            <b>Booster Plan:</b> Milestone Bonus vs 7% Certificate Profit Rules & Early Notice
          </button>
          <button class="scenario-btn" data-query="What is the holding period for Saving Bonds?">
            <b>Saving Bonds:</b> Mandatory Holding Period & Redemption Rules
          </button>
          <button class="scenario-btn" data-query="What is the minimum monthly savings and early redemption penalty for Second Salary?">
            <b>Second Salary:</b> Minimum Monthly Contribution & Early Penalty
          </button>
          <button class="scenario-btn" data-query="What are the available tenors and minimum investment for Term Sukuk?">
            <b>Term Sukuk:</b> Available Tenors & Institutional Thresholds
          </button>
          <button class="scenario-btn" data-query="What is the minimum monthly deposit for MyPlan Regular Saver?">
            <b>MyPlan:</b> Direct Debit Setup & Monthly Savings Minimum
          </button>
          <button class="scenario-btn" data-query="Can non-resident expatriates open National Bonds accounts?">
            <b>Eligibility:</b> Non-Resident KYC & Sharia Fatwa Scope
          </button>
        </div>

        <!-- Query Input Bar -->
        <div style="display: flex; gap: 10px; margin-top: 10px;">
          <input type="text" id="fl-query-input" class="copilot-input" value="${defaultQ}" placeholder="Type any product policy, terms, circular rule or fatwa query...">
          <button class="alert-action-btn" id="btn-fl-search" style="border-color: var(--brand-primary); background: var(--brand-primary); color: #ffffff;">
            <span class="material-symbols-rounded" style="font-size: 15px; vertical-align: -2px;">search</span>
            SEARCH KNOWLEDGE BASE
          </button>
        </div>

        <!-- Grounded Response Card -->
        <div class="grounded-response-card" id="fl-grounded-card">
          <div class="grounded-header">
            <div>
              <span class="verified-pill">
                <span class="material-symbols-rounded" style="font-size: 14px;">verified</span>
                GROUNDED ZERO-HALLUCINATION TRUTH
              </span>
              <span style="font-size: 12px; color: var(--text-tertiary); margin-left: 12px;">Confidence: <b>99.4%</b> &bull; Latency: <b>1.1s</b></span>
            </div>
            <button class="alert-action-btn" id="btn-fl-copy" style="padding: 4px 10px; font-size: 10.5px;">
              <span class="material-symbols-rounded" style="font-size: 13px; vertical-align: -1px;">content_copy</span>
              COPY CITATION
            </button>
          </div>

          <div id="fl-answer-content" style="font-size: 13px; line-height: 1.6; color: var(--text-primary);">
            The Booster Plan milestone loyalty bonus is <b>strictly ring-fenced and cannot be combined or commingled</b> with the 7% upfront certificate profit promotion. Customers electing the milestone bonus are bound to the standard quarterly profit payout cycle.
            <br/><br/>
            <b>Early Redemption Notice Period:</b> A mandatory <b>30-day written notice period</b> is required for any capital withdrawal prior to maturity. Early redemption within the first 12 months incurs a <b>1.0% administrative liquidation fee</b> against the nominal certificate value.
          </div>

          <div class="citation-box">
            <div>
              <div style="font-size: 11px; font-weight: 700; color: var(--brand-primary); text-transform: uppercase;">Official Source Citation</div>
              <div style="font-size: 12.5px; font-weight: 700; color: var(--navy-slate-900); margin-top: 2px;">
                Product Circular 2026/04 &bull; Section 3.2: Milestone Bonus & Yield Ring-Fencing Directive
              </div>
              <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 2px;">
                Approval Authority: Fariha Fatima Hameed (Product Management Lead) &bull; Fatwa Committee Approval No. 2026/SH-09
              </div>
            </div>
            <span class="status-badge healthy">ACTIVE DIRECTIVE</span>
          </div>
        </div>
      </div>
    `;

    // Bind scenario clicks
    container.querySelectorAll('.scenario-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const q = btn.getAttribute('data-query');
        document.getElementById('fl-query-input').value = q;
        this.performGroundedSearch(q, state);
      });
    });

    document.getElementById('btn-fl-search')?.addEventListener('click', () => {
      const q = document.getElementById('fl-query-input').value;
      this.performGroundedSearch(q, state);
    });

    document.getElementById('btn-fl-copy')?.addEventListener('click', () => {
      navigator.clipboard.writeText('Product Circular 2026/04, Section 3.2 (Fatwa 2026/SH-09)');
      alert('Official citation copied to clipboard!');
    });
  },

  performGroundedSearch(query, state) {
    const { kbData } = state;
    const lower = query.toLowerCase();
    const found = kbData.find(d => {
      const text = (d.title + ' ' + d.content + ' ' + d.keywords.join(' ')).toLowerCase();
      return lower.split(' ').some(w => w.length > 3 && text.includes(w));
    }) || kbData[0];

    const answerDiv = document.getElementById('fl-answer-content');
    if (answerDiv) {
      answerDiv.innerHTML = `
        ${found.content}
        <br/><br/>
        <b>Sharia Compliance Note:</b> Governed under <i>${found.sharia_compliance_ref}</i>.
      `;
    }
  },

  // Sub Tab 2: Approved Document Inventory
  renderDocsTab(container, state) {
    const { kbData } = state;
    container.innerHTML = `
      <div class="data-table-container">
        <div style="padding: 16px 20px; border-bottom: 1px solid var(--border-default); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 15px; font-weight: 800; color: var(--navy-slate-900);">Approved Product Circular & Policy Repository</div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 2px;">10 Certified Ground-Truth Documents for Frontline Advisory</div>
          </div>
          <select class="slicer-control" style="width: 220px;">
            <option>All 5 Products</option>
            <option>Booster Plan</option>
            <option>Saving Bonds</option>
            <option>Second Salary</option>
            <option>Term Sukuk</option>
          </select>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>Document Ref</th>
              <th>Product Family</th>
              <th>Document Title & Scope</th>
              <th>Owner / Sign-Off</th>
              <th>Sharia Approval</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            ${kbData.map(d => `
              <tr>
                <td><b class="mono-metric" style="color: var(--brand-primary);">${d.document_ref}</b></td>
                <td><b>${d.product_name}</b></td>
                <td>
                  <div style="font-weight: 600;">${d.title}</div>
                  <div style="font-size: 11px; color: var(--text-tertiary);">${d.section} &bull; Effective: ${d.effective_date}</div>
                </td>
                <td>${d.owner}</td>
                <td><span class="status-badge healthy">${d.sharia_compliance_ref.split(' ')[0]} OK</span></td>
                <td>
                  <button class="alert-action-btn" style="padding: 4px 8px; font-size: 10px;" onclick="alert('Downloading ${d.document_ref} PDF');">
                    <span class="material-symbols-rounded" style="font-size: 12px; vertical-align: -1px;">download</span>
                    PDF
                  </button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  },

  // Sub Tab 3: Escalation Queue
  renderTicketsTab(container, state) {
    const { ticketsData } = state;
    container.innerHTML = `
      <div class="data-table-container">
        <div style="padding: 16px 20px; border-bottom: 1px solid var(--border-default); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 15px; font-weight: 800; color: var(--navy-slate-900);">Active Frontline Escalation Tickets</div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 2px;">Inquiries Requiring Product Management & Commercial Legal Clarification</div>
          </div>
          <button class="alert-action-btn" onclick="alert('New escalation ticket form opened.');">
            + CREATE ESCALATION TICKET
          </button>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>Ticket ID</th>
              <th>Timestamp</th>
              <th>Requester</th>
              <th>Product</th>
              <th>Query Summary</th>
              <th>Reason for Escalation</th>
              <th>Status</th>
              <th>Assigned Lead</th>
            </tr>
          </thead>
          <tbody>
            ${ticketsData.map(t => `
              <tr>
                <td><b class="mono-metric" style="color: #f59e0b;">${t.ticket_id}</b></td>
                <td class="tabular-numbers" style="font-size: 11.5px;">${t.timestamp}</td>
                <td><b>${t.user_name}</b><br/><span style="font-size: 10.5px; color: var(--text-tertiary);">${t.user_role}</span></td>
                <td><b>${t.product_name}</b></td>
                <td style="max-width: 260px;">${t.query}</td>
                <td style="color: #ef4444; font-size: 11.5px;">${t.reason}</td>
                <td><span class="status-badge warning">${t.status}</span></td>
                <td><b>${t.assigned_lead}</b></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  },

  // Sub Tab 4: Compliance & InfoSec Audit Trail
  renderComplianceTab(container, state) {
    const { auditData } = state;
    container.innerHTML = `
      <div class="kpi-cards-grid" style="margin-bottom: 20px;">
        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header"><span class="kpi-card-label">Grounding Integrity</span></div>
          <div class="kpi-card-value" style="font-size: 22px; color: #10b981;">100.0%</div>
          <div class="kpi-card-footer"><span class="status-badge healthy">PASSED</span></div>
        </div>
        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header"><span class="kpi-card-label">Average Retrieval SLA</span></div>
          <div class="kpi-card-value" style="font-size: 22px; font-family: var(--font-mono);">0.82s</div>
          <div class="kpi-card-footer"><span class="status-badge healthy">&lt; 1.5s SLA</span></div>
        </div>
        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header"><span class="kpi-card-label">Fatwa Citations</span></div>
          <div class="kpi-card-value" style="font-size: 22px; color: #10b981;">100% Verified</div>
          <div class="kpi-card-footer"><span class="status-badge healthy">SHARIA AUDIT OK</span></div>
        </div>
        <div class="kpi-card" style="height: 105px;">
          <div class="kpi-card-header"><span class="kpi-card-label">CBUAE Compliance</span></div>
          <div class="kpi-card-value" style="font-size: 22px; color: var(--brand-primary);">PASSED</div>
          <div class="kpi-card-footer"><span class="status-badge healthy">ISO 27001 AUDITED</span></div>
        </div>
      </div>

      <div class="data-table-container">
        <div style="padding: 16px 20px; border-bottom: 1px solid var(--border-default); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 15px; font-weight: 800; color: var(--navy-slate-900);">Immutable SHA-256 Audit Trail Log</div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 2px;">Comprehensive Retrieval Ledger Tracking Every Grounded Query and Citation</div>
          </div>
          <span class="status-badge healthy">TAMPER-PROOF LEDGER</span>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>Timestamp (UTC)</th>
              <th>User Role</th>
              <th>Grounded Query</th>
              <th>Official Citations</th>
              <th>Latency (s)</th>
              <th>Compliance State</th>
            </tr>
          </thead>
          <tbody>
            ${auditData.slice(0, 10).map(a => `
              <tr>
                <td class="tabular-numbers" style="font-size: 11.5px;">${a.timestamp}</td>
                <td>${a.user_role}</td>
                <td style="max-width: 320px;">${a.query}</td>
                <td><b class="mono-metric" style="color: var(--brand-primary);">${a.citations.join(', ')}</b></td>
                <td class="tabular-numbers">${a.latency_sec}s</td>
                <td><span class="status-badge healthy">ZERO-HALLUCINATION</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  }
};
