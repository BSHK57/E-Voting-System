from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, CandidateProfileForm, UserEditForm, CandidateProfileEditForm
from .models import CandidateProfile, User
from voting.models import Voting

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # Set user as active
                user.is_active = True
                user.save()
                
                # Create candidate profile if user is registering as candidate
                if user.is_candidate:
                    CandidateProfile.objects.create(
                        user=user,
                        party="",  # Default empty party
                        bio=""     # Default empty bio
                    )
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to E-Voting System.')
                return redirect('dashboard')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            messages.error(request, f'An error occurred during registration. Please try again.')
            form = UserRegisterForm()  # Reset form
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        messages.error(request, 'Invalid username or password. Please try again.')
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
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = CandidateProfileEditForm(instance=profile)
        return render(request, 'edit_candidate_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    else:
        if request.method == 'POST':
            user_form = UserEditForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            user_form = UserEditForm(instance=request.user)
        return render(request, 'edit_user_profile.html', {'user_form': user_form})
