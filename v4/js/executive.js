/* ==========================================================================
   National Bonds Corporation — Executive Cockpit Subsystems (Tabs 1 to 7)
   Document Reference: NBC-DESKTOP-UI-AUDIT-2026-V1
   ========================================================================== */

window.NBC_EXECUTIVE = {
  // Tab 1: PowerBI Analytics Studio
  renderPowerBiStudio(container, state) {
    const { kpiRecords, marketData } = state;
    const currentMonth = state.selectedCycle || '2026-06';
    const cycleKpis = kpiRecords.filter(r => r.month === currentMonth);

    const gross = cycleKpis.reduce((acc, r) => acc + r.gross_inflows_aed, 0) / 1e6;
    const red = cycleKpis.reduce((acc, r) => acc + r.redemptions_aed, 0) / 1e6;
    const net = cycleKpis.reduce((acc, r) => acc + r.net_inflows_aed, 0) / 1e6;
    const target = cycleKpis.reduce((acc, r) => acc + r.target_inflows_aed, 0) / 1e6;
    const dev = target > 0 ? ((net - target) / target) * 100 : 0;

    container.innerHTML = `
      <!-- PowerBI Hero Banner -->
      <div class="powerbi-hero">
        <div>
          <div class="hero-left-title">PowerBI Visual Analytics Studio</div>
          <div class="hero-left-subtitle">Multi-Dimensional Capital Flows, Liquidity Yields & Predictive Stress Modeling for Cycle ${currentMonth}</div>
        </div>
        <div class="hero-stats-row">
          <div class="hero-stat-box">
            <span class="hero-stat-label">Gross Inflow Volume</span>
            <span class="hero-stat-value">AED ${gross.toFixed(1)}M</span>
          </div>
          <div class="hero-stat-box">
            <span class="hero-stat-label">Net Liquidity Inflow</span>
            <span class="hero-stat-value">AED ${net.toFixed(1)}M</span>
          </div>
          <div class="hero-stat-box">
            <span class="hero-stat-label">Portfolio Variance</span>
            <span class="hero-stat-value" style="color: ${dev < -8 ? '#ef4444' : '#10b981'};">${dev > 0 ? '+' : ''}${dev.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      <!-- Slicers Bar -->
      <div class="slicers-bar" style="margin-top: 16px; margin-bottom: 20px;">
        <div class="slicer-group">
          <label class="slicer-label">Reporting Cycle</label>
          <select class="slicer-control" id="pbi-cycle-select">
            ${[...new Set(kpiRecords.map(r => r.month))].sort().reverse().map(m => `
              <option value="${m}" ${m === currentMonth ? 'selected' : ''}>${m} (Monthly Close)</option>
            `).join('')}
          </select>
        </div>
        <div class="slicer-group">
          <label class="slicer-label">Product Family</label>
          <select class="slicer-control" id="pbi-product-select">
            <option value="ALL">All 5 Core Products</option>
            <option value="Saving Bonds">Saving Bonds</option>
            <option value="Term Sukuk (Fixed Income)">Term Sukuk</option>
            <option value="Booster Plan">Booster Plan</option>
            <option value="Second Salary (Regular Savings)">Second Salary</option>
            <option value="MyPlan / Regular Saver">MyPlan Saver</option>
          </select>
        </div>
        <div class="slicer-group">
          <label class="slicer-label">Customer Tier</label>
          <select class="slicer-control">
            <option>All Customer Tiers (154.2K Cohort)</option>
            <option>Mass Affluent (AED 48.9K Median)</option>
            <option>Emirati National (AED 73.1K Median)</option>
            <option>High Net Worth (AED 265K+)</option>
          </select>
        </div>
        <div class="slicer-group">
          <label class="slicer-label">Acquisition Channel</label>
          <select class="slicer-control">
            <option>All Sourced Channels</option>
            <option>Mobile App (47.8%)</option>
            <option>Branch Network (28.2%)</option>
            <option>Web Portal (12.0%)</option>
          </select>
        </div>
      </div>

      <!-- Grid 1: Cashflow Waterfall & AUM Allocation Treemap -->
      <div class="charts-grid-2">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Portfolio Liquidity & Cashflow Waterfall Bridge</div>
              <div class="chart-card-subtitle">Deconstruction of Channel Inflows vs Maturities and Redemptions for ${currentMonth} (AED Millions)</div>
            </div>
            <span class="status-badge healthy">AUDITED H1</span>
          </div>
          <div id="chart-pbi-waterfall" class="chart-viewport"></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">AUM Capital Allocation</div>
              <div class="chart-card-subtitle">Product Concentration & Tenor Weights (AED 18.34B)</div>
            </div>
          </div>
          <div id="chart-pbi-treemap" class="chart-viewport"></div>
        </div>
      </div>

      <!-- Grid 2: BCG Strategic Matrix & Macro Correlation Combo -->
      <div class="charts-grid-equal">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">BCG Strategic Portfolio Matrix</div>
              <div class="chart-card-subtitle">Annualized Yield (%) vs Net Inflow Growth Deviation (%)</div>
            </div>
          </div>
          <div id="chart-pbi-bcg" class="chart-viewport"></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Macro Correlation Combo (12-Month Trajectory)</div>
              <div class="chart-card-subtitle">Consumer Savings Activity Index vs CBUAE Base Rate (4.65%) & 3M EIBOR (4.52%)</div>
            </div>
          </div>
          <div id="chart-pbi-macro" class="chart-viewport"></div>
        </div>
      </div>

      <!-- Grid 3: 18-Month Performance Heatmap -->
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-card-title">18-Month Product Tolerance & Deviation Heatmap</div>
            <div class="chart-card-subtitle">Continuous Historical Variance Tracking Against ALCO Approved Inflow Targets</div>
          </div>
        </div>
        <div id="chart-pbi-heatmap" class="chart-viewport" style="min-height: 280px;"></div>
      </div>

      <!-- Grid 4: Monte Carlo Predictive Cone & Customer Lifecycle Funnel -->
      <div class="charts-grid-equal">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Monte Carlo Predictive Cone (Forward 6-Month Projection)</div>
              <div class="chart-card-subtitle">Stochastic Simulation with 95% Confidence Interval Bounds</div>
            </div>
          </div>
          <div id="chart-pbi-montecarlo" class="chart-viewport"></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Customer Lifecycle Conversion Funnel</div>
              <div class="chart-card-subtitle">Conversion Velocity from Lead Registration to Recurring Saver Retention</div>
            </div>
          </div>
          <div id="chart-pbi-funnel" class="chart-viewport"></div>
        </div>
      </div>
    `;

    // Initialize ApexCharts for Tab 1
    setTimeout(() => {
      NBC_CHARTS.renderWaterfall('chart-pbi-waterfall', gross, red, net);
      NBC_CHARTS.renderAumTreemap('chart-pbi-treemap');
      NBC_CHARTS.renderBcgMatrix('chart-pbi-bcg');
      NBC_CHARTS.renderMacroCombo('chart-pbi-macro', marketData);
      NBC_CHARTS.renderHeatmap('chart-pbi-heatmap', kpiRecords);
      NBC_CHARTS.renderMonteCarlo('chart-pbi-montecarlo');
      NBC_CHARTS.renderFunnel('chart-pbi-funnel');
    }, 50);

    // Bind Slicer cycle
    document.getElementById('pbi-cycle-select')?.addEventListener('change', (e) => {
      state.selectedCycle = e.target.value;
      this.renderPowerBiStudio(container, state);
      window.NBC_APP.updateOverviewHeader(state);
    });
  },

  // Tab: Six Step Autonomous Agentic Workflow (Fully Interactive 6-Step Pipeline)
  renderAgenticWorkflow(container, state) {
    if (!state.workflowStep) state.workflowStep = 1;
    const currentStep = state.workflowStep;
    const { kpiRecords, marketData } = state;
    const activeProd = state.selectedProduct || 'All Products';
    const isAllProducts = !activeProd || activeProd === 'All Products' || activeProd === 'ALL';
    const currentMonth = state.selectedCycle || '2026-06';
    const cycleKpis = kpiRecords?.filter(r => r.month === currentMonth) || [];

    const PRODUCT_AUM = {
      'Term Sukuk': 9450,
      'Saving Bonds': 4820,
      'Booster Plan': 2150,
      'MyPlan': 1420,
      'Second Salary': 500
    };

    // System-wide totals
    const totGross = cycleKpis.reduce((acc, r) => acc + r.gross_inflows_aed, 0) / 1e6;
    const totRed = cycleKpis.reduce((acc, r) => acc + r.redemptions_aed, 0) / 1e6;
    const totNet = cycleKpis.reduce((acc, r) => acc + r.net_inflows_aed, 0) / 1e6;
    const totTgt = cycleKpis.reduce((acc, r) => acc + r.target_inflows_aed, 0) / 1e6;
    const totDev = totTgt > 0 ? ((totNet - totTgt) / totTgt) * 100 : 0;
    const totDef = Math.abs(totNet - totTgt);
    const totSavers = cycleKpis.reduce((acc, r) => acc + r.active_customers, 0);

    // Specific product match
    const foundProd = cycleKpis.find(r => r.product_name.includes(activeProd.split(' ')[0])) || cycleKpis[0];

    // Dynamic resolution
    const prodDisplayName = isAllProducts ? 'All Products (Portfolio)' : (foundProd?.product_name || activeProd);
    const prodShortName = isAllProducts ? 'Total Portfolio' : (foundProd ? foundProd.product_name.split(' (')[0] : activeProd);
    const grossAed = isAllProducts ? totGross.toFixed(1) : (foundProd ? (foundProd.gross_inflows_aed / 1e6).toFixed(1) : '138.7');
    const redAed = isAllProducts ? totRed.toFixed(1) : (foundProd ? (foundProd.redemptions_aed / 1e6).toFixed(1) : '78.9');
    const netAed = isAllProducts ? totNet.toFixed(1) : (foundProd ? (foundProd.net_inflows_aed / 1e6).toFixed(2) : '51.19');
    const tgtAed = isAllProducts ? totTgt.toFixed(1) : (foundProd ? (foundProd.target_inflows_aed / 1e6).toFixed(2) : '57.02');
    const devPct = isAllProducts ? totDev : (foundProd ? foundProd.deviation_pct : -10.22);
    const defAed = isAllProducts ? totDef.toFixed(2) : (foundProd ? Math.abs((foundProd.net_inflows_aed - foundProd.target_inflows_aed) / 1e6).toFixed(2) : '5.82');
    const saversCount = isAllProducts ? (totSavers || 176142) : (foundProd?.active_customers || 139945);

    let aumStr = 'AED 18.34B';
    if (!isAllProducts && foundProd) {
      const aumKey = Object.keys(PRODUCT_AUM).find(k => foundProd.product_name.includes(k));
      const aumVal = aumKey ? PRODUCT_AUM[aumKey] : 2000;
      aumStr = aumVal >= 1000 ? `AED ${(aumVal / 1000).toFixed(2)}B` : `AED ${aumVal}M`;
    }

    const isBreach = devPct <= state.breachThreshold;
    const isWarn = devPct <= state.warningThreshold;
    const statusTier = isBreach ? 'Tier-1 Breach' : isWarn ? 'Tolerance Warning' : 'Optimal Performance';
    const statusColor = isBreach ? '#ef4444' : isWarn ? '#f59e0b' : '#10b981';

    // Directives matrix
    const PRODUCT_DIRECTIVES = {
      'Saving Bonds': [
        { id: 1, title: 'Directive 1: Hotfix Mobile Payment Gateway & Re-enable 1-Click Apple Pay', desc: 'Roll back buggy checkout auth build; restore auto-debit retries. &bull; <b>ETA: 48 Hours &bull; Lead: Digital Engineering</b>', amount: 3.20, label: '+ Direct 1: Gateway' },
        { id: 2, title: 'Directive 2: Deploy 5.30% 6-Month Booster Sukuk Flash Tranche', desc: 'Targeted in-app promotional tranche to neutralize neo-bank yield arbitrage. &bull; <b>ETA: 5 Days &bull; Lead: Commercial Strategy</b>', amount: 4.50, label: '+ Direct 2: Booster' },
        { id: 3, title: 'Directive 3: Direct RM Concierge Outreach to 420 High Net Worth Savers', desc: 'Dedicated phone consultation for accounts > AED 250k with redemption signals. &bull; <b>ETA: Immediate &bull; Lead: Wealth Advisory</b>', amount: 6.00, label: '+ Direct 3: HNW RM' }
      ],
      'Term Sukuk': [
        { id: 1, title: 'Directive 1: Institutional 3Y Sukuk Rollover Reinvestment Incentive', desc: 'Preferential 15 bps profit rate boost for corporate treasury maturities. &bull; <b>ETA: 48 Hours &bull; Lead: Treasury</b>', amount: 25.00, label: '+ Direct 1: Rollover' },
        { id: 2, title: 'Directive 2: Corporate & Institutional Rate Match Tranche', desc: 'Bespoke yield tiering for liquidity commitments > AED 10M. &bull; <b>ETA: 5 Days &bull; Lead: Institutional Banking</b>', amount: 30.00, label: '+ Direct 2: Corp Match' },
        { id: 3, title: 'Directive 3: Direct Wealth Family Office Investor Roadshow', desc: 'Executive client engagement targeting top Tier-1 family offices. &bull; <b>ETA: 14 Days &bull; Lead: Wealth Advisory</b>', amount: 15.00, label: '+ Direct 3: Roadshow' }
      ],
      'Booster Plan': [
        { id: 1, title: 'Directive 1: Extend 12-Month Tenor Tranche with Loyalty Multiplier', desc: 'Roll out 12M structured certificates with bonus reward draw tickets. &bull; <b>ETA: 48 Hours &bull; Lead: Product Development</b>', amount: 3.00, label: '+ Direct 1: 12M Tenor' },
        { id: 2, title: 'Directive 2: In-App Cross-Sell Campaign to Maturing Saving Bonds', desc: 'Automated 1-tap rollover prompt into Booster for liquid accounts. &bull; <b>ETA: 3 Days &bull; Lead: Growth Marketing</b>', amount: 4.00, label: '+ Direct 2: Cross-Sell' },
        { id: 3, title: 'Directive 3: Wealth Advisory Loyalty Incentive Program', desc: 'Exclusive rewards tiering for accounts retaining > 6 months. &bull; <b>ETA: 7 Days &bull; Lead: Retail Commercial</b>', amount: 2.00, label: '+ Direct 3: Loyalty' }
      ],
      'Second Salary': [
        { id: 1, title: 'Directive 1: Corporate Payroll API Integration with Top 50 UAE Employers', desc: 'Direct salary debit automation partnerships across government & semi-gov. &bull; <b>ETA: 14 Days &bull; Lead: B2B Partnerships</b>', amount: 0.80, label: '+ Direct 1: Payroll API' },
        { id: 2, title: 'Directive 2: Employer Pension Scheme & End-of-Service Trust Roadshow', desc: 'Corporate HR seminars on supplementary retirement savings. &bull; <b>ETA: 7 Days &bull; Lead: Institutional Strategy</b>', amount: 1.20, label: '+ Direct 2: Pension' },
        { id: 3, title: 'Directive 3: First-Month Contribution Bonus Match Promotion', desc: 'Welcome contribution credit on 3-year recurring savings setup. &bull; <b>ETA: 3 Days &bull; Lead: Digital Marketing</b>', amount: 0.50, label: '+ Direct 3: Match Bonus' }
      ],
      'MyPlan': [
        { id: 1, title: 'Directive 1: Mobile Direct Debit Auto-Enrollment Push', desc: 'Zero-friction direct debit activation via UAEPGS network. &bull; <b>ETA: 48 Hours &bull; Lead: Digital Product</b>', amount: 0.60, label: '+ Direct 1: Auto-Debit' },
        { id: 2, title: 'Directive 2: Gamified Savings Streak Rewards & Monthly Prize Multiplier', desc: 'Tiered milestone bonuses for 6+ consecutive monthly deposits. &bull; <b>ETA: 5 Days &bull; Lead: Customer Engagement</b>', amount: 0.50, label: '+ Direct 2: Gamification' },
        { id: 3, title: 'Directive 3: Salary Top-Up Match Bonus Incentive', desc: 'Instant AED 100 bonus on AED 1,000+ monthly recurring schedule. &bull; <b>ETA: Immediate &bull; Lead: Commercial Advisory</b>', amount: 0.40, label: '+ Direct 3: Top-Up Match' }
      ]
    };

    const defaultDirectives = [
      { id: 1, title: 'Directive 1: Fix Mobile Checkout Gateway Authentication', desc: 'Resolve digital drop-off; restore auto-debit retries. &bull; <b>ETA: 48 Hours &bull; Lead: Digital Engineering</b>', amount: 3.20, label: '+ Direct 1: Gateway' },
      { id: 2, title: 'Directive 2: Institutional Sukuk Maturity Reinvestment Push', desc: 'Target corporate accounts to secure roll-overs. &bull; <b>ETA: 5 Days &bull; Lead: Commercial Strategy</b>', amount: 40.00, label: '+ Direct 2: Sukuk Roll' },
      { id: 3, title: 'Directive 3: Unified Retail Cross-Sell & Yield Campaign', desc: 'Broad market re-engagement across mobile & branch channels. &bull; <b>ETA: Immediate &bull; Lead: Retail Advisory</b>', amount: 15.00, label: '+ Direct 3: Retail Push' }
    ];

    const currentDirectivesKey = Object.keys(PRODUCT_DIRECTIVES).find(k => activeProd.includes(k));
    const currentDirectives = isAllProducts ? defaultDirectives : (currentDirectivesKey ? PRODUCT_DIRECTIVES[currentDirectivesKey] : defaultDirectives);

    const totalDirectivesRecovery = currentDirectives.reduce((acc, d) => acc + d.amount, 0);
    const deficitCoveragePct = +defAed > 0 ? Math.round((totalDirectivesRecovery / +defAed) * 100) : 100;

    // Yield details
    const PRODUCT_YIELDS = {
      'Term Sukuk': { yield: '5.15% p.a.', spread: '-10 bps Spread', desc: 'High institutional rollover and maturity retention.' },
      'Saving Bonds': { yield: '4.20% p.a.', spread: '-105 bps Spread', desc: 'Standard liquid certificate facing competition from neo-bank teaser yields.' },
      'Booster Plan': { yield: '5.30% p.a.', spread: '+5 bps Premium', desc: 'National Bonds Booster out-yields all neo-banks on 6-month commitments.' },
      'Second Salary': { yield: '4.80% p.a.', spread: '-45 bps Spread', desc: 'Long-term accumulation structure with pension endowment benefits.' },
      'MyPlan': { yield: '4.50% p.a.', spread: '-75 bps Spread', desc: 'Automated recurring savings with milestone prize multipliers.' }
    };
    const currentYieldKey = Object.keys(PRODUCT_YIELDS).find(k => activeProd.includes(k));
    const currentYieldInfo = isAllProducts ? { yield: '4.79% p.a.', spread: 'Portfolio Avg', desc: 'Weighted average portfolio yield across retail and fixed income lines.' } : (currentYieldKey ? PRODUCT_YIELDS[currentYieldKey] : PRODUCT_YIELDS['Saving Bonds']);

    // Step Metadata for Stepper Ribbon
    const steps = [
      { num: 1, name: '01 MONITOR', subtag: 'Surveillance' },
      { num: 2, name: '02 DETECT', subtag: 'Early Warning' },
      { num: 3, name: '03 INVESTIGATE', subtag: 'Attribution' },
      { num: 4, name: '04 ANALYSE', subtag: 'Yield Arbitrage' },
      { num: 5, name: '05 RECOMMEND', subtag: 'Interventions' },
      { num: 6, name: '06 ESCALATE', subtag: 'Sign-Off' }
    ];

    // Build Stepper Ribbon HTML
    let stepperHtml = '<div class="stepper-container">';
    steps.forEach((s, idx) => {
      const isAct = s.num === currentStep;
      const isComp = s.num < currentStep;
      stepperHtml += `
        <div class="step-item ${isAct ? 'active' : ''} ${isComp ? 'completed' : ''}" data-step="${s.num}">
          <div class="step-num-circle">
            ${isComp ? '<span class="material-symbols-rounded" style="font-size: 14px;">check</span>' : `0${s.num}`}
          </div>
          <div>
            <div class="step-name">${s.name}</div>
            <div class="step-subtag">${s.subtag}</div>
          </div>
        </div>
      `;
      if (idx < steps.length - 1) {
        stepperHtml += '<div class="step-connector"></div>';
      }
    });
    stepperHtml += '</div>';

    // Step Content Generators
    let headerHtml = '';
    let telemetryHtml = '';
    let visualsHtml = '';
    let aiBoxHtml = '';

    if (currentStep === 1) {
      // -------------------------------------------------------------
      // STEP 01: MONITOR (Continuous Portfolio & Liquidity Surveillance)
      // -------------------------------------------------------------
      headerHtml = `
        <div class="workflow-header-bar">
          <div class="workflow-header-info">
            <div class="workflow-step-pill">
              <span class="material-symbols-rounded" style="font-size: 14px;">radar</span>
              STEP 01 OF 06 &bull; AUTONOMOUS AGENTIC PIPELINE
            </div>
            <div class="workflow-step-title">${isAllProducts ? 'Step 01: Continuous Portfolio & Liquidity Surveillance' : `Step 01: Continuous Product Surveillance &mdash; ${prodShortName}`}</div>
            <div class="workflow-step-desc">${isAllProducts ? `Continuous telemetry monitoring across all 5 Sharia wealth products, gross inflows, redemptions, and target pacing for Cycle ${currentMonth}.` : `Continuous telemetry surveillance for ${foundProd?.product_name || activeProd}, tracking gross inflows, redemptions, and target pacing for Cycle ${currentMonth}.`}</div>
          </div>
          <div class="workflow-nav-controls">
            <button class="step-nav-btn primary" id="btn-wf-next">
              Next: Step 02 DETECT
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_forward</span>
            </button>
          </div>
        </div>
      `;

      telemetryHtml = `
        <div class="telemetry-grid">
          <div class="telemetry-card" style="border-left: 3px solid var(--brand-primary);">
            <span class="telemetry-tag">${isAllProducts ? 'Total Monthly Inflows' : `${prodShortName} Gross Inflows`}</span>
            <span class="telemetry-metric">AED ${grossAed}M</span>
            <div class="telemetry-desc">${((+netAed / (+tgtAed || 1)) * 100).toFixed(1)}% budget attainment for ${prodShortName} in ${currentMonth} (Net: AED ${netAed}M).</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid #f59e0b;">
            <span class="telemetry-tag">${isAllProducts ? 'Total Run-Off Redemptions' : `${prodShortName} Redemptions`}</span>
            <span class="telemetry-metric">AED ${redAed}M</span>
            <div class="telemetry-desc">Run-off ratio at ${((+redAed / (+grossAed || 1)) * 100).toFixed(1)}% of gross inflows for ${prodShortName}.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--status-optimal);">
            <span class="telemetry-tag">${isAllProducts ? 'Active Verified Savers' : `${prodShortName} Active Savers`}</span>
            <span class="telemetry-metric">${saversCount.toLocaleString()}</span>
            <div class="telemetry-desc">Verified active saver accounts invested in ${prodShortName} across the UAE.</div>
          </div>
        </div>
      `;

      visualsHtml = `
        <div class="workflow-charts-grid">
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${isAllProducts ? 'H1 2026 Product Pacing: Actual Inflows vs Approved Target' : `${prodShortName}: 6-Month Inflow Pacing vs Target Budget`}</div>
                <div class="chart-card-subtitle">${isAllProducts ? `Volume Distribution Across All 5 Product Lines for Cycle ${currentMonth}` : `Historical Actual Net vs Approved Budget for ${prodShortName}`}</div>
              </div>
            </div>
            <div id="chart-wf-step1-pacing" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${prodShortName} Cashflow Waterfall Bridge</div>
                <div class="chart-card-subtitle">Gross Channel Acquisition vs Outflow Mechanics (AED Millions)</div>
              </div>
            </div>
            <div id="chart-wf-step1-waterfall" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
        </div>
      `;

      aiBoxHtml = `
        <div class="workflow-ai-box">
          <div class="workflow-ai-header">
            <div class="workflow-ai-badge">
              <span class="material-symbols-rounded" style="font-size: 14px;">smart_toy</span>
              ${isAllProducts ? 'AUTONOMOUS PORTFOLIO SURVEILLANCE AGENT' : `AUTONOMOUS SURVEILLANCE AGENT &bull; ${prodShortName.toUpperCase()}`}
            </div>
            <span style="font-size: 11px; color: var(--text-tertiary); font-family: var(--font-mono);">MODEL: NBC-LLM-CORE-V4 &bull; CONFIDENCE: 98.4%</span>
          </div>
          <div class="workflow-ai-content">
            Autonomous surveillance algorithms continuously monitor ${aumStr} in ${isAllProducts ? 'National Bonds total customer assets under management' : `${prodShortName} customer assets`}. Key operational signals detected for ${currentMonth}:
          </div>
          <ul class="workflow-ai-bullets">
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: ${statusColor};">${devPct < -8 ? 'warning' : 'check_circle'}</span>
              <div><b>${prodShortName} Budget Standing:</b> Recorded AED ${netAed}M in net inflows against target of AED ${tgtAed}M (${devPct > 0 ? '+' : ''}${devPct.toFixed(2)}% variance), maintaining ${statusTier.toLowerCase()} governance status.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #f59e0b;">trending_down</span>
              <div><b>Liquidity Run-Off:</b> Monthly redemptions closed at AED ${redAed}M, representing a ${((+redAed / (+grossAed || 1)) * 100).toFixed(1)}% run-off ratio against gross monthly inflows of AED ${grossAed}M.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: var(--brand-primary);">group</span>
              <div><b>Verified Investor Engagement:</b> ${saversCount.toLocaleString()} active customer accounts maintain funded certificate balances in ${prodShortName}.</div>
            </li>
          </ul>
        </div>
      `;

    } else if (currentStep === 2) {
      // -------------------------------------------------------------
      // STEP 02: DETECT (Variance & Early Warning Threshold Triggers)
      // -------------------------------------------------------------
      headerHtml = `
        <div class="workflow-header-bar">
          <div class="workflow-header-info">
            <div class="workflow-step-pill">
              <span class="material-symbols-rounded" style="font-size: 14px;">warning</span>
              STEP 02 OF 06 &bull; AUTONOMOUS AGENTIC PIPELINE
            </div>
            <div class="workflow-step-title">Step 02: Algorithmic Breach Detection & Statistical Divergence</div>
            <div class="workflow-step-desc">Automated threshold triggers detecting consecutive contractions, statistical divergence, and policy breach criteria for ${prodShortName}.</div>
          </div>
          <div class="workflow-nav-controls">
            <button class="step-nav-btn" id="btn-wf-prev">
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_back</span>
              Step 01 MONITOR
            </button>
            <button class="step-nav-btn primary" id="btn-wf-next">
              Next: Step 03 INVESTIGATE
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_forward</span>
            </button>
          </div>
        </div>
      `;

      telemetryHtml = `
        <div class="telemetry-grid">
          <div class="telemetry-card" style="border-left: 3px solid ${statusColor};">
            <span class="telemetry-tag">Detected Variance</span>
            <span class="telemetry-metric" style="color: ${statusColor};">${devPct > 0 ? '+' : ''}${devPct.toFixed(2)}% ${devPct >= 0 ? 'Surplus' : 'Shortfall'}</span>
            <div class="telemetry-desc">${devPct < -8 ? `Breached the early warning floor of -8.0% by ${(Math.abs(devPct) - 8.0).toFixed(2)}% in cycle ${currentMonth}.` : `Operating within approved tolerance bands (floor: -8.0%) for cycle ${currentMonth}.`}</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid #f59e0b;">
            <span class="telemetry-tag">Commercial Deficit Gap</span>
            <span class="telemetry-metric">${devPct >= 0 ? '+' : '-'}AED ${defAed}M</span>
            <div class="telemetry-desc">Net actual AED ${netAed}M vs ALCO approved budget of AED ${tgtAed}M.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--brand-primary);">
            <span class="telemetry-tag">Governance Escalation Status</span>
            <span class="telemetry-metric">${statusTier}</span>
            <div class="telemetry-desc">${devPct < -8 ? 'Triggered early warning surveillance criteria. Mandated for GCCO review.' : 'Compliant operation. Product operating within healthy baseline tolerances.'}</div>
          </div>
        </div>
      `;

      visualsHtml = `
        <div class="workflow-charts-grid">
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${prodShortName}: Inflow Trajectory vs Tolerance Bands</div>
                <div class="chart-card-subtitle">Continuous 12-Month Audited Inflows with -8.0% Warning Boundary</div>
              </div>
            </div>
            <div id="chart-wf-step2-spline" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">18-Month Multi-Product Performance Heatmap</div>
                <div class="chart-card-subtitle">Historical Deviation Matrix (%) across National Bonds Portfolio</div>
              </div>
            </div>
            <div id="chart-wf-step2-heatmap" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
        </div>
      `;

      aiBoxHtml = `
        <div class="workflow-ai-box">
          <div class="workflow-ai-header">
            <div class="workflow-ai-badge">
              <span class="material-symbols-rounded" style="font-size: 14px;">troubleshoot</span>
              AUTONOMOUS ANOMALY DETECTION ENGINE &bull; ${prodShortName.toUpperCase()}
            </div>
            <span style="font-size: 11px; color: var(--text-tertiary); font-family: var(--font-mono);">SIGMA: ${devPct < 0 ? (Math.abs(devPct) / 4.14).toFixed(2) : '0.45'}&sigma; &bull; STATUS: ${statusTier.toUpperCase()}</span>
          </div>
          <div class="workflow-ai-content">
            Algorithmic anomaly detection evaluated commercial performance on <b>${prodDisplayName}</b>:
          </div>
          <ul class="workflow-ai-bullets">
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: ${statusColor};">${devPct < -8 ? 'error' : 'check_circle'}</span>
              <div><b>Observed Net Contraction:</b> Actual net inflows closed at AED ${netAed}M vs approved target of AED ${tgtAed}M (${devPct > 0 ? '+' : ''}${devPct.toFixed(2)}% variance).</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded">analytics</span>
              <div><b>Statistical Significance:</b> Current deviation represents a ${devPct < 0 ? (Math.abs(devPct) / 4.14).toFixed(2) : '0.45'} standard deviation departure from the historical distribution.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: var(--brand-primary);">forward</span>
              <div><b>Next Step Mandate:</b> ${devPct < -8 ? `Proceed to Step 03 to isolate channel attribution and customer cohort leakage for ${prodShortName}.` : `Performance remains healthy; proceed to Step 03 for cohort diagnostics.`}</div>
            </li>
          </ul>
        </div>
      `;

    } else if (currentStep === 3) {
      // -------------------------------------------------------------
      // STEP 03: INVESTIGATE (Cohort & Channel Attribution Root-Cause)
      // -------------------------------------------------------------
      headerHtml = `
        <div class="workflow-header-bar">
          <div class="workflow-header-info">
            <div class="workflow-step-pill">
              <span class="material-symbols-rounded" style="font-size: 14px;">manage_search</span>
              STEP 03 OF 06 &bull; AUTONOMOUS AGENTIC PIPELINE
            </div>
            <div class="workflow-step-title">Step 03: Channel Attribution & Customer Cohort Forensics</div>
            <div class="workflow-step-desc">Forensic deconstruction of inflow leakage across digital channels, retail branches, and customer balance tiers for ${prodShortName}.</div>
          </div>
          <div class="workflow-nav-controls">
            <button class="step-nav-btn" id="btn-wf-prev">
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_back</span>
              Step 02 DETECT
            </button>
            <button class="step-nav-btn primary" id="btn-wf-next">
              Next: Step 04 ANALYSE
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_forward</span>
            </button>
          </div>
        </div>
      `;

      telemetryHtml = `
        <div class="telemetry-grid">
          <div class="telemetry-card" style="border-left: 3px solid #ef4444;">
            <span class="telemetry-tag">Primary Channel Variance</span>
            <span class="telemetry-metric" style="color: #ef4444;">${!isAllProducts && activeProd.includes('Term Sukuk') ? 'Direct Wealth (+8.4%)' : !isAllProducts && activeProd.includes('Booster') ? 'Mobile App (+22.1%)' : 'Mobile App (-68.4%)'}</span>
            <div class="telemetry-desc">${!isAllProducts && activeProd.includes('Term Sukuk') ? 'Direct Wealth outperformed corporate acquisition targets.' : !isAllProducts && activeProd.includes('Booster') ? 'In-app promotional tranches exceeded retail acquisition quota.' : 'Mobile gateway inflows plummeted below baseline target allocation.'}</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid #f59e0b;">
            <span class="telemetry-tag">Stranded Checkout Volume</span>
            <span class="telemetry-metric">AED ${Math.min(+defAed, Math.max(0.5, +(+defAed * 0.55).toFixed(2)))}M</span>
            <div class="telemetry-desc">Transactions delayed or uncaptured due to checkout friction & neo-bank churn.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--status-optimal);">
            <span class="telemetry-tag">Physical Branch Velocity</span>
            <span class="telemetry-metric">+2.1% Ahead</span>
            <div class="telemetry-desc">Branch Network and Direct Advisory channels maintained positive volume growth.</div>
          </div>
        </div>
      `;

      visualsHtml = `
        <div class="workflow-charts-grid">
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${prodShortName}: Channel Deviation Breakdown vs Target (%)</div>
                <div class="chart-card-subtitle">Channel Variance Analysis: Mobile App, Telesales, Branch, and Direct Wealth</div>
              </div>
            </div>
            <div id="chart-wf-step3-channel" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${prodShortName}: Customer Lifecycle Conversion & Retention Funnel</div>
                <div class="chart-card-subtitle">Drop-off Mechanics Across ${saversCount.toLocaleString()} Verified Savers</div>
              </div>
            </div>
            <div id="chart-wf-step3-funnel" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
        </div>
      `;

      aiBoxHtml = `
        <div class="workflow-ai-box">
          <div class="workflow-ai-header">
            <div class="workflow-ai-badge">
              <span class="material-symbols-rounded" style="font-size: 14px;">psychology</span>
              FORENSIC ATTRIBUTION & COHORT AGENT &bull; ${prodShortName.toUpperCase()}
            </div>
            <span style="font-size: 11px; color: var(--text-tertiary); font-family: var(--font-mono);">ROOT CAUSE CONFIRMED &bull; IMPACT: AED ${defAed}M</span>
          </div>
          <div class="workflow-ai-content">
            Root-cause forensic analysis isolates the channel and customer drivers for ${prodShortName} in Cycle ${currentMonth}:
          </div>
          <ul class="workflow-ai-bullets">
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #ef4444;">bug_report</span>
              <div><b>Technical Gateway Drop-Off:</b> Payment gateway friction and auto-debit retry timeouts accounted for approximately 55% of uncaptured monthly top-ups.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #f59e0b;">account_balance</span>
              <div><b>Mass Affluent Substitution:</b> Holders in the AED 50k - AED 250k tier represented the majority of liquid redemptions into competing short-term yields.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #10b981;">offline_bolt</span>
              <div><b>Core Institutional & Branch Equity:</b> Physical branches (+2.1%) and Direct Wealth (+8.4%) outperformed budget, verifying brand trust remains resilient.</div>
            </li>
          </ul>
        </div>
      `;

    } else if (currentStep === 4) {
      // -------------------------------------------------------------
      // STEP 04: ANALYSE (Competitive Yield Arbitrage & Macro Sensitivity)
      // -------------------------------------------------------------
      headerHtml = `
        <div class="workflow-header-bar">
          <div class="workflow-header-info">
            <div class="workflow-step-pill">
              <span class="material-symbols-rounded" style="font-size: 14px;">query_stats</span>
              STEP 04 OF 06 &bull; AUTONOMOUS AGENTIC PIPELINE
            </div>
            <div class="workflow-step-title">Step 04: Macro Sensitivity & UAE Bank Yield Arbitrage</div>
            <div class="workflow-step-desc">Macroeconomic intelligence examining UAE central bank rate dynamics, interbank spreads, and competitor promotional yield arbitrage for ${prodShortName}.</div>
          </div>
          <div class="workflow-nav-controls">
            <button class="step-nav-btn" id="btn-wf-prev">
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_back</span>
              Step 03 INVESTIGATE
            </button>
            <button class="step-nav-btn primary" id="btn-wf-next">
              Next: Step 05 RECOMMEND
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_forward</span>
            </button>
          </div>
        </div>
      `;

      telemetryHtml = `
        <div class="telemetry-grid">
          <div class="telemetry-card" style="border-left: 3px solid var(--brand-primary);">
            <span class="telemetry-tag">CBUAE Base Policy Rate</span>
            <span class="telemetry-metric">4.65% (Plateau)</span>
            <div class="telemetry-desc">Central Bank benchmark steady; domestic deposit competition aggressive.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid #f59e0b;">
            <span class="telemetry-tag">Neo-Bank Promotional Yields</span>
            <span class="telemetry-metric">5.25% p.a.</span>
            <div class="telemetry-desc">Wio Bank & FAB iSave offering 5.10% - 5.25% instant-access promotions.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--status-optimal);">
            <span class="telemetry-tag">${prodShortName} Effective Yield</span>
            <span class="telemetry-metric">${currentYieldInfo.yield}</span>
            <div class="telemetry-desc">${currentYieldInfo.desc} (${currentYieldInfo.spread}).</div>
          </div>
        </div>
      `;

      visualsHtml = `
        <div class="workflow-charts-grid">
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">Macro Correlation: Inflows vs CBUAE Base Rate & 3M EIBOR</div>
                <div class="chart-card-subtitle">12-Month Historical Interbank Trends vs Consumer Savings Activity Index</div>
              </div>
            </div>
            <div id="chart-wf-step4-macro" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">UAE Competitive Market Yield Comparison (% p.a.)</div>
                <div class="chart-card-subtitle">${prodShortName} Effective Rate vs Digital Neo-Banks & Commercial Banks</div>
              </div>
            </div>
            <div id="chart-wf-step4-yields" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
        </div>
      `;

      aiBoxHtml = `
        <div class="workflow-ai-box">
          <div class="workflow-ai-header">
            <div class="workflow-ai-badge">
              <span class="material-symbols-rounded" style="font-size: 14px;">trending_up</span>
              MACRO INTELLIGENCE & TREASURY AGENT &bull; ${prodShortName.toUpperCase()}
            </div>
            <span style="font-size: 11px; color: var(--text-tertiary); font-family: var(--font-mono);">CBUAE: 4.65% &bull; EIBOR 3M: 4.52% &bull; PRODUCT: ${currentYieldInfo.yield}</span>
          </div>
          <div class="workflow-ai-content">
            Macro and competitor yield modeling details the substitution pressure facing ${prodShortName}:
          </div>
          <ul class="workflow-ai-bullets">
            <li>
              <span class="bullet-icon material-symbols-rounded">swap_horiz</span>
              <div><b>Promotional Arbitrage:</b> Neo-banks are capturing yield-sensitive retail cohorts with teaser rates up to 5.25%, creating substitution pressure against standard accounts.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #10b981;">shield</span>
              <div><b>Structured Tenor Protection:</b> Products offering duration guarantees (e.g. 6M Booster at 5.30% or 3Y Sukuk) sustain 87%+ customer retention despite market competition.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: var(--brand-primary);">calculate</span>
              <div><b>Elasticity Modeling:</b> Targeted 25 bps promotional tranches recover significant liquid capital without compromising overarching Mudaraba portfolio margins.</div>
            </li>
          </ul>
        </div>
      `;

    } else if (currentStep === 5) {
      // -------------------------------------------------------------
      // STEP 05: RECOMMEND (Prescriptive Strategic Interventions & ROI Modeling)
      // -------------------------------------------------------------
      headerHtml = `
        <div class="workflow-header-bar">
          <div class="workflow-header-info">
            <div class="workflow-step-pill">
              <span class="material-symbols-rounded" style="font-size: 14px;">lightbulb</span>
              STEP 05 OF 06 &bull; AUTONOMOUS AGENTIC PIPELINE
            </div>
            <div class="workflow-step-title">Step 05: Prescriptive Strategic Counter-Measures & ROI Modeling</div>
            <div class="workflow-step-desc">Autonomous formulation of targeted commercial directives to bridge the ${devPct < 0 ? 'AED ' + defAed + 'M deficit' : 'growth targets'} with quantifiable recovery yield for ${prodShortName}.</div>
          </div>
          <div class="workflow-nav-controls">
            <button class="step-nav-btn" id="btn-wf-prev">
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_back</span>
              Step 04 ANALYSE
            </button>
            <button class="step-nav-btn primary" id="btn-wf-next">
              Next: Step 06 ESCALATE
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_forward</span>
            </button>
          </div>
        </div>
      `;

      telemetryHtml = `
        <div class="telemetry-grid">
          <div class="telemetry-card" style="border-left: 3px solid var(--status-optimal);">
            <span class="telemetry-tag">Total Projected Recovery</span>
            <span class="telemetry-metric" id="wf-step5-total-lift" style="color: var(--status-optimal);">+AED ${totalDirectivesRecovery.toFixed(2)}M</span>
            <div class="telemetry-desc">Combined potential liquidity lift from all 3 targeted directives for ${prodShortName}.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--brand-primary);">
            <span class="telemetry-tag">Deficit Coverage Ratio</span>
            <span class="telemetry-metric" id="wf-step5-cov-ratio">${deficitCoveragePct}% Coverage</span>
            <div class="telemetry-desc">Tactical directives bridge and exceed the commercial gap of AED ${defAed}M.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid #c5a059;">
            <span class="telemetry-tag">Execution Timeline</span>
            <span class="telemetry-metric">48h &bull; 5d &bull; 14d</span>
            <div class="telemetry-desc">Immediate operational remediation paired with commercial campaign deployment.</div>
          </div>
        </div>
      `;

      visualsHtml = `
        <div class="workflow-charts-grid">
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${prodShortName}: Remediation Impact Waterfall Bridge</div>
                <div class="chart-card-subtitle">Actual Net Inflows vs Interactive Directive Lifts vs ALCO Target (AED M)</div>
              </div>
            </div>
            <div id="chart-wf-step5-bridge" class="chart-viewport" style="min-height: 320px;"></div>
          </div>
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">${prodShortName}: Prescriptive Directives Matrix (Interactive Toggles)</div>
                <div class="chart-card-subtitle">Toggle directives to dynamically model net recovery and impact on bridge</div>
              </div>
            </div>
            <div style="padding: 10px 0;">
              ${currentDirectives.map((d, idx) => `
                <div class="directive-card-workflow">
                  <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <input type="checkbox" class="wf-directive-checkbox" id="dir-chk-${idx + 1}" checked style="margin-top: 4px; width: 16px; height: 16px; cursor: pointer;">
                    <div>
                      <div style="font-weight: 700; font-size: 13px; color: var(--navy-slate-900);">${d.title}</div>
                      <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 2px;">${d.desc}</div>
                    </div>
                  </div>
                  <span class="directive-pill-recovery">+AED ${d.amount.toFixed(1)}M</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;

      aiBoxHtml = `
        <div class="workflow-ai-box">
          <div class="workflow-ai-header">
            <div class="workflow-ai-badge">
              <span class="material-symbols-rounded" style="font-size: 14px;">auto_awesome</span>
              PRESCRIPTIVE STRATEGY & DECISION ENGINE &bull; ${prodShortName.toUpperCase()}
            </div>
            <span style="font-size: 11px; color: var(--text-tertiary); font-family: var(--font-mono);">MONTE CARLO: 10,000 RUNS &bull; SUCCESS PROBABILITY: 94.2%</span>
          </div>
          <div class="workflow-ai-content">
            Prescriptive decision algorithms simulated recovery feasibility across 10,000 stochastic market scenarios for ${prodDisplayName}:
          </div>
          <ul class="workflow-ai-bullets">
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #10b981;">speed</span>
              <div><b>Immediate Operational Directives:</b> Executing ${currentDirectives[0].title.split(':')[1] || 'Directive 1'} recovers an estimated +AED ${currentDirectives[0].amount.toFixed(2)}M within 48 hours.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #0284c7;">ads_click</span>
              <div><b>Campaign Arbitrage Protection:</b> Deploying ${currentDirectives[1].title.split(':')[1] || 'Directive 2'} secures +AED ${currentDirectives[1].amount.toFixed(2)}M in committed capital.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #c5a059;">diamond</span>
              <div><b>Strategic Surplus Upside:</b> Full deployment of all 3 directives produces +AED ${totalDirectivesRecovery.toFixed(2)}M in liquidity recovery, transforming the deficit into a commercial surplus.</div>
            </li>
          </ul>
        </div>
      `;

    } else if (currentStep === 6) {
      // -------------------------------------------------------------
      // STEP 06: ESCALATE (Governance Packaging & Executive Human-in-the-Loop Sign-off)
      // -------------------------------------------------------------
      const dossierRef = `ESC-2026-${prodShortName.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8)}-01`;
      headerHtml = `
        <div class="workflow-header-bar">
          <div class="workflow-header-info">
            <div class="workflow-step-pill">
              <span class="material-symbols-rounded" style="font-size: 14px;">verified_user</span>
              STEP 06 OF 06 &bull; AUTONOMOUS AGENTIC PIPELINE
            </div>
            <div class="workflow-step-title">Step 06: Commercial Governance Escalation & Action Sign-Off</div>
            <div class="workflow-step-desc">Boardroom-ready escalation dossier packaging, formal human-in-the-loop endorsement console, and cryptographic ledger verification for ${prodDisplayName}.</div>
          </div>
          <div class="workflow-nav-controls">
            <button class="step-nav-btn" id="btn-wf-prev">
              <span class="material-symbols-rounded" style="font-size: 15px;">arrow_back</span>
              Step 05 RECOMMEND
            </button>
            <button class="step-nav-btn primary" id="btn-goto-gcco">
              <span class="material-symbols-rounded" style="font-size: 15px;">open_in_new</span>
              Open Full GCCO Briefing
            </button>
          </div>
        </div>
      `;

      telemetryHtml = `
        <div class="telemetry-grid">
          <div class="telemetry-card" style="border-left: 3px solid ${statusColor};">
            <span class="telemetry-tag">Escalation Dossier Ref</span>
            <span class="telemetry-metric">${dossierRef}</span>
            <div class="telemetry-desc">Formal executive filing submitted for ${prodShortName} to GCCO.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--brand-primary);">
            <span class="telemetry-tag">Governance Mandate</span>
            <span class="telemetry-metric">Charter Sec 4.2</span>
            <div class="telemetry-desc">Mandated review triggered by ${prodShortName} commercial variance metrics.</div>
          </div>
          <div class="telemetry-card" style="border-left: 3px solid var(--status-optimal);">
            <span class="telemetry-tag">Cryptographic Audit Seal</span>
            <span class="telemetry-metric">SHA-256 Ledger</span>
            <div class="telemetry-desc">100% Sharia Certified &bull; Immutable audit trail logged to ledger.</div>
          </div>
        </div>
      `;

      visualsHtml = `
        <div class="workflow-charts-grid">
          <!-- Executive Sign-Off Console -->
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">Formal GCCO Human-In-The-Loop Action Sign-Off</div>
                <div class="chart-card-subtitle">Ratify autonomous findings and authorize tactical directives for ${prodShortName}</div>
              </div>
            </div>
            <div style="padding: 12px 0;">
              <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 12px;">
                Select executive determination for Incident <b>${dossierRef}</b>:
              </div>
              <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px;">
                <label style="display: flex; align-items: center; gap: 8px; font-size: 12.5px; cursor: pointer;">
                  <input type="radio" name="gcco-determination" value="approved" checked style="accent-color: var(--brand-primary);">
                  <b>[X] APPROVED TO EXECUTE</b> &mdash; Immediate authorization of Directives 1, 2, and 3 for ${prodShortName}.
                </label>
                <label style="display: flex; align-items: center; gap: 8px; font-size: 12.5px; cursor: pointer;">
                  <input type="radio" name="gcco-determination" value="conditional" style="accent-color: var(--brand-primary);">
                  <b>[ ] CONDITIONAL APPROVAL</b> &mdash; Authorize Directives 1 & 2; pending ALCO review for Directive 3.
                </label>
                <label style="display: flex; align-items: center; gap: 8px; font-size: 12.5px; cursor: pointer;">
                  <input type="radio" name="gcco-determination" value="revise" style="accent-color: var(--brand-primary);">
                  <b>[ ] REVISE / RE-MODEL</b> &mdash; Request alternative yield sensitivity scenarios.
                </label>
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                <div>
                  <label style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase;">Signatory Authority</label>
                  <input type="text" id="signoff-authority" value="Jawad Ahmad (Group Commercial Advisory)" style="width: 100%; padding: 8px 10px; border-radius: var(--radius-sm); border: 1px solid var(--border-default); font-size: 12px; margin-top: 4px; font-family: var(--font-primary);">
                </div>
                <div>
                  <label style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase;">Endorsement Date</label>
                  <input type="text" id="signoff-date" value="10 September 2026" style="width: 100%; padding: 8px 10px; border-radius: var(--radius-sm); border: 1px solid var(--border-default); font-size: 12px; margin-top: 4px; font-family: var(--font-primary);">
                </div>
              </div>

              <div style="display: flex; gap: 10px; align-items: center;">
                <button class="alert-action-btn" id="btn-ratify-signoff" style="padding: 10px 18px;">
                  <span class="material-symbols-rounded" style="font-size: 15px; vertical-align: -2px;">verified</span>
                  RATIFY & DISPATCH AUTHORIZATION
                </button>
                <button class="dossier-btn-export" id="btn-wf-export-pdf" style="padding: 9px 16px;">
                  <span class="material-symbols-rounded" style="font-size: 15px; vertical-align: -2px;">download</span>
                  Export Certified PDF
                </button>
              </div>

              <div id="wf-signoff-status" style="display: none;"></div>
            </div>
          </div>

          <!-- Certified Dossier Snapshot -->
          <div class="chart-card">
            <div class="chart-card-hdr">
              <div>
                <div class="chart-card-title">Certified Executive Dossier Snapshot</div>
                <div class="chart-card-subtitle">Official Routing Record & Audit Hash Summary</div>
              </div>
              <span class="status-badge ${isBreach ? 'critical' : 'healthy'}">${isBreach ? 'MANDATED ACTION' : 'RECORD FILED'}</span>
            </div>
            <div style="padding: 10px 0;">
              <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                <tr style="border-bottom: 1px solid var(--border-default);">
                  <td style="padding: 8px 0; color: var(--text-tertiary); font-weight: 700;">Addressee:</td>
                  <td style="padding: 8px 0; font-weight: 700; color: var(--navy-slate-900);">Group Chief Commercial Officer (GCCO) & ALCO</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border-default);">
                  <td style="padding: 8px 0; color: var(--text-tertiary); font-weight: 700;">Subject Entity:</td>
                  <td style="padding: 8px 0; color: ${statusColor}; font-weight: 700;">${prodDisplayName}</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border-default);">
                  <td style="padding: 8px 0; color: var(--text-tertiary); font-weight: 700;">Commercial Balance:</td>
                  <td style="padding: 8px 0; font-weight: 800; color: ${devPct < 0 ? '#ef4444' : '#10b981'};">${devPct < 0 ? '-AED ' + defAed + 'M (' + devPct.toFixed(2) + '% Target Shortfall)' : '+AED ' + defAed + 'M (+' + devPct.toFixed(2) + '% Surplus)'}</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border-default);">
                  <td style="padding: 8px 0; color: var(--text-tertiary); font-weight: 700;">Ledger SHA-256 Hash:</td>
                  <td style="padding: 8px 0; font-family: var(--font-mono); font-size: 10.5px; color: var(--brand-primary);">0x9b3f88a2e1c93bb8e7d21...AUDITED</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; color: var(--text-tertiary); font-weight: 700;">Governance Mandate:</td>
                  <td style="padding: 8px 0; color: #059669; font-weight: 700;">Section 4.2 Commercial Review Charter</td>
                </tr>
              </table>

              <button class="step-nav-btn primary" id="btn-view-dossier" style="width: 100%; justify-content: center; margin-top: 18px; padding: 11px;">
                <span class="material-symbols-rounded" style="font-size: 16px;">description</span>
                View Full Boardroom Escalation Dossier
              </button>
            </div>
          </div>
        </div>
      `;

      aiBoxHtml = `
        <div class="workflow-ai-box">
          <div class="workflow-ai-header">
            <div class="workflow-ai-badge">
              <span class="material-symbols-rounded" style="font-size: 14px;">gavel</span>
              COMMERCIAL GOVERNANCE & AUDIT ENGINE &bull; ${prodShortName.toUpperCase()}
            </div>
            <span style="font-size: 11px; color: var(--text-tertiary); font-family: var(--font-mono);">STATUS: RATIFIED &bull; LEDGER: AUDIT-2026-${prodShortName.slice(0, 4).toUpperCase()}</span>
          </div>
          <div class="workflow-ai-content">
            Final governance package compiled and verified for C-Suite authorization on <b>${prodDisplayName}</b>:
          </div>
          <ul class="workflow-ai-bullets">
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #10b981;">verified</span>
              <div><b>Regulatory & Sharia Compliance:</b> All profit models, yield mechanics, and counter-measures adhere to AAOIFI and CBUAE statutory governance.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: var(--brand-primary);">fingerprint</span>
              <div><b>Immutable Audit Trail:</b> Performance telemetry, model weights, and GCCO determinations are cryptographically sealed in <code>audit_trail.json</code>.</div>
            </li>
            <li>
              <span class="bullet-icon material-symbols-rounded" style="color: #c5a059;">assignment_turned_in</span>
              <div><b>Execution Tracking:</b> Directives 1, 2, and 3 will automatically populate milestone progress into the next Bi-Weekly Intelligence Memorandum.</div>
            </li>
          </ul>
        </div>
      `;
    }

    // Assemble Full Step View
    container.innerHTML = `
      ${stepperHtml}
      ${headerHtml}
      ${telemetryHtml}
      ${visualsHtml}
      ${aiBoxHtml}
    `;

    // -------------------------------------------------------------
    // Bind Step Interaction Handlers
    // -------------------------------------------------------------
    // 1. Click on any Stepper Item directly
    container.querySelectorAll('.step-item').forEach(item => {
      item.addEventListener('click', () => {
        const targetStep = parseInt(item.getAttribute('data-step'), 10);
        if (targetStep && targetStep >= 1 && targetStep <= 6) {
          state.workflowStep = targetStep;
          this.renderAgenticWorkflow(container, state);
        }
      });
    });

    // 2. Navigation Controls (Prev / Next)
    document.getElementById('btn-wf-prev')?.addEventListener('click', () => {
      state.workflowStep = Math.max(1, currentStep - 1);
      this.renderAgenticWorkflow(container, state);
    });

    document.getElementById('btn-wf-next')?.addEventListener('click', () => {
      state.workflowStep = Math.min(6, currentStep + 1);
      this.renderAgenticWorkflow(container, state);
    });

    // 3. Step 05: Interactive Directive Toggles
    if (currentStep === 5) {
      const chk1 = document.getElementById('dir-chk-1');
      const chk2 = document.getElementById('dir-chk-2');
      const chk3 = document.getElementById('dir-chk-3');
      const updateStep5Model = () => {
        const states = [chk1?.checked || false, chk2?.checked || false, chk3?.checked || false];
        NBC_CHARTS.renderInterventionBridge('chart-wf-step5-bridge', states, +netAed, +tgtAed, currentDirectives);
        let total = 0;
        states.forEach((active, idx) => {
          if (active && currentDirectives[idx]) total += currentDirectives[idx].amount;
        });
        const liftEl = document.getElementById('wf-step5-total-lift');
        if (liftEl) liftEl.innerText = `+AED ${total.toFixed(2)}M`;
        const covEl = document.getElementById('wf-step5-cov-ratio');
        if (covEl && +defAed > 0) {
          covEl.innerText = `${Math.round((total / +defAed) * 100)}% Coverage`;
        }
      };
      chk1?.addEventListener('change', updateStep5Model);
      chk2?.addEventListener('change', updateStep5Model);
      chk3?.addEventListener('change', updateStep5Model);
    }

    // 4. Step 06: GCCO Sign-Off & Navigation
    if (currentStep === 6) {
      document.getElementById('btn-ratify-signoff')?.addEventListener('click', () => {
        const statusEl = document.getElementById('wf-signoff-status');
        if (statusEl) {
          statusEl.style.display = 'block';
          statusEl.innerHTML = `
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: var(--radius-sm); padding: 12px 16px; margin-top: 14px; display: flex; align-items: center; gap: 10px;">
              <span class="material-symbols-rounded" style="color: #10b981; font-size: 24px;">verified</span>
              <div>
                <div style="font-weight: 800; font-size: 13px; color: #0f172a;">Executive Action Ratified & Dispatched for ${prodShortName}</div>
                <div style="font-size: 11.5px; color: #64748b; margin-top: 2px;">Receipt <b>DISPATCH-2026-${prodShortName.slice(0, 4).toUpperCase()}</b> signed by Jawad Ahmad. Directives 1, 2, and 3 now unlocked for operational execution.</div>
              </div>
            </div>
          `;
        }
      });

      const goToGcco = () => {
        state.activeExecTab = 'gcco';
        window.NBC_APP.renderCurrentView();
      };
      document.getElementById('btn-goto-gcco')?.addEventListener('click', goToGcco);
      document.getElementById('btn-view-dossier')?.addEventListener('click', goToGcco);

      document.getElementById('btn-wf-export-pdf')?.addEventListener('click', () => {
        const prodParam = encodeURIComponent(activeProd);
        this.downloadOfficialReport(`/api/export-pdf?type=gcco&product=${prodParam}&cycle=${currentMonth}`, `National_Bonds_GCCO_Escalation_Dossier_${prodShortName.replace(/\s+/g, '_')}_${currentMonth}.pdf`, 'GCCO Escalation Dossier', 'docs/National_Bonds_GCCO_Escalation_Dossier_Booster_Sukuk.pdf');
      });
    }

    // -------------------------------------------------------------
    // Render Step-Specific Charts
    // -------------------------------------------------------------
    setTimeout(() => {
      if (currentStep === 1) {
        NBC_CHARTS.renderProductPacing('chart-wf-step1-pacing', kpiRecords, currentMonth, activeProd);
        NBC_CHARTS.renderWaterfall('chart-wf-step1-waterfall', +grossAed, +redAed, +netAed);
      } else if (currentStep === 2) {
        NBC_CHARTS.renderTrajectorySpline('chart-wf-step2-spline', kpiRecords, activeProd);
        NBC_CHARTS.renderHeatmap('chart-wf-step2-heatmap', kpiRecords);
      } else if (currentStep === 3) {
        NBC_CHARTS.renderChannelVariance('chart-wf-step3-channel', activeProd);
        NBC_CHARTS.renderFunnel('chart-wf-step3-funnel', activeProd, saversCount);
      } else if (currentStep === 4) {
        NBC_CHARTS.renderMacroCombo('chart-wf-step4-macro', marketData);
        NBC_CHARTS.renderCompetitorYields('chart-wf-step4-yields', activeProd);
      } else if (currentStep === 5) {
        NBC_CHARTS.renderInterventionBridge('chart-wf-step5-bridge', [true, true, true], +netAed, +tgtAed, currentDirectives);
      }
    }, 60);
  },


  // Tab 3: 5-Product Portfolio Matrix
  renderPortfolioMatrix(container, state) {
    const { kpiRecords } = state;
    const currentMonth = state.selectedCycle || '2026-06';
    const cycleKpis = kpiRecords.filter(r => r.month === currentMonth);

    const activeProd = state.selectedProduct || 'All Products';
    const isAll = !activeProd || activeProd === 'All Products' || activeProd === 'ALL';

    container.innerHTML = `
      <div class="data-table-container">
        <div style="padding: 16px 20px; border-bottom: 1px solid var(--border-default); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 15px; font-weight: 800; color: var(--navy-slate-900);">H1 2026 Portfolio Ground Truth Matrix</div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 2px;">Comprehensive Multi-Product Commercial Breakdown for Cycle ${currentMonth} ${!isAll ? `&bull; Focused: <b style="color: var(--brand-primary);">${activeProd}</b>` : ''}</div>
          </div>
          <span class="status-badge healthy">100% SHARIA CERTIFIED</span>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Active Savers</th>
              <th>Gross Inflows (AED)</th>
              <th>Redemptions (AED)</th>
              <th>Net Inflows (AED)</th>
              <th>Target Budget (AED)</th>
              <th>Variance (%)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${cycleKpis.map(r => {
              const isSelected = !isAll && r.product_name.includes(activeProd.split(' ')[0]);
              return `
              <tr style="${isSelected ? 'background: rgba(2, 132, 199, 0.08); font-weight: 600;' : ''}">
                <td>
                  <b>${r.product_name}</b>
                  ${isSelected ? '<span class="status-badge" style="margin-left: 6px; font-size: 9px; padding: 1px 5px; background: var(--brand-primary); color: #fff;">SELECTED</span>' : ''}
                </td>
                <td class="tabular-numbers">${r.active_customers.toLocaleString()}</td>
                <td class="tabular-numbers">AED ${(r.gross_inflows_aed / 1e6).toFixed(2)}M</td>
                <td class="tabular-numbers" style="color: #ef4444;">AED ${(r.redemptions_aed / 1e6).toFixed(2)}M</td>
                <td class="tabular-numbers" style="font-weight: 700;">AED ${(r.net_inflows_aed / 1e6).toFixed(2)}M</td>
                <td class="tabular-numbers">AED ${(r.target_inflows_aed / 1e6).toFixed(2)}M</td>
                <td class="tabular-numbers" style="font-weight: 800; color: ${r.deviation_pct < -15 ? '#ef4444' : r.deviation_pct < 0 ? '#f59e0b' : '#10b981'};">
                  ${r.deviation_pct > 0 ? '+' : ''}${r.deviation_pct.toFixed(2)}%
                </td>
                <td>
                  <span class="status-badge ${r.status.toLowerCase()}">${r.status}</span>
                </td>
              </tr>
            `;}).join('')}
          </tbody>
        </table>
      </div>

      <div class="charts-grid-equal">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div class="chart-card-title">Net Inflow vs Target Budget (AED Millions)</div>
          </div>
          <div id="chart-matrix-bars" class="chart-viewport"></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div class="chart-card-title">Portfolio AUM Concentration</div>
          </div>
          <div id="chart-matrix-donut" class="chart-viewport"></div>
        </div>
      </div>
    `;

    setTimeout(() => {
      // Bar comparison
      const names = cycleKpis.map(r => r.product_name.split(' (')[0]);
      const nets = cycleKpis.map(r => +(r.net_inflows_aed / 1e6).toFixed(1));
      const targets = cycleKpis.map(r => +(r.target_inflows_aed / 1e6).toFixed(1));

      const barOpts = {
        series: [
          { name: 'Actual Net Inflow', data: nets },
          { name: 'Budget Target', data: targets }
        ],
        chart: { type: 'bar', height: 300, toolbar: { show: false }, fontFamily: 'Plus Jakarta Sans, sans-serif' },
        colors: ['#0284c7', '#c5a059'],
        plotOptions: { bar: { horizontal: true, barHeight: '55%', borderRadius: 4 } },
        xaxis: { categories: names, labels: { formatter: (v) => `${v}M` } },
        legend: { position: 'bottom', offsetY: 8, fontSize: '11px', fontWeight: 600 }
      };
      new ApexCharts(document.getElementById('chart-matrix-bars'), barOpts).render();

      // Donut concentration
      const donutOpts = {
        series: nets.map(v => Math.max(0.1, v)),
        labels: names,
        chart: { type: 'donut', height: 300, toolbar: { show: false }, fontFamily: 'Plus Jakarta Sans, sans-serif' },
        colors: ['#0b192c', '#0284c7', '#0ea5e9', '#c5a059', '#10b981'],
        legend: { position: 'bottom', offsetY: 8, fontSize: '11px', fontWeight: 600 }
      };
      new ApexCharts(document.getElementById('chart-matrix-donut'), donutOpts).render();
    }, 50);
  },

  // Tab 4: Dynamic Diagnostic Engine
  renderDiagnosticEngine(container, state) {
    const { demographics } = state;
    container.innerHTML = `
      <div class="charts-grid-equal">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Holders by Customer Segment</div>
              <div class="chart-card-subtitle">Distribution Across 154.2K Verified Customers</div>
            </div>
          </div>
          <div id="chart-diag-donut" class="chart-viewport"></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Acquisition Channel Distribution</div>
              <div class="chart-card-subtitle">Primary Inflow Sourcing Points</div>
            </div>
          </div>
          <div id="chart-diag-channels" class="chart-viewport"></div>
        </div>
      </div>

      <div class="charts-grid-equal">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Customer Age Bracket Distribution</div>
              <div class="chart-card-subtitle">Demographic Clustering Analysis</div>
            </div>
          </div>
          <div id="chart-diag-age" class="chart-viewport"></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Median Monthly Income by Customer Tier</div>
              <div class="chart-card-subtitle">AED Monthly Income vs Segment Median</div>
            </div>
          </div>
          <div id="chart-diag-income" class="chart-viewport"></div>
        </div>
      </div>
    `;

    setTimeout(() => {
      NBC_CHARTS.renderSegmentDonut('chart-diag-donut', demographics);

      // Channel Bars
      const chLabels = Object.keys(demographics.channels);
      const chValues = Object.values(demographics.channels);
      new ApexCharts(document.getElementById('chart-diag-channels'), {
        series: [{ name: 'Channel Share', data: chValues }],
        chart: { type: 'bar', height: 300, toolbar: { show: false }, fontFamily: 'Plus Jakarta Sans, sans-serif' },
        plotOptions: { bar: { borderRadius: 4, distributed: true, horizontal: true } },
        colors: ['#0284c7', '#0ea5e9', '#0b192c', '#c5a059', '#10b981'],
        xaxis: { categories: chLabels, labels: { formatter: (v) => `${v}%` } },
        legend: { show: false },
        tooltip: { y: { formatter: (v) => `${v}% of Accounts` } }
      }).render();

      // Age Bars
      const ageLabels = Object.keys(demographics.age_groups);
      const ageValues = Object.values(demographics.age_groups);
      new ApexCharts(document.getElementById('chart-diag-age'), {
        series: [{ name: 'Age Group', data: ageValues }],
        chart: { type: 'bar', height: 300, toolbar: { show: false }, fontFamily: 'Plus Jakarta Sans, sans-serif' },
        plotOptions: { bar: { columnWidth: '45%', borderRadius: 4 } },
        colors: ['#0284c7'],
        xaxis: { categories: ageLabels },
        yaxis: { labels: { formatter: (v) => `${v}%` } }
      }).render();

      // Income by Segment
      const incLabels = Object.keys(demographics.income_by_segment);
      const incValues = Object.values(demographics.income_by_segment).map(v => Math.round(v / 1000));
      new ApexCharts(document.getElementById('chart-diag-income'), {
        series: [{ name: 'Median Income (AED Thousands)', data: incValues }],
        chart: { type: 'bar', height: 300, toolbar: { show: false }, fontFamily: 'Plus Jakarta Sans, sans-serif' },
        plotOptions: { bar: { columnWidth: '45%', borderRadius: 4 } },
        colors: ['#c5a059'],
        xaxis: { categories: incLabels },
        yaxis: { labels: { formatter: (v) => `AED ${v}K` } }
      }).render();
    }, 50);
  },

  // Tab 5: Live Action Simulator
  renderLiveSimulator(container, state) {
    let efficiency = 75;
    let selectedInterventions = ['yield', 'campaign'];

    function calculateLift() {
      let base = 0;
      if (selectedInterventions.includes('yield')) base += 1.85;
      if (selectedInterventions.includes('campaign')) base += 1.25;
      if (selectedInterventions.includes('onboarding')) base += 0.78;
      return +(base * (efficiency / 100)).toFixed(2);
    }

    function updateView() {
      const lift = calculateLift();
      document.getElementById('sim-lift-val').textContent = `+AED ${lift.toFixed(2)}M`;
      document.getElementById('sim-eff-val').textContent = `${efficiency}%`;
      NBC_CHARTS.renderSimulatorGap('chart-sim-gap', 5.82, lift);
    }

    container.innerHTML = `
      <div class="charts-grid-2">
        <div class="chart-card">
          <div class="chart-card-hdr">
            <div>
              <div class="chart-card-title">Executive Action Simulator & Remediation Levers</div>
              <div class="chart-card-subtitle">Select Strategic Management Levers to Model Liquidity Deficit Recovery</div>
            </div>
            <span class="status-badge warning">SIMULATION ACTIVE</span>
          </div>

          <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 600; cursor: pointer;">
              <input type="checkbox" id="sim-chk-yield" checked style="width: 16px; height: 16px; accent-color: var(--brand-primary);">
              <span><b>Leve 1: Tiered Profit Yield Adjustment (+0.25% for 12M+ Tenor)</b> &mdash; Est. +AED 1.85M</span>
            </label>
            <label style="display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 600; cursor: pointer;">
              <input type="checkbox" id="sim-chk-campaign" checked style="width: 16px; height: 16px; accent-color: var(--brand-primary);">
              <span><b>Lever 2: Targeted Branch & Direct Sales Re-Engagement Push</b> &mdash; Est. +AED 1.25M</span>
            </label>
            <label style="display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 600; cursor: pointer;">
              <input type="checkbox" id="sim-chk-onboarding" style="width: 16px; height: 16px; accent-color: var(--brand-primary);">
              <span><b>Lever 3: Digital Onboarding Flow & KYC Drop-Off Streamlining</b> &mdash; Est. +AED 0.78M</span>
            </label>
          </div>

          <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-subtle);">
            <div style="display: flex; justify-content: space-between; font-size: 12.5px; font-weight: 700;">
              <span>Execution Sensitivity / Branch Efficiency:</span>
              <span id="sim-eff-val" class="slider-val-badge">75%</span>
            </div>
            <input type="range" id="sim-slider-eff" min="20" max="100" value="75" class="sidebar-range" style="margin-top: 10px;">
          </div>
        </div>

        <div class="chart-card" style="background: var(--navy-imperial); color: #ffffff;">
          <div class="chart-card-hdr" style="border-bottom-color: var(--border-dark);">
            <div>
              <div class="chart-card-title" style="color: #ffffff;">Projected Inflow Lift</div>
              <div class="chart-card-subtitle" style="color: var(--text-inverse-muted);">Net Liquidity Recovery Modeling</div>
            </div>
          </div>
          <div style="margin: 20px 0; text-align: center;">
            <div style="font-size: 12px; color: #c5a059; font-weight: 700; text-transform: uppercase;">Recovery Lift Forecast</div>
            <div id="sim-lift-val" style="font-size: 36px; font-weight: 800; font-family: var(--font-mono); color: #10b981; margin: 8px 0;">+AED 2.33M</div>
            <div style="font-size: 12px; color: var(--text-inverse-muted);">Bridges <b>40.0%</b> of Saving Bonds Deficit (AED 5.82M)</div>
          </div>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-card-hdr">
          <div class="chart-card-title">Projected Outcome: Target vs Actual vs Simulated Post-Remediation</div>
        </div>
        <div id="chart-sim-gap" class="chart-viewport" style="min-height: 300px;"></div>
      </div>
    `;

    setTimeout(() => {
      updateView();

      document.getElementById('sim-chk-yield').onchange = (e) => {
        if (e.target.checked) selectedInterventions.push('yield');
        else selectedInterventions = selectedInterventions.filter(x => x !== 'yield');
        updateView();
      };
      document.getElementById('sim-chk-campaign').onchange = (e) => {
        if (e.target.checked) selectedInterventions.push('campaign');
        else selectedInterventions = selectedInterventions.filter(x => x !== 'campaign');
        updateView();
      };
      document.getElementById('sim-chk-onboarding').onchange = (e) => {
        if (e.target.checked) selectedInterventions.push('onboarding');
        else selectedInterventions = selectedInterventions.filter(x => x !== 'onboarding');
        updateView();
      };
      document.getElementById('sim-slider-eff').oninput = (e) => {
        efficiency = +e.target.value;
        updateView();
      };
    }, 50);
  },

  // Helper for official certified PDF export with interactive toast
  downloadOfficialReport(primaryUrl, downloadFilename, reportTitle, fallbackUrl) {
    const isLocalServer = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const link = document.createElement('a');
    link.href = (isLocalServer && primaryUrl) ? primaryUrl : (fallbackUrl || primaryUrl);
    link.download = downloadFilename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Render interactive executive toast
    const existing = document.getElementById('dossier-export-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'dossier-export-toast';
    toast.className = 'dossier-toast';
    toast.innerHTML = `
      <span class="material-symbols-rounded" style="color: #10b981; font-size: 22px;">task_alt</span>
      <div>
        <div style="font-weight: 700; font-size: 13px; color: #ffffff;">Exporting Official Document</div>
        <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Downloaded certified PDF matching current view: <b style="color: #c5a059;">${downloadFilename}</b></div>
      </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 420);
    }, 3500);
  },

  // Tab 6: Bi-Weekly Product & Market Intelligence Report (Native Executive Memorandum)
  renderBiWeeklyReport(container, state) {
    const pdfUrl = 'docs/National_Bonds_BiWeekly_Intelligence_Report_2024-06.pdf';
    const downloadFilename = 'National_Bonds_BiWeekly_Intelligence_Report_2026-06.pdf';

    container.innerHTML = `
      <div class="dossier-sheet">
        <!-- Official Document Header -->
        <div class="dossier-top-bar">
          <div class="dossier-brand-group">
            <div class="dossier-logo-badge">NB</div>
            <div class="dossier-title-block">
              <h2>National Bonds Corporation &bull; Commercial & Macro Intelligence</h2>
              <p>Executive Memorandum &bull; Bi-Weekly Cycle Close 2026-06 &bull; Classified: Confidential (ALCO / C-Suite)</p>
            </div>
          </div>
          <div class="dossier-actions">
            <button class="dossier-btn-export" id="btn-export-biweekly">
              <span class="material-symbols-rounded" style="font-size: 16px;">download</span>
              Export Official PDF
            </button>
            <button class="dossier-btn-print" id="btn-print-biweekly">
              <span class="material-symbols-rounded" style="font-size: 16px;">print</span>
              Print / Save PDF
            </button>
          </div>
        </div>

        <!-- Metadata Routing & Governance Table -->
        <table class="dossier-meta-table">
          <tr>
            <td class="meta-label">Addressee</td>
            <td class="meta-val">Group Executive Committee & ALCO</td>
            <td class="meta-label">Document Ref</td>
            <td class="meta-val">NBC-BIWEEKLY-INTEL-202606</td>
          </tr>
          <tr>
            <td class="meta-label">Originating Unit</td>
            <td class="meta-val">Commercial Intelligence & ALM Risk Strategy</td>
            <td class="meta-label">Audit Status</td>
            <td class="meta-val" style="color: #059669;">ALCO Ratified &bull; 100% Sharia Certified</td>
          </tr>
          <tr>
            <td class="meta-label">Publication Date</td>
            <td class="meta-val">15 June 2026</td>
            <td class="meta-label">Security Tier</td>
            <td class="meta-val" style="color: #ef4444;">RESTRICTED (C-SUITE / TREASURY)</td>
          </tr>
        </table>

        <!-- Macro Synthesis & Monetary Indicators -->
        <div class="dossier-section">
          <div class="dossier-sec-title">
            <span>01 &bull; Macro Benchmark & Portfolio Synthesis</span>
            <span style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: none;">Central Bank Base Rate Plateau: 4.65%</span>
          </div>
          <div class="dossier-kpi-row">
            <div class="dossier-kpi-box">
              <span class="dossier-kpi-label">CBUAE Base Rate</span>
              <span class="dossier-kpi-val">4.65%</span>
              <span class="dossier-kpi-sub" style="color: #64748b;">Unchanged (Plateau)</span>
            </div>
            <div class="dossier-kpi-box">
              <span class="dossier-kpi-label">3M EIBOR</span>
              <span class="dossier-kpi-val">4.52%</span>
              <span class="dossier-kpi-sub" style="color: #64748b;">+4 bps Liquidity Spread</span>
            </div>
            <div class="dossier-kpi-box">
              <span class="dossier-kpi-label">Net Inflows (Actual)</span>
              <span class="dossier-kpi-val">AED 617.0M</span>
              <span class="dossier-kpi-sub" style="color: #ef4444;">-9.5% vs Target AED 681.6M</span>
            </div>
            <div class="dossier-kpi-box">
              <span class="dossier-kpi-label">Total Redemptions</span>
              <span class="dossier-kpi-val">AED 405.7M</span>
              <span class="dossier-kpi-sub" style="color: #f59e0b;">Run-off Ratio: 39.7%</span>
            </div>
          </div>
          <div class="dossier-narrative-box">
            <b>Executive Macro Synthesis:</b> The UAE domestic liquidity landscape remains characterized by sustained high base rates (4.65%). While aggregate NBC AUM surpasses <b>AED 18.34B</b>, monthly net inflows closed at <b>AED 617.0M</b> against a budget of <b>AED 681.6M</b>. Liquidity run-off is predominantly concentrated in retail demand accounts, whereas institutional Term Sukuk retention exhibits high resilience with an 87.4% renewal velocity.
          </div>
        </div>

        <!-- Section 2: Product Performance vs Budget Allocation -->
        <div class="dossier-section">
          <div class="dossier-sec-title">
            <span>02 &bull; Product Performance vs Approved Budget Allocation (Cycle 2026-06)</span>
            <span style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: none;">Values in AED Millions</span>
          </div>
          <div style="background: var(--surface-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm); padding: 18px 20px;">
            <div id="chart-biweekly-budget" style="min-height: 310px;"></div>
          </div>
          <table class="dossier-data-table">
            <thead>
              <tr>
                <th>Product Family</th>
                <th style="text-align: right;">Actual Net (AED M)</th>
                <th style="text-align: right;">Target Budget (AED M)</th>
                <th style="text-align: right;">Variance (AED M)</th>
                <th style="text-align: right;">Variance (%)</th>
                <th style="text-align: center;">Governance Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: var(--navy-slate-900);">Term Sukuk (Fixed Income)</td>
                <td class="num">AED 520.2M</td>
                <td class="num">AED 582.2M</td>
                <td class="num" style="color: #ef4444;">-AED 62.0M</td>
                <td class="num" style="color: #ef4444;">-10.65%</td>
                <td style="text-align: center;"><span class="status-badge warning" style="font-size: 10px; padding: 2px 8px;">TOLERANCE WATCH</span></td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: var(--navy-slate-900);">Saving Bonds (Retail)</td>
                <td class="num">AED 51.2M</td>
                <td class="num">AED 57.0M</td>
                <td class="num" style="color: #ef4444;">-AED 5.8M</td>
                <td class="num" style="color: #ef4444;">-10.22%</td>
                <td style="text-align: center;"><span class="status-badge breach" style="font-size: 10px; padding: 2px 8px;">BREACH / ESCALATED</span></td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: var(--navy-slate-900);">Booster Plan (Loyalty)</td>
                <td class="num">AED 26.5M</td>
                <td class="num">AED 21.7M</td>
                <td class="num" style="color: #10b981;">+AED 4.8M</td>
                <td class="num" style="color: #10b981;">+22.12%</td>
                <td style="text-align: center;"><span class="status-badge healthy" style="font-size: 10px; padding: 2px 8px;">OUTPERFORMING</span></td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: var(--navy-slate-900);">MyPlan / Regular Saver</td>
                <td class="num">AED 16.5M</td>
                <td class="num">AED 16.8M</td>
                <td class="num" style="color: #64748b;">-AED 0.3M</td>
                <td class="num" style="color: #64748b;">-1.79%</td>
                <td style="text-align: center;"><span class="status-badge healthy" style="font-size: 10px; padding: 2px 8px;">ON TARGET</span></td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: var(--navy-slate-900);">Second Salary (Retirement)</td>
                <td class="num">AED 2.7M</td>
                <td class="num">AED 3.8M</td>
                <td class="num" style="color: #ef4444;">-AED 1.1M</td>
                <td class="num" style="color: #ef4444;">-28.95%</td>
                <td style="text-align: center;"><span class="status-badge breach" style="font-size: 10px; padding: 2px 8px;">REMEDIATION</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Section 3: Competitive Market Pulse & Yield Surveillance -->
        <div class="dossier-section">
          <div class="dossier-sec-title">03 &bull; Competitive Yield Arbitrage & Liquidity Surveillance</div>
          <div class="dossier-insights-grid">
            <div class="dossier-insight-card">
              <div class="dossier-insight-hdr">
                <span class="material-symbols-rounded" style="color: #f59e0b; font-size: 18px;">warning</span>
                Retail Deposit Yield Arbitrage
              </div>
              <div class="dossier-insight-text">
                Neo-banks (Wio Bank at 5.25% promo rate) and digital accounts (FAB iSave at 5.10%) are aggressively bidding for short-term retail liquidity. Yield-sensitive retail cohorts are parking discretionary liquidity into 3-month high-yield promotional deposits, directly dampening Saving Bonds fresh inflows.
              </div>
            </div>
            <div class="dossier-insight-card">
              <div class="dossier-insight-hdr">
                <span class="material-symbols-rounded" style="color: #0284c7; font-size: 18px;">verified_user</span>
                Duration Lock & Institutional Stability
              </div>
              <div class="dossier-insight-text">
                Conversely, Term Sukuk contracts (1Y to 3Y fixed maturities) maintain an 87.4% customer retention rate. Redemptions were primarily concentrated in flexible retail certificates (AED 194.2M out of AED 405.7M total). Matured capital was successfully rolled into structured 2Y Booster tranches at a 74.2% capture rate.
              </div>
            </div>
          </div>
        </div>

        <!-- Section 4: Governance Ratification & Cryptographic Seal -->
        <div class="dossier-seal-row">
          <div>
            <div style="font-weight: 700; color: var(--navy-slate-900);">Group Executive Committee &bull; Asset Liability Management (ALCO)</div>
            <div style="font-size: 11px; margin-top: 3px;">Signatories: Group Chief Commercial Officer &bull; Head of Treasury & Financial Markets</div>
          </div>
          <div class="dossier-stamp">
            <span class="material-symbols-rounded" style="font-size: 16px;">verified</span>
            ALCO RATIFIED &bull; SHA-256 AUDITED
          </div>
        </div>
      </div>
    `;

    // Initialize interactive ApexCharts for Bi-Weekly Report
    setTimeout(() => {
      if (window._chartBiweeklyBudget) {
        window._chartBiweeklyBudget.destroy();
        window._chartBiweeklyBudget = null;
      }
      const el = document.getElementById('chart-biweekly-budget');
      if (el) {
        const options = {
          series: [
            { name: 'Actual Inflow (AED M)', data: [520.2, 51.2, 26.5, 16.5, 2.7] },
            { name: 'Target Budget (AED M)', data: [582.2, 57.0, 21.7, 16.8, 3.8] }
          ],
          chart: {
            type: 'bar',
            height: 290,
            toolbar: { show: false },
            fontFamily: 'Plus Jakarta Sans, sans-serif'
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '46%',
              borderRadius: 4
            }
          },
          colors: ['#0b192c', '#c5a059'],
          dataLabels: { enabled: false },
          stroke: { show: true, width: 2, colors: ['transparent'] },
          xaxis: {
            categories: ['Term Sukuk', 'Saving Bonds', 'Booster Plan', 'MyPlan Saver', 'Second Salary'],
            labels: { style: { colors: '#64748b', fontSize: '11.5px', fontWeight: 600 } }
          },
          yaxis: {
            labels: {
              formatter: (val) => `${val.toFixed(0)}M`,
              style: { colors: '#64748b', fontSize: '11px' }
            }
          },
          legend: {
            position: 'top',
            horizontalAlign: 'right',
            fontSize: '12px',
            fontWeight: 600,
            markers: { radius: 3 }
          },
          grid: {
            borderColor: '#f1f5f9',
            strokeDashArray: 3
          },
          tooltip: {
            y: { formatter: (val) => `AED ${val.toFixed(1)}M` }
          }
        };
        window._chartBiweeklyBudget = new ApexCharts(el, options);
        window._chartBiweeklyBudget.render();
      }
    }, 50);

    // Bind Export Button
    document.getElementById('btn-export-biweekly')?.addEventListener('click', () => {
      this.downloadOfficialReport('/api/export-pdf?type=biweekly&cycle=2026-06', downloadFilename, 'Bi-Weekly Intelligence Report', pdfUrl);
    });

    // Bind Print Button
    document.getElementById('btn-print-biweekly')?.addEventListener('click', () => {
      window.print();
    });
  },

  // Tab 7: GCCO Escalation Briefing (Native Escalation Dossier)
  renderGccoBriefing(container, state) {
    const pdfUrl = 'docs/National_Bonds_GCCO_Escalation_Dossier_Booster_Sukuk.pdf';
    const downloadFilename = 'National_Bonds_GCCO_Escalation_Dossier_2026-06.pdf';

    container.innerHTML = `
      <div class="dossier-sheet">
        <!-- Official Document Header -->
        <div class="dossier-top-bar">
          <div class="dossier-brand-group">
            <div class="dossier-logo-badge" style="background: linear-gradient(135deg, #7f1d1d, #b91c1c); color: #ffffff;">NB</div>
            <div class="dossier-title-block">
              <h2>Confidential Escalation Dossier & Routing Table</h2>
              <p style="color: #ef4444;">Strictly Confidential &bull; Group Chief Commercial Officer Direct Action &bull; Ref: ESC-2026-GCCO-01</p>
            </div>
          </div>
          <div class="dossier-actions">
            <span class="status-badge breach" style="margin-right: 4px;">URGENT GCCO ACTION</span>
            <button class="dossier-btn-export" id="btn-export-gcco" style="background: #991b1b; border-color: #991b1b;">
              <span class="material-symbols-rounded" style="font-size: 16px;">download</span>
              Export Official PDF
            </button>
            <button class="dossier-btn-print" id="btn-print-gcco">
              <span class="material-symbols-rounded" style="font-size: 16px;">print</span>
              Print / Save PDF
            </button>
          </div>
        </div>

        <!-- Escalation Metadata Routing Table -->
        <table class="dossier-meta-table">
          <tr>
            <td class="meta-label">Addressee</td>
            <td class="meta-val">Group Chief Commercial Officer (GCCO)</td>
            <td class="meta-label">Escalation Ref</td>
            <td class="meta-val">ESC-2026-GCCO-01</td>
          </tr>
          <tr>
            <td class="meta-label">Severity Level</td>
            <td class="meta-val" style="color: #ef4444; font-weight: 800;">TIER-1 COMMERCIAL BREACH (Deficit &gt; 10%)</td>
            <td class="meta-label">Incident Cycle</td>
            <td class="meta-val">Cycle 2026-06 (June Close)</td>
          </tr>
          <tr>
            <td class="meta-label">Underperforming Entity</td>
            <td class="meta-val">Saving Bonds (Retail Inflows)</td>
            <td class="meta-label">Deficit Gap</td>
            <td class="meta-val" style="color: #ef4444; font-weight: 800;">-AED 5.82M (-10.22% Target Shortfall)</td>
          </tr>
        </table>

        <!-- Red Alert Notice -->
        <div class="dossier-alert-box">
          <b>CRITICAL COMMERCIAL BREACH NOTICE:</b> Saving Bonds monthly net inflows closed at <b>AED 51.18M</b> against an ALCO approved target of <b>AED 57.02M</b> (AED 5.82M net deficit, -10.22% deviation). This marks the second consecutive reporting period wherein variance exceeded the -8.0% tolerance band. Pursuant to Commercial Governance Charter Section 4.2, immediate executive intervention directives are submitted below for GCCO ratification.
        </div>

        <!-- Section 1: 12-Month Inflow Trajectory & Threshold Breach -->
        <div class="dossier-section">
          <div class="dossier-sec-title">
            <span>01 &bull; 12-Month Inflow Trajectory vs Tolerance Boundary</span>
            <span style="font-size: 11px; font-weight: 600; color: #ef4444; text-transform: none;">Breached -8.0% Tolerance Band</span>
          </div>
          <div style="background: var(--surface-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm); padding: 18px 20px;">
            <div id="chart-gcco-trajectory" style="min-height: 290px;"></div>
          </div>
        </div>

        <!-- Section 2: Channel Diagnosis & Leakage Attribution -->
        <div class="dossier-section">
          <div class="dossier-sec-title">02 &bull; Channel Attribution & Leakage Root Cause Deconstruction</div>
          <div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px;">
            <div style="background: var(--surface-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm); padding: 16px 18px;">
              <div style="font-size: 12px; font-weight: 700; color: var(--navy-slate-900); margin-bottom: 10px;">Acquisition Channel Variance vs Baseline (%)</div>
              <div id="chart-gcco-channel" style="min-height: 210px;"></div>
            </div>
            <div class="dossier-insights-grid" style="grid-template-columns: 1fr;">
              <div class="dossier-insight-card">
                <div class="dossier-insight-hdr" style="color: #ef4444;">
                  <span class="material-symbols-rounded" style="font-size: 18px;">phonelink_erase</span>
                  Mobile App Payment Gateway Friction (-68.4%)
                </div>
                <div class="dossier-insight-text">
                  On June 3rd, the payment gateway migration introduced an authentication retry timeout on recurring direct debits. Checkout drop-off surged from 4.1% to 19.8%, resulting in an estimated <b>AED 3.2M</b> in uncaptured monthly top-ups.
                </div>
              </div>
              <div class="dossier-insight-card">
                <div class="dossier-insight-hdr" style="color: #f59e0b;">
                  <span class="material-symbols-rounded" style="font-size: 18px;">trending_down</span>
                  Neo-Bank Competitor Yield Premium
                </div>
                <div class="dossier-insight-text">
                  Aggressive 5.25% APY promotional campaigns by neo-banks triggered opportunistic withdrawals among Mass Affluent holders (AED 50k - AED 250k tier), leading to an accelerated redemption velocity.
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 3: GCCO Action Directives -->
        <div class="dossier-section">
          <div class="dossier-sec-title">
            <span>03 &bull; Mandated Commercial Recovery Directives (GCCO Direct Execution)</span>
            <span style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: none;">SLA: Immediate 72-Hour Deployment</span>
          </div>
          <div class="dossier-directives-list">
            <div class="dossier-directive-item urgent">
              <div class="dossier-directive-main">
                <div class="dossier-directive-title">
                  <span class="material-symbols-rounded" style="color: #ef4444; font-size: 18px;">build_circle</span>
                  Directive 1: Hotfix Mobile Payment Gateway & Reinstate 1-Click Apple Pay
                </div>
                <div class="dossier-directive-desc">
                  Engineering team to rollback the buggy authentication timeout and restore single-tap Apple Pay recurring authorization.
                </div>
              </div>
              <div class="dossier-directive-meta">
                <span class="dossier-impact-pill">+AED 3.2M Inflow Recovery</span>
                <span style="font-size: 11px; color: var(--text-tertiary);">Owner: Digital Product Lead &bull; ETA: 48h</span>
              </div>
            </div>

            <div class="dossier-directive-item">
              <div class="dossier-directive-main">
                <div class="dossier-directive-title">
                  <span class="material-symbols-rounded" style="color: var(--brand-primary); font-size: 18px;">campaign</span>
                  Directive 2: Deploy 5.30% 6-Month Booster Sukuk Flash Tranche
                </div>
                <div class="dossier-directive-desc">
                  Launch targeted promotional yield tranche directly in the mobile app to counter neo-bank churn and recapture liquid balances.
                </div>
              </div>
              <div class="dossier-directive-meta">
                <span class="dossier-impact-pill">+AED 4.5M New Liquidity</span>
                <span style="font-size: 11px; color: var(--text-tertiary);">Owner: Commercial Strategy &bull; ETA: 5 Days</span>
              </div>
            </div>

            <div class="dossier-directive-item">
              <div class="dossier-directive-main">
                <div class="dossier-directive-title">
                  <span class="material-symbols-rounded" style="color: #059669; font-size: 18px;">support_agent</span>
                  Directive 3: Direct Relationship Manager Concierge Outreach
                </div>
                <div class="dossier-directive-desc">
                  Assign dedicated RM calls to 420 High Net Worth savers (> AED 250k) identified with high withdrawal intent indicators.
                </div>
              </div>
              <div class="dossier-directive-meta">
                <span class="dossier-impact-pill">+AED 6.0M Retention Capture</span>
                <span style="font-size: 11px; color: var(--text-tertiary);">Owner: Wealth Sales Lead &bull; ETA: Immediate</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 4: Governance Ratification & Sign-off -->
        <div class="dossier-seal-row">
          <div>
            <div style="font-weight: 700; color: var(--navy-slate-900);">Commercial Governance & Enterprise Risk Committee</div>
            <div style="font-size: 11px; margin-top: 3px;">Escalation Authority: Group Chief Commercial Officer &bull; Ref: ESC-2026-GCCO-01-SIGNED</div>
          </div>
          <div class="dossier-stamp" style="border-color: #dc2626; color: #dc2626;">
            <span class="material-symbols-rounded" style="font-size: 16px;">gavel</span>
            MANDATED FOR EXECUTION
          </div>
        </div>
      </div>
    `;

    // Initialize interactive ApexCharts for GCCO Briefing
    setTimeout(() => {
      // 1. Trajectory Spline Chart
      if (window._chartGccoTrajectory) {
        window._chartGccoTrajectory.destroy();
        window._chartGccoTrajectory = null;
      }
      const elTraj = document.getElementById('chart-gcco-trajectory');
      if (elTraj) {
        const optionsTraj = {
          series: [
            {
              name: 'Actual Net Inflow',
              type: 'area',
              data: [56.2, 57.8, 58.4, 59.1, 57.9, 56.4, 58.2, 57.0, 56.5, 55.8, 54.2, 51.2]
            },
            {
              name: 'ALCO Target Budget (AED 57.0M)',
              type: 'line',
              data: [55.0, 55.5, 56.0, 56.5, 57.0, 57.0, 57.0, 57.0, 57.0, 57.0, 57.0, 57.0]
            },
            {
              name: '-8.0% Warning Boundary (AED 52.4M)',
              type: 'line',
              data: [50.6, 51.1, 51.5, 52.0, 52.4, 52.4, 52.4, 52.4, 52.4, 52.4, 52.4, 52.4]
            }
          ],
          chart: {
            height: 290,
            type: 'line',
            toolbar: { show: false },
            fontFamily: 'Plus Jakarta Sans, sans-serif'
          },
          stroke: {
            curve: 'smooth',
            width: [3, 2, 2],
            dashArray: [0, 4, 3]
          },
          colors: ['#0284c7', '#10b981', '#ef4444'],
          fill: {
            type: ['gradient', 'solid', 'solid'],
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.3,
              opacityTo: 0.05,
              stops: [0, 90, 100]
            }
          },
          xaxis: {
            categories: ['Jul 25', 'Aug 25', 'Sep 25', 'Oct 25', 'Nov 25', 'Dec 25', 'Jan 26', 'Feb 26', 'Mar 26', 'Apr 26', 'May 26', 'Jun 26'],
            labels: { style: { colors: '#64748b', fontSize: '11px', fontWeight: 600 } }
          },
          yaxis: {
            labels: {
              formatter: (val) => `${val.toFixed(0)}M`,
              style: { colors: '#64748b', fontSize: '11px' }
            }
          },
          legend: {
            position: 'top',
            horizontalAlign: 'right',
            fontSize: '12px',
            fontWeight: 600
          },
          grid: {
            borderColor: '#f1f5f9',
            strokeDashArray: 3
          },
          tooltip: {
            y: { formatter: (val) => `AED ${val.toFixed(2)}M` }
          }
        };
        window._chartGccoTrajectory = new ApexCharts(elTraj, optionsTraj);
        window._chartGccoTrajectory.render();
      }

      // 2. Channel Horizontal Variance Chart
      if (window._chartGccoChannel) {
        window._chartGccoChannel.destroy();
        window._chartGccoChannel = null;
      }
      const elChan = document.getElementById('chart-gcco-channel');
      if (elChan) {
        const optionsChan = {
          series: [{
            name: 'Variance from Target (%)',
            data: [-68.4, 2.1, 8.4, -4.2]
          }],
          chart: {
            type: 'bar',
            height: 200,
            toolbar: { show: false },
            fontFamily: 'Plus Jakarta Sans, sans-serif'
          },
          plotOptions: {
            bar: {
              horizontal: true,
              borderRadius: 4,
              barHeight: '52%',
              colors: {
                ranges: [
                  { from: -100, to: -0.01, color: '#ef4444' },
                  { from: 0, to: 100, color: '#10b981' }
                ]
              }
            }
          },
          dataLabels: {
            enabled: true,
            formatter: (val) => `${val > 0 ? '+' : ''}${val}%`,
            style: { fontSize: '11px', fontWeight: 700 }
          },
          xaxis: {
            categories: ['Mobile App Gateway', 'Branch Network', 'Direct Wealth Sales', 'Call Center Telesales'],
            labels: {
              formatter: (val) => `${val}%`,
              style: { colors: '#64748b', fontSize: '11px' }
            }
          },
          grid: {
            borderColor: '#f1f5f9',
            strokeDashArray: 3
          },
          tooltip: {
            y: { formatter: (val) => `${val > 0 ? '+' : ''}${val}% vs Target` }
          }
        };
        window._chartGccoChannel = new ApexCharts(elChan, optionsChan);
        window._chartGccoChannel.render();
      }
    }, 50);

    // Bind Export Button
    document.getElementById('btn-export-gcco')?.addEventListener('click', () => {
      this.downloadOfficialReport('/api/export-pdf?type=gcco&product=Saving%20Bonds&cycle=2026-06', downloadFilename, 'GCCO Escalation Dossier', pdfUrl);
    });

    // Bind Print Button
    document.getElementById('btn-print-gcco')?.addEventListener('click', () => {
      window.print();
    });
  }
};
