from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, CandidateProfileForm, UserEditForm, CandidateProfileEditForm
from .models import CandidateProfile, User
from voting.models import Voting

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_candidate:
                CandidateProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        return render(request, 'admin_dashboard.html')
    elif request.user.is_candidate:
        elections = Voting.objects.filter(is_active=True)
        return render(request, 'candidate_dashboard.html', {'elections': elections})
    else:
        return render(request, 'user_dashboard.html')

@login_required
def edit_profile_view(request):
    if request.user.is_candidate:
        profile = request.user.candidate_profile
        if request.method == 'POST':
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = CandidateProfileEditForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('dashboard')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = CandidateProfileEditForm(instance=profile)
        return render(request, 'edit_candidate_profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        if request.method == 'POST':
            user_form = UserEditForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('dashboard')
        else:
            user_form = UserEditForm(instance=request.user)
        return render(request, 'edit_user_profile.html', {'user_form': user_form})
