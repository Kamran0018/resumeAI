# applications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Application
from django.http import HttpResponse    

@login_required
def application_detail(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    
    if request.user.user_type == 'candidate' and application.candidate != request.user:
        messages.error(request, 'You do not own this application')
        return redirect('dashboard')
    
    if request.user.user_type == 'recruiter' and application.job.recruiter != request.user:
        messages.error(request, 'You do not own this application')
        return redirect('dashboard')
    
    return render(request, 'applications/application_detail.html', {'application': application})

@login_required
def my_applications(request):
    applications = Application.objects.filter(candidate=request.user)
    return render(request, 'applications/my_applications.html', {'applications': applications})

@login_required
def all_applications(request):
    if request.user.user_type != 'recruiter':
        messages.error(request, 'Only recruiters can view applications')
        return redirect('dashboard')
    
    applications = Application.objects.filter(job__recruiter=request.user)
    return render(request, 'applications/all_applications.html', {'applications': applications})

@login_required
def update_status(request, app_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, id=app_id)
        
        # Verify the user is a recruiter and owns the job
        if request.user.user_type != 'recruiter' or application.job.recruiter != request.user:
            messages.error(request, 'You do not have permission to update this application.')
            return redirect('dashboard')
            
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
        
        if new_status in valid_statuses:
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status.')
            
        return redirect('application_detail', app_id=application.id)
    return redirect('dashboard')


def inam(request, resume_id):
    return HttpResponse("Hellow Inam ")