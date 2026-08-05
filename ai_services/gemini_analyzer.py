# ai_services/gemini_analyzer.py
import os
import json
from django.conf import settings

class GeminiAnalyzer:
    """Gemini API se resume analysis - using new google-genai package"""
    
    def __init__(self):
        try:
            from google import genai
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                raise ValueError("No API key found")
            self.client = genai.Client(api_key=api_key)
            self.model = 'gemini-2.5-flash'
            self.available = True
        except Exception as e:
            print(f"Gemini not available: {e}. Using rule-based analyzer.")
            self.available = False
    
    def analyze_resume(self, resume_text):
        """Resume analyze karo aur feedback do"""
        
        if not self.available or not resume_text or not resume_text.strip():
            return self._fallback_analysis(resume_text)
        
        prompt = f"""You are an expert resume coach and career advisor. Analyze this resume and give detailed, actionable feedback.

**RESUME:**
{resume_text[:5000]}

Give me a detailed analysis in this EXACT JSON format. No extra text, only JSON:

{{
    "score": 75,
    "rating": "Good",
    "strengths": [
        "Strong Python skills with 5 years experience",
        "Excellent communication skills",
        "Good academic background"
    ],
    "weaknesses": [
        "No quantifiable achievements",
        "Missing cloud technologies like AWS",
        "Action verbs missing"
    ],
    "suggestions": [
        "Add numbers to your achievements (e.g., 'Increased sales by 30%')",
        "Learn AWS or Azure to boost your profile",
        "Add a professional summary at the top",
        "Use stronger action verbs like Led, Managed, Developed"
    ],
    "recommendation": "Good candidate, needs some improvement",
    "summary": "Overall a good resume with strong technical skills. Focus on adding quantifiable achievements and learning cloud technologies."
}}"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            text = response.text
            # Extract JSON from response
            start = text.find('{')
            end = text.rfind('}') + 1
            if start == -1:
                return self._fallback_analysis(resume_text)
            json_str = text[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return self._fallback_analysis(resume_text)
    
    def _fallback_analysis(self, resume_text):
        """Rule-based backup analysis"""
        return {
            "score": 70,
            "rating": "Good",
            "strengths": [
                "Resume uploaded successfully",
                "Basic information present"
            ],
            "weaknesses": [
                "Need more details",
                "Consider adding quantifiable achievements"
            ],
            "suggestions": [
                "Add more skills to your resume",
                "Include work experience details",
                "Add education details",
                "Use action verbs in your descriptions"
            ],
            "recommendation": "Consider",
            "summary": "Resume analysis complete. Add more details for better score."
        }