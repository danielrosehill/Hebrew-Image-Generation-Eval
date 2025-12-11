#!/usr/bin/env python3
"""Generate PDF report for Hebrew text rendering evaluation."""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from PIL import Image as PILImage
from io import BytesIO
import tempfile
import os

# Register Hebrew-compatible font
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

def reverse_hebrew(text):
    """Reverse Hebrew text for proper RTL display in PDF."""
    # Find Hebrew portions and reverse them
    result = []
    hebrew_buffer = []
    for char in text:
        if '\u0590' <= char <= '\u05FF':  # Hebrew Unicode range
            hebrew_buffer.append(char)
        else:
            if hebrew_buffer:
                result.extend(reversed(hebrew_buffer))
                hebrew_buffer = []
            result.append(char)
    if hebrew_buffer:
        result.extend(reversed(hebrew_buffer))
    return ''.join(result)

# Results data
SHALOM_RESULTS = [
    ("Gemini 3 Pro", 1, "Correct Hebrew"),
    ("Nano Banana Pro", 1, "Correct Hebrew"),
    ("Wan 2.5", 0, "Valid letters, wrong word"),
    ("Flux 2", 0, "Hebrew mixed with Latin"),
    ("Flux 2 Pro", 0, "Missing letters"),
    ("Flux Dev", 0, "Arabic script"),
    ("Imagen 4", 0, "Hebrew letters, nonsensical"),
    ("Ideogram V2", 0, "Russian-like text"),
    ("Qwen Image", 0, "Invalid characters"),
    ("SD 3.5 Large", 0, "Nonsensical"),
    ("Recraft V3", 0, "Invalid characters"),
    ("Aura Flow", 0, "English word"),
]

FIRGUN_RESULTS = [
    ("Gemini 3 Pro", 1, "Correct + contextual emojis"),
    ("Nano Banana Pro", 1, "Correct"),
    ("Wan 2.5", 1, "Correct"),
    ("Flux 2", 0, "Valid letters, nonsensical word"),
    ("Flux 2 Pro", 0, "Valid letters, nonsensical word"),
    ("Flux Dev", 0, "Random English words"),
    ("Imagen 4", 0, "Hebrew letters, nonsensical"),
    ("Ideogram V2", 0, "Russian-like text"),
    ("Qwen Image", 0, "Nonsensical"),
    ("SD 3.5 Large", 0, "Nonsensical"),
    ("Recraft V3", 0, "Random English word"),
    ("Aura Flow", 0, "Invalid Hebrew-like"),
]

OVERALL_SCORES = [
    ("Gemini 3 Pro", 1, 1, 2, "Best - contextual understanding"),
    ("Nano Banana Pro", 1, 1, 2, "Reliable Hebrew rendering"),
    ("Wan 2.5", 0, 1, 1, "Partial success"),
    ("Flux 2", 0, 0, 0, ""),
    ("Flux 2 Pro", 0, 0, 0, ""),
    ("Flux Dev", 0, 0, 0, ""),
    ("Imagen 4", 0, 0, 0, ""),
    ("Ideogram V2", 0, 0, 0, ""),
    ("Qwen Image", 0, 0, 0, ""),
    ("SD 3.5 Large", 0, 0, 0, ""),
    ("Recraft V3", 0, 0, 0, ""),
    ("Aura Flow", 0, 0, 0, ""),
]

def compress_image(img_path, max_width=1200, quality=60):
    """Compress image and return path to temp file and aspect ratio."""
    img = PILImage.open(img_path)
    aspect_ratio = img.width / img.height

    # Resize if too large
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, PILImage.LANCZOS)

    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Save to temp file as JPEG
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    img.save(temp_file.name, 'JPEG', quality=quality, optimize=True)
    return temp_file.name, aspect_ratio

