"""
Deep Analysis of all 58 Slides from National Bonds H1 Product Report 2026.
Extracts product performance, volumes, targets, initiatives, and visual audits.
"""

import json
import os
import glob
import re

with open('svg_extracted_data.json', 'r', encoding='utf-8') as f:
    slides = json.load(f)

print(f"Total Slides Analyzed: {len(slides)}")

with open('comprehensive_slide_audit.txt', 'w', encoding='utf-8') as out_f:
    for idx, s in enumerate(slides, 1):
        num = s['slide_number']
        fname = s['filename']
        text = s['full_text']
        imgs = s['embedded_images']
        
        out_f.write(f"\n{'='*80}\n")
        out_f.write(f"SLIDE {num} | {fname} | Embedded Images: {len(imgs)}\n")
        out_f.write(f"{'='*80}\n")
        
        if imgs:
            out_f.write("Embedded Images:\n")
            for img in imgs:
                out_f.write(f"  - {img['image_filename']} ({img['size_bytes']:,} bytes)\n")
                
        out_f.write("\nExtracted Text Lines:\n")
        for line in s['text_elements']:
            out_f.write(f"  * {line}\n")
            
print("Audit written to comprehensive_slide_audit.txt")
