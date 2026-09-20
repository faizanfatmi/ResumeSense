from django.db import models
from apps.documents.models import UploadedFile


class Analysis(models.Model):
    """Stores the overall analysis result for an uploaded document."""

    uploaded_file = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name='analyses'
    )
    analysis_type = models.CharField(
        max_length=20,
        choices=[('resume', 'Resume'), ('ppt', 'Presentation')],
        default='resume'
    )

    # Overall score
    score = models.FloatField(default=0, help_text='Overall ATS compatibility score (0-100)')

    # Score breakdown
    text_score = models.FloatField(default=0, help_text='Text extraction quality score')
    structure_score = models.FloatField(default=0, help_text='Section structure score')
    formatting_score = models.FloatField(default=0, help_text='Formatting quality score')
    keyword_score = models.FloatField(default=0, help_text='Keyword coverage score')
    contact_score = models.FloatField(default=0, help_text='Contact information score')

    # Extracted content
    extracted_text = models.TextField(blank=True, help_text='Full extracted text')
    summary = models.TextField(blank=True, help_text='AI-generated analysis summary')

    # Metadata
    page_count = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    processing_time = models.FloatField(default=0, help_text='Processing time in seconds')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analyses'
        ordering = ['-created_at']
        verbose_name_plural = 'Analyses'
        indexes = [
            models.Index(fields=['uploaded_file', '-created_at']),
        ]

    def __str__(self):
        return f"Analysis for {self.uploaded_file.original_name} — Score: {self.score}"


class Finding(models.Model):
    """Individual finding/issue from an analysis."""

    class Severity(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        IMPORTANT = 'important', 'Important'
        SUGGESTION = 'suggestion', 'Suggestion'
        GOOD = 'good', 'Good'

    class Category(models.TextChoices):
        TEXT_EXTRACTION = 'text_extraction', 'Text Extraction'
        SECTION_STRUCTURE = 'section_structure', 'Section Structure'
        FORMATTING = 'formatting', 'Formatting'
        KEYWORDS = 'keywords', 'Keywords'
        CONTACT_INFO = 'contact_info', 'Contact Information'
        CONTENT = 'content', 'Content'
        LAYOUT = 'layout', 'Layout'
        IMAGES = 'images', 'Images'
        SLIDE_ANALYSIS = 'slide_analysis', 'Slide Analysis'

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='findings')
    severity = models.CharField(max_length=20, choices=Severity.choices)
    category = models.CharField(max_length=30, choices=Category.choices)
    title = models.CharField(max_length=255)
    description = models.TextField()
    recommendation = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'findings'
        ordering = ['severity', 'category']

    def __str__(self):
        return f"[{self.severity}] {self.title}"


class ExtractedSection(models.Model):
    """Detected section in a document."""

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='sections')
    section_name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    detected = models.BooleanField(default=True)
    confidence = models.FloatField(default=1.0, help_text='Confidence of detection (0-1)')
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'extracted_sections'
        ordering = ['order']

    def __str__(self):
        return f"{self.section_name} ({'✓' if self.detected else '✗'})"


class KeywordGroup(models.Model):
    """Group of extracted keywords from analysis."""

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='keyword_groups')
    group_name = models.CharField(max_length=100)
    keywords = models.JSONField(default=list)

    class Meta:
        db_table = 'keyword_groups'

    def __str__(self):
        return f"{self.group_name}: {', '.join(self.keywords[:5])}"


class SlideAnalysis(models.Model):
    """Per-slide analysis for PPT/PPTX files."""

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='slides')
    slide_number = models.IntegerField()
    extracted_text = models.TextField(blank=True)
    text_quality = models.CharField(
        max_length=20,
        choices=[('good', 'Good'), ('warning', 'Warning'), ('poor', 'Poor')],
        default='good'
    )
    has_images = models.BooleanField(default=False)
    has_tables = models.BooleanField(default=False)
    font_issues = models.JSONField(default=list, blank=True)
    warnings = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'slide_analyses'
        ordering = ['slide_number']

    def __str__(self):
        return f"Slide {self.slide_number} — {self.text_quality}"
