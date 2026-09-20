"""
Job Matcher Service — Compares resume content against job descriptions using
keyword extraction, taxonomy matching, and TF-IDF/embeddings semantic similarity.
"""
import logging
from dataclasses import dataclass, field
from apps.analysis.services.keyword_analyzer import (
    analyze_keywords, TECHNICAL_SKILLS, SOFT_SKILLS, TOOLS_AND_PLATFORMS
)

logger = logging.getLogger(__name__)

# Global model cache for sentence-transformers
_EMBEDDING_MODEL = None


def get_embedding_model():
    """Lazily load sentence-transformers model if installed, else fallback."""
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded sentence-transformers model: all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Could not load sentence-transformers: {e}. Falling back to TF-IDF.")
            _EMBEDDING_MODEL = False
    return _EMBEDDING_MODEL if _EMBEDDING_MODEL is not False else None


@dataclass
class JobMatchResult:
    match_score: float = 0.0
    matched_skills: list = field(default_factory=list)
    missing_skills: list = field(default_factory=list)
    jd_skills: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """Compute semantic similarity using sentence-transformers or TF-IDF cosine similarity."""
    if not text1.strip() or not text2.strip():
        return 0.0

    model = get_embedding_model()
    if model:
        try:
            from sentence_transformers import util
            emb1 = model.encode(text1, convert_to_tensor=True)
            emb2 = model.encode(text2, convert_to_tensor=True)
            cosine_score = util.cos_sim(emb1, emb2).item()
            return max(0.0, min(1.0, float(cosine_score)))
        except Exception as e:
            logger.warning(f"Embedding comparison error: {e}")

    # Fallback to TF-IDF cosine similarity via scikit-learn
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return max(0.0, min(1.0, float(score)))
    except Exception as e:
        logger.warning(f"TF-IDF comparison error: {e}")
        return 0.5


def match_resume_to_job(resume_text: str, job_description: str) -> JobMatchResult:
    """Analyze alignment between resume and job description."""
    result = JobMatchResult()

    if not resume_text or not job_description:
        return result

    # Extract keywords from JD and Resume
    jd_analysis = analyze_keywords(job_description)
    resume_analysis = analyze_keywords(resume_text)

    jd_keywords = set(k.lower() for k in jd_analysis.all_keywords)
    resume_keywords = set(k.lower() for k in resume_analysis.all_keywords)

    result.jd_skills = jd_analysis.all_keywords

    # Find matched and missing skills
    matched_lower = jd_keywords.intersection(resume_keywords)
    missing_lower = jd_keywords.difference(resume_keywords)

    # Format properly with original capitalization
    skill_title_map = {k.lower(): k for k in jd_analysis.all_keywords + resume_analysis.all_keywords}

    result.matched_skills = sorted([skill_title_map.get(k, k.title()) for k in matched_lower])
    result.missing_skills = sorted([skill_title_map.get(k, k.title()) for k in missing_lower])

    # Compute keyword coverage ratio
    if jd_keywords:
        keyword_overlap_ratio = len(matched_lower) / len(jd_keywords)
    else:
        keyword_overlap_ratio = 0.5

    # Compute semantic text similarity
    semantic_sim = calculate_semantic_similarity(resume_text, job_description)

    # Combined weighted score (60% keyword coverage, 40% semantic similarity)
    combined = (keyword_overlap_ratio * 0.60) + (semantic_sim * 0.40)
    result.match_score = round(min(100.0, max(0.0, combined * 100)), 1)

    # Generate factual and honest recommendations
    if result.missing_skills:
        top_missing = result.missing_skills[:3]
        result.suggestions.append(
            f"Key technical requirements such as {', '.join(top_missing)} appear in the job description but were not detected in your resume."
        )
        result.suggestions.append(
            f"If you genuinely have experience with any of these competencies ({', '.join(top_missing)}), consider highlighting them prominently in your Skills or Project sections."
        )

    if len(result.matched_skills) >= 4:
        result.suggestions.append(
            f"Strong alignment detected on core competencies: {', '.join(result.matched_skills[:4])}."
        )

    if result.match_score < 60:
        result.suggestions.append(
            "The resume vocabulary differs significantly from the job posting. Review the role requirements to ensure industry-standard terminology is used."
        )

    return result
