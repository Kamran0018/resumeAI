# resumes/views.py - Complete Updated Version
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.db import models
from .models import Resume
import os
import re

# ===== HOME FUNCTION =====
def home(request):
    """Home page - renders home.html for visitors, redirects to dashboard if authenticated (unless ?view=landing)"""
    if request.user.is_authenticated and request.GET.get('view') != 'landing':
        return redirect('dashboard')
    return render(request, 'home.html')

# ===== DASHBOARD FUNCTION (UPDATED & BULLETPROOF) =====
@login_required
def dashboard(request):
    """Main dashboard page with role-based content"""
    user = request.user
    resumes = Resume.objects.filter(user=user)
    
    context = {
        'user': user,
        'resumes': resumes,
        'resume_count': resumes.count(),
    }
    
    if user.user_type == 'candidate':
        # Candidate Dashboard - Show resume stats and recent resumes
        total_resumes = resumes.count()
        total_skills = 0
        for r in resumes:
            if r.skills and isinstance(r.skills, (list, tuple)):
                total_skills += len(r.skills)
        
        try:
            from applications.models import Application
            applications = Application.objects.filter(candidate=user)
            total_applications = applications.count()
            shortlisted = applications.filter(status='shortlisted').count()
            interviewing = applications.filter(status='interview').count()
            recent_applications = applications.order_by('-applied_at')[:3]
        except Exception:
            total_applications = 0
            shortlisted = 0
            interviewing = 0
            recent_applications = []
            
        context.update({
            'total_resumes': total_resumes,
            'total_skills': total_skills,
            'recent_resumes': resumes[:5],
            'total_applications': total_applications,
            'shortlisted': shortlisted,
            'interviewing': interviewing,
            'recent_applications': recent_applications,
        })
        return render(request, 'candidate/dashboard.html', context)
    
    else:
        # Recruiter Dashboard - Show job stats and applications
        try:
            from jobs.models import Job
            from applications.models import Application
            
            # Get all jobs posted by this recruiter
            jobs = Job.objects.filter(recruiter=user, is_active=True)
            
            # Get all applications for these jobs
            applications = Application.objects.filter(job__in=jobs).select_related('candidate', 'job')
            
            ranked_candidates = []
            for app in applications.order_by('-match_score', '-applied_at')[:10]:
                c_name = app.candidate.get_full_name() or app.candidate.username
                if hasattr(app.candidate, 'candidate_profile') and app.candidate.candidate_profile:
                    prof = app.candidate.candidate_profile
                    if hasattr(prof, 'first_name') and prof.first_name:
                        c_name = f"{prof.first_name} {prof.last_name}".strip()
                
                score = app.match_score or 0
                mb = app.match_breakdown if isinstance(app.match_breakdown, dict) else {}
                
                ranked_candidates.append({
                    'id': app.id,
                    'rank': len(ranked_candidates) + 1,
                    'application_id': app.id,
                    'candidate_name': c_name,
                    'candidate_email': app.candidate.email,
                    'score': round(score, 1),
                    'hire_probability': app.hire_probability or score,
                    'matched_skills': mb.get('matched_skills', []),
                    'missing_skills': mb.get('missing_skills', []),
                    'ai_recommendation': app.ai_recommendation or 'Consider',
                    'job_title': app.job.title if app.job else 'Job',
                    'status': app.status,
                    'applied_at': app.applied_at,
                })
            
            total_applications = applications.count()
            shortlisted = applications.filter(status='shortlisted').count()
            ai_matched = applications.filter(match_score__gte=70).count()
            avg_score = applications.aggregate(avg=models.Avg('match_score'))['avg'] or 0
            
            context.update({
                'jobs_posted': jobs.count(),
                'total_applications': total_applications,
                'shortlisted': shortlisted,
                'ai_matched': ai_matched,
                'applications': ranked_candidates,
                'hire_ready_count': len([c for c in ranked_candidates if c['score'] >= 80]),
                'avg_score': round(avg_score, 1),
            })
            
        except Exception as e:
            print(f"RECRUITER DASHBOARD NOTICE: {e}")
            context.update({
                'jobs_posted': 0,
                'total_applications': 0,
                'shortlisted': 0,
                'ai_matched': 0,
                'applications': [],
                'hire_ready_count': 0,
                'avg_score': 0,
            })
        
        return render(request, 'recruiter/dashboard.html', context)

