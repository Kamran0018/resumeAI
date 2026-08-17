# applications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('<int:app_id>/', views.application_detail, name='application_detail'),
    path('my/', views.my_applications, name='my_applications'),
    path('all/', views.all_applications, name='all_applications'),
    path('<int:app_id>/update-status/', views.update_status, name='update_application_status'),
]   