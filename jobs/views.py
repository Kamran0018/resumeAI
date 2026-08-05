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
    
    applications = Application.objects.filter(job=job)
    matcher = ResumeJobMatcher()
    ranked = matcher.rank_candidates(job, applications)
    
    context = {
        'job': job,
        'ranked_candidates': ranked,
        'applications_count': applications.count(),
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
def apply_job(request, job_id):
    """Candidate applies to a job"""
    if request.user.user_type != 'candidate':
        messages.error(request, 'Only candidates can apply')
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    if Application.objects.filter(candidate=request.user, job=job).exists():
        messages.warning(request, 'You have already applied to this job')
        return redirect('job_detail', job_id=job.id)
    
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        messages.error(request, 'Please upload a resume first')
        return redirect('upload_resume')
    
    application = Application.objects.create(
        candidate=request.user,
        job=job,
        resume=resume
    )
    
    matcher = ResumeJobMatcher()
    match_result = matcher.match_resume_to_job(resume, job)
    
    application.match_score = match_result['overall_score']
    application.match_breakdown = match_result
    application.ai_recommendation = match_result['recommendation']
    
    # v2.0 fields
    application.gemini_match = match_result.get('gemini_match', {})
    application.grok_match = match_result.get('grok_match', {})
    application.fusion_match = match_result
    application.hire_probability = match_result.get('hire_probability', 0)
    application.interview_questions = match_result.get('interview_questions', [])
    application.save()
    
    job.applications_count += 1
    job.save()
    
    messages.success(request, f'Applied to {job.title}! Score: {match_result["overall_score"]}%')
    return redirect('my_applications')


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