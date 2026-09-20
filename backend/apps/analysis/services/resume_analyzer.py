"""
Resume Analyzer — Detects resume sections, contact info, and structure quality.
"""
import re
import logging
from dataclasses import dataclass, field
from typing import Optional
from .document_parser import DocumentData

logger = logging.getLogger(__name__)


# Standard resume section patterns
SECTION_PATTERNS = {
    'contact': r'(?i)^(contact\s*(info|information|details)?|personal\s*(info|information|details)?)$',
    'summary': r'(?i)^(summary|professional\s*summary|profile|about\s*me|objective|career\s*objective)$',
    'experience': r'(?i)^(experience|work\s*experience|professional\s*experience|employment|work\s*history|career\s*history)$',
    'education': r'(?i)^(education|academic|academics|qualifications|educational\s*background)$',
    'skills': r'(?i)^(skills|technical\s*skills|core\s*skills|competencies|technologies|tech\s*stack|expertise)$',
    'projects': r'(?i)^(projects|personal\s*projects|academic\s*projects|key\s*projects|portfolio)$',
    'certifications': r'(?i)^(certifications?|certificates?|licenses?|credentials?)$',
    'achievements': r'(?i)^(achievements?|awards?|honors?|accomplishments?|recognition)$',
    'languages': r'(?i)^(languages?|language\s*skills)$',
    'publications': r'(?i)^(publications?|research|papers?)$',
    'volunteer': r'(?i)^(volunteer|volunteering|community\s*service|extracurricular)$',
    'interests': r'(?i)^(interests?|hobbies?|activities)$',
    'references': r'(?i)^(references?)$',
}

# Contact information patterns
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_PATTERN = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
LINKEDIN_PATTERN = re.compile(r'(?:linkedin\.com/in/|linkedin:?\s*)[a-zA-Z0-9_-]+', re.IGNORECASE)
GITHUB_PATTERN = re.compile(r'(?:github\.com/|github:?\s*)[a-zA-Z0-9_-]+', re.IGNORECASE)
URL_PATTERN = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')

# Standard fonts that ATS systems handle well
ATS_FRIENDLY_FONTS = {
    'arial', 'calibri', 'cambria', 'garamond', 'georgia', 'helvetica',
    'times new roman', 'times', 'trebuchet ms', 'verdana', 'tahoma',
    'palatino', 'book antiqua', 'century gothic', 'lucida sans',
    'segoe ui', 'roboto', 'open sans', 'lato', 'montserrat',
}


@dataclass
class ContactInfo:
    name: str = ''
    email: str = ''
    phone: str = ''
    linkedin: str = ''
    github: str = ''
    website: str = ''
    location: str = ''


@dataclass
class SectionDetection:
    name: str
    detected: bool
    content: str = ''
    confidence: float = 1.0


@dataclass
class ResumeAnalysisResult:
    contact_info: ContactInfo = field(default_factory=ContactInfo)
    sections: list = field(default_factory=list)  # List[SectionDetection]
    structure_issues: list = field(default_factory=list)
    formatting_issues: list = field(default_factory=list)
    text_quality_score: float = 100.0
    structure_score: float = 100.0
    formatting_score: float = 100.0
    contact_score: float = 0.0


def analyze_resume(doc_data: DocumentData) -> ResumeAnalysisResult:
    """Analyze a resume document for structure, contact info, and formatting."""
    result = ResumeAnalysisResult()

    text = doc_data.text
    if not text or len(text.strip()) < 10:
        result.text_quality_score = 0
        result.structure_score = 0
        result.formatting_score = 0
        result.contact_score = 0
        result.structure_issues.append({
            'severity': 'critical',
            'title': 'No text extracted',
            'description': 'No readable text could be extracted from this document.',
            'recommendation': 'Ensure the document contains actual text and is not an image-only file. Try saving the document in a different format.',
        })
        return result

    # 1. Extract contact information
    result.contact_info = extract_contact_info(text)
    result.contact_score = calculate_contact_score(result.contact_info)

    # 2. Detect sections
    result.sections = detect_sections(text)

    # 3. Analyze structure
    result.structure_score, structure_issues = analyze_structure(result.sections, text)
    result.structure_issues.extend(structure_issues)

    # 4. Analyze formatting
    result.formatting_score, formatting_issues = analyze_formatting(doc_data)
    result.formatting_issues.extend(formatting_issues)

    # 5. Analyze text quality
    result.text_quality_score = analyze_text_quality(doc_data)

    return result


