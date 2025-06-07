from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_voter = models.BooleanField(default=True)
    # Add more fields as needed

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    bio = models.TextField(blank=True)
    party = models.CharField(max_length=100)
    manifesto = models.TextField(blank=True)
    image = models.ImageField(upload_to='candidate_images/', blank=True, null=True)
    # For college elections only

    def __str__(self):
        return self.user.get_full_name() or self.user.username
