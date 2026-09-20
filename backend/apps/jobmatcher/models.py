from django.db import models
from django.contrib.auth.models import User
from apps.analysis.models import Analysis


class JobDescription(models.Model):
    """Stores target job description provided by the user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_descriptions')
    title = models.CharField(max_length=200, blank=True, default='Target Role')
    content = models.TextField(help_text='Full pasted job description text')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_descriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title or 'Job Description'} ({self.user.username})"


class JobMatch(models.Model):
    """Stores the match results between an Analysis and a JobDescription."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_matches')
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='job_matches')
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='matches')

    match_score = models.FloatField(default=0, help_text='Match score (0-100)')
    matched_keywords = models.JSONField(default=list, help_text='Keywords present in both resume and JD')
    missing_keywords = models.JSONField(default=list, help_text='Keywords in JD but missing/weak in resume')
    suggestions = models.JSONField(default=list, help_text='Ethical, actionable improvement suggestions')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_matches'
        ordering = ['-created_at']

    def __str__(self):
        return f"Match: {self.analysis.uploaded_file.original_name} — {self.match_score}%"
