# jobs/models.py
from django.db import models
from accounts.models import User

class Job(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    )
    
    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level (0-2 years)'),
        ('junior', 'Junior (2-4 years)'),
        ('mid', 'Mid Level (4-7 years)'),
        ('senior', 'Senior (7-10 years)'),
        ('lead', 'Lead (10+ years)'),
        ('manager', 'Manager (10+ years)'),
    )
    
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    
    # Basic Info
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='mid')
    
    # Description
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField()
    preferred_qualifications = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    
    # Skills - Store as comma-separated for SQLite
    required_skills = models.TextField(blank=True, default='')
    preferred_skills = models.TextField(blank=True, default='')
    
    # Compensation
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    application_deadline = models.DateField(null=True, blank=True)
    
    # Tracking
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_required_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]
    
    def get_preferred_skills_list(self):
        return [s.strip() for s in self.preferred_skills.split(',') if s.strip()]
    
    def __str__(self):
        return f"{self.title} - {self.company}"
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'jobs'