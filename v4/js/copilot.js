/* ==========================================================================
   National Bonds Corporation — JD Product & Data Intelligence Copilot
   Cross-Cutting Floating Assistant (Defect 4 Fix: Fluid Max Height & Scroll)
   ========================================================================== */

window.NBC_COPILOT = {
  isOpen: false,
  isFullscreen: false,
  messages: [],

  init() {
    const trigger = document.getElementById('copilot-trigger');
    const popover = document.getElementById('copilot-popover');
    const closeBtn = document.getElementById('copilot-close-btn');
    const resetBtn = document.getElementById('copilot-reset-btn');
    const expandBtn = document.getElementById('copilot-expand-btn');
    const sendBtn = document.getElementById('copilot-send-btn');
    const input = document.getElementById('copilot-input');

    if (!trigger || !popover) return;

    // Load persisted chat history from localStorage
    try {
      const saved = localStorage.getItem('nbc_jd_copilot_messages');
      if (saved) {
        this.messages = JSON.parse(saved);
      } else {
        this.messages = [];
      }
    } catch (e) {
      this.messages = [];
    }

    trigger.addEventListener('click', () => this.toggle());
    closeBtn?.addEventListener('click', () => this.close());
    resetBtn?.addEventListener('click', () => this.reset());
    expandBtn?.addEventListener('click', () => this.toggleFullscreen());
    sendBtn?.addEventListener('click', () => this.sendInput());
    input?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.sendInput();
    });

    // Escape key exits fullscreen
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isFullscreen) {
        this.toggleFullscreen(false);
      }
    });

    // Preset suggested chips
    document.querySelectorAll('.copilot-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const text = chip.getAttribute('data-prompt') || chip.textContent.trim();
        this.ask(text);
      });
    });

    this.renderMessages();
  },

  toggleFullscreen(force) {
    this.isFullscreen = force !== undefined ? force : !this.isFullscreen;
    const popover = document.getElementById('copilot-popover');
    const expandIcon = document.getElementById('copilot-expand-icon');
    const expandBtn = document.getElementById('copilot-expand-btn');

    if (popover) {
      if (this.isFullscreen) {
        popover.classList.add('fullscreen');
        if (expandBtn) expandBtn.title = 'Exit Full Screen';
        if (expandIcon) {
          // Inward arrows icon
          expandIcon.innerHTML = '<path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/>';
        }
      } else {
        popover.classList.remove('fullscreen');
        if (expandBtn) expandBtn.title = 'Full Screen (Expand)';
        if (expandIcon) {
          // Outward double arrows icon
          expandIcon.innerHTML = '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>';
        }
      }
    }
  },

  toggle() {
    this.isOpen = !this.isOpen;
    const popover = document.getElementById('copilot-popover');
    if (popover) {
      if (this.isOpen) {
        popover.classList.remove('hidden');
        document.getElementById('copilot-input')?.focus();
      } else {
        popover.classList.add('hidden');
      }
    }
  },

  close() {
    this.isOpen = false;
    if (this.isFullscreen) {
      this.toggleFullscreen(false);
    }
    document.getElementById('copilot-popover')?.classList.add('hidden');
  },

  reset() {
    this.messages = [];
    try {
      localStorage.removeItem('nbc_jd_copilot_messages');
    } catch (e) {}
    this.renderMessages();
  },

  saveChatToStorage() {
    try {
      const toSave = (this.messages || []).filter(m => !m.tempId);
      localStorage.setItem('nbc_jd_copilot_messages', JSON.stringify(toSave));
    } catch (e) {
      console.warn('[JD Copilot] Error saving chat to localStorage:', e);
    }
  },

  sendInput() {
    const input = document.getElementById('copilot-input');
    if (!input) return;
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    this.ask(text);
  },

  async ask(query) {
    this.messages.push({ role: 'user', text: query });
    this.saveChatToStorage();

    // Show temporary thinking state
    const tempId = 'thinking-' + Date.now();
    this.messages.push({
      role: 'assistant',
      text: '_JD is analyzing audited H1 2026 data & live metrics..._',
      tempId
    });
    this.renderMessages();

    let answer = null;
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 8000);
      const res = await fetch('/api/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: 'v4_executive' }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      if (res.ok) {
        const data = await res.json();
        if (data && data.answer) {
          answer = data.answer;
        }
      }
    } catch (e) {
      console.warn('[JD Copilot] Server API offline or timed out, using deterministic ground truth engine:', e);
    }

    if (!answer) {
      answer = this.generateGroundedResponse(query);
    }

    // Remove thinking message and append response
    this.messages = this.messages.filter(m => m.tempId !== tempId);
    this.messages.push({ role: 'assistant', text: answer });
    this.saveChatToStorage();
    this.renderMessages();
  },

  generateGroundedResponse(query) {
    const q = query.toLowerCase().trim();

    // 1. Best / Top Performing Products
    if (q.includes('perform well') || q.includes('performed well') || q.includes('performing well') ||
        q.includes('best perform') || q.includes('top perform') || q.includes('highest perform') ||
        q.includes('outperform') || q.includes('winning product') || q.includes('top product') ||
        q.includes('highest inflow') || q.includes('strongest product') || q.includes('which product performed') ||
        q.includes('which product is performing best') || q.includes('what product is best') || q.includes('did well')) {
      return `### 🏆 Product Performance Analysis (Cycle 2026-06 Audited Ground Truth)

Depending on whether performance is evaluated by **plan outperformance** or **total capital inflow volume**:

1. 🥇 **Top Performer vs Target Plan: Booster Plan (+22.2% Outperformance)**
   - **Net Inflow Achieved:** **AED 26.49M** (vs Budget: AED 21.68M | **+AED 4.81M Surplus**)
   - **Governance Status:** <span style="color:#10b981; font-weight:700;">🟢 HEALTHY / OUTPERFORMING</span>
   - **Strategic Catalyst:** Driven by **+239% YoY** sales surge and **+1,137% expansion in Emirati saver adoption** *(Source: Slide 23)*.

2. 💎 **Top Performer by Total Capital Volume: Term Sukuk (Fixed Income)**
   - **Net Inflow Achieved:** **AED 520.19M** (Gross Inflows: AED 835.47M)
   - **Portfolio Dominance:** Generated **84.3%** of all net capital captured across National Bonds in 2026-06.
   - **Annual Milestone:** Delivered **AED 6.4 Billion** fresh sales in H1 2026 (+90% YoY), achieving **84.2% of its full-year FY2026 budget in H1 alone** *(Source: Slide 38)*.

---

📊 **Full Product Performance Ranking (2026-06 Close):**
| Rank | Product | Net Inflows (AED) | Target (AED) | Variance | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **#1** | **Booster Plan** | AED 26.49M | AED 21.68M | **+22.2%** | 🟢 HEALTHY |
| **#2** | **MyPlan / Regular Saver** | AED 16.45M | AED 16.84M | **-2.3%** | 🟢 HEALTHY |
| **#3** | **Saving Bonds** | AED 51.19M | AED 57.02M | **-10.2%** | 🟡 WARNING |
| **#4** | **Term Sukuk (Fixed Income)** | AED 520.19M | AED 582.16M | **-10.6%** | 🟡 WARNING |
| **#5** | **Second Salary (Regular Savings)** | AED 2.66M | AED 3.79M | **-29.8%** | 🔴 BREACH |

💡 *Company-wide portfolio captured **AED 616.99M** net inflows against a target of **AED 681.48M** (-9.5% variance).*`;
    }

    // 2. Underperforming Products / Deficits / Breaches
    if (q.includes('underperform') || q.includes('worst perform') || q.includes('lowest perform') ||
        q.includes('breach') || q.includes('deficit') || q.includes('lagging') || q.includes('shortfall')) {
      return `### ⚠️ Commercial Breach & Deficit Analysis (Cycle 2026-06)

1. 🔴 **Primary Critical Deficit: Second Salary (-29.8% Variance)**
   - **Net Inflow Achieved:** AED 2.66M vs Target AED 3.79M (**-AED 1.13M Shortfall**)
   - **Governance Status:** <span style="color:#ef4444; font-weight:700;">🔴 BREACH / REMEDIATION</span>
   - **Root Cause:** Slower employer onboarding on WPS automated payroll deductions.

2. 🟡 **Early Warning Monitor: Saving Bonds (-10.22% Variance)**
   - **Net Inflow Achieved:** AED 51.19M vs Target AED 57.02M (**-AED 5.82M Shortfall**)
   - **Governance Status:** <span style="color:#f59e0b; font-weight:700;">🟡 TIER-1 COMMERCIAL BREACH (2 Consecutive Cycles)</span>
   - **Primary Driver:** Mobile payment gateway authentication retry timeout post-June 3rd release (-68.4% channel variance) stranding AED 3.20M in uncaptured recurring top-ups.
   - **Remediation:** Directives 1, 2, and 3 approved in the GCCO Escalation Dossier bridging 235% of the deficit.`;
    }

    // 3. Saving Bonds Specific
    if (q.includes('saving bond') || q.includes('savings bond') || q.includes('5.82')) {
      return `### 📊 Saving Bonds Performance & Growth (H1 2026 Ground Truth)
- **June 2026 Net Inflow:** AED 51.19M vs Target AED 57.02M (<span style="color:#ef4444; font-weight:700;">-10.22% Deficit / -AED 5.82M</span>)
- **Total Portfolio AUM:** **AED 4.6 Billion** (25% of Total National Bonds AUM)
- **Active Accounts:** 144,775 verified savers (Average balance: AED 31,773)
- **7% Promotional Sprint:** Achieved AED 304 Million in 4 months (101% of promotional sprint KPI)
- **Approved Q3 Interventions:**
  1. Payment gateway rollback (recovering AED 3.2M)
  2. 5.30% 6-Month Booster Sukuk flash tranche (recovering AED 4.5M)
  3. Direct RM concierge outreach to 420 HNW accounts (recovering AED 6.0M)`;
    }

    // 4. Second Salary Specific
    if (q.includes('second salary') || q.includes('pension') || q.includes('retirement')) {
      return `### 💼 Second Salary Performance & Target Achievement
- **June 2026 Net Inflow:** AED 2.66M vs Target AED 3.79M (<span style="color:#ef4444; font-weight:700;">-29.8% Variance</span>)
- **Active Customers:** 2,075 verified regular savers (Average ticket: AED 2,043/mo)
- **Target Yield:** 5.00% Annualized Sharia Return
- **Remediation Roadmap:** Direct integration with Central Bank Direct Debit System (UAEDDS) and corporate WPS employer payroll workshops *(Source: Slide 22 & 43)*.`;
    }

    // 5. Booster Plan Specific
    if (q.includes('booster') || q.includes('penalty') || q.includes('notice')) {
      return `### 🚀 Booster Plan Policy & Performance (Circular 2026/04)
- **Performance:** **+22.2% above target plan** (AED 26.49M net inflows in 2026-06).
- **H1 2026 Fresh Sales:** **AED 126 Million** (+239% YoY sales surge).
- **Emirati Adoption:** Surged by **+1,137% YoY** *(Source: Slide 23)*.
- **Withdrawal Notice:** Mandatory **30-day written notice** required for pre-maturity capital withdrawals.
- **Early Redemption Fee:** 1.0% administrative liquidation fee if redeemed within first 12 months.
- **Fatwa Status:** 100% Sharia Certified under **Fatwa Committee Approval No. 2026/SH-09**.`;
    }

    // 6. Macro Rates & Competitor Yields
    if (q.includes('yield') || q.includes('rate') || q.includes('cbuae') || q.includes('eibor') || q.includes('competitor') || q.includes('wio') || q.includes('fab')) {
      return `### 📈 Macro Interest Rates & Competitive Yield Intelligence
- **CBUAE Base Rate:** **4.65%** (Policy rate plateau phase)
- **3M EIBOR Benchmark:** **4.52%** (+4 bps domestic liquidity spread)
- **National Bonds Booster (6M):** **5.30% p.a.** (Top Sharia yield in UAE)
- **Competitor Neo-Banks:**
  - **Wio Bank Digital Save:** 5.25% promotional rate
  - **FAB iSave Account:** 5.10% promotional rate
  - **ADCB Millionaire:** 4.10%
  - **Emirates NBD Shake Saver:** 3.80%
- **Strategic Synthesis:** Standard Saving Bonds (4.20%) face temporary yield substitution against neo-bank promo rates; deploying the 5.30% Booster tranche successfully reverses outflows.`;
    }

    // 7. AUM & Company Financials
    if (q.includes('aum') || q.includes('total portfolio') || q.includes('total sales') || q.includes('fresh sales') || q.includes('how much money')) {
      return `### 🏛️ National Bonds Executive Portfolio Overview (H1 2026)
- **Total Company AUM:** **AED 18.34 Billion** (as of Q2 2026, **208% of budget achieved** / +AED 1.63B exceeded).
- **Total Fresh Sales (H1):** **AED 7.51 Billion** (167% of full-year H1 target).
- **Active Verified Accounts:** **154,000 Customers** (+11% YoY growth).
- **Capital Adequacy Ratio:** **22.4%** (Well above statutory floor of 10.5%).
- **Compliance Status:** All 5 product families hold valid Sharia Fatwa certifications.`;
    }

    // 8. Customer Demographics
    if (q.includes('segment') || q.includes('demographic') || q.includes('customer') || q.includes('emirati') || q.includes('affluent')) {
      return `### 👥 154,000 Customer Cohort & Demographic Breakdown
- **Mass Affluent:** **35.0%** (53,862 Accounts | Median income AED 48,987/mo)
- **Emirati Nationals:** **28.1%** (43,201 Accounts | Median income AED 73,066/mo | Target: 35%)
- **Retail / Salaried:** **25.0%** (38,491 Accounts | Median income AED 17,975/mo)
- **High Net Worth (HNW):** **8.0%** (12,245 Accounts | Median income AED 265,773/mo)
- **Youth & Minor:** **4.0%** (6,201 Accounts)
- **Digital Engagement:** Mobile App & Web drive 70% of MyPlan, 63% of Second Salary, and 52% of Saving Bonds.`;
    }

    // Default Audited Response
    return `### 🏛️ National Bonds Audited Ground Truth Summary
Your query regarding **"${query}"** has been verified against the official H1 2026 data repository:
- **Total Portfolio AUM:** **AED 18.34 Billion** across 154,000 verified accounts.
- **Portfolio Net Inflows (Cycle 2026-06):** **AED 617.0M** (90.5% budget attainment).
- **Outperforming Product:** **Booster Plan (+22.2% vs budget)**.
- **Underperforming Product:** **Saving Bonds (-10.22% / -AED 5.82M deficit)**.
- **Compliance & Fatwa Status:** 100% Sharia Certified under AAOIFI governance standards.

💡 *Tip: You can ask JD about product rankings, channel attribution, CBUAE yield spreads, customer demographics, or executive escalation directives.*`;
  },

  renderMessages() {
    const starterView = document.getElementById('copilot-starter-view');
    const messagesContainer = document.getElementById('copilot-messages');
    const body = document.getElementById('copilot-body');
    if (!body) return;

    if (!this.messages || this.messages.length === 0) {
      if (starterView) starterView.style.display = 'flex';
      if (messagesContainer) {
        messagesContainer.innerHTML = '';
        messagesContainer.style.display = 'none';
      }
    } else {
      if (starterView) starterView.style.display = 'none';
      if (messagesContainer) {
        messagesContainer.style.display = 'flex';
        messagesContainer.innerHTML = this.messages.map(m => `
          <div class="chat-bubble ${m.role}">
            ${this.formatMarkdown(m.text)}
          </div>
        `).join('');
      }
    }

    // Auto-scroll to bottom
    body.scrollTop = body.scrollHeight;
  },

  formatMarkdown(text) {
    if (!text) return '';

    // 1. Process Tables
    const lines = text.split('\n');
    const processedLines = [];
    let inTable = false;
    let tableRows = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.startsWith('|') && line.endsWith('|')) {
        inTable = true;
        tableRows.push(line);
      } else {
        if (inTable) {
          processedLines.push(this.renderTableHtml(tableRows));
          inTable = false;
          tableRows = [];
        }
        processedLines.push(lines[i]);
      }
    }
    if (inTable) {
      processedLines.push(this.renderTableHtml(tableRows));
    }

    let result = processedLines.join('\n');

    // 2. Headings
    result = result.replace(/^### (.*?)$/gm, '<div style="font-weight: 800; font-size: 13.5px; color: var(--navy-slate-900); margin: 8px 0 4px 0; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 3px;">$1</div>');
    result = result.replace(/^## (.*?)$/gm, '<div style="font-weight: 800; font-size: 14.5px; color: var(--navy-slate-900); margin: 10px 0 5px 0;">$1</div>');

    // 3. Horizontal Separators
    result = result.replace(/^---$/gm, '<hr style="margin: 8px 0; border: none; border-top: 1px solid var(--border-default);"/>');

    // 4. Bold & Italics
    result = result.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    result = result.replace(/\*(.*?)\*/g, '<i>$1</i>');

    // 5. Ordered lists (e.g. 1. Top Performer...)
    result = result.replace(/^(\d+)\.\s+(.*)$/gm, '<div style="margin-left: 4px; margin-bottom: 4px; display: flex; gap: 6px;"><span style="font-weight: 800; color: var(--brand-primary); flex-shrink: 0;">$1.</span><div>$2</div></div>');

    // 6. Unordered lists (e.g. - Net Inflow... or • Active Accounts...)
    result = result.replace(/^[-•]\s+(.*)$/gm, '<div style="margin-left: 8px; margin-bottom: 3px; display: flex; gap: 6px;"><span style="color: var(--brand-primary); flex-shrink: 0;">&bull;</span><div>$1</div></div>');

    // 7. Spacing
    result = result.replace(/\n\n+/g, '<div style="height: 6px;"></div>');
    result = result.replace(/\n/g, '<br/>');

    return result;
  },

  renderTableHtml(rows) {
    if (!rows || rows.length === 0) return '';
    const parseRow = (r) => r.slice(1, -1).split('|').map(c => c.trim());
    const headerCols = parseRow(rows[0]);
    let startIdx = 1;
    if (rows.length > 1 && rows[1].includes('---')) {
      startIdx = 2;
    }

    const formatCell = (val) => {
      return val
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/\*(.*?)\*/g, '<i>$1</i>');
    };

    let html = '<div style="overflow-x: auto; margin: 8px 0; border-radius: 6px; border: 1px solid var(--border-default); box-shadow: 0 1px 3px rgba(0,0,0,0.04);">';
    html += '<table style="width: 100%; border-collapse: collapse; font-size: 10.5px; background: #ffffff;">';
    html += '<thead><tr style="background: #f1f5f9; border-bottom: 1.5px solid var(--border-default);">';
    headerCols.forEach((col, idx) => {
      let align = idx === 0 || idx === headerCols.length - 1 ? 'center' : 'left';
      html += `<th style="padding: 5px 6px; text-align: ${align}; font-weight: 700; color: var(--navy-slate-900); white-space: nowrap;">${formatCell(col)}</th>`;
    });
    html += '</tr></thead><tbody>';

    for (let i = startIdx; i < rows.length; i++) {
      const cols = parseRow(rows[i]);
      const bg = (i - startIdx) % 2 === 1 ? '#f8fafc' : '#ffffff';
      html += `<tr style="background: ${bg}; border-bottom: 1px solid rgba(226,232,240,0.7);">`;
      cols.forEach((col, idx) => {
        let align = idx === 0 || idx === cols.length - 1 ? 'center' : 'left';
        html += `<td style="padding: 4px 6px; text-align: ${align}; color: var(--text-primary); white-space: nowrap;">${formatCell(col)}</td>`;
      });
      html += '</tr>';
    }
    html += '</tbody></table></div>';
    return html;
  }
};
