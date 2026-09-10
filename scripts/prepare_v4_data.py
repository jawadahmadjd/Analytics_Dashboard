import os
import json
import pandas as pd

def compile_data():
    kpi_df = pd.read_csv('data/product_portfolio_kpis_alerts.csv')
    kpi_records = kpi_df.to_dict(orient='records')

    with open('data/market_intelligence_data.json', 'r', encoding='utf-8') as f:
        market_data = json.load(f)

    with open('data/product_knowledge_base.json', 'r', encoding='utf-8') as f:
        kb_data = json.load(f)

    with open('data/escalation_tickets.json', 'r', encoding='utf-8') as f:
        tickets_data = json.load(f)

    with open('data/dispatch_log.json', 'r', encoding='utf-8') as f:
        dispatch_data = json.load(f)

    with open('data/audit_trail.json', 'r', encoding='utf-8') as f:
        audit_data = json.load(f)

    customer_demographics = {
        "segments": {
            "Mass Affluent": 34.98,
            "Emirati National": 28.05,
            "Retail / Salaried": 24.99,
            "High Net Worth (HNW)": 7.95,
            "Youth & Minor": 4.03
        },
        "channels": {
            "Mobile App": 47.86,
            "Branch Network": 28.17,
            "Web Portal": 11.98,
            "Direct Sales Agents": 8.0,
            "Exchange Houses": 3.99
        },
        "age_groups": {
            "18-30": 22.63,
            "31-45": 49.78,
            "46-60": 19.08,
            "60+": 8.51
        },
        "income_by_segment": {
            "Emirati National": 73066,
            "High Net Worth (HNW)": 265773,
            "Mass Affluent": 48987,
            "Retail / Salaried": 17975,
            "Youth & Minor": 18029
        }
    }

    slides_summary = []
    if os.path.exists('data/svg_extracted_data.json'):
        with open('data/svg_extracted_data.json', 'r', encoding='utf-8') as f:
            slides_data = json.load(f)
            for s in slides_data:
                slides_summary.append({
                    "slide_id": s.get("slide_id"),
                    "title": s.get("title", f"Slide {s.get('slide_id')}"),
                    "category": s.get("category", "General"),
                    "snippet": s.get("text", "")[:280]
                })

    bundle = {
        "kpi_records": kpi_records,
        "market_data": market_data,
        "kb_data": kb_data,
        "tickets_data": tickets_data,
        "dispatch_data": dispatch_data,
        "audit_data": audit_data,
        "demographics": customer_demographics,
        "slides_summary": slides_summary
    }

    os.makedirs('v4/data', exist_ok=True)
    with open('v4/data/ground_truth.json', 'w', encoding='utf-8') as f:
        json.dump(bundle, f, indent=2)

    js_content = f"// Ground Truth Data Module for National Bonds Corporation V4\nwindow.NBC_DATA = {json.dumps(bundle, indent=2)};\n"
    with open('v4/js/data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

    print("Successfully compiled v4/data/ground_truth.json and v4/js/data.js")

if __name__ == '__main__':
    compile_data()
