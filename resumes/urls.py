# resumes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('list/', views.resume_list, name='resume_list'),
    path('<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('<int:resume_id>/print/', views.resume_print_preview, name='resume_print_preview'),
    path('<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    path('<int:resume_id>/analyze/', views.analyze_resume, name='analyze_resume'),
    path('search/', views.search_resumes, name='search_resumes'),  # For recruiters
]