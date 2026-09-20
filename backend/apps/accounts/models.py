from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile for ResumeSense users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.display_name or self.user.username

    @property
    def name(self):
        return self.display_name or self.user.get_full_name() or self.user.username
