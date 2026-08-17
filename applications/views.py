# applications/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Application
from jobs.models import Job
from resumes.models import Resume


@login_required
def apply_job(request, job_id):

    # Only candidates can apply
    if request.user.user_type != 'candidate':
        messages.error(
            request,
            'Only candidates can apply for jobs.'
        )
        return redirect('dashboard')

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    # Check duplicate application
    if Application.objects.filter(
        candidate=request.user,
        job=job
    ).exists():

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect(
            'application_detail',
            app_id=Application.objects.get(
                candidate=request.user,
                job=job
            ).id
        )

    # Get candidate resumes
    resumes = Resume.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # GET → show resume selection page
    if request.method == 'GET':

        return render(
            request,
            'applications/apply_job.html',
            {
                'job': job,
                'resumes': resumes,
            }
        )

    # POST → selected resume
    resume_id = request.POST.get('resume_id')

    if not resume_id:
        messages.error(
            request,
            'Please select a resume.'
        )

        return render(
            request,
            'applications/apply_job.html',
            {
                'job': job,
                'resumes': resumes,
            }
        )

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    # --------------------------------
    # Create Application
    # --------------------------------

    application = Application.objects.create(
        candidate=request.user,
        job=job,
        resume=resume,
        status='applied'
    )

    # --------------------------------
    # Calculate AI/ML Match
    # --------------------------------

    try:

        from matching.application_matcher import (
            calculate_application_match
        )

        calculate_application_match(
            application
        )

        messages.success(
            request,
            'Application submitted and resume matched successfully!'
        )

    except Exception as e:

        # Application should remain submitted
        # even if matching fails.

        messages.warning(
            request,
            f'Application submitted, but matching could not be completed: {str(e)}'
        )

    return redirect(
        'application_detail',
        app_id=application.id
    )


@login_required
def application_detail(request, app_id):

    application = get_object_or_404(
        Application,
        id=app_id
    )

    # Candidate ownership check
    if (
        request.user.user_type == 'candidate'
        and application.candidate != request.user
    ):
        messages.error(
            request,
            'You do not own this application.'
        )

        return redirect('dashboard')

    # Recruiter ownership check
    if (
        request.user.user_type == 'recruiter'
        and application.job.recruiter != request.user
    ):
        messages.error(
            request,
            'You do not own this application.'
        )

        return redirect('dashboard')

    return render(
        request,
        'applications/application_detail.html',
        {
            'application': application
        }
    )


@login_required
def my_applications(request):

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related(
        'job',
        'resume'
    )

    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': applications
        }
    )


@login_required
def all_applications(request):

    if request.user.user_type != 'recruiter':

        messages.error(
            request,
            'Only recruiters can view applications.'
        )

        return redirect('dashboard')

    applications = Application.objects.filter(
        job__recruiter=request.user
    ).select_related(
        'candidate',
        'job',
        'resume'
    )

    return render(
        request,
        'applications/all_applications.html',
        {
            'applications': applications
        }
    )


@login_required
def update_status(request, app_id):

    if request.method != 'POST':
        return redirect('dashboard')

    application = get_object_or_404(
        Application,
        id=app_id
    )

    # Recruiter ownership check
    if (
        request.user.user_type != 'recruiter'
        or application.job.recruiter != request.user
    ):

        messages.error(
            request,
            'You do not have permission to update this application.'
        )

        return redirect('dashboard')

    new_status = request.POST.get('status')

    valid_statuses = [
        choice[0]
        for choice in Application.STATUS_CHOICES
    ]

    if new_status in valid_statuses:

        application.status = new_status

        application.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        messages.success(
            request,
            f'Application status updated to '
            f'{application.get_status_display()}.'
        )

    else:

        messages.error(
            request,
            'Invalid status.'
        )

    return redirect(
        'application_detail',
        app_id=application.id
    )