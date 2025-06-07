from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, CandidateProfile

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_candidate']

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'party', 'manifesto', 'image']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CandidateProfileEditForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'party', 'manifesto', 'image']
