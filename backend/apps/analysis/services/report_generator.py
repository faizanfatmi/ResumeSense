"""
Report Generator — Generates downloadable PDF reports of analysis results using ReportLab.
"""
import io
import logging
from apps.analysis.models import Analysis

logger = logging.getLogger(__name__)


def generate_pdf_report(analysis: Analysis) -> io.BytesIO:
    """Generate a clean, professional ATS Analysis Report as a PDF buffer."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        'DocHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4,
    )
    subhead_style = ParagraphStyle(
        'DocSubhead',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15,
    )
    section_heading = ParagraphStyle(
        'SecHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=14,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        leading=14,
    )
    score_big = ParagraphStyle(
        'ScoreBig',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        textColor=colors.HexColor('#16A34A') if analysis.score >= 80 else colors.HexColor('#2563EB'),
        alignment=1,
    )

    elements = []

    # Title & Brand
    elements.append(Paragraph("ResumeSense™ Analysis Report", header_style))
    file_name = analysis.uploaded_file.original_name if analysis.uploaded_file else "Document"
    date_str = analysis.created_at.strftime("%B %d, %Y, %I:%M %p")
    elements.append(Paragraph(f"File: <b>{file_name}</b> | Analyzed on: {date_str}", subhead_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#E2E8F0'), spaceAfter=15))

    # Executive Score Table
    score_data = [
        [
            Paragraph(f"<b>Overall ATS Compatibility</b><br/>{analysis.score} / 100", score_big),
            Paragraph(
                f"<b>Score Breakdown:</b><br/>"
                f"• Text Readability: {analysis.text_score}%<br/>"
                f"• Section Structure: {analysis.structure_score}%<br/>"
                f"• Keyword Match: {analysis.keyword_score}%<br/>"
                f"• Formatting: {analysis.formatting_score}%<br/>"
                f"• Contact Info: {analysis.contact_score}%",
                body_style,
            )
        ]
    ]
    t = Table(score_data, colWidths=[200, 320])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    # Summary
    if analysis.summary:
        elements.append(Paragraph("Summary", section_heading))
        elements.append(Paragraph(analysis.summary, body_style))
        elements.append(Spacer(1, 10))

    # Detected Sections
    sections = analysis.sections.all()
    if sections.exists():
        elements.append(Paragraph("Detected Document Sections", section_heading))
        sec_rows = [["Section Name", "Status", "Detection Confidence"]]
        for s in sections:
            status = "✓ Detected" if s.detected else "✗ Missing / Weak"
            conf = f"{int(s.confidence * 100)}%"
            sec_rows.append([s.section_name, status, conf])

        sec_table = Table(sec_rows, colWidths=[220, 160, 140])
        sec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(sec_table)
        elements.append(Spacer(1, 15))

    # Findings & Recommendations
    findings = analysis.findings.all()
    if findings.exists():
        elements.append(Paragraph("Detailed Findings & Actionable Recommendations", section_heading))
        for f in findings:
            sev_color = {
                'critical': '#DC2626',
                'important': '#EA580C',
                'suggestion': '#2563EB',
                'good': '#16A34A',
            }.get(f.severity, '#64748B')

            f_header = f"<font color='{sev_color}'><b>[{f.severity.upper()}] {f.title}</b></font>"
            elements.append(Paragraph(f_header, body_style))
            elements.append(Paragraph(f"{f.description}", body_style))
            if f.recommendation:
                elements.append(Paragraph(f"<i>Recommendation:</i> {f.recommendation}", body_style))
            elements.append(Spacer(1, 6))

    # Keyword Groups
    kw_groups = analysis.keyword_groups.all()
    if kw_groups.exists():
        elements.append(Paragraph("Extracted Keyword Groups", section_heading))
        for g in kw_groups:
            kw_list = ", ".join(g.keywords) if g.keywords else "None detected"
            elements.append(Paragraph(f"<b>{g.group_name}:</b> {kw_list}", body_style))
            elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceAfter=8))
    elements.append(Paragraph(
        "Generated by ResumeSense — Professional ATS Resume & PPT Compatibility Platform. "
        "Scores represent simulated parser compatibility metrics.",
        ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#94A3B8'))
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