def create_pdf():
    pdf_path = "hebrew-eval-report-compressed.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='DejaVuSans-Bold',
        fontSize=28,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName='DejaVuSans-Bold',
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontName='DejaVuSans-Bold',
        fontSize=14,
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=15
    )

    elements = []
    temp_files = []

    # === PAGE 1: Overall Results ===
    elements.append(Paragraph("Hebrew Text Rendering Evaluation", title_style))
    elements.append(Paragraph("Testing Image Generation Models on Hebrew Typography", subtitle_style))
    elements.append(Paragraph("Overall Results", section_style))

    table_data = [["Model", reverse_hebrew("שלום"), reverse_hebrew("פירגון"), "Score", "Notes"]]
    for model, shalom, firgun, total, notes in OVERALL_SCORES:
        table_data.append([
            model,
            "✓" if shalom else "✗",
            "✓" if firgun else "✗",
            f"{total}/2",
            notes
        ])

    table = Table(table_data, colWidths=[1.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgreen),
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgreen),
        ('BACKGROUND', (0, 3), (-1, 3), colors.lightyellow),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    # === PAGE 2: Test 1 Results ===
    elements.append(PageBreak())
    elements.append(Paragraph("Test 1: " + reverse_hebrew("שלום") + " (Shalom)", section_style))

    t1_data = [["Model", "Pass", "Notes"]]
    for model, passed, notes in SHALOM_RESULTS:
        t1_data.append([model, "✓" if passed else "✗", notes])

    t1_table = Table(t1_data, colWidths=[1.6*inch, 0.5*inch, 3*inch])
    t1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t1_table)

    # === PAGE 3: Test 2 Results ===
    elements.append(PageBreak())
    elements.append(Paragraph("Test 2: " + reverse_hebrew("פירגון") + " (Firgun)", section_style))

    t2_data = [["Model", "Pass", "Notes"]]
    for model, passed, notes in FIRGUN_RESULTS:
        t2_data.append([model, "✓" if passed else "✗", notes])

    t2_table = Table(t2_data, colWidths=[1.6*inch, 0.5*inch, 3*inch])
    t2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t2_table)

    # Footer style
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    footer_text = "Inference: Fal  |  Date: 11 Dec 2025  |  Daniel Rosehill (danielrosehill.com)"

    # Horizontal line for footer
    from reportlab.platypus import HRFlowable

    # === IMAGE PAGES (one per page) ===
    image_dirs = [
        ("outputs/shalom", "Target: " + reverse_hebrew("שלום")),
        ("outputs/firgun", "Target: " + reverse_hebrew("פירגון"))
    ]

    for img_dir, section_title in image_dirs:
        img_path = Path(img_dir)
        images = sorted(img_path.glob("*.png"))

        for img in images:
            elements.append(PageBreak())

            # Header with target word only
            elements.append(Paragraph(section_title, subtitle_style))

            # Compress and add image
            temp_path, aspect_ratio = compress_image(img)
            temp_files.append(temp_path)

            # Calculate dimensions preserving aspect ratio
            # Max available space: ~10.7 x 5.5 inches (landscape A4 minus margins, title, footer)
            max_width = 10*inch
            max_height = 5.5*inch

            if aspect_ratio > (max_width / max_height):
                # Image is wider - constrain by width
                img_width = max_width
                img_height = max_width / aspect_ratio
            else:
                # Image is taller - constrain by height
                img_height = max_height
                img_width = max_height * aspect_ratio

            img_obj = Image(temp_path, width=img_width, height=img_height)
            elements.append(img_obj)

            # Footer with horizontal line
            elements.append(Spacer(1, 0.2*inch))
            elements.append(HRFlowable(width="80%", thickness=1, color=colors.grey, spaceBefore=5, spaceAfter=5))
            elements.append(Paragraph(footer_text, footer_style))

    doc.build(elements)

    # Cleanup temp files
    for f in temp_files:
        try:
            os.unlink(f)
        except:
            pass

    print(f"PDF created: {pdf_path}")

if __name__ == "__main__":
    create_pdf()
