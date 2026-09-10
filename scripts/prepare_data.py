"""
Data Preparation & Repurposing Pipeline for National Bonds Product Intelligence
Processes Full 13.6M Record Santander Dataset into Enterprise-Scale 5-Product Portfolio.
"""

import os
import glob
import pandas as pd
import numpy as np

# 5 Target Products mapped to robust, high-volume Santander core products
PRODUCT_MAPPING = {
    'ind_cco_fin_ult1': 'National Bonds Savings Certificates',  # Core universal savings account (~500k+ holders/month)
    'ind_plan_fin_ult1': 'Booster Plan',                        # Milestone / pension plan (~25k+ holders/month)
    'ind_dela_fin_ult1': 'Term Sukuk (Fixed Income)',           # Long-term placement / deposit (~45k+ holders/month)
    'ind_nomina_ult1': 'Second Salary (Regular Savings)',       # Payroll / regular recurring (~60k+ holders/month)
    'ind_fond_fin_ult1': 'Global Growth Mudaraba Fund'          # Multi-asset investment fund (~20k+ holders/month)
}

CHANNELS = ['Mobile App', 'Web Portal', 'Branch Network', 'Direct Sales Agents', 'Corporate Partnerships']
CUSTOMER_SEGMENTS = ['Mass Affluent', 'High Net Worth (HNW)', 'Retail / Salaried', 'Corporate / Institutional', 'Youth & Family']

def load_full_parquet(parquet_folder='paraquet files', sample_fraction=0.35):
    """
    Reads all 35 Santander parquet partitions (~13.6M rows total).
    A 35% sample produces ~4.8 Million customer records across 17 months
    (~280,000 - 320,000 customers per monthly snapshot), representing enterprise scale.
    """
    files = glob.glob(os.path.join(parquet_folder, '*.parquet'))
    if not files:
        raise FileNotFoundError(f"No parquet files found in {parquet_folder}")
    
    print(f"[1/4] Loading all {len(files)} parquet files (Targeting enterprise cohort: {int(sample_fraction*100)}% of 13.6M rows)...")
    
    cols = ['fecha_dato', 'ncodpers', 'age', 'renta', 'segmento'] + list(PRODUCT_MAPPING.keys())
    
    sampled_chunks = []
    for f in files:
        df_part = pd.read_parquet(f, columns=cols)
        if sample_fraction < 1.0:
            df_part = df_part.sample(frac=sample_fraction, random_state=42)
        sampled_chunks.append(df_part)
        
    df = pd.concat(sampled_chunks, ignore_index=True)
    print(f"Loaded {len(df):,} records across all monthly cycles.")
    return df

def clean_and_repurpose(df):
    """Cleans demographic attributes and maps to National Bonds structure."""
    print("[2/4] Cleaning demographics and mapping to National Bonds Enterprise Portfolio...")
    
    # 1. Clean Age
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(38).astype(int)
    df['age'] = df['age'].clip(18, 85)
    
    # 2. Clean Income / Renta (AED equivalent)
    df['income_aed'] = pd.to_numeric(df['renta'], errors='coerce')
    median_income = df['income_aed'].median() if not df['income_aed'].isna().all() else 125000
    df['income_aed'] = df['income_aed'].fillna(median_income).round(2)
    
    # 3. Standardize Date and map to 2025-2026 pilot horizon
    df['fecha_dato'] = pd.to_datetime(df['fecha_dato'], errors='coerce')
    unique_dates = sorted(df['fecha_dato'].dropna().unique())
    new_dates = pd.date_range('2025-02-01', periods=len(unique_dates), freq='MS')
    date_map = {orig: new_dates[i] for i, orig in enumerate(unique_dates)}
    
    df['date'] = df['fecha_dato'].map(date_map).fillna(pd.to_datetime('2026-06-01'))
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    # 4. Map Customer Segments
    segment_map = {
        '01 - TOP': 'High Net Worth (HNW)',
        '02 - PARTICULARES': 'Mass Affluent',
        '03 - UNIVERSITARIO': 'Youth & Family'
    }
    np.random.seed(42)
    if 'segmento' in df.columns:
        fallback_segments = pd.Series(np.random.choice(CUSTOMER_SEGMENTS, size=len(df), p=[0.35, 0.15, 0.30, 0.10, 0.10]), index=df.index)
        df['customer_segment'] = df['segmento'].map(segment_map).fillna(fallback_segments)
    else:
        df['customer_segment'] = np.random.choice(CUSTOMER_SEGMENTS, size=len(df))
        
    # 5. Map Inflow Channels
    df['primary_channel'] = np.random.choice(CHANNELS, size=len(df), p=[0.45, 0.25, 0.15, 0.10, 0.05])
    
    # 6. Map 5 Pilot Products (scale to full population)
    for orig_col, target_prod in PRODUCT_MAPPING.items():
        if orig_col in df.columns:
            df[target_prod] = pd.to_numeric(df[orig_col], errors='coerce').fillna(0).astype(int)
        else:
            df[target_prod] = 0
            
    df['customer_id'] = df['ncodpers'].fillna(0).astype(int)
    
    final_cols = ['customer_id', 'date', 'month', 'age', 'income_aed', 'customer_segment', 'primary_channel'] + list(PRODUCT_MAPPING.values())
    return df[final_cols]

