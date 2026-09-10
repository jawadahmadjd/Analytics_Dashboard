import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT

out_dir = os.path.dirname(os.path.abspath(__file__))
docx_path = os.path.join(out_dir, "Professional_Services_Quotation_Jawad_Ahmad.docx")
pdf_path = os.path.join(out_dir, "Professional_Services_Quotation_Jawad_Ahmad.pdf")

# ==============================================================================
# 1. DOCX GENERATION
# ==============================================================================
doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.55)
section.bottom_margin = Inches(0.55)
section.left_margin = Inches(0.7)
section.right_margin = Inches(0.7)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(10)
styles["Normal"].font.color.rgb = RGBColor(55, 65, 81)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run("QUOTATION")
r.bold = True
r.font.size = Pt(25)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
r = p.add_run("AI Infrastructure and Business Intelligence")
r.bold = True
r.font.size = Pt(11)
r.font.color.rgb = RGBColor(107, 114, 128)

meta = doc.add_table(rows=2, cols=2)
meta.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Prepared For", "National Bonds (UAE)", "Date", "07 September 2026"),
    ("Payment Frequency", "Weekly", "Currency", "AED"),
]
for i, row in enumerate(meta.rows):
    vals = meta_data[i]
    for j in range(2):
        cell = row.cells[j]
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.text = f"{vals[j*2]}\n{vals[j*2+1]}"
        for k, para in enumerate(cell.paragraphs):
            para.paragraph_format.space_after = Pt(0)
            if k == 0:
                para.runs[0].bold = True
                para.runs[0].font.size = Pt(8)
                para.runs[0].font.color.rgb = RGBColor(107, 114, 128)
            else:
                para.runs[0].font.size = Pt(10)
                para.runs[0].font.color.rgb = RGBColor(31, 41, 55)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), 'F3F6F9')
        cell._tc.get_or_add_tcPr().append(shd)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.space_after = Pt(6)
r = p.add_run("FEE SUMMARY")
r.bold = True
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(31, 78, 121)

table = doc.add_table(rows=1, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = "Table Grid"
headers = ["SERVICE / COST CATEGORY", "BILLING BASIS", "WEEKLY FEE"]
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if i < 2 else WD_ALIGN_PARAGRAPH.RIGHT
    for run in cell.paragraphs[0].runs:
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), '1F4E79')
    cell._tc.get_or_add_tcPr().append(shd)

rows = [
    ("AI Automated Analysis Dashboard", "Weekly", "AED 3,000"),
    ("AI Tokens & API Usage", "One-time payment", "AED 4,000"),
]
for item, basis, fee in rows:
    cells = table.add_row().cells
    for idx, text in enumerate([item, basis, fee]):
        cells[idx].text = text
        cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cells[idx].paragraphs[0].paragraph_format.space_after = Pt(0)
        cells[idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT if idx == 2 else WD_ALIGN_PARAGRAPH.LEFT
        if idx == 2:
            cells[idx].paragraphs[0].runs[0].bold = True
        cells[idx].paragraphs[0].runs[0].font.size = Pt(9.5)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after = Pt(3)
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("WEEKLY AI AUTOMATED ANALYSIS DASHBOARD  ")
r.bold = True
r.font.size = Pt(10)
r.font.color.rgb = RGBColor(55, 65, 81)
r = p.add_run("AED 3,000")
r.bold = True
r.font.size = Pt(17)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(3)
p.paragraph_format.space_after = Pt(2)
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("ONE-TIME AI / API COST  ")
r.bold = True
r.font.size = Pt(10)
r.font.color.rgb = RGBColor(55, 65, 81)
r = p.add_run("AED 4,000")
r.bold = True
r.font.size = Pt(17)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("Payment Summary")
r.bold = True
r.font.size = Pt(10)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(8)
p.add_run(
    "The AI Automated Analysis Dashboard fee is AED 3,000 per week. A one-time payment of AED 4,000 "
    "covers the initial AI token and API usage costs required for the agreed scope of work."
)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("Prepared by")
r.bold = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(107, 114, 128)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(1)
r = p.add_run("Jawad Ahmad")
r.bold = True
r.font.size = Pt(11)
r.font.color.rgb = RGBColor(31, 41, 55)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
r = p.add_run("Lead AI & Business Solutions Architect")
r.font.size = Pt(9.5)
r.font.color.rgb = RGBColor(107, 114, 128)

doc.save(docx_path)

# ==============================================================================
# 2. PDF GENERATION
# ==============================================================================
pdf = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=38, bottomMargin=38)
styles = getSampleStyleSheet()
blue = colors.HexColor("#1F4E79")
dark = colors.HexColor("#273444")
muted = colors.HexColor("#6B7280")
light = colors.HexColor("#F3F6F9")

