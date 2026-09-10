/* ==========================================================================
   National Bonds Corporation — Master Application Controller (V4)
   Zero-Streamlit Modern Web App
   Document Reference: NBC-DESKTOP-UI-AUDIT-2026-V1
   ========================================================================== */

window.NBC_APP = {
  state: {
    mode: 'executive',          // 'executive' or 'frontline'
    activeExecTab: 'powerbi',   // powerbi, workflow, portfolio, diagnostic, simulator, report, gcco
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
    demographics: {}
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
      document.getElementById('exec-tabs-nav').style.display = 'flex';
      this.updateOverviewHeader();
      this.renderCurrentView();
    });

    btnFrontline?.addEventListener('click', () => {
      this.state.mode = 'frontline';
      btnFrontline.classList.add('active');
      btnExec?.classList.remove('active');
      document.getElementById('exec-tabs-nav').style.display = 'none';
      this.updateOverviewHeader();
      this.renderCurrentView();
    });

    // Product selector in sidebar
    const productSelect = document.getElementById('sidebar-product-select');
    productSelect?.addEventListener('change', (e) => {
      this.state.selectedProduct = e.target.value;
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
  },

  bindNavigationTabs() {
    document.querySelectorAll('[data-exec-tab]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-exec-tab]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.activeExecTab = btn.getAttribute('data-exec-tab');
        this.renderCurrentView();
      });
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
    const varianceGap = net - target;

    // 1. Alert Banner
    const banner = document.getElementById('exec-alert-banner');
    const breaches = cycleKpis.filter(r => r.deviation_pct <= this.state.breachThreshold);
    const warnings = cycleKpis.filter(r => r.deviation_pct > this.state.breachThreshold && r.deviation_pct <= this.state.warningThreshold);

    if (banner) {
      if (this.state.mode === 'frontline') {
        banner.style.display = 'none';
      } else {
        banner.style.display = 'flex';
        if (breaches.length > 0) {
          banner.className = 'alert-banner breach';
          const bList = breaches.map(r => `<b>${r.product_name}</b> (${r.deviation_pct.toFixed(1)}%)`).join(', ');
          const wList = warnings.map(r => `<b>${r.product_name}</b> (${r.deviation_pct.toFixed(1)}%)`).join(', ');
          banner.innerHTML = `
            <div class="alert-content-left">
              <div class="alert-icon-wrap">
                <span class="material-symbols-rounded">warning</span>
              </div>
              <div class="alert-text-group">
                <div class="alert-title">Active Tolerance Deviations &mdash; Cycle ${selectedCycle}</div>
                <div class="alert-desc">
                  Material Breaches: ${bList} ${wList ? `&bull; Early Warnings: ${wList}` : ''}
                </div>
              </div>
            </div>
            <button class="alert-action-btn" onclick="document.querySelector('[data-exec-tab=workflow]').click();">
              ACTION REQUIRED
            </button>
          `;
        } else if (warnings.length > 0) {
          banner.className = 'alert-banner warning';
          const wList = warnings.map(r => `<b>${r.product_name}</b> (${r.deviation_pct.toFixed(1)}%)`).join(', ');
          banner.innerHTML = `
            <div class="alert-content-left">
              <div class="alert-icon-wrap">
                <span class="material-symbols-rounded">info</span>
              </div>
              <div class="alert-text-group">
                <div class="alert-title">Early Warning Sensitivity Detected &mdash; Cycle ${selectedCycle}</div>
                <div class="alert-desc">Products Approaching Threshold: ${wList}</div>
              </div>
            </div>
            <button class="alert-action-btn" style="border-color: var(--status-warning); background: rgba(245,158,11,0.1); color: var(--status-warning);" onclick="document.querySelector('[data-exec-tab=diagnostic]').click();">
              DIAGNOSE GAP
            </button>
          `;
        } else {
          banner.className = 'alert-banner healthy';
          banner.innerHTML = `
            <div class="alert-content-left">
              <div class="alert-icon-wrap">
                <span class="material-symbols-rounded">check_circle</span>
              </div>
              <div class="alert-text-group">
                <div class="alert-title">Portfolio Stability: Optimal Operational Governance</div>
                <div class="alert-desc">All 5 products are operating strictly within approved target variance parameters for cycle ${selectedCycle}.</div>
              </div>
            </div>
            <span class="status-badge healthy">STABLE</span>
          `;
        }
      }
    }

    // 2. Overview KPI Cards
    const kpiGrid = document.getElementById('exec-kpi-grid');
    if (kpiGrid) {
      if (this.state.mode === 'frontline') {
        kpiGrid.style.display = 'none';
      } else {
        kpiGrid.style.display = 'grid';
        kpiGrid.innerHTML = `
          <!-- KPI 1: Total Portfolio AUM -->
          <div class="kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-card-label">Total Portfolio AUM</span>
              <div class="kpi-card-icon"><span class="material-symbols-rounded">account_balance</span></div>
            </div>
            <div class="kpi-card-value">AED 18.34B</div>
            <div class="kpi-card-footer">
              <span class="kpi-trend-pill positive">
                <span class="material-symbols-rounded" style="font-size: 13px;">trending_up</span> +8.4% YoY
              </span>
              <span class="kpi-target-note">154.2K Savers</span>
            </div>
          </div>

          <!-- KPI 2: Net Inflow Run-Rate -->
          <div class="kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-card-label">Net Inflow Run-Rate</span>
              <div class="kpi-card-icon"><span class="material-symbols-rounded">payments</span></div>
            </div>
            <div class="kpi-card-value">AED ${net.toFixed(1)}M</div>
            <div class="kpi-card-footer">
              <span class="kpi-trend-pill ${variancePct >= 0 ? 'positive' : variancePct > -10 ? 'warning' : 'negative'}">
                <span class="material-symbols-rounded" style="font-size: 13px;">${variancePct >= 0 ? 'trending_up' : 'trending_down'}</span>
                ${variancePct > 0 ? '+' : ''}${variancePct.toFixed(1)}% vs Target
              </span>
              <span class="kpi-target-note">Target: AED ${target.toFixed(1)}M</span>
            </div>
          </div>

          <!-- KPI 3: Portfolio Variance Gap -->
          <div class="kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-card-label">Portfolio Variance Gap</span>
              <div class="kpi-card-icon"><span class="material-symbols-rounded">crisis_alert</span></div>
            </div>
            <div class="kpi-card-value" style="color: ${varianceGap < 0 ? '#ef4444' : '#10b981'};">
              ${varianceGap > 0 ? '+' : ''}AED ${varianceGap.toFixed(1)}M
            </div>
            <div class="kpi-card-footer">
              <span class="kpi-trend-pill ${varianceGap < 0 ? 'negative' : 'positive'}">
                ${varianceGap < 0 ? 'AMBER DEFICIT' : 'SURPLUS'}
              </span>
              <span class="kpi-target-note">Tolerance: -8.0% Floor</span>
            </div>
          </div>

          <!-- KPI 4: Capital Adequacy & Sharia -->
          <div class="kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-card-label">Capital Adequacy & Sharia</span>
              <div class="kpi-card-icon"><span class="material-symbols-rounded">verified_user</span></div>
            </div>
            <div class="kpi-card-value" style="color: #10b981;">100% Sharia</div>
            <div class="kpi-card-footer">
              <span class="kpi-trend-pill positive">
                <span class="material-symbols-rounded" style="font-size: 13px;">shield</span> CAR 22.4%
              </span>
              <span class="kpi-target-note">CBUAE Basel III Compliant</span>
            </div>
          </div>
        `;
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

    // Executive Cockpit Subsystems (Tabs 1 to 7)
    switch (this.state.activeExecTab) {
      case 'powerbi':
        window.NBC_EXECUTIVE.renderPowerBiStudio(container, this.state);
        break;
      case 'workflow':
        window.NBC_EXECUTIVE.renderAgenticWorkflow(container, this.state);
        break;
      case 'portfolio':
        window.NBC_EXECUTIVE.renderPortfolioMatrix(container, this.state);
        break;
      case 'diagnostic':
        window.NBC_EXECUTIVE.renderDiagnosticEngine(container, this.state);
        break;
      case 'simulator':
        window.NBC_EXECUTIVE.renderLiveSimulator(container, this.state);
        break;
      case 'report':
        window.NBC_EXECUTIVE.renderBiWeeklyReport(container, this.state);
        break;
      case 'gcco':
        window.NBC_EXECUTIVE.renderGccoBriefing(container, this.state);
        break;
      default:
        window.NBC_EXECUTIVE.renderPowerBiStudio(container, this.state);
    }
  }
};

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.NBC_APP.init();
});
