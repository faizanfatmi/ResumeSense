import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def upload_path(instance, filename):
    """Generate unique upload path: uploads/<user_id>/<uuid>_<filename>"""
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('uploads', str(instance.user.id), unique_name)


class UploadedFile(models.Model):
    """Represents an uploaded document file."""

    class FileType(models.TextChoices):
        PDF = 'PDF', 'PDF'
        DOCX = 'DOCX', 'DOCX'
        PPTX = 'PPTX', 'PPTX'
        PPT = 'PPT', 'PPT'

    class ProcessingStatus(models.TextChoices):
        UPLOADED = 'UPLOADED', 'Uploaded'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_path)
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    file_size = models.PositiveIntegerField(help_text='File size in bytes')
    mime_type = models.CharField(max_length=100, blank=True)
    processing_status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.UPLOADED
    )
    error_message = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'uploaded_files'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
            models.Index(fields=['processing_status']),
        ]

    def __str__(self):
        return f"{self.original_name} ({self.file_type})"

    @property
    def size_display(self):
        """Human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def delete(self, *args, **kwargs):
        """Delete file from storage when model is deleted."""
        if self.file:
            storage = self.file.storage
            if storage.exists(self.file.name):
                storage.delete(self.file.name)
        super().delete(*args, **kwargs)
