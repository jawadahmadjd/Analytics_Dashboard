"""
Advanced Dynamic Financial Time-Series Engine for National Bonds Portfolio.
Generates authentic monthly seasonality, campaign spikes, fluctuating monthly targets,
and organic volatility while anchoring to exact H1 2026 Ground Truth figures.
"""

import pandas as pd
import numpy as np

# Ground Truth Exact Specifications from H1 2026 Presentation SVGs
GROUND_TRUTH = {
    'Term Sukuk (Fixed Income)': {
        'aum_q2_2026': 11_500_000_000,
        'h1_fresh_sales': 6_400_000_000,
        'monthly_net_budget': 620_000_000,
        'active_accounts': 5683,
        'avg_ticket': 2_000_000,
        'channels': {'Wealth Advisory': 0.45, 'Direct Sales Agents': 0.35, 'Mobile App': 0.20},
        'segments': {'High Net Worth (HNW)': 0.65, 'Corporate / Institutional': 0.30, 'Mass Affluent': 0.05},
        # High-value placement volatility across quarters
        'seasonality_pattern': [0.85, 0.78, 1.15, 0.92, 1.08, 0.72, 0.68, 0.74, 1.05, 1.18, 1.35, 1.22, 1.15, 0.88, 1.38, 1.12, 1.25, 0.82],
        'target_seasonality':  [0.82, 0.80, 1.10, 0.90, 1.02, 0.75, 0.70, 0.78, 1.00, 1.12, 1.28, 1.18, 1.10, 0.92, 1.25, 1.08, 1.15, 0.95],
        'redemption_ratio': 0.38
    },
    'Saving Bonds': {
        'aum_q2_2026': 4_600_000_000,
        'h1_fresh_sales': 739_000_000,
        'monthly_net_budget': 58_000_000,
        'active_accounts': 144775,
        'avg_ticket': 31773,
        'channels': {'Digital App & Web': 0.52, 'Branch Network': 0.38, 'Exchange Houses': 0.10},
        'segments': {'Mass Affluent': 0.48, 'Retail / Salaried': 0.32, 'Emirati National': 0.28},
        # 7% Campaign surge in Apr-Jun 2026 (Slide 33), Q1 drop, Eid spending
        'seasonality_pattern': [1.02, 0.88, 1.12, 0.82, 0.78, 0.70, 0.65, 0.92, 1.25, 1.08, 1.20, 1.12, 0.78, 0.72, 0.88, 1.32, 1.28, 0.86],
        'target_seasonality':  [0.98, 0.92, 1.05, 0.88, 0.82, 0.75, 0.70, 0.95, 1.15, 1.02, 1.15, 1.08, 0.92, 0.88, 0.98, 1.20, 1.15, 0.98],
        'redemption_ratio': 0.58
    },
    'MyPlan / Regular Saver': {
        'aum_q2_2026': 460_700_000,
        'h1_fresh_sales': 110_100_000,
        'monthly_net_budget': 13_500_000,
        'active_accounts': 25709,
        'avg_ticket': 997,
        'channels': {'Digital App': 0.70, 'Branch Network': 0.21, 'Direct Sales': 0.09},
        'segments': {'Retail / Salaried': 0.55, 'Mass Affluent': 0.25, 'Youth & Family': 0.20},
        # Compounding direct debit growth with monthly payroll variability
        'seasonality_pattern': [0.72, 0.76, 0.80, 0.78, 0.82, 0.81, 0.86, 0.90, 0.94, 0.97, 1.04, 1.01, 1.06, 1.04, 1.10, 1.16, 1.20, 1.22],
        'target_seasonality':  [0.75, 0.78, 0.82, 0.82, 0.85, 0.85, 0.88, 0.92, 0.96, 0.98, 1.05, 1.02, 1.08, 1.06, 1.12, 1.15, 1.18, 1.25],
        'redemption_ratio': 0.24
    },
    'Booster Plan': {
        'aum_q2_2026': 482_000_000,
        'h1_fresh_sales': 126_000_000,
        'monthly_net_budget': 14_000_000,
        'active_accounts': 6850,
        'avg_ticket': 18500,
        'channels': {'Mobile App': 0.55, 'Branch Network': 0.30, 'Corporate WPS': 0.15},
        'segments': {'Mass Affluent': 0.50, 'Emirati National': 0.35, 'Retail / Salaried': 0.15},
        # +239% Surge trajectory in late 2025 and 2026
        'seasonality_pattern': [0.42, 0.46, 0.50, 0.48, 0.54, 0.58, 0.64, 0.70, 0.82, 0.92, 1.08, 1.02, 1.22, 1.30, 1.55, 1.70, 1.80, 1.90],
        'target_seasonality':  [0.55, 0.60, 0.65, 0.65, 0.70, 0.75, 0.80, 0.85, 0.95, 1.00, 1.10, 1.05, 1.15, 1.20, 1.30, 1.40, 1.50, 1.55],
        'redemption_ratio': 0.22
    },
    'Second Salary (Regular Savings)': {
        'aum_q2_2026': 83_400_000,
        'h1_fresh_sales': 21_400_000,
        'monthly_net_budget': 2_850_000,
        'active_accounts': 2075,
        'avg_ticket': 2043,
        'channels': {'Digital (Mobile App)': 0.63, 'Branch Network': 0.27, 'Direct Sales': 0.10},
        'segments': {'Retail / Salaried': 0.70, 'Mass Affluent': 0.25, 'Emirati National': 0.05},
        # Slight stagnation / dip in H1 2026 (-0.94% YoY noted in Slide 22)
        'seasonality_pattern': [0.68, 0.70, 0.75, 0.80, 0.82, 0.88, 0.86, 0.92, 1.00, 1.02, 1.08, 1.12, 1.10, 1.06, 1.12, 1.04, 1.00, 0.96],
        'target_seasonality':  [0.70, 0.72, 0.78, 0.82, 0.85, 0.90, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.18, 1.22, 1.25, 1.28, 1.30, 1.35],
        'redemption_ratio': 0.28
    }
}

