# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('parse-jd/', views.parse_jd, name='parse_jd'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('all/', views.all_jobs, name='all_jobs'),
]