# ===== RESUME UPLOAD (v2.0 — Full AI Pipeline) =====
@login_required
def upload_resume(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'My Resume')
        file  = request.FILES.get('file')

        if not file:
            messages.error(request, 'Please select a file')
            return redirect('upload_resume')

        if file.size > 10 * 1024 * 1024:
            messages.error(request, 'File size must be under 10MB.')
            return redirect('upload_resume')

        valid_extensions = ['.pdf', '.docx', '.doc', '.txt']
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in valid_extensions:
            messages.error(request, f'Invalid file type. Allowed: {", ".join(valid_extensions)}')
            return redirect('upload_resume')

        # Save resume record
        resume = Resume.objects.create(user=request.user, title=title, file=file)

        # Step 1: Parse resume
        try:
            from .services import ResumeParser
            parser      = ResumeParser()
            parsed_data = parser.parse(resume.file.path)

            resume.raw_text    = parsed_data.get('raw_text', '')
            resume.skills      = parsed_data.get('skills', [])
            resume.experience  = parsed_data.get('experience', [])
            resume.education   = parsed_data.get('education', [])
            resume.contact_info= parsed_data.get('contact_info', {})
            resume.save()
            skill_count = len(resume.skills)
        except Exception as e:
            skill_count = 0
            messages.warning(request, f'Parsing note: {str(e)}')

        # Step 2: Full AI analysis pipeline (Gemini + Grok + Fusion + ATS)
        try:
            from ai_services.views import _run_full_analysis
            _run_full_analysis(resume)
            messages.success(
                request,
                f'✅ Resume uploaded & analyzed! Found {skill_count} skills. '
                f'Resume Score: {round(resume.resume_score)}/100, '
                f'ATS Score: {round(resume.ats_score)}/100'
            )
        except Exception as e:
            messages.success(request, f'Resume uploaded! Found {skill_count} skills. (AI analysis pending)')

        return redirect('resume_detail', resume_id=resume.id)

    return render(request, 'resumes/upload.html')


# ===== RESUME LIST =====
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/list.html', {'resumes': resumes})

# ===== RESUME DETAIL (v2.0) =====
@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Debug print to check parsed text and skills
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(resume.file.path)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
            
        with open('scratch_status.txt', 'w', encoding='utf-8') as f:
            f.write(f"ID: {resume_id}\n")
            f.write(f"Title: {resume.title}\n")
            f.write(f"File Path: {resume.file.path}\n")
            f.write(f"PDF Text Len: {len(pdf_text)}\n")
            f.write(f"PDF Text Preview: {repr(pdf_text[:500])}\n")
            f.write(f"Raw Text Len: {len(resume.raw_text or '')}\n")
            f.write(f"Raw Text Preview: {repr((resume.raw_text or '')[:500])}\n")
            f.write(f"Skills: {resume.skills}\n")
            f.write(f"Fusion Analysis: {resume.fusion_analysis}\n")
    except Exception as e:
        print(f"Failed to write debug file: {e}")


    # Run AI analysis if not yet done
    if not resume.fusion_analysis:
        try:
            from ai_services.views import _run_full_analysis
            _run_full_analysis(resume)
        except Exception as e:
            print(f"AI analysis deferred: {e}")

    fusion   = resume.fusion_analysis or {}
    gemini   = resume.gemini_analysis or {}
    grok     = resume.grok_analysis   or {}

    context = {
        'resume'          : resume,
        # Scores
        'resume_score'    : round(resume.resume_score or fusion.get('resume_score', 0)),
        'ats_score'       : round(resume.ats_score    or fusion.get('ats_score', 0)),
        'grammar_score'   : round(resume.grammar_score or fusion.get('grammar_score', 0)),
        'technical_score' : round(resume.technical_score or fusion.get('technical_score', 0)),
        'hire_probability': round(fusion.get('hire_probability', 0)),
        # Analysis
        'strengths'       : fusion.get('strengths', [])[:6],
        'weaknesses'      : fusion.get('weaknesses', [])[:6],
        'suggestions'     : fusion.get('suggestions', [])[:8],
        'keywords_found'  : fusion.get('keywords_found', []),
        'keywords_missing': fusion.get('keywords_missing', []),
        'interview_topics': fusion.get('interview_topics', []),
        'certifications'  : fusion.get('certifications', []),
        'recommendation'  : fusion.get('recommendation', ''),
        # Generated content
        'built_resume'    : resume.built_resume,
        'cover_letter'    : resume.cover_letter,
        # Raw model outputs
        'gemini_score'    : gemini.get('score', 0),
        'grok_score'      : grok.get('technical_score', 0),
        'fusion'          : fusion,
    }
    return render(request, 'resumes/detail.html', context)


