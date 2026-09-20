from rest_framework import serializers
from .models import JobDescription, JobMatch


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ('id', 'title', 'content', 'created_at')


class JobMatchSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='analysis.uploaded_file.original_name', read_only=True)

    class Meta:
        model = JobMatch
        fields = (
            'id', 'analysis', 'file_name', 'job_description',
            'match_score', 'matched_keywords', 'missing_keywords',
            'suggestions', 'created_at'
        )


class MatchRequestSerializer(serializers.Serializer):
    analysis_id = serializers.IntegerField(required=False, allow_null=True)
    job_description = serializers.CharField(required=True, max_length=10000)
    title = serializers.CharField(required=False, default='Target Role')
