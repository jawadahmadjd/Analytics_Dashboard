"""
SVG Extraction & Visual Audit Processor for National Bonds H1 Product Report 2026
Extracts all text nodes, tables, embedded charts/images, and structured data from 58 SVGs.
"""

import os
import glob
import re
import json
import base64
from PIL import Image
import io

svg_dir = r'D:\Tools of Jawad\24- Data Analysis\Raw SVGs 2 Sep'
output_img_dir = r'D:\Tools of Jawad\24- Data Analysis\extracted_svg_images'
os.makedirs(output_img_dir, exist_ok=True)

svg_files = glob.glob(os.path.join(svg_dir, '*.svg'))

def get_slide_num(path):
    name = os.path.basename(path)
    nums = re.findall(r'\d+(?:\.\d+)?', name)
    return float(nums[0]) if nums else 999.0

svg_files.sort(key=get_slide_num)

extracted_data = []
all_embedded_images = []

for sf in svg_files:
    fname = os.path.basename(sf)
    with open(sf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Extract text from tags
    texts = re.findall(r'>([^<]+)<', content)
    cleaned_texts = []
    for t in texts:
        t_str = t.strip()
        if t_str and not t_str.startswith('<!--') and not t_str.startswith('{'):
            cleaned_texts.append(t_str)
            
    # Extract embedded base64 images
    img_matches = re.findall(r'<image[^>]+(?:href|xlink:href)=["\'](data:image/[^;]+;base64,([^"\']+))["\']', content)
    slide_images = []
    
    for idx, (data_uri, b64_str) in enumerate(img_matches):
        try:
            # Determine extension
            ext = 'png'
            if 'image/jpeg' in data_uri or 'image/jpg' in data_uri:
                ext = 'jpg'
            elif 'image/webp' in data_uri:
                ext = 'webp'
                
            img_filename = f"{fname.replace('.svg', '')}_img_{idx+1}.{ext}"
            img_path = os.path.join(output_img_dir, img_filename)
            
            # Decode and save
            img_bytes = base64.b64decode(b64_str)
            with open(img_path, 'wb') as img_f:
                img_f.write(img_bytes)
                
            slide_images.append({
                'image_filename': img_filename,
                'image_path': img_path,
                'size_bytes': len(img_bytes)
            })
            all_embedded_images.append(img_path)
        except Exception as e:
            print(f"Error saving image from {fname}: {e}")
            
    slide_entry = {
        'filename': fname,
        'slide_number': get_slide_num(sf),
        'text_elements': cleaned_texts,
        'full_text': ' '.join(cleaned_texts),
        'embedded_images': slide_images,
        'has_images': len(slide_images) > 0
    }
    extracted_data.append(slide_entry)

# Save JSON
with open('svg_extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, indent=2, ensure_ascii=False)

# Save Markdown summary
with open('svg_extracted_text_data.md', 'w', encoding='utf-8') as f:
    f.write('# National Bonds - H1 Product Report 2026: Extracted Text & Asset Inventory\n\n')
    for item in extracted_data:
        f.write(f'## Slide: {item["filename"]}\n')
        if item['has_images']:
            f.write(f'> *Contains {len(item["embedded_images"])} embedded raster image(s)*\n\n')
            for img in item['embedded_images']:
                f.write(f'- Saved Image: `{img["image_filename"]}` ({img["size_bytes"]:,} bytes)\n')
            f.write('\n')
        f.write(f'**Extracted Text Elements:**\n\n')
        for t in item['text_elements']:
            f.write(f'- {t}\n')
        f.write('\n---\n\n')

print(f"Extraction complete for {len(extracted_data)} SVG slides.")
print(f"Total embedded images extracted: {len(all_embedded_images)}")
