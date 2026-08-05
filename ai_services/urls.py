# ai_services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ── Analysis ──────────────────────────────
    path('analyze/<int:resume_id>/',        views.analyze_resume,        name='analyze_resume'),
    path('match/<int:job_id>/',             views.match_job,             name='match_job'),
    path('rank/<int:job_id>/',              views.rank_candidates,       name='rank_candidates'),

    # ── Resume Builder ────────────────────────
    path('build/<int:resume_id>/',          views.build_resume,          name='build_resume'),
    path('download/<int:resume_id>/',       views.download_built_resume, name='download_built_resume'),
    path('download-docx/<int:resume_id>/',  views.download_built_resume_docx, name='download_built_resume_docx'),

    # ── Cover Letter ──────────────────────────
    path('cover-letter/<int:resume_id>/',   views.generate_cover_letter, name='generate_cover_letter'),
    path('cover-letter/<int:resume_id>/dl/',views.download_cover_letter, name='download_cover_letter'),

    # ── Voice (browser Speech API) ────────────
    path('voice/<int:resume_id>/',          views.generate_voice,        name='generate_voice'),
    path('voice-match/<int:job_id>/',       views.generate_match_voice,  name='generate_match_voice'),

    # ── Recruiter Intelligence ────────────────
    path('interview/<int:app_id>/',         views.interview_questions,   name='interview_questions'),
    path('analytics/',                      views.analytics_dashboard,   name='analytics_dashboard'),
]