#!/usr/bin/env python3
"""
Convert PIPELINE_GUIDE.md to PDF
Requires: pip install reportlab markdown2
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

def create_pdf():
    """Generate PDF from PIPELINE_GUIDE.md"""

    # Read markdown file
    with open('PIPELINE_GUIDE.md', 'r') as f:
        content = f.read()

    # Create PDF
    pdf_filename = 'PIPELINE_GUIDE.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#d62728'),
        spaceAfter=10,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Courier',
        leftIndent=20,
        textColor=colors.HexColor('#333333'),
        backColor=colors.HexColor('#f5f5f5'),
        borderColor=colors.HexColor('#cccccc'),
        borderWidth=1,
        borderPadding=5
    )

    # Build document
    elements = []

    # Title
    elements.append(Paragraph("MLOps Pipeline Guide", title_style))
    elements.append(Paragraph("Deine aktuelle vs. echte Production Pipelines", styles['Italic']))
    elements.append(Spacer(1, 0.3*inch))

    # Parse markdown content
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue

        # Headings
        if line.startswith('# '):
            elements.append(Paragraph(line.replace('# ', ''), h1_style))
            i += 1

        elif line.startswith('## '):
            elements.append(Paragraph(line.replace('## ', ''), h2_style))
            i += 1

        elif line.startswith('### '):
            elements.append(Paragraph(line.replace('### ', ''), h2_style))
            i += 1

        # Code blocks
        elif line.strip().startswith('```'):
            # Collect code block
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```

            code_text = '\n'.join(code_lines).strip()
            elements.append(Preformatted(code_text, code_style))
            elements.append(Spacer(1, 0.1*inch))

        # Bold/Italic text
        elif line.strip().startswith('**') or line.strip().startswith('✅') or line.strip().startswith('❌'):
            # Clean up markdown formatting
            text = line.replace('**', '').replace('```', '')
            elements.append(Paragraph(text, body_style))
            i += 1

        # Tables (simplified - just convert to text for PDF)
        elif '|' in line:
            # Skip tables for simplicity in PDF
            while i < len(lines) and '|' in lines[i]:
                i += 1

        # Regular paragraphs
        else:
            # Clean up markdown
            text = line.replace('**', '<b>').replace('**', '</b>')
            text = text.replace('`', '<font face="Courier">')

            if text.strip():
                elements.append(Paragraph(text, body_style))
            i += 1

        # Add page break if needed (every ~30 elements)
        if len(elements) % 30 == 0 and len(elements) > 0:
            elements.append(PageBreak())

    # Build PDF
    try:
        doc.build(elements)
        print(f"✓ PDF created: {pdf_filename}")
        print(f"  Size: {os.path.getsize(pdf_filename) / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False

if __name__ == '__main__':
    create_pdf()
