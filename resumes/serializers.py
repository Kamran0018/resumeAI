# resumes/serializers.py
from rest_framework import serializers
from .models import Resume, ResumeFeedback

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'id', 'title', 'file', 'skills', 'experience', 
            'education', 'contact_info', 'ai_suggestions', 
            'is_active', 'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ResumeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(required=False, default='My Resume')
    
    def validate_file(self, value):
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size too large. Max 10MB")
        
        # Check file extension
        valid_extensions = ['.pdf', '.docx', '.doc', '.txt']
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(f"Invalid file type. Allowed: {', '.join(valid_extensions)}")
        
        return value

class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = ['id', 'feedback_type', 'suggestions', 'strengths', 'weaknesses', 'score', 'created_at']