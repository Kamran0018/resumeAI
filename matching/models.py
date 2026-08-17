from django.db import models


class ApplicationMatch(models.Model):

    application = models.OneToOneField(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='match'
    )

    skill_score = models.FloatField(default=0)
    experience_score = models.FloatField(default=0)
    education_score = models.FloatField(default=0)
    semantic_score = models.FloatField(default=0)
    preferred_skill_score = models.FloatField(default=0)

    overall_score = models.FloatField(default=0)

    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)

    explanation = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - {self.overall_score}%"