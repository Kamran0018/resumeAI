# applications/models.py
from django.db import models
from accounts.models import User
from jobs.models import Job
from resumes.models import Resume

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied',     'Applied'),
        ('reviewing',   'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview',   'Interview'),
        ('offered',     'Offered'),
        ('rejected',    'Rejected'),
        ('withdrawn',   'Withdrawn'),
    )

    candidate = models.ForeignKey(User,   on_delete=models.CASCADE, related_name='applications')
    job       = models.ForeignKey(Job,    on_delete=models.CASCADE, related_name='applications')
    resume    = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)

    # ===== Legacy AI Scores (kept) =====
    match_score      = models.FloatField(default=0)
    match_breakdown  = models.JSONField(default=dict)
    ai_recommendation = models.CharField(max_length=50, blank=True)

    # ===== v2.0 AI Match Fields =====
    gemini_match         = models.JSONField(default=dict, blank=True)   # Gemini semantic match
    grok_match           = models.JSONField(default=dict, blank=True)   # Grok technical match
    fusion_match         = models.JSONField(default=dict, blank=True)   # Merged match report

    # Ranking & hiring intelligence
    rank                 = models.IntegerField(default=0)
    hire_probability     = models.FloatField(default=0)       # 0-100 %
    interview_questions  = models.JSONField(default=list, blank=True)

    # Status
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    recruiter_notes = models.TextField(blank=True)

    applied_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.email} → {self.job.title}"

    class Meta:
        ordering = ['-match_score', '-applied_at']
        db_table = 'applications'
        unique_together = ['candidate', 'job']