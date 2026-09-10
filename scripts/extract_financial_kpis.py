"""
Structured Financial Metric Extractor from National Bonds H1 2026 Product Report
Extracts all product names, AUM, inflows, redemptions, campaigns, and KPIs.
"""

import json
import re

with open('svg_extracted_data.json', 'r', encoding='utf-8') as f:
    slides = json.load(f)

financial_slides = []

for s in slides:
    text = s['full_text']
    num = s['slide_number']
    fname = s['filename']
    imgs = s['embedded_images']
    
    # Filter key lines
    lines = s['text_elements']
    key_lines = [l for l in lines if any(c.isdigit() for c in l) or any(k in l.lower() for k in ['aed', 'mn', 'sukuk', 'salary', 'saving', 'booster', 'mudaraba', 'product', 'target', 'inflow', 'redemption'])]
    
    if key_lines:
        financial_slides.append({
            'slide_num': num,
            'filename': fname,
            'key_lines': key_lines,
            'image_count': len(imgs)
        })

print(f"Total Slides with Key Financial / Product Data: {len(financial_slides)}")

with open('extracted_h1_financial_metrics.txt', 'w', encoding='utf-8') as f:
    for item in financial_slides:
        f.write(f"\n================ SLIDE {item['slide_num']} ({item['filename']}) ================\n")
        f.write(f"Images: {item['image_count']}\n")
        for l in item['key_lines']:
            f.write(f"  - {l}\n")

print("Saved to extracted_h1_financial_metrics.txt")