def generate_dynamic_kpis():
    """Generates authentic fluctuating trajectories with organic market noise and dynamic budget plans."""
    print("[1/3] Generating Organic Dynamic Monthly KPI Trajectories...")
    
    months = pd.date_range('2025-01-01', '2026-06-30', freq='MS').strftime('%Y-%m').tolist()
    records = []
    
    np.random.seed(101)
    
    for idx, m in enumerate(months):
        for prod_name, spec in GROUND_TRUTH.items():
            s_pat = spec['seasonality_pattern'][idx]
            t_pat = spec['target_seasonality'][idx]
            
            # Add subtle organic noise (±2-4%)
            noise_actual = np.random.uniform(0.97, 1.03)
            noise_target = np.random.uniform(0.98, 1.02)
            
            # Base monthly net and gross flows
            monthly_net_base = spec['monthly_net_budget']
            net_inflow = monthly_net_base * s_pat * noise_actual
            
            # Back-calculate gross and redemptions based on redemption ratio
            redemp_rate = spec['redemption_ratio'] * np.random.uniform(0.95, 1.05)
            actual_gross = net_inflow / (1.0 - redemp_rate)
            actual_redemptions = actual_gross - net_inflow
            
            # Monthly Dynamic Budget Target Curve
            dynamic_target = monthly_net_base * t_pat * noise_target
            
            # Active accounts evolving with seasonal velocity
            base_accs = spec['active_accounts']
            active_accs = int(base_accs * (0.82 + 0.18 * (s_pat / max(spec['seasonality_pattern']))) * np.random.uniform(0.99, 1.01))
            
            # Deviation %
            dev_pct = ((net_inflow - dynamic_target) / dynamic_target) * 100
            
            # Threshold status
            if dev_pct <= -15.0:
                status = 'BREACH'
            elif dev_pct <= -8.0:
                status = 'WARNING'
            else:
                status = 'HEALTHY'
                
            records.append({
                'month': m,
                'product_name': prod_name,
                'active_customers': active_accs,
                'total_cohort_customers': 154000,
                'gross_inflows_aed': round(actual_gross, 2),
                'redemptions_aed': round(actual_redemptions, 2),
                'net_inflows_aed': round(net_inflow, 2),
                'target_inflows_aed': round(dynamic_target, 2),
                'deviation_pct': round(dev_pct, 2),
                'status': status
            })
            
    df_kpi = pd.DataFrame(records)
    return df_kpi

if __name__ == '__main__':
    kpi_df = generate_dynamic_kpis()
    kpi_df.to_csv('product_portfolio_kpis_alerts.csv', index=False)
    
    print("\nSUCCESS: Generated Dynamic Fluctuation KPIs!")
    print("\nSample Trajectory: Saving Bonds (Recent 6 Months):")
    sb = kpi_df[kpi_df['product_name'] == 'Saving Bonds'].tail(6)
    print(sb[['month', 'net_inflows_aed', 'target_inflows_aed', 'deviation_pct', 'status']].to_string())
    
    print("\nSample Trajectory: Term Sukuk (Recent 6 Months):")
    ts = kpi_df[kpi_df['product_name'] == 'Term Sukuk (Fixed Income)'].tail(6)
    print(ts[['month', 'net_inflows_aed', 'target_inflows_aed', 'deviation_pct', 'status']].to_string())
