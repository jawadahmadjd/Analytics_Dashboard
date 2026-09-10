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

  // Tab: Six Step Autonomous Agentic Workflow
  renderAgenticWorkflow(container, state) {
    const { kpiRecords } = state;
    const activeProd = state.selectedProduct || 'Saving Bonds';
    const currentMonth = state.selectedCycle || '2026-06';
    const cycleKpis = kpiRecords.filter(r => r.month === currentMonth);
    const foundProd = cycleKpis.find(r => r.product_name.includes(activeProd.split(' ')[0])) || cycleKpis[0];
    const devPct = foundProd ? foundProd.deviation_pct : -10.22;
    const netAed = foundProd ? (foundProd.net_inflows_aed / 1e6).toFixed(2) : '51.19';
    const tgtAed = foundProd ? (foundProd.target_inflows_aed / 1e6).toFixed(2) : '57.02';
    const defAed = foundProd ? Math.abs((foundProd.net_inflows_aed - foundProd.target_inflows_aed) / 1e6).toFixed(2) : '5.82';

    container.innerHTML = `
      <!-- Stepper Ribbon -->
      <div class="stepper-container">
        <div class="step-item completed">
          <div class="step-num-circle"><span class="material-symbols-rounded" style="font-size: 14px;">check</span></div>
          <div class="step-name">01 MONITOR</div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item active">
          <div class="step-num-circle">02</div>
          <div class="step-name">02 DETECT</div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item">
          <div class="step-num-circle">03</div>
          <div class="step-name">03 INVESTIGATE</div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item">
          <div class="step-num-circle">04</div>
          <div class="step-name">04 ANALYSE</div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item">
          <div class="step-num-circle">05</div>
          <div class="step-name">05 RECOMMEND</div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item">
          <div class="step-num-circle">06</div>
          <div class="step-name">06 ESCALATE</div>
        </div>
      </div>

      <!-- Telemetry Cards -->
      <div class="telemetry-grid">
        <div class="telemetry-card" style="border-left: 3px solid ${devPct < -15 ? 'var(--status-critical)' : devPct < 0 ? 'var(--status-warning)' : 'var(--status-optimal)'};">
          <span class="telemetry-tag">Autonomous Detection</span>
          <span class="telemetry-metric" style="color: ${devPct < -15 ? 'var(--status-critical)' : devPct < 0 ? 'var(--status-warning)' : 'var(--status-optimal)'};">
            ${devPct > 0 ? '+' : ''}${devPct.toFixed(2)}% Variance
          </span>
          <div class="telemetry-desc">${foundProd?.product_name || activeProd} registered <b>AED ${netAed}M</b> net inflow vs <b>AED ${tgtAed}M</b> target for ${currentMonth}.</div>
        </div>
        <div class="telemetry-card" style="border-left: 3px solid var(--brand-primary);">
          <span class="telemetry-tag">Primary Causal Attribution</span>
          <span class="telemetry-metric">Digital Web / App Drop</span>
          <div class="telemetry-desc">68% of redemption volume originated from digital self-service accounts with tenure &lt; 9 months.</div>
        </div>
        <div class="telemetry-card" style="border-left: 3px solid var(--status-optimal);">
          <span class="telemetry-tag">Recommended Resolution</span>
          <span class="telemetry-metric">+AED 2.91M Recovery</span>
          <div class="telemetry-desc">Execute Tiered Loyalty Boost + Corporate Channel re-engagement to bridge 62% of deficit within 45 days.</div>
        </div>
      </div>

      <!-- Trajectory Spline Chart -->
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-card-title">${foundProd?.product_name || activeProd}: Trajectory Spline vs Approved Inflow Budget</div>
            <div class="chart-card-subtitle">Continuous 12-Month Audited Inflows with Dynamic Alert Threshold Bands</div>
          </div>
          <button class="alert-action-btn" id="btn-dispatch-gcco">
            <span class="material-symbols-rounded" style="font-size: 14px; vertical-align: -2px;">send</span>
            DISPATCH TO GCCO
          </button>
        </div>
        <div id="chart-workflow-spline" class="chart-viewport" style="min-height: 340px;"></div>
      </div>
    `;

    setTimeout(() => {
      NBC_CHARTS.renderTrajectorySpline('chart-workflow-spline', kpiRecords, activeProd);
    }, 50);

    document.getElementById('btn-dispatch-gcco')?.addEventListener('click', () => {
      alert('Official Escalation Memo successfully dispatched to Group Chief Commercial Officer (GCCO) and ALCO Committee via Secure SMTP Webhook (Receipt: DISPATCH-2026-84127).');
    });
  },

  // Tab 3: 5-Product Portfolio Matrix
  renderPortfolioMatrix(container, state) {
    const { kpiRecords } = state;
    const currentMonth = state.selectedCycle || '2026-06';
    const cycleKpis = kpiRecords.filter(r => r.month === currentMonth);

    container.innerHTML = `
      <div class="data-table-container">
        <div style="padding: 16px 20px; border-bottom: 1px solid var(--border-default); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 15px; font-weight: 800; color: var(--navy-slate-900);">H1 2026 Portfolio Ground Truth Matrix</div>
            <div style="font-size: 12px; color: var(--text-tertiary); margin-top: 2px;">Comprehensive Multi-Product Commercial Breakdown for Cycle ${currentMonth}</div>
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
            ${cycleKpis.map(r => `
              <tr>
                <td><b>${r.product_name}</b></td>
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
            `).join('')}
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
  downloadOfficialReport(pdfUrl, downloadFilename, reportTitle) {
    const link = document.createElement('a');
    link.href = pdfUrl;
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
      this.downloadOfficialReport(pdfUrl, downloadFilename, 'Bi-Weekly Intelligence Report');
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
      this.downloadOfficialReport(pdfUrl, downloadFilename, 'GCCO Escalation Dossier');
    });

    // Bind Print Button
    document.getElementById('btn-print-gcco')?.addEventListener('click', () => {
      window.print();
    });
  }
};
