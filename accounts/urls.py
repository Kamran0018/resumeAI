# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/candidate/', views.register_candidate, name='register_candidate'),
    path('register/recruiter/', views.register_recruiter, name='register_recruiter'),
    path('login/candidate/', views.login_candidate, name='login_candidate'),
    path('login/recruiter/', views.login_recruiter, name='login_recruiter'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]