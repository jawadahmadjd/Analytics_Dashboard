/* ==========================================================================
   National Bonds Corporation — Master Application Controller (V4)
   Zero-Streamlit Modern Web App
   Document Reference: NBC-DESKTOP-UI-AUDIT-2026-V1
   ========================================================================== */

window.NBC_APP = {
  state: {
    mode: 'executive',          // 'executive' or 'frontline'
    activeExecTab: 'workflow',   // workflow, portfolio, diagnostic, report, gcco
    selectedCycle: '2026-06',
    selectedProduct: 'Saving Bonds',
    warningThreshold: -8.0,
    breachThreshold: -15.0,
    kpiRecords: [],
    marketData: [],
    kbData: [],
    ticketsData: [],
    dispatchData: [],
    auditData: [],
    demographics: {},
    reviewedAlerts: new Set()
  },

  init() {
    // Load Ground Truth Data from data.js or window.NBC_DATA
    if (window.NBC_DATA) {
      this.state.kpiRecords = window.NBC_DATA.kpi_records;
      this.state.marketData = window.NBC_DATA.market_data;
      this.state.kbData = window.NBC_DATA.kb_data;
      this.state.ticketsData = window.NBC_DATA.tickets_data;
      this.state.dispatchData = window.NBC_DATA.dispatch_data;
      this.state.auditData = window.NBC_DATA.audit_data;
      this.state.demographics = window.NBC_DATA.demographics;
    }

    this.bindSidebarEvents();
    this.bindNavigationTabs();
    this.bindInlineFilters();
    this.bindNotificationCenter();
    this.updateOverviewHeader();
    this.renderCurrentView();

    // Initialize JD Copilot
    if (window.NBC_COPILOT) {
      window.NBC_COPILOT.init();
    }
  },

  bindSidebarEvents() {
    // Mode Switcher: Executive Cockpit vs Frontline Portal
    const btnExec = document.getElementById('btn-mode-executive');
    const btnFrontline = document.getElementById('btn-mode-frontline');

    btnExec?.addEventListener('click', () => {
      this.state.mode = 'executive';
      btnExec.classList.add('active');
      btnFrontline?.classList.remove('active');
      const cmdBar = document.getElementById('exec-command-bar');
      if (cmdBar) cmdBar.style.display = 'flex';
      this.updateOverviewHeader();
      this.renderCurrentView();
    });

    btnFrontline?.addEventListener('click', () => {
      this.state.mode = 'frontline';
      btnFrontline.classList.add('active');
      btnExec?.classList.remove('active');
      const cmdBar = document.getElementById('exec-command-bar');
      if (cmdBar) cmdBar.style.display = 'none';
      this.updateOverviewHeader();
      this.renderCurrentView();
    });

    // Product selector in sidebar
    const productSelect = document.getElementById('sidebar-product-select');
    productSelect?.addEventListener('change', (e) => {
      this.state.selectedProduct = e.target.value;
      const topProd = document.getElementById('filter-product-select');
      if (topProd) topProd.value = e.target.value;
      this.updateProductCard();
      if (this.state.mode === 'executive') {
        this.renderCurrentView();
      }
    });

    // Cycle selector / slider in sidebar
    const cycleSlider = document.getElementById('sidebar-cycle-slider');
    const cycleBadge = document.getElementById('sidebar-cycle-badge');
    const months = [...new Set(this.state.kpiRecords.map(r => r.month))].sort();

    if (cycleSlider && months.length > 0) {
      cycleSlider.max = months.length - 1;
      cycleSlider.value = months.indexOf(this.state.selectedCycle);

      cycleSlider.addEventListener('input', (e) => {
        const idx = +e.target.value;
        const chosen = months[idx] || '2026-06';
        this.state.selectedCycle = chosen;
        if (cycleBadge) cycleBadge.textContent = chosen;
        const topCycle = document.getElementById('filter-cycle-select');
        if (topCycle) topCycle.value = chosen;
        this.updateOverviewHeader();
        this.renderCurrentView();
      });
    }

    // Threshold range
    const threshRange = document.getElementById('sidebar-thresh-range');
    const threshBadge = document.getElementById('sidebar-thresh-badge');
    threshRange?.addEventListener('input', (e) => {
      this.state.warningThreshold = +e.target.value;
      if (threshBadge) threshBadge.textContent = `${this.state.warningThreshold}%`;
      this.updateOverviewHeader();
    });

    // Sidebar Executive Reports: Memo & GCCO Briefing
    const navMemo = document.getElementById('sidebar-nav-memo');
    const navGcco = document.getElementById('sidebar-nav-gcco');

    navMemo?.addEventListener('click', () => {
      document.querySelectorAll('[data-exec-tab]').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('[data-exec-report]').forEach(b => b.classList.remove('active'));
      navMemo.classList.add('active');
      this.state.activeExecTab = 'report';
      this.renderCurrentView();
    });

    navGcco?.addEventListener('click', () => {
      document.querySelectorAll('[data-exec-tab]').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('[data-exec-report]').forEach(b => b.classList.remove('active'));
      navGcco.classList.add('active');
      this.state.activeExecTab = 'gcco';
      this.renderCurrentView();
    });
  },

  bindNavigationTabs() {
    document.querySelectorAll('[data-exec-tab]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-exec-tab]').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('[data-exec-report]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.activeExecTab = btn.getAttribute('data-exec-tab');
        this.renderCurrentView();
      });
    });
  },

  bindInlineFilters() {
    // Top Inline Cycle Filter
    const filterCycle = document.getElementById('filter-cycle-select');
    const months = [...new Set(this.state.kpiRecords.map(r => r.month))].sort();

    if (filterCycle && months.length > 0) {
      filterCycle.innerHTML = months.slice().reverse().map(m => `
        <option value="${m}" ${m === this.state.selectedCycle ? 'selected' : ''}>${m}</option>
      `).join('');

      filterCycle.addEventListener('change', (e) => {
        this.state.selectedCycle = e.target.value;
        const cycleBadge = document.getElementById('sidebar-cycle-badge');
        const cycleSlider = document.getElementById('sidebar-cycle-slider');
        if (cycleBadge) cycleBadge.textContent = this.state.selectedCycle;
        if (cycleSlider) cycleSlider.value = months.indexOf(this.state.selectedCycle);
        this.updateOverviewHeader();
        this.renderCurrentView();
      });
    }

    // Top Inline Product Filter
    const filterProduct = document.getElementById('filter-product-select');
    filterProduct?.addEventListener('change', (e) => {
      const val = e.target.value;
      if (val !== 'All Products') {
        this.state.selectedProduct = val;
        const sideProd = document.getElementById('sidebar-product-select');
        if (sideProd) sideProd.value = val;
        this.updateProductCard();
      }
      this.renderCurrentView();
    });

    // Tier & Channel Filter triggers
    const filterTier = document.getElementById('filter-tier-select');
    filterTier?.addEventListener('change', () => {
      if (this.state.activeExecTab === 'diagnostic') {
        this.renderCurrentView();
      }
    });

    const filterChannel = document.getElementById('filter-channel-select');
    filterChannel?.addEventListener('change', () => {
      if (this.state.activeExecTab === 'diagnostic') {
        this.renderCurrentView();
      }
    });
  },

  bindNotificationCenter() {
    const btnNotif = document.getElementById('notification-btn');
    const popover = document.getElementById('notification-popover');
    const btnClose = document.getElementById('notif-close-btn');

    // Toggle popover on bell click
    btnNotif?.addEventListener('click', (e) => {
      e.stopPropagation();
      popover?.classList.toggle('hidden');
    });

    // Close button inside popover header
    btnClose?.addEventListener('click', (e) => {
      e.stopPropagation();
      popover?.classList.add('hidden');
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (popover && !popover.classList.contains('hidden') && !popover.contains(e.target) && e.target !== btnNotif) {
        popover.classList.add('hidden');
      }
    });

    // Delegate clicks inside alert popover
    const notifList = document.getElementById('notif-popover-list');
    notifList?.addEventListener('click', (e) => {
      // 1. Check if user clicked "Mark as Reviewed" button
      const reviewBtn = e.target.closest('[data-review-product]');
      if (reviewBtn) {
        e.stopPropagation();
        const prod = reviewBtn.getAttribute('data-review-product');
        if (this.state.reviewedAlerts.has(prod)) {
          this.state.reviewedAlerts.delete(prod);
        } else {
          this.state.reviewedAlerts.add(prod);
        }
        this.updateOverviewHeader();
        return;
      }

      // 2. Check if user clicked the alert card itself -> Navigate to Six Step Workflow for this product
      const card = e.target.closest('.notif-item');
      if (card) {
        const prod = card.getAttribute('data-product');
        if (prod) {
          this.state.selectedProduct = prod;
          const topProd = document.getElementById('filter-product-select');
          if (topProd) topProd.value = prod;
          const sideProd = document.getElementById('sidebar-product-select');
          if (sideProd) sideProd.value = prod;
          this.updateProductCard();

          // Switch to Six Step Workflow
          document.querySelector('[data-exec-tab=workflow]')?.click();

          // Close popover
          popover?.classList.add('hidden');
        }
      }
    });
  },

  updateOverviewHeader() {
    const { kpiRecords, selectedCycle, selectedProduct } = this.state;
    const cycleKpis = kpiRecords.filter(r => r.month === selectedCycle);

    // Calculate aggregations
    const gross = cycleKpis.reduce((acc, r) => acc + r.gross_inflows_aed, 0) / 1e6;
    const red = cycleKpis.reduce((acc, r) => acc + r.redemptions_aed, 0) / 1e6;
    const net = cycleKpis.reduce((acc, r) => acc + r.net_inflows_aed, 0) / 1e6;
    const target = cycleKpis.reduce((acc, r) => acc + r.target_inflows_aed, 0) / 1e6;
    const variancePct = target > 0 ? ((net - target) / target) * 100 : 0;
    const savers = cycleKpis.reduce((acc, r) => acc + r.active_customers, 0);

    // 1. Update Slim Horizontal Header Strip
    const statAum = document.getElementById('hdr-stat-aum');
    const statNet = document.getElementById('hdr-stat-net');
    const statNetBadge = document.getElementById('hdr-stat-net-badge');
    const statSavers = document.getElementById('hdr-stat-savers');

    if (statAum) statAum.textContent = 'AED 18.34B';
    if (statNet) statNet.textContent = `AED ${net.toFixed(1)}M`;
    if (statNetBadge) {
      statNetBadge.textContent = `${variancePct > 0 ? '+' : ''}${variancePct.toFixed(1)}% vs Target`;
      statNetBadge.className = `stat-badge ${variancePct >= 0 ? 'positive' : variancePct > -10 ? 'warning' : 'negative'}`;
    }
    if (statSavers) {
      statSavers.textContent = savers > 0 ? `${(savers / 1000).toFixed(1)}K` : '154.2K';
    }

    // 2. Populate Notification Center Drawer & Badge
    const breaches = cycleKpis.filter(r => r.deviation_pct <= this.state.breachThreshold);
    const warnings = cycleKpis.filter(r => r.deviation_pct > this.state.breachThreshold && r.deviation_pct <= this.state.warningThreshold);
    const allAlerts = [...breaches, ...warnings];
    const unreviewedAlerts = allAlerts.filter(r => !this.state.reviewedAlerts.has(r.product_name));
    const unreviewedCount = unreviewedAlerts.length;

    const notifBadge = document.getElementById('notification-badge');
    if (notifBadge) {
      notifBadge.textContent = unreviewedCount;
      if (unreviewedCount === 0) {
        notifBadge.style.backgroundColor = '#10b981';
      } else if (unreviewedAlerts.some(r => r.deviation_pct <= this.state.breachThreshold)) {
        notifBadge.style.backgroundColor = '#ef4444';
      } else {
        notifBadge.style.backgroundColor = '#f59e0b';
      }
    }

    const notifCycle = document.getElementById('notif-popover-cycle');
    if (notifCycle) notifCycle.textContent = `Cycle ${selectedCycle}`;

    const notifList = document.getElementById('notif-popover-list');
    if (notifList) {
      if (allAlerts.length === 0) {
        notifList.innerHTML = `
          <div style="padding: 20px 16px; text-align: center; color: var(--text-tertiary); font-size: 12px;">
            <span class="material-symbols-rounded" style="color: #10b981; font-size: 28px; display: block; margin-bottom: 6px;">verified</span>
            All 5 products are operating within approved tolerance parameters for cycle ${selectedCycle}.
          </div>
        `;
      } else {
        notifList.innerHTML = allAlerts.map(r => {
          const isBreach = r.deviation_pct <= this.state.breachThreshold;
          const isReviewed = this.state.reviewedAlerts.has(r.product_name);

          return `
            <div class="notif-item ${isBreach ? 'breach' : 'warning'} ${isReviewed ? 'reviewed collapsed' : ''}" data-product="${r.product_name}" title="Click to view ${r.product_name} in Workflow">
              <div class="notif-item-hdr">
                <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                  <span class="material-symbols-rounded" style="font-size: 16px; color: ${isReviewed ? '#10b981' : isBreach ? '#ef4444' : '#d97706'}; flex-shrink: 0;">
                    ${isReviewed ? 'check_circle' : isBreach ? 'error' : 'warning'}
                  </span>
                  <b style="color: ${isReviewed ? 'var(--text-secondary)' : isBreach ? '#ef4444' : '#d97706'}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    ${r.product_name}
                  </b>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
                  <button class="notif-review-btn ${isReviewed ? 'is-reviewed' : ''}" data-review-product="${r.product_name}" title="${isReviewed ? 'Click to unmark as reviewed' : 'Click to mark as reviewed and collapse'}">
                    <span class="material-symbols-rounded" style="font-size: 13px;">${isReviewed ? 'check' : 'done'}</span>
                    <span>${isReviewed ? 'Reviewed' : 'Mark Reviewed'}</span>
                  </button>
                  <span class="status-badge ${isBreach ? 'breach' : 'warning'}" style="font-size: 9px; padding: 1px 5px;">
                    ${isBreach ? 'BREACH' : 'WARNING'}
                  </span>
                </div>
              </div>
              <div class="notif-item-body">
                <div style="color: var(--text-secondary); font-size: 11.5px; margin-top: 2px;">
                  Observed Variance: <b style="color: ${isBreach ? '#ef4444' : '#d97706'};">${r.deviation_pct.toFixed(1)}%</b> ${isBreach ? 'vs Target Budget' : 'approaching floor'}
                </div>
                <div style="color: var(--text-tertiary); font-size: 11px;">
                  Actual Net: AED ${(r.net_inflows_aed / 1e6).toFixed(1)}M &bull; Budget: AED ${(r.target_inflows_aed / 1e6).toFixed(1)}M
                </div>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    this.updateProductCard();
  },

  updateProductCard() {
    const { kpiRecords, selectedCycle, selectedProduct } = this.state;
    const found = kpiRecords.find(r => r.month === selectedCycle && r.product_name.includes(selectedProduct.split(' ')[0]));
    if (!found) return;

    const nameEl = document.getElementById('sidebar-prod-name');
    const netEl = document.getElementById('sidebar-prod-net');
    const varEl = document.getElementById('sidebar-prod-var');

    if (nameEl) nameEl.textContent = found.product_name.split(' (')[0];
    if (netEl) netEl.textContent = `AED ${(found.net_inflows_aed / 1e6).toFixed(1)}M`;
    if (varEl) {
      varEl.textContent = `${found.deviation_pct > 0 ? '+' : ''}${found.deviation_pct.toFixed(1)}%`;
      varEl.style.color = found.deviation_pct < -15 ? '#ef4444' : found.deviation_pct < 0 ? '#f59e0b' : '#10b981';
    }
  },

  renderCurrentView() {
    const container = document.getElementById('view-container');
    if (!container) return;

    if (this.state.mode === 'frontline') {
      window.NBC_FRONTLINE.render(container, this.state);
      return;
    }

    // Executive Cockpit Views: Six Step Workflow, Portfolio Matrix, Diagnostics, Bi-Weekly Memo, GCCO Briefing
    switch (this.state.activeExecTab) {
      case 'workflow':
        window.NBC_EXECUTIVE.renderAgenticWorkflow(container, this.state);
        break;
      case 'portfolio':
        window.NBC_EXECUTIVE.renderPortfolioMatrix(container, this.state);
        break;
      case 'diagnostic':
        window.NBC_EXECUTIVE.renderDiagnosticEngine(container, this.state);
        break;
      case 'report':
        window.NBC_EXECUTIVE.renderBiWeeklyReport(container, this.state);
        break;
      case 'gcco':
        window.NBC_EXECUTIVE.renderGccoBriefing(container, this.state);
        break;
      default:
        window.NBC_EXECUTIVE.renderAgenticWorkflow(container, this.state);
    }
  }
};

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.NBC_APP.init();
});