def generate_portfolio_kpis(df, scale_factor=2.85):
    """
    Aggregates product performance by Month, scaling sample counts to represent
    the full National Bonds verified customer population (~800k+ total customer accounts).
    """
    print("[3/4] Calculating Enterprise Monthly Portfolio KPIs & Threshold Deviations...")
    
    product_names = list(PRODUCT_MAPPING.values())
    records = []
    
    # Average financial ticket sizes per product in AED
    avg_ticket = {
        'National Bonds Savings Certificates': 3500,
        'Booster Plan': 12000,
        'Term Sukuk (Fixed Income)': 45000,
        'Second Salary (Regular Savings)': 3800,
        'Global Growth Mudaraba Fund': 22000
    }
    
    for m, group in df.groupby('month'):
        total_monthly_sample = len(group)
        total_active_population = int(total_monthly_sample * scale_factor)
        
        for prod in product_names:
            sample_active = int(group[prod].sum())
            # Scale to full enterprise population count
            active_holders = int(sample_active * scale_factor)
            
            ticket = avg_ticket.get(prod, 10000)
            
            # Monthly transaction volume simulation
            inflows = active_holders * ticket * np.random.uniform(0.12, 0.18)
            redemption_rate = 0.05 if 'Sukuk' in prod else (0.07 if 'Certificates' in prod else 0.06)
            redemptions = active_holders * ticket * redemption_rate * np.random.uniform(0.9, 1.15)
            net_inflow = inflows - redemptions
            
            # Target variance logic
            target_mult = np.random.uniform(1.05, 1.22)
            # Inject realistic scenario in recent cycles (e.g. Term Sukuk rate pressure)
            if m in ['2026-05', '2026-06'] and 'Term Sukuk' in prod:
                target_mult = 1.32
                net_inflow *= 0.85
            elif m in ['2026-04', '2026-05'] and 'Second Salary' in prod:
                target_mult = 1.28
                net_inflow *= 0.88
                
            target_inflow = (inflows - redemptions) * target_mult
            deviation_pct = ((net_inflow - target_inflow) / target_inflow) * 100
            
            if deviation_pct <= -15.0:
                status = 'BREACH'
            elif deviation_pct <= -8.0:
                status = 'WARNING'
            else:
                status = 'HEALTHY'
                
            records.append({
                'month': m,
                'product_name': prod,
                'active_customers': active_holders,
                'total_cohort_customers': total_active_population,
                'gross_inflows_aed': round(inflows, 2),
                'redemptions_aed': round(redemptions, 2),
                'net_inflows_aed': round(net_inflow, 2),
                'target_inflows_aed': round(target_inflow, 2),
                'deviation_pct': round(deviation_pct, 2),
                'status': status
            })
            
    kpi_df = pd.DataFrame(records)
    return kpi_df

if __name__ == '__main__':
    print("=== National Bonds Enterprise Scale Data Generation ===")
    
    # 1. Ingest 35% sample of 13.6M records (~4.8 Million customer snapshot records)
    raw_df = load_full_parquet('paraquet files', sample_fraction=0.35)
    
    # 2. Clean and map
    cleaned_df = clean_and_repurpose(raw_df)
    
    # 3. Generate KPI aggregations
    kpi_df = generate_portfolio_kpis(cleaned_df, scale_factor=2.85)
    
    # 4. Save prepared data (save a fast 250k slice for app UI queries and full KPIs)
    print("[4/4] Writing enterprise datasets to disk...")
    cleaned_df.sample(min(250000, len(cleaned_df)), random_state=42).to_csv('cleaned_national_bonds_customers.csv', index=False)
    kpi_df.to_csv('product_portfolio_kpis_alerts.csv', index=False)
    
    print("\nSUCCESS: Generated Enterprise Scale Portfolio Data:")
    for prod in PRODUCT_MAPPING.values():
        latest = kpi_df[(kpi_df['month'] == '2026-06') & (kpi_df['product_name'] == prod)].iloc[0]
        print(f" -> {prod:38s}: {latest['active_customers']:,} Active Accounts | Net Inflow: AED {latest['net_inflows_aed']/1e6:.1f}M")