# ===== DELETE RESUME =====
@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    # Delete file from storage
    if resume.file:
        try:
            if os.path.exists(resume.file.path):
                os.remove(resume.file.path)
        except Exception as e:
            pass
    resume.delete()
    messages.success(request, 'Resume deleted successfully')
    return redirect('resume_list')

# ===== AI FEEDBACK GENERATOR (ENHANCED) =====
def generate_ai_feedback(resume):
    """Generate AI feedback for resume"""
    suggestions = []
    strengths = []
    
    # Skills analysis
    if len(resume.skills) == 0:
        suggestions.append("⚠️ No skills found. Add your technical skills to the resume.")
    elif len(resume.skills) < 3:
        suggestions.append(f"💡 Only {len(resume.skills)} skills found. Add more relevant skills.")
    elif len(resume.skills) < 6:
        suggestions.append(f"💡 Good start with {len(resume.skills)} skills. Consider adding more diverse skills.")
    else:
        strengths.append(f"✅ Great! You have {len(resume.skills)} skills listed.")
    
    # Experience analysis
    if len(resume.experience) == 0:
        suggestions.append("⚠️ No work experience found. Add your professional experience.")
    elif len(resume.experience) < 2:
        suggestions.append("💡 Consider adding more details to your work experience.")
    else:
        strengths.append(f"✅ Good! You have {len(resume.experience)} experience entries.")
    
    # Education analysis
    if len(resume.education) == 0:
        suggestions.append("⚠️ No education details found. Add your educational background.")
    else:
        strengths.append(f"✅ Education details present ({len(resume.education)} entries).")
    
    # Contact info analysis
    if not resume.contact_info.get('email'):
        suggestions.append("⚠️ Add email to contact information.")
    if not resume.contact_info.get('phone'):
        suggestions.append("⚠️ Add phone number to contact information.")
    
    # General improvements
    suggestions.append("📝 Add quantifiable achievements (e.g., 'Increased sales by 30%')")
    suggestions.append("💪 Use strong action verbs (Led, Managed, Developed, Created)")
    suggestions.append("🎯 Customize your resume for each job application")
    suggestions.append("📄 Keep resume to 1-2 pages maximum")
    
    return {
        'suggestions': suggestions[:6],
        'strengths': strengths,
        'score': calculate_resume_score(resume)
    }

def calculate_resume_score(resume):
    """Calculate resume score out of 100"""
    score = 0
    
    # Skills (max 30)
    skill_count = len(resume.skills)
    if skill_count >= 8:
        score += 30
    elif skill_count >= 5:
        score += 20
    elif skill_count >= 3:
        score += 10
    
    # Experience (max 30)
    exp_count = len(resume.experience)
    if exp_count >= 3:
        score += 30
    elif exp_count >= 2:
        score += 20
    elif exp_count >= 1:
        score += 10
    
    # Education (max 20)
    edu_count = len(resume.education)
    if edu_count >= 2:
        score += 20
    elif edu_count >= 1:
        score += 10
    
    # Contact info (max 20)
    if resume.contact_info.get('email'):
        score += 10
    if resume.contact_info.get('phone'):
        score += 10
    
    return min(score, 100)

# ===== ANALYZE RESUME (API) =====
@login_required
def analyze_resume(request, resume_id):
    """Get AI suggestions for resume (JSON response)"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Generate feedback
    feedback = generate_ai_feedback(resume)
    
    return JsonResponse({
        'suggestions': feedback.get('suggestions', []),
        'strengths': feedback.get('strengths', []),
        'score': feedback.get('score', 0),
    })

# ===== SEARCH RESUMES (FOR RECRUITER) =====
@login_required
def search_resumes(request):
    """Search resumes by skills or keywords (Recruiter only)"""
    if request.user.user_type != 'recruiter':
        return JsonResponse({'error': 'Only recruiters can search'}, status=403)
    
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'results': []})
    
    resumes = Resume.objects.filter(
        Q(skills__icontains=query) |
        Q(title__icontains=query) |
        Q(parsed_text__icontains=query)
    )[:20]
    
    results = []
    for resume in resumes:
        results.append({
            'id': resume.id,
            'title': resume.title,
            'user': resume.user.email,
            'skills': resume.skills[:5],
            'created_at': resume.created_at.strftime('%Y-%m-%d')
        })
    
    return JsonResponse({'results': results})


@login_required
def resume_print_preview(request, resume_id):
    """Render a clean, minimalist print-ready resume layout for candidate"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if not resume.built_resume:
        messages.warning(request, 'Please build the AI resume first.')
        return redirect('resume_detail', resume_id=resume.id)
        
    return render(request, 'resumes/print_preview.html', {'resume': resume})