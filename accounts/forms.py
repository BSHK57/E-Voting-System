from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, CandidateProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_candidate = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_candidate']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_candidate = self.cleaned_data.get('is_candidate', False)
        if commit:
            user.save()
        return user

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
