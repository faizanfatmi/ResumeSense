from rest_framework import serializers
from .models import Analysis, Finding, ExtractedSection, KeywordGroup, SlideAnalysis
from apps.documents.serializers import UploadedFileSerializer


class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = ('id', 'severity', 'category', 'title', 'description', 'recommendation', 'metadata')


class ExtractedSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedSection
        fields = ('id', 'section_name', 'content', 'detected', 'confidence', 'order')


class KeywordGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordGroup
        fields = ('id', 'group_name', 'keywords')


class SlideAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideAnalysis
        fields = (
            'id', 'slide_number', 'extracted_text', 'text_quality',
            'has_images', 'has_tables', 'font_issues', 'warnings'
        )


class AnalysisDetailSerializer(serializers.ModelSerializer):
    file = UploadedFileSerializer(source='uploaded_file', read_only=True)
    findings = FindingSerializer(many=True, read_only=True)
    sections = ExtractedSectionSerializer(many=True, read_only=True)
    keyword_groups = KeywordGroupSerializer(many=True, read_only=True)
    slides = SlideAnalysisSerializer(many=True, read_only=True)

    counts = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = (
            'id', 'file', 'analysis_type', 'score',
            'text_score', 'structure_score', 'formatting_score',
            'keyword_score', 'contact_score',
            'extracted_text', 'summary',
            'page_count', 'word_count', 'processing_time',
            'created_at',
            'findings', 'sections', 'keyword_groups', 'slides',
            'counts',
        )

    def get_counts(self, obj):
        findings = obj.findings.all()
        return {
            'total': findings.count(),
            'critical': findings.filter(severity='critical').count(),
            'important': findings.filter(severity='important').count(),
            'suggestion': findings.filter(severity='suggestion').count(),
            'good': findings.filter(severity='good').count(),
        }


class AnalysisListSerializer(serializers.ModelSerializer):
    original_name = serializers.CharField(source='uploaded_file.original_name', read_only=True)
    file_type = serializers.CharField(source='uploaded_file.file_type', read_only=True)

    class Meta:
        model = Analysis
        fields = (
            'id', 'original_name', 'file_type', 'analysis_type',
            'score', 'created_at'
        )