title = ParagraphStyle("DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=28, textColor=blue, spaceAfter=3)
subtitle = ParagraphStyle("DocSubtitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=muted, spaceAfter=14)
body = ParagraphStyle("DocBody", parent=styles["BodyText"], fontSize=9.2, leading=14, textColor=dark)
small = ParagraphStyle("DocSmall", parent=styles["Normal"], fontSize=8.5, leading=12, textColor=muted)
total = ParagraphStyle("DocTotal", parent=styles["Normal"], alignment=TA_RIGHT, fontName="Helvetica-Bold", fontSize=10, leading=18, textColor=dark)

story = [
    Paragraph("QUOTATION", title),
    Paragraph("AI Infrastructure and Business Intelligence", subtitle)
]

meta_tbl = Table([
    [Paragraph("<b>PREPARED FOR</b><br/>National Bonds (UAE)", body),
     Paragraph("<b>DATE</b><br/>07 September 2026", body)],
    [Paragraph("<b>PAYMENT FREQUENCY</b><br/>Weekly", body),
     Paragraph("<b>CURRENCY</b><br/>AED", body)]
], colWidths=[255, 255], rowHeights=[42, 42])
meta_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), light),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
]))
story += [
    meta_tbl,
    Paragraph("FEE SUMMARY", ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, textColor=blue, spaceBefore=12, spaceAfter=7))
]

header_style = ParagraphStyle("Header", parent=small, fontName="Helvetica-Bold", textColor=colors.white, fontSize=8.5)
fee_tbl = Table([
    [Paragraph("SERVICE / COST CATEGORY", header_style), Paragraph("BILLING BASIS", header_style), Paragraph("WEEKLY FEE", header_style)],
    ["AI Automated Analysis Dashboard", "Weekly", "AED 3,000"],
    ["AI Tokens & API Usage", "One-time payment", "AED 4,000"],
], colWidths=[260, 150, 100], rowHeights=[31, 34, 40])
fee_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), blue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E1E8")),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 1), (-1, -1), 9),
    ("TEXTCOLOR", (0, 1), (-1, -1), dark),
    ("ALIGN", (2, 1), (2, -1), "RIGHT"),
    ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
]))
story += [fee_tbl, Spacer(1, 10)]

summary_tbl = Table([
    [Paragraph("WEEKLY AI AUTOMATED ANALYSIS DASHBOARD&nbsp;&nbsp; <font size='16' color='#1F4E79'>AED 3,000</font>", total)],
    [Paragraph("ONE-TIME AI / API COST&nbsp;&nbsp; <font size='16' color='#1F4E79'>AED 4,000</font>", total)]
], colWidths=[510], rowHeights=[35, 35])
summary_tbl.setStyle(TableStyle([
    ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#D9E1E8")),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E5E7EB")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
]))
story += [
    summary_tbl,
    Paragraph("Payment Summary", ParagraphStyle("Section2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, textColor=blue, spaceBefore=12, spaceAfter=7)),
    Paragraph("The AI Automated Analysis Dashboard fee is <b>AED 3,000 per week</b>. A <b>one-time payment of AED 4,000</b> covers the initial AI token and API usage costs required for the agreed scope of work.", body),
    Spacer(1, 14),
    Paragraph("<b>Prepared by</b>", small),
    Paragraph("Jawad Ahmad", ParagraphStyle("Name", parent=body, fontName="Helvetica-Bold", fontSize=10.5, spaceAfter=2)),
    Paragraph("Lead AI &amp; Business Solutions Architect", ParagraphStyle("Role", parent=small, fontName="Helvetica", fontSize=8.8, textColor=muted)),
]

pdf.build(story)
print(f"Updated files successfully created:\n- {pdf_path}\n- {docx_path}")
