/* ==========================================================================
   National Bonds Corporation — Master Application Controller (V4)
   Zero-Streamlit Modern Web App
   Document Reference: NBC-DESKTOP-UI-AUDIT-2026-V1
   ========================================================================== */

window.NBC_APP = {
  state: {
    mode: 'executive',          // 'executive' or 'frontline'
    activeExecTab: 'workflow',   // workflow, portfolio, diagnostic, report, gcco
    workflowStep: 1,             // 1: Monitor, 2: Detect, 3: Investigate, 4: Analyse, 5: Recommend, 6: Escalate
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
    this.initAuth();
    this.initEscalationModal();
    this.startLiveTelemetry();
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

          // Switch to Six Step Workflow (Step 02: Detect)
          this.state.workflowStep = 2;
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
  },

  /* ==========================================================================
     Executive Authentication & Profile Management
     ========================================================================== */
  initAuth() {
    const profileBtn = document.getElementById('btn-user-profile');
    const pencilBtn = document.getElementById('btn-sidebar-edit-pencil');
    const modalOverlay = document.getElementById('auth-modal-overlay');
    const closeBtn = document.getElementById('btn-close-auth-modal');
    const tabLogin = document.getElementById('tab-btn-login');
    const tabSignup = document.getElementById('tab-btn-signup');
    const tabEdit = document.getElementById('tab-btn-edit-profile');
    const formLogin = document.getElementById('form-auth-login');
    const formSignup = document.getElementById('form-auth-signup');
    const formEdit = document.getElementById('form-auth-edit');

    // Restore saved user or load default
    const savedUserJson = localStorage.getItem('nb_active_user');
    let currentUser = null;
    if (savedUserJson) {
      try { currentUser = JSON.parse(savedUserJson); } catch (e) {}
    }
    if (!currentUser) {
      currentUser = {
        name: "Jawad Ahmad",
        email: "jawad.ahmad@nationalbonds.ae",
        phone: "+971 50 123 4567",
        designation: "GCCO Commercial Advisory Lead",
        avatar: "JA"
      };
    }
    this.applyUserProfile(currentUser);

    // Open Modal via Profile Card
    profileBtn?.addEventListener('click', (e) => {
      // If pencil button was clicked directly, let its handler take priority
      if (e.target.closest('#btn-sidebar-edit-pencil')) return;
      this.loadQuickProfiles();
      this.clearAuthFeedback();
      tabLogin?.classList.add('active');
      tabSignup?.classList.remove('active');
      tabEdit?.classList.remove('active');
      if (formLogin) formLogin.style.display = 'block';
      if (formSignup) formSignup.style.display = 'none';
      if (formEdit) formEdit.style.display = 'none';
      modalOverlay?.classList.add('active');
    });

    // Open Modal directly to Edit Profile via Pencil Icon
    pencilBtn?.addEventListener('click', (e) => {
      e.stopPropagation();
      this.switchToEditProfileTab();
      modalOverlay?.classList.add('active');
    });

    // Close Modal
    const closeModal = () => modalOverlay?.classList.remove('active');
    closeBtn?.addEventListener('click', closeModal);
    modalOverlay?.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });

    // Tab Switcher
    tabLogin?.addEventListener('click', () => {
      tabLogin.classList.add('active');
      tabSignup?.classList.remove('active');
      tabEdit?.classList.remove('active');
      if (formLogin) formLogin.style.display = 'block';
      if (formSignup) formSignup.style.display = 'none';
      if (formEdit) formEdit.style.display = 'none';
      this.clearAuthFeedback();
    });

    tabSignup?.addEventListener('click', () => {
      tabSignup.classList.add('active');
      tabLogin?.classList.remove('active');
      tabEdit?.classList.remove('active');
      if (formLogin) formLogin.style.display = 'none';
      if (formSignup) formSignup.style.display = 'block';
      if (formEdit) formEdit.style.display = 'none';
      this.clearAuthFeedback();
    });

    tabEdit?.addEventListener('click', () => {
      this.switchToEditProfileTab();
    });

    // Handle Login Submit
    formLogin?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email')?.value.trim();
      const password = document.getElementById('login-password')?.value.trim();
      
      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (data.success && data.user) {
          this.showAuthFeedback('success', `Welcome back, ${data.user.name}!`);
          this.applyUserProfile(data.user);
          setTimeout(closeModal, 800);
        } else {
          this.showAuthFeedback('error', data.message || 'Login failed.');
        }
      } catch (err) {
        this.showAuthFeedback('error', 'Network error contacting server.');
      }
    });

    // Handle Signup Submit
    formSignup?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('signup-name')?.value.trim();
      const email = document.getElementById('signup-email')?.value.trim();
      const phone = document.getElementById('signup-phone')?.value.trim();
      const designation = document.getElementById('signup-designation')?.value.trim();
      const password = document.getElementById('signup-password')?.value.trim();

      try {
        const res = await fetch('/api/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, phone, designation, password })
        });
        const data = await res.json();
        if (data.success && data.user) {
          this.showAuthFeedback('success', `Account created successfully! Logged in as ${data.user.name}.`);
          this.applyUserProfile(data.user);
          formSignup.reset();
          setTimeout(closeModal, 1000);
        } else {
          this.showAuthFeedback('error', data.message || 'Signup failed.');
        }
      } catch (err) {
        this.showAuthFeedback('error', 'Network error contacting server.');
      }
    });

    // Handle Edit Profile Submit
    formEdit?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('edit-name')?.value.trim();
      const email = document.getElementById('edit-email')?.value.trim().toLowerCase();
      const phone = document.getElementById('edit-phone')?.value.trim();
      const designation = document.getElementById('edit-designation')?.value.trim();
      const password = document.getElementById('edit-password')?.value.trim();

      try {
        const res = await fetch('/api/auth/update-profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, phone, designation, password })
        });
        const data = await res.json();
        if (data.success && data.user) {
          this.showAuthFeedback('success', 'Profile updated successfully!');
          this.applyUserProfile(data.user);
          setTimeout(closeModal, 800);
        } else {
          this.showAuthFeedback('error', data.message || 'Profile update failed.');
        }
      } catch (err) {
        this.showAuthFeedback('error', 'Network error updating profile.');
      }
    });
  },

  switchToEditProfileTab() {
    const tabLogin = document.getElementById('tab-btn-login');
    const tabSignup = document.getElementById('tab-btn-signup');
    const tabEdit = document.getElementById('tab-btn-edit-profile');
    const formLogin = document.getElementById('form-auth-login');
    const formSignup = document.getElementById('form-auth-signup');
    const formEdit = document.getElementById('form-auth-edit');

    tabEdit?.classList.add('active');
    tabLogin?.classList.remove('active');
    tabSignup?.classList.remove('active');
    if (formLogin) formLogin.style.display = 'none';
    if (formSignup) formSignup.style.display = 'none';
    if (formEdit) formEdit.style.display = 'block';
    this.clearAuthFeedback();

    const savedUserJson = localStorage.getItem('nb_active_user');
    let u = null;
    if (savedUserJson) {
      try { u = JSON.parse(savedUserJson); } catch (e) {}
    }
    if (!u) {
      u = {
        name: "Jawad Ahmad",
        email: "jawad.ahmad@nationalbonds.ae",
        phone: "+971 50 123 4567",
        designation: "GCCO Commercial Advisory Lead"
      };
    }

    const editName = document.getElementById('edit-name');
    const editEmail = document.getElementById('edit-email');
    const editPhone = document.getElementById('edit-phone');
    const editDesig = document.getElementById('edit-designation');
    const editPass = document.getElementById('edit-password');

    if (editName) editName.value = u.name || '';
    if (editEmail) editEmail.value = u.email || '';
    if (editPhone) editPhone.value = u.phone || '';
    if (editDesig) editDesig.value = u.designation || u.role || '';
    if (editPass) editPass.value = '';
  },

  applyUserProfile(user) {
    if (!user) return;
    localStorage.setItem('nb_active_user', JSON.stringify(user));
    const avatarEl = document.getElementById('sidebar-user-avatar');
    const nameEl = document.getElementById('sidebar-user-name');
    const roleEl = document.getElementById('sidebar-user-role');
    if (avatarEl) avatarEl.textContent = user.avatar || user.name.slice(0, 2).toUpperCase();
    if (nameEl) nameEl.textContent = user.name;
    if (roleEl) roleEl.textContent = user.designation || user.role || 'Executive';
  },

  async loadQuickProfiles() {
    const quickList = document.getElementById('quick-profiles-list');
    if (!quickList) return;
    try {
      const res = await fetch('/api/auth/users');
      const data = await res.json();
      if (data.users && data.users.length > 0) {
        quickList.innerHTML = data.users.map(u => `
          <div class="quick-profile-item" data-user-email="${u.email}">
            <div class="quick-profile-avatar">${u.avatar}</div>
            <div>
              <div class="quick-profile-name">${u.name}</div>
              <div style="font-size: 10.5px; color: #64748b;">${u.email}</div>
            </div>
            <div class="quick-profile-role">${u.designation || u.role}</div>
          </div>
        `).join('');

        quickList.querySelectorAll('.quick-profile-item').forEach(item => {
          item.addEventListener('click', () => {
            const email = item.getAttribute('data-user-email');
            const found = data.users.find(u => u.email === email);
            if (found) {
              this.applyUserProfile(found);
              this.showAuthFeedback('success', `Switched active persona to ${found.name}.`);
              setTimeout(() => {
                document.getElementById('auth-modal-overlay')?.classList.remove('active');
              }, 600);
            }
          });
        });
      }
    } catch (err) {
      console.warn('Failed to fetch quick profiles:', err);
    }
  },

  showAuthFeedback(type, message) {
    const banner = document.getElementById('auth-feedback-banner');
    if (!banner) return;
    banner.className = `auth-feedback-banner ${type}`;
    banner.innerHTML = `
      <span class="material-symbols-rounded" style="font-size: 18px;">${type === 'success' ? 'check_circle' : 'error'}</span>
      <span>${message}</span>
    `;
    banner.style.display = 'flex';
  },

  clearAuthFeedback() {
    const banner = document.getElementById('auth-feedback-banner');
    if (banner) {
      banner.className = 'auth-feedback-banner';
      banner.innerHTML = '';
      banner.style.display = 'none';
    }
  },

  /* ==========================================================================
     Live Data Stream Telemetry Poller
     ========================================================================== */
  startLiveTelemetry() {
    let lastSavers = null;

    const fetchTelemetry = async () => {
      try {
        const res = await fetch('/api/live-metrics');
        if (!res.ok) return;
        const data = await res.json();
        if (data.is_live) {
          const saversEl = document.getElementById('hdr-stat-savers');
          const aumEl = document.getElementById('hdr-stat-aum');
          const netEl = document.getElementById('hdr-stat-net');
          const badgeEl = document.getElementById('live-telemetry-badge');

          if (saversEl && data.total_savers_formatted) {
            if (lastSavers !== null && data.total_savers !== lastSavers) {
              saversEl.classList.remove('stat-val-pulse');
              void saversEl.offsetWidth;
              saversEl.classList.add('stat-val-pulse');

              if (aumEl) {
                aumEl.classList.remove('stat-val-pulse');
                void aumEl.offsetWidth;
                aumEl.classList.add('stat-val-pulse');
              }
            }
            saversEl.textContent = data.total_savers_formatted;
            lastSavers = data.total_savers;
          }

          if (aumEl && data.total_aum_formatted) {
            aumEl.textContent = data.total_aum_formatted;
          }

          if (netEl && data.net_inflows_formatted) {
            netEl.textContent = data.net_inflows_formatted;
          }

          if (badgeEl && data.added_customers !== undefined) {
            badgeEl.title = `Live Ingestion Active: +${data.added_customers} dummy customer records appended. Last sync: ${data.timestamp}`;
          }
        }
      } catch (err) {
        // Silently retry on next tick
      }
    };

    fetchTelemetry();
    setInterval(fetchTelemetry, 2000);
  },

  /* ==========================================================================
     Frontline Escalation Ticket Modal Controller
     ========================================================================== */
  initEscalationModal() {
    const overlay = document.getElementById('escalation-modal-overlay');
    const closeBtn = document.getElementById('btn-close-escalation-modal');
    const cancelBtn = document.getElementById('btn-cancel-escalation');
    const form = document.getElementById('form-create-escalation');

    const closeModal = () => this.closeEscalationModal();
    closeBtn?.addEventListener('click', closeModal);
    cancelBtn?.addEventListener('click', closeModal);
    overlay?.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });

    form?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById('btn-submit-escalation');
      const banner = document.getElementById('escalation-feedback-banner');

      const user_name = document.getElementById('esc-user-name')?.value.trim() || 'Ahmed (RM)';
      const user_role = document.getElementById('esc-user-role')?.value.trim() || 'Sales / Relationship Manager';
      const product_name = document.getElementById('esc-product')?.value || 'Booster Plan';
      const priority = document.getElementById('esc-priority')?.value || 'HIGH';
      const reason = document.getElementById('esc-reason')?.value || 'Policy Exception / Fee Waiver';
      const query = document.getElementById('esc-query')?.value.trim();
      const assigned_lead = document.getElementById('esc-assigned')?.value || 'Fariha Fatima Hameed (Product Management Lead)';

      if (!query) {
        if (banner) {
          banner.className = 'auth-feedback-banner error';
          banner.innerHTML = '<span class="material-symbols-rounded">error</span><span>Please describe the commercial inquiry or policy issue.</span>';
          banner.style.display = 'flex';
        }
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="material-symbols-rounded" style="font-size: 18px;">hourglass_empty</span> Submitting Ticket...';
      }

      try {
        const res = await fetch('/api/escalate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_name,
            user_role,
            product_name,
            priority,
            reason,
            query,
            assigned_lead
          })
        });

        const data = await res.json();
        if (data.success && data.ticket) {
          const newTicket = { ...data.ticket, isNew: true };
          if (this.state.ticketsData) {
            this.state.ticketsData.unshift(newTicket);
          }
          if (window.NBC_DATA && window.NBC_DATA.tickets_data) {
            window.NBC_DATA.tickets_data.unshift(newTicket);
          }

          if (banner) {
            banner.className = 'auth-feedback-banner success';
            banner.innerHTML = `<span class="material-symbols-rounded">check_circle</span><span>Ticket <b>${newTicket.ticket_id}</b> created and routed to ${assigned_lead.split(' (')[0]}!</span>`;
            banner.style.display = 'flex';
          }

          if (this.state.mode === 'frontline') {
            const pane = document.getElementById('frontline-tab-pane');
            if (pane && window.NBC_FRONTLINE.activeTab === 'tickets') {
              window.NBC_FRONTLINE.renderTicketsTab(pane, this.state);
            }
            const openKpi = document.querySelector('[data-fl-tab="tickets"] .tab-badge');
            if (openKpi) openKpi.textContent = this.state.ticketsData.length;
          }

          setTimeout(() => {
            this.closeEscalationModal();
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.innerHTML = '<span class="material-symbols-rounded" style="font-size: 18px;">send</span> Submit Escalation Ticket';
            }
          }, 900);
        } else {
          throw new Error(data.error || 'Failed to submit escalation ticket.');
        }
      } catch (err) {
        if (banner) {
          banner.className = 'auth-feedback-banner error';
          banner.innerHTML = `<span class="material-symbols-rounded">error</span><span>Error: ${err.message}</span>`;
          banner.style.display = 'flex';
        }
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<span class="material-symbols-rounded" style="font-size: 18px;">send</span> Submit Escalation Ticket';
        }
      }
    });
  },

  openEscalationModal(prefillQuery = '', prefillProduct = '') {
    const overlay = document.getElementById('escalation-modal-overlay');
    const banner = document.getElementById('escalation-feedback-banner');
    if (banner) {
      banner.className = 'auth-feedback-banner';
      banner.style.display = 'none';
      banner.innerHTML = '';
    }

    const savedUserJson = localStorage.getItem('nb_active_user');
    if (savedUserJson) {
      try {
        const u = JSON.parse(savedUserJson);
        const nameInput = document.getElementById('esc-user-name');
        const roleInput = document.getElementById('esc-user-role');
        if (nameInput) nameInput.value = u.name;
        if (roleInput) roleInput.value = u.designation || u.role;
      } catch (e) {}
    }

    if (prefillQuery) {
      const qInput = document.getElementById('esc-query');
      if (qInput) qInput.value = prefillQuery;
    }
    if (prefillProduct) {
      const pSelect = document.getElementById('esc-product');
      if (pSelect) pSelect.value = prefillProduct;
    }

    overlay?.classList.add('active');
  },

  closeEscalationModal() {
    const overlay = document.getElementById('escalation-modal-overlay');
    overlay?.classList.remove('active');
  }
};

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.NBC_APP.init();
});