def extract_contact_info(text: str) -> ContactInfo:
    """Extract contact information from resume text."""
    info = ContactInfo()

    # Extract email
    emails = EMAIL_PATTERN.findall(text)
    if emails:
        info.email = emails[0]

    # Extract phone
    phones = PHONE_PATTERN.findall(text)
    if phones:
        # Filter out unlikely phone numbers (too short or too long)
        valid_phones = [p for p in phones if 7 <= len(re.sub(r'[^\d]', '', p)) <= 15]
        if valid_phones:
            info.phone = valid_phones[0]

    # Extract LinkedIn
    linkedin = LINKEDIN_PATTERN.findall(text)
    if linkedin:
        info.linkedin = linkedin[0]

    # Extract GitHub
    github = GITHUB_PATTERN.findall(text)
    if github:
        info.github = github[0]

    # Extract URLs
    urls = URL_PATTERN.findall(text)
    non_social_urls = [u for u in urls if 'linkedin' not in u.lower() and 'github' not in u.lower()]
    if non_social_urls:
        info.website = non_social_urls[0]

    # Extract name (heuristic: first non-empty line that's not an email/phone/URL)
    lines = text.strip().split('\n')
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if not line or len(line) < 2:
            continue
        if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line) or URL_PATTERN.search(line):
            continue
        # Likely a name if it's short, alphabetic, and at the top
        if len(line) < 60 and re.match(r'^[A-Za-z\s.\'-]+$', line):
            info.name = line
            break

    return info


def detect_sections(text: str) -> list:
    """Detect standard resume sections in the text."""
    lines = text.split('\n')
    detected_sections = []
    current_section = None
    current_content = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this line matches a section header
        matched_section = None
        for section_name, pattern in SECTION_PATTERNS.items():
            if re.match(pattern, stripped):
                matched_section = section_name
                break

        # Also check for all-caps headings (common in resumes)
        if not matched_section and stripped.isupper() and 2 <= len(stripped) <= 40:
            for section_name, pattern in SECTION_PATTERNS.items():
                if re.match(pattern, stripped):
                    matched_section = section_name
                    break
            # Try matching against section names directly
            if not matched_section:
                stripped_lower = stripped.lower()
                for section_name in SECTION_PATTERNS:
                    if stripped_lower == section_name or stripped_lower == section_name + 's':
                        matched_section = section_name
                        break

        if matched_section:
            # Save previous section
            if current_section:
                detected_sections.append(SectionDetection(
                    name=current_section,
                    detected=True,
                    content='\n'.join(current_content).strip(),
                    confidence=0.9,
                ))
            current_section = matched_section
            current_content = []
        else:
            current_content.append(stripped)

    # Save last section
    if current_section:
        detected_sections.append(SectionDetection(
            name=current_section,
            detected=True,
            content='\n'.join(current_content).strip(),
            confidence=0.9,
        ))

    # Check for expected sections not found
    expected_sections = ['experience', 'education', 'skills']
    detected_names = {s.name for s in detected_sections}

    for section in expected_sections:
        if section not in detected_names:
            # Try content-based detection
            confidence, content = detect_section_by_content(text, section)
            detected_sections.append(SectionDetection(
                name=section,
                detected=confidence > 0.5,
                content=content,
                confidence=confidence,
            ))

    return detected_sections


def detect_section_by_content(text: str, section_name: str) -> tuple:
    """Try to detect a section by its content patterns rather than headings."""
    text_lower = text.lower()

    if section_name == 'experience':
        # Look for date patterns near job-like content
        date_pattern = re.compile(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|present|\d{4})', re.IGNORECASE)
        matches = date_pattern.findall(text)
        if len(matches) >= 2:
            return 0.6, ''
    elif section_name == 'education':
        edu_keywords = ['university', 'college', 'bachelor', 'master', 'degree', 'diploma', 'b.tech', 'b.sc', 'm.tech', 'phd', 'gpa', 'cgpa']
        found = sum(1 for k in edu_keywords if k in text_lower)
        if found >= 2:
            return 0.7, ''
    elif section_name == 'skills':
        # Look for comma-separated or bullet-pointed skill lists
        skill_indicators = ['python', 'java', 'javascript', 'sql', 'html', 'css', 'react',
                           'node', 'django', 'flask', 'docker', 'aws', 'git', 'excel',
                           'communication', 'leadership', 'teamwork', 'machine learning']
        found = sum(1 for k in skill_indicators if k in text_lower)
        if found >= 3:
            return 0.7, ''

    return 0.2, ''


