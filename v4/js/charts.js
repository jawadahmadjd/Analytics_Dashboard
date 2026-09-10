/* ==========================================================================
   National Bonds Corporation — Charts Engine (ApexCharts Suite)
   Defect 1 Remediation: Zero Legend-Title Collisions & Generous Margins
   ========================================================================== */

window.NBC_CHARTS = {
  instances: {},

  destroyChart(id) {
    if (this.instances[id]) {
      this.instances[id].destroy();
      delete this.instances[id];
    }
  },

  // --------------------------------------------------------------------------
  // 1. Cashflow Waterfall Bridge
  // --------------------------------------------------------------------------
  renderWaterfall(containerId, totGross = 998.6, totRed = 381.6, totNet = 617.0) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const digital = +(totGross * 0.42).toFixed(1);
    const branch = +(totGross * 0.38).toFixed(1);
    const wealth = +(totGross * 0.20).toFixed(1);
    const matureRed = +(-1 * (totRed * 0.65)).toFixed(1);
    const earlyRed = +(-1 * (totRed * 0.35)).toFixed(1);
    const netPos = +totNet.toFixed(1);

    const options = {
      series: [{
        name: 'AED Millions',
        data: [
          { x: 'Digital Inflows', y: digital },
          { x: 'Branch Network', y: branch },
          { x: 'Wealth Direct', y: wealth },
          { x: 'Maturity Outflows', y: matureRed },
          { x: 'Early Liquidation', y: earlyRed },
          { x: 'Net Position', y: netPos }
        ]
      }],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          columnWidth: '50%',
          borderRadius: 4,
          colors: {
            ranges: [
              { from: -10000, to: -0.01, color: '#ef4444' },
              { from: 0, to: 10000, color: '#0284c7' }
            ]
          }
        }
      },
      dataLabels: {
        enabled: true,
        formatter: (val) => `${val > 0 ? '+' : ''}${val}M`,
        style: { fontSize: '11px', fontFamily: 'JetBrains Mono', colors: ['#0f172a'] },
        offsetY: -20
      },
      grid: { borderColor: '#eaeff5' },
      xaxis: {
        labels: { style: { colors: '#64748b', fontSize: '11px', fontWeight: 600 } }
      },
      yaxis: {
        labels: {
          style: { colors: '#64748b', fontSize: '11px' },
          formatter: (val) => `${val}M`
        }
      },
      tooltip: {
        theme: 'light',
        y: { formatter: (val) => `AED ${val} Million` }
      }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 2. AUM Allocation Treemap
  // --------------------------------------------------------------------------
  renderAumTreemap(containerId) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const options = {
      series: [{
        data: [
          { x: 'Term Sukuk (Fixed)', y: 9450 },
          { x: 'Saving Bonds (Retail)', y: 4820 },
          { x: 'Booster Plan (Loyalty)', y: 2150 },
          { x: 'MyPlan (Regular)', y: 1420 },
          { x: 'Second Salary (Pension)', y: 500 }
        ]
      }],
      chart: {
        type: 'treemap',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      colors: ['#0b192c', '#0284c7', '#0ea5e9', '#c5a059', '#10b981'],
      plotOptions: {
        treemap: {
          distributed: true,
          enableShades: false
        }
      },
      dataLabels: {
        enabled: true,
        style: { fontSize: '12px', fontWeight: 700 },
        formatter: (text, op) => [text, `AED ${op.value}M`]
      },
      tooltip: {
        theme: 'light',
        y: { formatter: (val) => `AED ${val} Million AUM` }
      }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 3. BCG Strategic Matrix (Annualized Yield vs Net Inflows)
  // --------------------------------------------------------------------------
  renderBcgMatrix(containerId) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const options = {
      series: [
        { name: 'Term Sukuk', data: [[12.5, 5.35, 35]] },
        { name: 'Saving Bonds', data: [[4.2, 4.80, 50]] },
        { name: 'Booster Plan', data: [[22.2, 6.10, 25]] },
        { name: 'MyPlan', data: [[-2.3, 4.50, 20]] },
        { name: 'Second Salary', data: [[-29.8, 5.00, 15]] }
      ],
      chart: {
        type: 'bubble',
        height: 340,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      colors: ['#0b192c', '#0284c7', '#10b981', '#f59e0b', '#ef4444'],
      dataLabels: { enabled: false },
      fill: { opacity: 0.8 },
      xaxis: {
        title: { text: 'Net Inflow Deviation vs Target (%)', style: { color: '#64748b', fontSize: '11px', fontWeight: 700 } },
        tickAmount: 7,
        labels: { formatter: (val) => `${val}%` }
      },
      yaxis: {
        title: { text: 'Annualized Yield (%)', style: { color: '#64748b', fontSize: '11px', fontWeight: 700 } },
        min: 3.5,
        max: 7.0,
        labels: { formatter: (val) => `${val.toFixed(1)}%` }
      },
      legend: {
        position: 'bottom',
        offsetY: 10,
        fontSize: '11px',
        fontWeight: 600
      },
      grid: { borderColor: '#eaeff5' },
      tooltip: {
        theme: 'light',
        custom: ({ series, seriesIndex, dataPointIndex, w }) => {
          const item = w.config.series[seriesIndex];
          const [dev, yieldVal, aumWeight] = item.data[0];
          return `<div style="padding: 10px; font-size: 12px; font-family: Plus Jakarta Sans;">
            <strong>${item.name}</strong><br/>
            Deviation: <span style="color: ${dev < 0 ? '#ef4444' : '#10b981'}">${dev > 0 ? '+' : ''}${dev}%</span><br/>
            Yield: <b>${yieldVal}%</b><br/>
            Portfolio Weight: <b>${aumWeight}%</b>
          </div>`;
        }
      }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 4. Macro Correlation Combo (Inflows vs CBUAE & EIBOR)
  // --------------------------------------------------------------------------
  renderMacroCombo(containerId, marketData) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el || !marketData) return;

    const recent = marketData.slice(-12);
    const months = recent.map(r => r.month);
    const baseRates = recent.map(r => r.cbuae_base_rate_pct);
    const eibor = recent.map(r => r.eibor_3m_pct);
    const savingsIndex = recent.map(r => r.consumer_savings_index * 4.5);

    const options = {
      series: [
        { name: 'Consumer Savings Activity (Index)', type: 'column', data: savingsIndex },
        { name: 'CBUAE Base Rate (%)', type: 'line', data: baseRates },
        { name: '3M EIBOR (%)', type: 'line', data: eibor }
      ],
      chart: {
        height: 340,
        type: 'line',
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      stroke: { width: [0, 3, 3], curve: 'smooth' },
      colors: ['#e2e8f0', '#0284c7', '#c5a059'],
      plotOptions: { bar: { columnWidth: '40%', borderRadius: 4 } },
      fill: { opacity: [0.65, 1, 1] },
      labels: months,
      xaxis: { labels: { style: { colors: '#64748b', fontSize: '11px' } } },
      yaxis: [
        {
          title: { text: 'Savings Index Volume', style: { color: '#64748b', fontSize: '10.5px' } },
          labels: { style: { colors: '#64748b' } }
        },
        {
          opposite: true,
          title: { text: 'Benchmark Yield (%)', style: { color: '#64748b', fontSize: '10.5px' } },
          labels: { style: { colors: '#64748b' }, formatter: (v) => `${v.toFixed(2)}%` },
          min: 4.0,
          max: 6.0
        }
      ],
      legend: { position: 'bottom', offsetY: 10, fontSize: '11px', fontWeight: 600 },
      grid: { borderColor: '#eaeff5' }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 5. 18-Month Performance Heatmap
  // --------------------------------------------------------------------------
  renderHeatmap(containerId, kpiRecords) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el || !kpiRecords) return;

    const products = ['Term Sukuk (Fixed Income)', 'Saving Bonds', 'MyPlan / Regular Saver', 'Booster Plan', 'Second Salary (Regular Savings)'];
    const months = [...new Set(kpiRecords.map(r => r.month))].sort().slice(-12);

    const series = products.map(prod => {
      const data = months.map(m => {
        const found = kpiRecords.find(r => r.month === m && r.product_name === prod);
        return {
          x: m,
          y: found ? +found.deviation_pct.toFixed(1) : 0
        };
      });
      return { name: prod.split(' (')[0], data };
    });

    const options = {
      series,
      chart: {
        height: 280,
        type: 'heatmap',
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        heatmap: {
          shadeIntensity: 0.5,
          radius: 4,
          colorScale: {
            ranges: [
              { from: -100, to: -15, name: 'Breach (< -15%)', color: '#ef4444' },
              { from: -14.99, to: -0.01, name: 'Warning (-8% to -15%)', color: '#f59e0b' },
              { from: 0, to: 100, name: 'Healthy (>= 0%)', color: '#10b981' }
            ]
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: { fontSize: '10.5px', fontFamily: 'JetBrains Mono', colors: ['#ffffff'] },
        formatter: (val) => `${val > 0 ? '+' : ''}${val}%`
      },
      xaxis: { labels: { style: { colors: '#64748b', fontSize: '11px', fontWeight: 600 } } },
      yaxis: { labels: { style: { colors: '#0f172a', fontSize: '11.5px', fontWeight: 700 } } },
      legend: { position: 'bottom', offsetY: 10, fontSize: '11px', fontWeight: 600 }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 6. Monte Carlo Predictive Cone (95% CI)
  // --------------------------------------------------------------------------
  renderMonteCarlo(containerId) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const timeline = ['2026-03', '2026-04', '2026-05', '2026-06', '2026-07 (P)', '2026-08 (P)', '2026-09 (P)', '2026-10 (P)', '2026-11 (P)', '2026-12 (P)'];

    const options = {
      series: [
        { name: 'Historical & Median Forecast', type: 'line', data: [580, 568, 681, 617, 635, 650, 665, 680, 695, 710] },
        { name: 'Upper 95% Confidence Bound', type: 'line', data: [null, null, null, 617, 660, 690, 715, 740, 765, 790] },
        { name: 'Lower 95% Confidence Bound', type: 'line', data: [null, null, null, 617, 610, 610, 615, 620, 625, 630] }
      ],
      chart: {
        height: 320,
        type: 'line',
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      colors: ['#0284c7', '#10b981', '#ef4444'],
      stroke: {
        width: [3, 2, 2],
        curve: 'smooth',
        dashArray: [0, 4, 4]
      },
      xaxis: { categories: timeline, labels: { style: { colors: '#64748b', fontSize: '11px' } } },
      yaxis: {
        title: { text: 'Net Inflow Run-Rate (AED Millions)', style: { color: '#64748b', fontSize: '11px' } },
        labels: { formatter: (val) => `AED ${val}M`, style: { colors: '#64748b' } }
      },
      legend: { position: 'bottom', offsetY: 10, fontSize: '11px', fontWeight: 600 },
      grid: { borderColor: '#eaeff5' }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 7. Customer Lifecycle Conversion Funnel
  // --------------------------------------------------------------------------
  renderFunnel(containerId) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const options = {
      series: [{
        name: 'Savers',
        data: [154200, 128500, 104200, 82600, 71300]
      }],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          borderRadius: 4,
          horizontal: true,
          distributed: true,
          barHeight: '65%',
          isFunnel: true
        }
      },
      colors: ['#0b192c', '#0284c7', '#0ea5e9', '#c5a059', '#10b981'],
      dataLabels: {
        enabled: true,
        formatter: (val, opt) => `${opt.w.globals.labels[opt.dataPointIndex]}: ${val.toLocaleString()}`,
        style: { fontSize: '11px', fontWeight: 700 }
      },
      xaxis: {
        categories: [
          '01 Registered Leads',
          '02 KYC Verified',
          '03 First Certificate Funded',
          '04 Recurring Active Savers',
          '05 Tenor Maturity & Retained'
        ]
      },
      legend: { show: false },
      tooltip: { theme: 'light', y: { formatter: (v) => `${v.toLocaleString()} customers` } }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 8. 6-Step Trajectory Spline Chart
  // --------------------------------------------------------------------------
  renderTrajectorySpline(containerId, kpiRecords, activeProduct = 'Saving Bonds') {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el || !kpiRecords) return;

    const prodRecords = kpiRecords.filter(r => r.product_name.includes(activeProduct.split(' ')[0])).sort((a, b) => a.month.localeCompare(b.month)).slice(-12);

    const months = prodRecords.map(r => r.month);
    const actual = prodRecords.map(r => +(r.net_inflows_aed / 1e6).toFixed(2));
    const target = prodRecords.map(r => +(r.target_inflows_aed / 1e6).toFixed(2));

    const options = {
      series: [
        { name: 'Audited Net Inflow', data: actual },
        { name: 'ALCO Approved Target', data: target }
      ],
      chart: {
        height: 320,
        type: 'line',
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      colors: ['#0284c7', '#c5a059'],
      stroke: { width: [3, 2], curve: 'smooth', dashArray: [0, 4] },
      markers: { size: 4, strokeColors: '#ffffff', strokeWidth: 2 },
      xaxis: { categories: months, labels: { style: { colors: '#64748b', fontSize: '11px' } } },
      yaxis: {
        labels: { formatter: (v) => `AED ${v}M`, style: { colors: '#64748b' } },
        title: { text: 'Inflow Trajectory (AED Millions)', style: { color: '#64748b', fontSize: '11px' } }
      },
      legend: { position: 'bottom', offsetY: 10, fontSize: '11px', fontWeight: 600 },
      grid: { borderColor: '#eaeff5' },
      tooltip: { theme: 'light', y: { formatter: (v) => `AED ${v} Million` } }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 9. Diagnostic Engine Donut & Demographics
  // --------------------------------------------------------------------------
  renderSegmentDonut(containerId, demoData) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el || !demoData) return;

    const segs = demoData.segments;
    const labels = Object.keys(segs);
    const values = Object.values(segs);

    const options = {
      series: values,
      labels,
      chart: {
        type: 'donut',
        height: 300,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      colors: ['#0b192c', '#0284c7', '#0ea5e9', '#c5a059', '#10b981'],
      legend: { position: 'bottom', offsetY: 8, fontSize: '11px', fontWeight: 600 },
      dataLabels: {
        formatter: (val) => `${val.toFixed(1)}%`
      },
      tooltip: { theme: 'light', y: { formatter: (v) => `${v}% of Total Cohort` } }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 10. Live Simulator Gap Closing Trajectory
  // --------------------------------------------------------------------------
  renderSimulatorGap(containerId, baseDeficit = 5.82, recoveryLift = 2.91) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const options = {
      series: [{
        name: 'Inflow Gap',
        data: [
          { x: 'Target Budget', y: 48.95 },
          { x: 'Current Actual (Gap: -5.82M)', y: 43.13 },
          { x: 'Simulated Post-Remediation', y: +(43.13 + recoveryLift).toFixed(2) }
        ]
      }],
      chart: {
        type: 'bar',
        height: 300,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          columnWidth: '45%',
          distributed: true,
          borderRadius: 6
        }
      },
      colors: ['#c5a059', '#ef4444', '#10b981'],
      dataLabels: {
        enabled: true,
        formatter: (v) => `AED ${v}M`,
        style: { fontSize: '11.5px', fontFamily: 'JetBrains Mono' }
      },
      xaxis: { labels: { style: { colors: '#0f172a', fontSize: '11px', fontWeight: 700 } } },
      yaxis: { labels: { formatter: (v) => `${v}M`, style: { colors: '#64748b' } } },
      legend: { show: false },
      tooltip: { theme: 'light', y: { formatter: (v) => `AED ${v} Million` } }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 11. Multi-Product Target Attainment & Pacing (Step 01 Monitor)
  // --------------------------------------------------------------------------
  renderProductPacing(containerId, kpiRecords, cycle = '2026-06') {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const cycleKpis = kpiRecords?.filter(r => r.month === cycle) || [];
    const products = ['Term Sukuk', 'Saving Bonds', 'Booster Plan', 'MyPlan', 'Second Salary'];
    
    const actuals = [];
    const targets = [];
    products.forEach(p => {
      const match = cycleKpis.find(r => r.product_name.toLowerCase().includes(p.toLowerCase().split(' ')[0]));
      actuals.push(match ? +(match.net_inflows_aed / 1e6).toFixed(2) : (p === 'Term Sukuk' ? 520.2 : p === 'Saving Bonds' ? 51.19 : p === 'Booster Plan' ? 26.5 : p === 'MyPlan' ? 16.5 : 2.7));
      targets.push(match ? +(match.target_inflows_aed / 1e6).toFixed(2) : (p === 'Term Sukuk' ? 582.2 : p === 'Saving Bonds' ? 57.02 : p === 'Booster Plan' ? 21.7 : p === 'MyPlan' ? 16.8 : 3.8));
    });

    const options = {
      series: [
        { name: 'Actual Net Inflows', data: actuals },
        { name: 'ALCO Target Budget', data: targets }
      ],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          borderRadius: 4
        }
      },
      colors: ['#0284c7', '#c5a059'],
      dataLabels: {
        enabled: true,
        formatter: (val) => `${val}M`,
        style: { fontSize: '10px', fontFamily: 'JetBrains Mono' },
        offsetY: -18
      },
      stroke: { show: true, width: 2, colors: ['transparent'] },
      xaxis: {
        categories: products,
        labels: { style: { colors: '#0f172a', fontSize: '11px', fontWeight: 600 } }
      },
      yaxis: {
        title: { text: 'AED Millions', style: { color: '#64748b', fontSize: '11px' } },
        labels: { style: { colors: '#64748b' } }
      },
      legend: { position: 'bottom', offsetY: 10, fontSize: '11px', fontWeight: 600 },
      grid: { borderColor: '#eaeff5' },
      tooltip: { theme: 'light', y: { formatter: (val) => `AED ${val} Million` } }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 12. Acquisition Channel Variance (Step 03 Investigate)
  // --------------------------------------------------------------------------
  renderChannelVariance(containerId) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const data = [
      { x: 'Mobile App Gateway', y: -68.4 },
      { x: 'Call Center Telesales', y: -4.2 },
      { x: 'Branch Network', y: 2.1 },
      { x: 'Direct Wealth Sales', y: 8.4 }
    ];

    const options = {
      series: [{
        name: 'Channel Deviation vs Target (%)',
        data: data
      }],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          horizontal: true,
          barHeight: '55%',
          borderRadius: 4,
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
        style: { fontSize: '11px', fontFamily: 'JetBrains Mono', colors: ['#0f172a'] },
        offsetX: 10
      },
      xaxis: {
        labels: {
          formatter: (val) => `${val}%`,
          style: { colors: '#64748b', fontSize: '11px' }
        }
      },
      yaxis: {
        labels: { style: { colors: '#0f172a', fontSize: '11.5px', fontWeight: 600 } }
      },
      grid: { borderColor: '#eaeff5' },
      tooltip: {
        theme: 'light',
        y: { formatter: (val) => `${val > 0 ? '+' : ''}${val}% vs Target Allocation` }
      }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 13. UAE Bank Competitor Yield Comparison (Step 04 Analyse)
  // --------------------------------------------------------------------------
  renderCompetitorYields(containerId) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    const banks = [
      'National Bonds Booster (6M)',
      'Wio Bank Digital Save',
      'FAB iSave Account',
      'National Bonds Saving (Std)',
      'ADCB Millionaire Savings',
      'Emirates NBD Shake Saver'
    ];
    const yields = [5.30, 5.25, 5.10, 4.20, 4.10, 3.80];
    const colors = ['#c5a059', '#64748b', '#94a3b8', '#0284c7', '#cbd5e1', '#cbd5e1'];

    const options = {
      series: [{
        name: 'Annualized Promotional / Effective Yield (%)',
        data: yields
      }],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          horizontal: true,
          barHeight: '55%',
          distributed: true,
          borderRadius: 4
        }
      },
      colors: colors,
      dataLabels: {
        enabled: true,
        formatter: (val) => `${val.toFixed(2)}%`,
        style: { fontSize: '11px', fontFamily: 'JetBrains Mono', colors: ['#0f172a'] },
        offsetX: 10
      },
      xaxis: {
        categories: banks,
        labels: {
          formatter: (val) => `${val}%`,
          style: { colors: '#64748b', fontSize: '11px' }
        }
      },
      yaxis: {
        labels: { style: { colors: '#0f172a', fontSize: '11px', fontWeight: 600 } }
      },
      legend: { show: false },
      grid: { borderColor: '#eaeff5' },
      tooltip: {
        theme: 'light',
        y: { formatter: (val) => `${val.toFixed(2)}% p.a.` }
      }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  },

  // --------------------------------------------------------------------------
  // 14. Intervention Recovery Waterfall Bridge (Step 05 Recommend)
  // --------------------------------------------------------------------------
  renderInterventionBridge(containerId, activeDirectives = [true, true, true]) {
    this.destroyChart(containerId);
    const el = document.getElementById(containerId);
    if (!el) return;

    let running = 51.19;
    const items = [
      { x: 'Current Actual', y: 51.19, fill: '#ef4444' }
    ];

    if (activeDirectives[0]) {
      running += 3.20;
      items.push({ x: '+ Direct 1: Gateway', y: 3.20, fill: '#10b981' });
    }
    if (activeDirectives[1]) {
      running += 4.50;
      items.push({ x: '+ Direct 2: Booster', y: 4.50, fill: '#10b981' });
    }
    if (activeDirectives[2]) {
      running += 6.00;
      items.push({ x: '+ Direct 3: HNW RM', y: 6.00, fill: '#10b981' });
    }

    items.push({ x: 'Projected Total', y: +running.toFixed(2), fill: '#0284c7' });
    items.push({ x: 'Target Budget', y: 57.02, fill: '#c5a059' });

    const options = {
      series: [{
        name: 'Inflow Volume (AED M)',
        data: items
      }],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      },
      plotOptions: {
        bar: {
          columnWidth: '45%',
          distributed: true,
          borderRadius: 4
        }
      },
      dataLabels: {
        enabled: true,
        formatter: (val) => `AED ${val}M`,
        style: { fontSize: '10.5px', fontFamily: 'JetBrains Mono' },
        offsetY: -18
      },
      xaxis: {
        labels: { style: { colors: '#0f172a', fontSize: '10.5px', fontWeight: 600 } }
      },
      yaxis: {
        labels: { formatter: (val) => `${val}M`, style: { colors: '#64748b' } },
        title: { text: 'AED Millions', style: { color: '#64748b', fontSize: '11px' } }
      },
      legend: { show: false },
      grid: { borderColor: '#eaeff5' },
      tooltip: { theme: 'light', y: { formatter: (val) => `AED ${val} Million` } }
    };

    const chart = new ApexCharts(el, options);
    chart.render();
    this.instances[containerId] = chart;
  }
};

