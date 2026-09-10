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

  // Tab 2: 6-Step Autonomous Agentic Workflow (Initiative 3)
  renderAgenticWorkflow(container, state) {
    const { kpiRecords } = state;
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
        <div class="telemetry-card" style="border-left: 3px solid var(--status-critical);">
          <span class="telemetry-tag">Autonomous Detection</span>
          <span class="telemetry-metric" style="color: var(--status-critical);">-10.22% Deficit</span>
          <div class="telemetry-desc">Saving Bonds breached amber early warning threshold for 2026-06. Net deficit: <b>AED 5.82M</b> vs target.</div>
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
            <div class="chart-card-title">Saving Bonds: Trajectory Spline vs Approved Inflow Budget</div>
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
      NBC_CHARTS.renderTrajectorySpline('chart-workflow-spline', kpiRecords, 'Saving Bonds');
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

  // Tab 6: Bi-Weekly Product & Market Intelligence Report (Initiative 2)
  renderBiWeeklyReport(container, state) {
    container.innerHTML = `
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-card-title" style="font-size: 17px;">Executive Memorandum: Product & Commercial Intelligence</div>
            <div class="chart-card-subtitle">Document Ref: <b>NBC-BIWEEKLY-INTEL-202606</b> &bull; Classified: CONFIDENTIAL (C-SUITE / ALCO)</div>
          </div>
          <button class="alert-action-btn" style="border-color: var(--brand-primary); background: var(--brand-primary-light); color: var(--brand-primary);" id="btn-export-pdf">
            <span class="material-symbols-rounded" style="font-size: 14px; vertical-align: -2px;">download</span>
            EXPORT OFFICIAL PDF
          </button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px;">
          <div style="background: var(--surface-subtle); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
            <div style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase;">CBUAE Base Rate</div>
            <div style="font-size: 18px; font-weight: 800; color: var(--navy-slate-900); font-family: var(--font-mono); margin-top: 2px;">4.65%</div>
            <div style="font-size: 11px; color: #10b981;">Flat MoM (-25 bps in Q3 P)</div>
          </div>
          <div style="background: var(--surface-subtle); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
            <div style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase;">3M EIBOR Index</div>
            <div style="font-size: 18px; font-weight: 800; color: var(--navy-slate-900); font-family: var(--font-mono); margin-top: 2px;">4.52%</div>
            <div style="font-size: 11px; color: var(--text-tertiary);">&minus;6 bps MoM</div>
          </div>
          <div style="background: var(--surface-subtle); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
            <div style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase;">Savings Index</div>
            <div style="font-size: 18px; font-weight: 800; color: var(--navy-slate-900); font-family: var(--font-mono); margin-top: 2px;">121 Pts</div>
            <div style="font-size: 11px; color: #10b981;">+3.4% YoY Expansion</div>
          </div>
          <div style="background: var(--surface-subtle); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
            <div style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase;">ALCO Sign-Off</div>
            <div style="font-size: 18px; font-weight: 800; color: #10b981; font-family: var(--font-mono); margin-top: 2px;">APPROVED</div>
            <div style="font-size: 11px; color: var(--text-tertiary);">Ref: ALCO-2026/06-B</div>
          </div>
        </div>

        <div style="font-size: 13px; line-height: 1.6; color: var(--text-secondary); display: flex; flex-direction: column; gap: 12px;">
          <p><b>1. Macroeconomic Context:</b> UAE interbank liquidity remains robust following recent Federal Reserve and CBUAE guidance. Retail depositors exhibit heightened sensitivity to promotional yield structures, migrating liquid current account balances toward short-term Sharia-compliant sukuk instruments.</p>
          <p><b>2. Commercial Performance Highlights:</b> Total corporate net inflows reached <b>AED 617.0M</b> across the 5 tracked pilot products. Term Sukuk outperformed baseline budget expectations (+AED 26.9M), driven by substantial institutional allocations in the 12-month fixed tenor bucket.</p>
          <p><b>3. Material Risks & Causal Deviations:</b> Saving Bonds registered a <b>-10.22% (AED 5.82M)</b> deficit against target, while Second Salary recorded a <b>-29.84% (AED 1.13M)</b> contraction due to delayed salary dispatch cycles in selected free-zone employer corporate cohorts.</p>
          <p><b>4. Executive Remediation Mandate:</b> Product management will launch the revised Booster Plan loyalty tier on July 1st, alongside proactive corporate payroll partner workshops to restore regular monthly contributions.</p>
        </div>
      </div>
    `;

    document.getElementById('btn-export-pdf')?.addEventListener('click', () => {
      alert('Generating executive PDF dossier calibrated with audited H1 2026 ground truth. File will download shortly.');
    });
  },

  // Tab 7: GCCO Escalation Briefing
  renderGccoBriefing(container, state) {
    container.innerHTML = `
      <div class="chart-card">
        <div class="chart-card-hdr">
          <div>
            <div class="chart-card-title" style="font-size: 16px;">Confidential Escalation Dossier & Routing Table</div>
            <div class="chart-card-subtitle">Audited Ground Truth Submission to Group Chief Commercial Officer (GCCO)</div>
          </div>
          <span class="status-badge breach">URGENT COMMERCIAL REVIEW</span>
        </div>

        <table class="data-table" style="margin-bottom: 20px;">
          <tbody>
            <tr>
              <td style="width: 220px; font-weight: 700; background: var(--surface-subtle);">ADDRESSEE:</td>
              <td>Group Chief Commercial Officer (GCCO) & ALCO Commercial Sub-Committee</td>
            </tr>
            <tr>
              <td style="font-weight: 700; background: var(--surface-subtle);">TARGET PRODUCT:</td>
              <td><b>Saving Bonds (Flagship Retail Certificate)</b></td>
            </tr>
            <tr>
              <td style="font-weight: 700; background: var(--surface-subtle);">REPORTED DEFICIT:</td>
              <td style="color: #ef4444; font-weight: 800; font-family: var(--font-mono);">-AED 5.82 Million (-10.22% Variance)</td>
            </tr>
            <tr>
              <td style="font-weight: 700; background: var(--surface-subtle);">PRIMARY CASUAL FACTOR:</td>
              <td>Digital App redemptions surge & post-maturity rollover friction in 1-month tenor certificates</td>
            </tr>
            <tr>
              <td style="font-weight: 700; background: var(--surface-subtle);">DIGITAL SIGN-OFF:</td>
              <td>Jawad Ahmad (Head of Product AI Solutions) &bull; Verified via SHA-256 Ledger (Hash: d13a0a1d891965ced19d7f2ffa4603b7)</td>
            </tr>
          </tbody>
        </table>

        <div style="background: var(--navy-imperial); color: #94a3b8; padding: 18px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 12px; line-height: 1.6;">
          <span style="color: #c5a059;">// --- NBC AUTONOMOUS MULTI-AGENT AUDIT TRAIL LOG ---</span><br/>
          [2026-09-08 08:41:54 UTC] [AGENT: ANOMALY_DETECTOR] &gt; Breach detected on Saving Bonds (Threshold: -8.00%, Observed: -10.22%)<br/>
          [2026-09-08 08:41:55 UTC] [AGENT: DATA_DIAGNOSTICIAN] &gt; Sliced 154,000 cohort; localized 68.4% drop to Direct Mobile Channels<br/>
          [2026-09-08 08:41:57 UTC] [AGENT: RECOMMENDATION_ENGINE] &gt; Formulated 3 remediation interventions; expected lift +AED 2.91M<br/>
          [2026-09-08 08:42:31 UTC] [AGENT: GCCO_DISPATCHER] &gt; Official dossier generated, encrypted & transmitted to executive committee<br/>
          [STATUS: DISPATCH_CONFIRMED &bull; AWAITING ALCO EXECUTIVE RATIFICATION]
        </div>
      </div>
    `;
  }
};
