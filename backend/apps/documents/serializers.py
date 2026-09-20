from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    """Serializer for uploaded file details."""
    size_display = serializers.CharField(read_only=True)

    class Meta:
        model = UploadedFile
        fields = (
            'id', 'original_name', 'file_type', 'file_size', 'size_display',
            'mime_type', 'processing_status', 'error_message',
            'uploaded_at', 'updated_at'
        )
        read_only_fields = fields


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file upload request."""
    file = serializers.FileField()
    analysis_type = serializers.ChoiceField(
        choices=[('resume', 'Resume'), ('ppt', 'Presentation')],
        default='resume'
    )


class FileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for file listing."""
    size_display = serializers.CharField(read_only=True)
    latest_score = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = (
            'id', 'original_name', 'file_type', 'file_size', 'size_display',
            'processing_status', 'uploaded_at', 'latest_score'
        )

    def get_latest_score(self, obj):
        latest = obj.analyses.order_by('-created_at').first()
        return latest.score if latest else None
