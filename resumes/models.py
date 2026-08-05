# resumes/models.py
from django.db import models
from accounts.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, default='My Resume')
    file = models.FileField(upload_to='resumes/')

    # Parsed data
    raw_text = models.TextField(blank=True, default='')
    skills = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    contact_info = models.JSONField(default=dict, blank=True)

    # Legacy — kept for backwards compatibility
    ai_suggestions = models.JSONField(default=dict, blank=True)

    # ===== v2.0 AI Analysis Fields =====
    gemini_analysis = models.JSONField(default=dict, blank=True)   # Gemini resume coach output
    grok_analysis   = models.JSONField(default=dict, blank=True)   # Grok technical analysis
    fusion_analysis = models.JSONField(default=dict, blank=True)   # Merged final report

    # Score breakdown
    resume_score    = models.FloatField(default=0)   # Overall quality 0-100
    ats_score       = models.FloatField(default=0)   # ATS compatibility 0-100
    grammar_score   = models.FloatField(default=0)   # Grammar/writing 0-100
    technical_score = models.FloatField(default=0)   # Technical depth 0-100

    # Generated content
    built_resume    = models.TextField(blank=True, default='')   # AI-built resume text
    cover_letter    = models.TextField(blank=True, default='')   # AI cover letter

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def get_resume_text(self):
        """Reconstruct resume text from stored fields for AI prompts"""
        if self.raw_text:
            return self.raw_text
        parts = []
        if self.skills:
            parts.append('Skills: ' + ', '.join(self.skills))
        for exp in self.experience:
            if isinstance(exp, dict):
                parts.append(
                    f"{exp.get('role','')} at {exp.get('company','')} ({exp.get('years','')})"
                )
        for edu in self.education:
            if isinstance(edu, dict):
                parts.append(
                    f"{edu.get('degree','')} from {edu.get('institution','')} ({edu.get('year','')})"
                )
        return '\n'.join(parts)