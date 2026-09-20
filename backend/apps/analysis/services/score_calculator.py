"""
Score Calculator — Transparent weighted ATS compatibility score calculation.
Weights are loaded from Django settings.
"""
from django.conf import settings


def calculate_ats_score(
    text_score: float,
    structure_score: float,
    formatting_score: float,
    keyword_score: float,
    contact_score: float,
) -> dict:
    """
    Calculate weighted ATS compatibility score and category label.
    Formula:
      Text Extraction       25%
      Section Structure     20%
      Formatting            20%
      Keyword Coverage      20%
      Contact Information   15%
    """
    weights = getattr(settings, 'ATS_SCORE_WEIGHTS', {
        'text_extraction': 0.25,
        'section_structure': 0.20,
        'formatting': 0.20,
        'keyword_coverage': 0.20,
        'contact_information': 0.15,
    })

    # Clamp scores to [0, 100]
    t = max(0.0, min(100.0, float(text_score)))
    s = max(0.0, min(100.0, float(structure_score)))
    f = max(0.0, min(100.0, float(formatting_score)))
    k = max(0.0, min(100.0, float(keyword_score)))
    c = max(0.0, min(100.0, float(contact_score)))

    weighted_score = (
        (t * weights.get('text_extraction', 0.25)) +
        (s * weights.get('section_structure', 0.20)) +
        (f * weights.get('formatting', 0.20)) +
        (k * weights.get('keyword_coverage', 0.20)) +
        (c * weights.get('contact_information', 0.15))
    )

    final_score = round(weighted_score, 1)

    # Category determination
    if final_score >= 90:
        category_label = "Excellent compatibility"
        level = "excellent"
        summary_hint = "Great! Your document is highly ATS-compatible based on ResumeSense's analysis."
    elif final_score >= 75:
        category_label = "Good compatibility"
        level = "good"
        summary_hint = "Great! Your resume is mostly ATS-friendly based on ResumeSense's analysis."
    elif final_score >= 60:
        category_label = "Needs improvement"
        level = "moderate"
        summary_hint = "Your document has fair compatibility, but several formatting and structural elements need attention."
    else:
        category_label = "Major improvements recommended"
        level = "poor"
        summary_hint = "Your document has significant compatibility blockers for automated parsing systems."

    return {
        'score': final_score,
        'category_label': category_label,
        'level': level,
        'summary_hint': summary_hint,
        'breakdown': {
            'text_score': round(t, 1),
            'structure_score': round(s, 1),
            'formatting_score': round(f, 1),
            'keyword_score': round(k, 1),
            'contact_score': round(c, 1),
        },
        'weights': weights,
    }
