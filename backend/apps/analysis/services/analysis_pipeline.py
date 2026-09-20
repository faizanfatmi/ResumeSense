"""
Analysis Pipeline — Orchestrates parsing, rule-based extraction, scoring,
finding generation, and database persistence.
"""
import time
import logging
from django.db import transaction
from apps.documents.models import UploadedFile
from apps.analysis.models import (
    Analysis, Finding, ExtractedSection, KeywordGroup, SlideAnalysis
)
from .document_parser import parse_document
from .resume_analyzer import analyze_resume
from .keyword_analyzer import analyze_keywords
from .ppt_analyzer import analyze_ppt
from .score_calculator import calculate_ats_score

logger = logging.getLogger(__name__)


def run_analysis_pipeline(uploaded_file: UploadedFile, analysis_type: str = 'resume') -> Analysis:
    """Run full deterministic analysis pipeline on an uploaded file."""
    start_time = time.time()
    file_path = uploaded_file.file.path
    file_type = uploaded_file.file_type

    logger.info(f"Starting analysis for file: {uploaded_file.original_name} ({file_type})")

    # 1. Parse document text and layout
    doc_data = parse_document(file_path, file_type)

    with transaction.atomic():
        # Clean up any prior analyses on this specific file record
        uploaded_file.analyses.all().delete()

        # Create base Analysis instance
        analysis = Analysis(
            uploaded_file=uploaded_file,
            analysis_type=analysis_type,
            page_count=doc_data.page_count,
            word_count=doc_data.word_count,
            extracted_text=doc_data.text,
        )

        findings_to_create = []

        if file_type in ('PPT', 'PPTX') or analysis_type == 'ppt':
            analysis.analysis_type = 'ppt'
            ppt_result = analyze_ppt(doc_data)
            kw_result = analyze_keywords(doc_data.text)

            score_res = calculate_ats_score(
                text_score=ppt_result.text_extraction_score,
                structure_score=ppt_result.overall_quality_score,
                formatting_score=ppt_result.formatting_score,
                keyword_score=kw_result.keyword_score,
                contact_score=70.0,  # presentations typically don't have standard resume contact headers
            )

            analysis.score = score_res['score']
            analysis.text_score = score_res['breakdown']['text_score']
            analysis.structure_score = score_res['breakdown']['structure_score']
            analysis.formatting_score = score_res['breakdown']['formatting_score']
            analysis.keyword_score = score_res['breakdown']['keyword_score']
            analysis.contact_score = score_res['breakdown']['contact_score']

            analysis.summary = (
                f"Presentation Analysis: {ppt_result.summary} "
                f"Detected {len(kw_result.technical_skills)} technical keywords and {doc_data.page_count} slides."
            )
            analysis.save()

            # Save slide analyses
            for slide in ppt_result.slides:
                SlideAnalysis.objects.create(
                    analysis=analysis,
                    slide_number=slide.slide_number,
                    extracted_text=slide.text,
                    text_quality=slide.text_quality,
                    has_images=slide.has_images,
                    has_tables=slide.has_tables,
                    font_issues=slide.font_issues,
                    warnings=slide.warnings,
                )

            # Collect findings
            for f in ppt_result.findings:
                findings_to_create.append(
                    Finding(
                        analysis=analysis,
                        severity=f.get('severity', 'suggestion'),
                        category=f.get('category', 'slide_analysis'),
                        title=f.get('title', ''),
                        description=f.get('description', ''),
                        recommendation=f.get('recommendation', ''),
                    )
                )

        else:
            # Resume Analysis
            resume_result = analyze_resume(doc_data)
            kw_result = analyze_keywords(doc_data.text)

            score_res = calculate_ats_score(
                text_score=resume_result.text_quality_score,
                structure_score=resume_result.structure_score,
                formatting_score=resume_result.formatting_score,
                keyword_score=kw_result.keyword_score,
                contact_score=resume_result.contact_score,
            )

            analysis.score = score_res['score']
            analysis.text_score = score_res['breakdown']['text_score']
            analysis.structure_score = score_res['breakdown']['structure_score']
            analysis.formatting_score = score_res['breakdown']['formatting_score']
            analysis.keyword_score = score_res['breakdown']['keyword_score']
            analysis.contact_score = score_res['breakdown']['contact_score']

            # Dynamic summary
            if analysis.score >= 85:
                analysis.summary = (
                    "Your resume is well-structured and mostly ATS-friendly. A few improvements "
                    "can make it even stronger. Check the detailed feedback for suggestions."
                )
            elif analysis.score >= 70:
                analysis.summary = (
                    "Your document demonstrates good baseline readability, but several section structures "
                    "or keyword alignments need attention to maximize ATS parser compatibility."
                )
            else:
                analysis.summary = (
                    "Automated document parsers may encounter significant difficulty extracting sections "
                    "or keywords from this resume. Review the critical issues below."
                )

            analysis.save()

            # Save detected sections
            for idx, sec in enumerate(resume_result.sections):
                ExtractedSection.objects.create(
                    analysis=analysis,
                    section_name=sec.name.title(),
                    content=sec.content,
                    detected=sec.detected,
                    confidence=sec.confidence,
                    order=idx,
                )

            # Collect resume findings
            for item in resume_result.structure_issues:
                findings_to_create.append(
                    Finding(
                        analysis=analysis,
                        severity=item.get('severity', 'suggestion'),
                        category='section_structure',
                        title=item.get('title', ''),
                        description=item.get('description', ''),
                        recommendation=item.get('recommendation', ''),
                    )
                )

            for item in resume_result.formatting_issues:
                findings_to_create.append(
                    Finding(
                        analysis=analysis,
                        severity=item.get('severity', 'suggestion'),
                        category='formatting',
                        title=item.get('title', ''),
                        description=item.get('description', ''),
                        recommendation=item.get('recommendation', ''),
                    )
                )

            # Contact findings
            contact = resume_result.contact_info
            if contact.email and contact.phone:
                findings_to_create.append(
                    Finding(
                        analysis=analysis,
                        severity='good',
                        category='contact_info',
                        title='Contact Information Detected',
                        description=f'Contact email ({contact.email}) and telephone were successfully detected.',
                        recommendation='',
                    )
                )
            else:
                missing = []
                if not contact.email: missing.append('email')
                if not contact.phone: missing.append('phone number')
                findings_to_create.append(
                    Finding(
                        analysis=analysis,
                        severity='critical',
                        category='contact_info',
                        title='Incomplete Contact Information',
                        description=f"Missing standard contact fields: {', '.join(missing)}.",
                        recommendation='Place clear email and phone number at the top of your resume.',
                    )
                )

        # Keyword groups and findings (common to both)
        if kw_result.technical_skills:
            KeywordGroup.objects.create(
                analysis=analysis,
                group_name='Technical Skills',
                keywords=kw_result.technical_skills,
            )
        if kw_result.soft_skills:
            KeywordGroup.objects.create(
                analysis=analysis,
                group_name='Soft Skills',
                keywords=kw_result.soft_skills,
            )
        if kw_result.tools:
            KeywordGroup.objects.create(
                analysis=analysis,
                group_name='Tools & Platforms',
                keywords=kw_result.tools,
            )

        for item in kw_result.issues:
            findings_to_create.append(
                Finding(
                    analysis=analysis,
                    severity=item.get('severity', 'suggestion'),
                    category='keywords',
                    title=item.get('title', ''),
                    description=item.get('description', ''),
                    recommendation=item.get('recommendation', ''),
                )
            )

        # Bulk create findings
        if findings_to_create:
            Finding.objects.bulk_create(findings_to_create)

        elapsed = round(time.time() - start_time, 2)
        analysis.processing_time = elapsed
        analysis.save(update_fields=['processing_time'])

        logger.info(f"Analysis completed in {elapsed}s with score {analysis.score}")
        return analysis
