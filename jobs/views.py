# jobs/views.py
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Job
from applications.models import Application
from resumes.models import Resume
from ai_services.matcher import ResumeJobMatcher
from ai_services.jd_parser import JDParser
from django.db.models import Avg, Max

@login_required
def post_job(request):
    """Recruiter posts a new job"""
    if request.user.user_type != 'recruiter':
        messages.error(request, 'Only recruiters can post jobs')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        experience_level = request.POST.get('experience_level')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        responsibilities = request.POST.get('responsibilities', '')
        benefits = request.POST.get('benefits', '')
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        required_skills = request.POST.get('required_skills', '')
        preferred_skills = request.POST.get('preferred_skills', '')
        
        job = Job.objects.create(
            recruiter=request.user,
            title=title,
            company=company,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            description=description,
            requirements=requirements,
            responsibilities=responsibilities,
            benefits=benefits,
            salary_min=salary_min or None,
            salary_max=salary_max or None,
            required_skills=required_skills,
            preferred_skills=preferred_skills
        )
        
        messages.success(request, f'Job "{title}" posted successfully!')
        return redirect('my_jobs')
    
    return render(request, 'jobs/post_job.html')

@login_required
def my_jobs(request):
    """Recruiter sees all their jobs"""
    if request.user.user_type != 'recruiter':
        messages.error(request, 'Only recruiters can view jobs')
        return redirect('dashboard')
    
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    """View job details with applications"""
    job = get_object_or_404(Job, id=job_id)
    
    if request.user.user_type == 'recruiter' and job.recruiter != request.user:
        messages.error(request, 'You do not own this job')
        return redirect('dashboard')
    
    applications = Application.objects.filter(job=job).select_related('candidate', 'candidate__candidate_profile')
    
    # Calculate Stats
    stats = {
        'total': applications.count(),
        'avg_match': applications.aggregate(Avg('match_score'))['match_score__avg'] or 0,
        'top_match': applications.aggregate(Max('match_score'))['match_score__max'] or 0,
    }
    
    # Filtering
    min_score = request.GET.get('min_score')
    if min_score and min_score.isdigit():
        applications = applications.filter(match_score__gte=int(min_score))
        
    # Sorting
    sort_by = request.GET.get('sort', 'rank')
    if sort_by == 'score_desc':
        applications = applications.order_by('-match_score')
    elif sort_by == 'score_asc':
        applications = applications.order_by('match_score')
    elif sort_by == 'newest':
        applications = applications.order_by('-applied_at')
    else:
        applications = applications.order_by('rank') # default ranking
    
    context = {
        'job': job,
        'applications': applications,
        'stats': stats,
        'current_sort': sort_by,
        'current_min_score': min_score,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def all_jobs(request):
    """Candidates see all active jobs"""
    if request.user.user_type != 'candidate':
        messages.error(request, 'Only candidates can view jobs')
        return redirect('dashboard')
    
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'jobs/all_jobs.html', {'jobs': jobs})


@login_required
def parse_jd(request):
    """AJAX view to parse an uploaded Job Description document and return structured fields"""
    if request.user.user_type != 'recruiter':
        return JsonResponse({'error': 'Only recruiters can parse JDs'}, status=403)
        
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Validate size (10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            return JsonResponse({'error': 'File is too large. Max size is 10MB.'}, status=400)
            
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.pdf', '.docx', '.doc', '.txt']:
            return JsonResponse({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}, status=400)
            
        # Save temp file
        try:
            # Ensure temp directory exists
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_jd')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                
            path = default_storage.save('temp_jd/' + uploaded_file.name, ContentFile(uploaded_file.read()))
            full_path = os.path.join(settings.MEDIA_ROOT, path)
        except Exception as e:
            return JsonResponse({'error': f'Failed to write temporary file: {str(e)}'}, status=500)
        
        try:
            parser = JDParser()
            result = parser.parse_file(full_path)
            
            # Clean up
            if os.path.exists(full_path):
                os.remove(full_path)
                
            if not result:
                return JsonResponse({'error': 'Could not extract information from the file.'}, status=400)
                
            return JsonResponse({'success': True, 'data': result})
        except Exception as e:
            if os.path.exists(full_path):
                os.remove(full_path)
            return JsonResponse({'error': f'Parsing failed: {str(e)}'}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)