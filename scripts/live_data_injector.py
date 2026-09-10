# National Bonds Corporation — Live Customer Data Injector
# Injects 100 random dummy customers every minute for 3 hours (180 iterations = 18,000 customers).

import os
import sys
import time
import json
import random
import datetime
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH_ROOT = os.path.join(BASE_DIR, 'cleaned_national_bonds_customers.csv')
CSV_PATH_DATA = os.path.join(BASE_DIR, 'data', 'cleaned_national_bonds_customers.csv')
STATUS_PATH = os.path.join(BASE_DIR, 'data', 'injector_status.json')

SEGMENTS = ['Mass Affluent', 'Youth & Minor', 'Retail / Salaried', 'Emirati National', 'High Net Worth (HNW)']
SEGMENT_WEIGHTS = [0.35, 0.15, 0.25, 0.15, 0.10]

CHANNELS = ['Mobile App', 'Web Portal', 'Branch Network', 'Direct Sales Agents', 'Exchange Houses']
CHANNEL_WEIGHTS = [0.45, 0.25, 0.15, 0.10, 0.05]

def get_current_max_id():
    try:
        if os.path.exists(CSV_PATH_ROOT):
            df = pd.read_csv(CSV_PATH_ROOT, usecols=['customer_id'])
            return int(df['customer_id'].max())
    except Exception as e:
        print(f'[Injector] Warning reading max id: {e}')
    return 1154000

def generate_100_customers(start_id):
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    month_str = now.strftime('%Y-%m')
    
    rows = []
    for i in range(100):
        cid = start_id + i + 1
        age = random.randint(21, 72)
        income = round(random.uniform(8500.0, 115000.0), 2)
        seg = random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS, k=1)[0]
        chan = random.choices(CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]
        
        # Ensure customer holds at least 1 product
        p_saving = 1 if random.random() < 0.70 else 0
        p_sukuk = 1 if random.random() < 0.35 else 0
        p_myplan = 1 if random.random() < 0.40 else 0
        p_booster = 1 if random.random() < 0.25 else 0
        p_salary = 1 if random.random() < 0.20 else 0
        
        if (p_saving + p_sukuk + p_myplan + p_booster + p_salary) == 0:
            p_saving = 1
            
        rows.append({
            'customer_id': cid,
            'date': date_str,
            'month': month_str,
            'age': age,
            'income_aed': income,
            'customer_segment': seg,
            'primary_channel': chan,
            'Term Sukuk (Fixed Income)': p_sukuk,
            'Saving Bonds': p_saving,
            'MyPlan / Regular Saver': p_myplan,
            'Booster Plan': p_booster,
            'Second Salary (Regular Savings)': p_salary
        })
    return rows

def append_to_csv(rows, filepath):
    if not os.path.exists(filepath):
        return
    df_new = pd.DataFrame(rows)
    df_new.to_csv(filepath, mode='a', header=False, index=False)

def update_status(iteration, total_iterations, injected_count, last_id):
    status_data = {
        'current_iteration': iteration,
        'total_iterations': total_iterations,
        'records_injected_this_session': injected_count,
        'last_customer_id': last_id,
        'last_injected_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'running' if iteration < total_iterations else 'completed',
        'rate': '100 records/minute',
        'planned_duration_hours': 3.0
    }
    try:
        os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
        with open(STATUS_PATH, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        print(f'[Injector] Error writing status: {e}')

def main():
    TOTAL_ITERATIONS = 180 # 3 hours * 60 min = 180 iterations
    INTERVAL_SECONDS = 60 # 1 minute
    
    current_id = get_current_max_id()
    print(f'=== National Bonds Real-Time Customer Data Injector ===')
    print(f'Target: 100 dummy records/minute for 3 hours (180 iterations = 18,000 records)')
    print(f'Starting from Customer ID: {current_id + 1}')
    print(f'CSV Targets: {CSV_PATH_ROOT} & {CSV_PATH_DATA}')
    print('========================================================')
    sys.stdout.flush()
    
    total_injected = 0
    for iteration in range(1, TOTAL_ITERATIONS + 1):
        try:
            rows = generate_100_customers(current_id)
            append_to_csv(rows, CSV_PATH_ROOT)
            append_to_csv(rows, CSV_PATH_DATA)
            
            current_id += 100
            total_injected += 100
            update_status(iteration, TOTAL_ITERATIONS, total_injected, current_id)
            
            ts = datetime.datetime.now().strftime('%H:%M:%S')
            print(f'[{ts}] [Iteration {iteration:3d}/{TOTAL_ITERATIONS}] Injected 100 records. (Total Session Injected: {total_injected:,} | Last ID: {current_id})')
            sys.stdout.flush()
            
            if iteration < TOTAL_ITERATIONS:
                time.sleep(INTERVAL_SECONDS)
        except Exception as ex:
            print(f'[Injector] Error during iteration {iteration}: {ex}')
            sys.stdout.flush()
            time.sleep(10)
            
    print(f'=== Data Injector Session Successfully Completed ({total_injected:,} records) ===')
    update_status(TOTAL_ITERATIONS, TOTAL_ITERATIONS, total_injected, current_id)

if __name__ == '__main__':
    main()
