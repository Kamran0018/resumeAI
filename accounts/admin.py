# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CandidateProfile, RecruiterProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'user_type', 'is_verified', 'is_active']
    list_filter = ['user_type', 'is_verified', 'is_active']
    search_fields = ['email', 'username']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('user_type', 'is_verified', 'email_verified', 
                                   'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type'),
        }),
    )

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'title', 'experience_years']
    list_filter = ['experience_years']
    search_fields = ['first_name', 'last_name', 'user__email']

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'position', 'verified']
    list_filter = ['verified']
    search_fields = ['company', 'user__email']