from django import forms
from .models import Voting

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['title', 'description', 'start_time', 'end_time', 'candidates']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
