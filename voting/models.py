from django.db import models
from accounts.models import User

# Create your models here.

class Voting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    candidates = models.ManyToManyField('accounts.CandidateProfile', related_name='elections')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    candidate = models.ForeignKey('accounts.CandidateProfile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'voting')

    def __str__(self):
        return f"{self.voter.username} voted in {self.voting.title}"
