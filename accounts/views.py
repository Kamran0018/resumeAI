# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, CandidateProfile, RecruiterProfile

def register_candidate(request):
    """Register as Candidate"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password')
        password2 = request.POST.get('password_confirm') or request.POST.get('password2')
        phone = request.POST.get('phone', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validation
        if not email or not username or not password:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'accounts/register_candidate.html')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register_candidate.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register_candidate.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register_candidate.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                user_type='candidate',
                phone=phone
            )
            
            # Create candidate profile
            CandidateProfile.objects.create(
                user=user,
                first_name=first_name or username,
                last_name=last_name
            )
            
            login(request, user)
            messages.success(request, 'Candidate registered successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'accounts/register_candidate.html')
    
    return render(request, 'accounts/register_candidate.html')

def register_recruiter(request):
    """Register as Recruiter"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password')
        password2 = request.POST.get('password_confirm') or request.POST.get('password2')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company_name') or request.POST.get('company', '')
        position = request.POST.get('position', 'Recruiter')
        
        # Validation
        if not email or not username or not password:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'accounts/register_recruiter.html')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register_recruiter.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register_recruiter.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register_recruiter.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                user_type='recruiter',
                phone=phone
            )
            
            # Create recruiter profile
            RecruiterProfile.objects.create(
                user=user,
                company=company or 'Company',
                position=position
            )
            
            login(request, user)
            messages.success(request, 'Recruiter registered successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'accounts/register_recruiter.html')
    
    return render(request, 'accounts/register_recruiter.html')

def login_candidate(request):
    """Login as Candidate"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please fill all fields')
            return render(request, 'accounts/login_candidate.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.user_type != 'candidate':
                messages.error(request, 'This account is not a candidate account')
                return render(request, 'accounts/login_candidate.html')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login_candidate.html')
    
    return render(request, 'accounts/login_candidate.html')

def login_recruiter(request):
    """Login as Recruiter"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please fill all fields')
            return render(request, 'accounts/login_recruiter.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.user_type != 'recruiter':
                messages.error(request, 'This account is not a recruiter account')
                return render(request, 'accounts/login_recruiter.html')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login_recruiter.html')
    
    return render(request, 'accounts/login_recruiter.html')

def user_logout(request):
    """Logout - Django's logout() handles session clearing safely"""
    logout(request)  # clears auth + rotates CSRF token (no manual flush needed)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

@login_required
def profile(request):
    """User Profile"""
    context = {}
    if request.user.user_type == 'candidate' and hasattr(request.user, 'candidate_profile'):
        context['profile'] = request.user.candidate_profile
    elif request.user.user_type == 'recruiter' and hasattr(request.user, 'recruiter_profile'):
        context['profile'] = request.user.recruiter_profile
    return render(request, 'accounts/profile.html', context)


def csrf_failure(request, reason=''):
    """
    Custom CSRF failure handler.
    Instead of a 403 page, redirect gracefully:
    - Authenticated users → dashboard
    - Unauthenticated users → login page with a friendly message
    """
    if request.user.is_authenticated:
        # Already logged in — just go to dashboard (stale form was submitted)
        messages.warning(request, 'Your form session expired. Please try again.')
        return redirect('dashboard')
    else:
        # Not logged in — send to login with a helpful notice
        messages.warning(request, 'Your session expired. Please log in again.')
        return redirect('login_candidate')