def analyze_structure(sections: list, text: str) -> tuple:
    """Analyze the structural quality of the resume."""
    score = 100.0
    issues = []

    detected_sections = [s for s in sections if s.detected]
    detected_names = {s.name for s in detected_sections}

    # Check for critical missing sections
    if 'experience' not in detected_names:
        score -= 15
        issues.append({
            'severity': 'important',
            'title': 'Experience section not clearly detected',
            'description': 'An Experience or Work Experience section was not clearly identified in your document.',
            'recommendation': 'Use a clear heading such as "Experience", "Work Experience", or "Professional Experience".',
        })

    if 'education' not in detected_names:
        score -= 10
        issues.append({
            'severity': 'important',
            'title': 'Education section not clearly detected',
            'description': 'An Education section was not clearly identified.',
            'recommendation': 'Use a clear heading such as "Education" or "Academic Background".',
        })

    if 'skills' not in detected_names:
        score -= 10
        issues.append({
            'severity': 'important',
            'title': 'Skills section not clearly detected',
            'description': 'A Skills section was not clearly identified.',
            'recommendation': 'Add a "Skills" or "Technical Skills" section to highlight your capabilities.',
        })

    # Check document length
    word_count = len(text.split())
    if word_count < 100:
        score -= 20
        issues.append({
            'severity': 'critical',
            'title': 'Document has very little text content',
            'description': f'Only {word_count} words were extracted. This may indicate a parsing issue or incomplete document.',
            'recommendation': 'Ensure your resume has substantial text content describing your experience, skills, and education.',
        })
    elif word_count > 2000:
        score -= 5
        issues.append({
            'severity': 'suggestion',
            'title': 'Document is quite lengthy',
            'description': f'The document contains {word_count} words. Very long resumes may be difficult for automated parsers.',
            'recommendation': 'Consider condensing to 1-2 pages for most positions.',
        })

    # Good findings
    if len(detected_sections) >= 4:
        issues.append({
            'severity': 'good',
            'title': 'Well-organized section structure',
            'description': f'{len(detected_sections)} clear sections detected. Good document organization helps automated parsers.',
        })

    return max(0, score), issues


def analyze_formatting(doc_data: DocumentData) -> tuple:
    """Analyze formatting quality."""
    score = 100.0
    issues = []

    # Check fonts
    if doc_data.fonts_used:
        non_standard = []
        for font in doc_data.fonts_used:
            font_lower = font.lower().strip()
            # Check against ATS-friendly fonts
            is_friendly = any(f in font_lower for f in ATS_FRIENDLY_FONTS)
            if not is_friendly and font_lower not in ('symbol', 'wingdings', 'zapfdingbats'):
                non_standard.append(font)

        if non_standard and len(non_standard) > len(doc_data.fonts_used) * 0.5:
            score -= 10
            issues.append({
                'severity': 'suggestion',
                'title': 'Consider using standard fonts',
                'description': f'Fonts detected: {", ".join(non_standard[:5])}. Some automated parsers work best with common fonts.',
                'recommendation': 'Consider using fonts such as Arial, Calibri, Times New Roman, or Helvetica.',
            })
        else:
            issues.append({
                'severity': 'good',
                'title': 'Standard fonts used',
                'description': 'The document uses fonts that are well-recognized by most document parsers.',
            })

    # Check for excessive images
    image_pages = sum(1 for p in doc_data.pages if p.is_image_only)
    if image_pages > 0:
        score -= 15 * image_pages
        issues.append({
            'severity': 'critical',
            'title': f'{image_pages} page(s) appear to be image-only',
            'description': 'Image-only pages cannot be read by automated document parsers.',
            'recommendation': 'Replace image-based content with actual text. If using a graphic design tool, export text separately.',
        })

    # Check for tables (can cause parsing issues)
    if doc_data.has_tables:
        score -= 5
        issues.append({
            'severity': 'suggestion',
            'title': 'Tables detected in document',
            'description': 'Some automated parsers may struggle with table layouts.',
            'recommendation': 'If possible, present tabular information using simple text formatting instead of tables.',
        })

    # Check page count
    if doc_data.page_count > 3:
        score -= 5
        issues.append({
            'severity': 'suggestion',
            'title': f'Document has {doc_data.page_count} pages',
            'description': 'Multi-page resumes may not be fully processed by all automated systems.',
            'recommendation': 'Consider condensing to 1-2 pages.',
        })

    return max(0, score), issues


def calculate_contact_score(contact: ContactInfo) -> float:
    """Calculate score for contact information completeness."""
    score = 0
    total_weight = 0

    checks = [
        (contact.name, 30, 'Name'),
        (contact.email, 30, 'Email'),
        (contact.phone, 20, 'Phone'),
        (contact.linkedin or contact.github or contact.website, 20, 'Online profile'),
    ]

    for value, weight, label in checks:
        total_weight += weight
        if value:
            score += weight

    return (score / total_weight) * 100 if total_weight > 0 else 0


def analyze_text_quality(doc_data: DocumentData) -> float:
    """Analyze text extraction quality."""
    score = 100.0

    if not doc_data.text or len(doc_data.text.strip()) < 10:
        return 0.0

    text = doc_data.text

    # Check for garbage characters (encoding issues)
    garbage_chars = sum(1 for c in text if ord(c) > 0xFFFF or (ord(c) < 32 and c not in '\n\r\t'))
    garbage_ratio = garbage_chars / len(text) if text else 0
    if garbage_ratio > 0.05:
        score -= 30

    # Check for very short word count relative to page count
    words_per_page = doc_data.word_count / max(1, doc_data.page_count)
    if words_per_page < 50:
        score -= 20

    # Check for excessive whitespace
    lines = text.split('\n')
    empty_lines = sum(1 for l in lines if not l.strip())
    if lines and empty_lines / len(lines) > 0.5:
        score -= 10

    return max(0, score)
