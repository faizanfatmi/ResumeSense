"""
PPT Analyzer — Slide-by-slide analysis for PowerPoint presentations (PPTX).
Checks text extraction, image content, font sizes, complex shapes, and readability.
"""
import logging
from dataclasses import dataclass, field
from .document_parser import DocumentData, PageInfo

logger = logging.getLogger(__name__)


@dataclass
class SlideFeedback:
    slide_number: int
    text_quality: str  # 'good', 'warning', 'poor'
    text: str = ''
    has_images: bool = False
    has_tables: bool = False
    font_issues: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    positives: list = field(default_factory=list)


@dataclass
class PPTAnalysisResult:
    total_slides: int = 0
    slides_analyzed: int = 0
    slides: list = field(default_factory=list)  # List[SlideFeedback]
    overall_quality_score: float = 100.0
    text_extraction_score: float = 100.0
    formatting_score: float = 100.0
    findings: list = field(default_factory=list)
    summary: str = ''


def analyze_ppt(doc_data: DocumentData) -> PPTAnalysisResult:
    """Analyze a presentation document slide-by-slide."""
    result = PPTAnalysisResult()
    result.total_slides = doc_data.page_count
    result.slides_analyzed = len(doc_data.pages)

    if not doc_data.pages:
        result.overall_quality_score = 0
        result.text_extraction_score = 0
        result.formatting_score = 0
        result.findings.append({
            'severity': 'critical',
            'category': 'slide_analysis',
            'title': 'No slides found',
            'description': 'The presentation does not contain any readable slides or failed to parse.',
            'recommendation': 'Verify that the presentation file is valid and not corrupted.',
        })
        return result

    slides_with_warnings = 0
    image_only_count = 0
    small_text_count = 0
    total_words = doc_data.word_count

    for page in doc_data.pages:
        feedback = SlideFeedback(
            slide_number=page.page_number,
            text=page.text,
            has_images=page.has_images,
            has_tables=page.has_tables,
        )

        # Evaluate text length
        word_count = len(page.text.split())
        if page.is_image_only or (page.has_images and word_count < 5):
            feedback.text_quality = 'poor'
            feedback.warnings.append('Important content or skills may be trapped inside images.')
            image_only_count += 1
            slides_with_warnings += 1
        elif word_count < 10:
            feedback.text_quality = 'warning'
            feedback.warnings.append('Very little extractable text found on this slide.')
            slides_with_warnings += 1
        elif word_count > 150:
            feedback.text_quality = 'warning'
            feedback.warnings.append('High text density — may reduce visual readability.')
            slides_with_warnings += 1
        else:
            feedback.text_quality = 'good'
            feedback.positives.append('Good text readability and length.')

        # Transfer page warnings
        for w in page.warnings:
            if 'small text' in w.lower():
                small_text_count += 1
                feedback.font_issues.append(w)
                if feedback.text_quality == 'good':
                    feedback.text_quality = 'warning'
            elif w not in feedback.warnings:
                feedback.warnings.append(w)

        if not feedback.warnings:
            feedback.positives.append('Standard formatting and clean object structure.')

        result.slides.append(feedback)

    # Calculate subscores
    # Text extraction score
    poor_ratio = image_only_count / max(1, result.total_slides)
    text_score = max(20.0, 100.0 - (poor_ratio * 70.0))
    result.text_extraction_score = round(text_score, 1)

    # Formatting score
    warning_ratio = slides_with_warnings / max(1, result.total_slides)
    format_score = max(30.0, 100.0 - (warning_ratio * 40.0) - (min(small_text_count, 5) * 5.0))
    result.formatting_score = round(format_score, 1)

    result.overall_quality_score = round((result.text_extraction_score * 0.6) + (result.formatting_score * 0.4), 1)

    # Generate overarching findings
    if image_only_count > 0:
        result.findings.append({
            'severity': 'critical' if image_only_count > 2 else 'important',
            'category': 'images',
            'title': f'Image-heavy slides detected ({image_only_count} slide{"s" if image_only_count > 1 else ""})',
            'description': f'{image_only_count} slide(s) appear to rely primarily on images or screenshots rather than native text.',
            'recommendation': 'Ensure key qualifications, project outcomes, and takeaways are written as editable text boxes rather than embedded images.',
        })

    if small_text_count > 0:
        result.findings.append({
            'severity': 'important',
            'category': 'formatting',
            'title': 'Very small font sizes detected',
            'description': f'Found {small_text_count} instances of font size below 10pt across slides.',
            'recommendation': 'Use font sizes of at least 14pt–18pt for slide content to ensure accessibility and clear parsing.',
        })

    if result.total_slides > 30:
        result.findings.append({
            'severity': 'suggestion',
            'category': 'layout',
            'title': 'High slide count',
            'description': f'Presentation has {result.total_slides} slides.',
            'recommendation': 'Consider creating an executive summary deck with fewer than 15-20 slides for hiring or technical reviews.',
        })

    if slides_with_warnings == 0:
        result.findings.append({
            'severity': 'good',
            'category': 'layout',
            'title': 'Clean slide structure',
            'description': 'All slides contain clearly structured, native text objects with readable font sizes.',
            'recommendation': '',
        })

    result.summary = (
        f"Analyzed {result.total_slides} slides. Overall presentation readiness score: "
        f"{result.overall_quality_score}/100. {image_only_count} image-heavy slide(s) identified."
    )

    return result
