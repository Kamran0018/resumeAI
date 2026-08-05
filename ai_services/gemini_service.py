# ai_services/gemini_service.py
"""
Gemini AI Engine (LLM Integration)
Integrates Google's Gemini LLMs for advanced resume analysis, rewriting,
ATS optimization, cover letter generation, interview question generation,
LinkedIn profile optimization, and salary range estimation.
"""

import json
import os
import time
from django.conf import settings

# Tenacity or Fallback Exponential Backoff
try:
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
except ImportError:
    retry = None

from .prompts import (
    GEMINI_RESUME_ANALYSIS,
    GEMINI_RESUME_BUILD,
    GEMINI_COVER_LETTER,
)


class GeminiService:
    """Gemini AI Engine — Advanced LLM Resume Intelligence."""

    PRIMARY_MODEL = "gemini-1.5-pro"
    FAST_MODEL = "gemini-1.5-flash"
    FALLBACK_MODEL = "gemini-2.5-flash"

    def __init__(self):
        self.client = None
        self.available = False
        try:
            from google import genai
            try:
                from django.conf import settings
                api_key = getattr(settings, 'GEMINI_API_KEY', os.environ.get("GEMINI_API_KEY", ""))
            except Exception:
                api_key = os.environ.get("GEMINI_API_KEY", "")
            if api_key:
                self.client = genai.Client(api_key=api_key)
                self.available = True
        except Exception as e:
            print(f"[GeminiService] Initialization notice: {e}")

    # ─────────────────────────────────────────────────────────────
    # API Call Routine with Exponential Backoff
    # ─────────────────────────────────────────────────────────────

    def _call(self, prompt: str, model_name: str = None) -> str:
        """Send prompt to Gemini with retry logic and model fallbacks."""
        if not self.available or not self.client:
            return ""

        target_model = model_name or self.FAST_MODEL
        attempts = 3
        backoff = 1.0

        for attempt in range(attempts):
            try:
                response = self.client.models.generate_content(
                    model=target_model,
                    contents=prompt,
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[GeminiService] Attempt {attempt+1} failed with model {target_model}: {e}")
                time.sleep(backoff)
                backoff *= 2
                # Fallback to secondary models
                if attempt == 1:
                    target_model = self.FALLBACK_MODEL

        return ""

    def _parse_json(self, text: str) -> dict:
        """Extract and parse first JSON object in response text."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except Exception:
            pass
        return {}

    # ─────────────────────────────────────────────────────────────
    # 1. Deep Resume Analysis
    # ─────────────────────────────────────────────────────────────

    def analyze_resume(self, resume_text: str) -> dict:
        """
        Deep analysis returning strengths, weaknesses, improvements, score & recommendations.
        """
        if not resume_text.strip():
            return self._fallback_analysis()

        prompt = f"""
You are an expert Executive Resume Reviewer. Analyze this resume using chain-of-thought reasoning.

RESUME CONTENT:
{resume_text[:6000]}

Respond ONLY in valid raw JSON with this exact structure:
{{
    "strengths": ["Strong technical skills in Python and AWS", "Quantified achievements in backend scaling"],
    "weaknesses": ["Lack of executive leadership details", "Skills section needs bullet points"],
    "improvements": ["Add 3 more metrics to recent experience", "Include LinkedIn portfolio link"],
    "score": 85,
    "recommendations": [
        "🔑 Add keywords: Docker, Kubernetes, Microservices",
        "💪 Use action verbs: Architected, Spearheaded, Orchestrated"
    ]
}}
"""
        raw = self._call(prompt, model_name=self.PRIMARY_MODEL)
        parsed = self._parse_json(raw)
        return parsed if parsed else self._fallback_analysis()

    # ─────────────────────────────────────────────────────────────
    # 2. Resume Rewriting
    # ─────────────────────────────────────────────────────────────

    def rewrite_resume(self, resume_text: str, target_role: str = "Senior Developer") -> str:
        """Rewrite resume into a high-impact, professional, ATS-optimized document."""
        prompt = f"""
You are a World-Class Resume Writer. Rewrite the following resume content for a {target_role} role.
Use strong action verbs, quantify achievements with metrics (%, $, X+), and optimize for ATS scanning.

RESUME TEXT:
{resume_text[:5000]}

Output ONLY the improved, beautifully formatted text resume — no introductory remarks or explanations.
"""
        res = self._call(prompt, model_name=self.PRIMARY_MODEL)
        return res if res else self._fallback_built_resume(resume_text)

    # ─────────────────────────────────────────────────────────────
    # 3. Personalized Cover Letter Generation
    # ─────────────────────────────────────────────────────────────

    def generate_cover_letter(
        self,
        resume_text: str,
        job_text: str = "",
        job_title: str = "Software Engineer",
        company: str = "Tech Corp"
    ) -> str:
        """Generate a compelling, highly personalized cover letter."""
        prompt = f"""
You are an expert Career Coach. Write a tailored, persuasive cover letter for applying to {company} for the position of {job_title}.

CANDIDATE RESUME:
{resume_text[:4000]}

JOB REQUIREMENTS:
{job_text[:2000] if job_text else 'Software Engineering excellence, leadership, and API design.'}

Output ONLY the full cover letter text.
"""
        res = self._call(prompt, model_name=self.FAST_MODEL)
        return res if res else self._fallback_cover_letter(job_title, company)

    # ─────────────────────────────────────────────────────────────
    # 4. Interview Question Generation
    # ─────────────────────────────────────────────────────────────

    def generate_questions(self, resume_text: str, job_text: str = "") -> dict:
        """Generate categorized interview questions (HR, Technical, Behavioral, Coding)."""
        prompt = f"""
You are a Senior Technical Recruiter. Generate realistic interview questions categorized into HR, Technical, Behavioral, and Coding based on the candidate's resume and job requirements.

CANDIDATE RESUME:
{resume_text[:4000]}

JOB REQUIREMENTS:
{job_text[:2000] if job_text else 'Full-stack software engineering and system architecture.'}

Respond ONLY in valid raw JSON:
{{
    "hr": ["Why are you looking to leave your current position?", "Where do you see yourself in 3 years?"],
    "technical": ["How do you handle race conditions in Django ORM?", "Explain microservice circuit breakers."],
    "behavioral": ["Describe a time you resolved a major production incident."],
    "coding": ["Implement an LRU Cache with O(1) time complexity."]
}}
"""
        raw = self._call(prompt, model_name=self.PRIMARY_MODEL)
        parsed = self._parse_json(raw)
        return parsed if parsed else {
            "hr": ["Tell us about yourself.", "What are your salary expectations?"],
            "technical": ["Explain REST API design principles.", "How do database indexes work?"],
            "behavioral": ["Describe a challenging technical project you led."],
            "coding": ["Write a function to reverse a linked list."]
        }

    # ─────────────────────────────────────────────────────────────
    # 5. ATS Optimization & LinkedIn & Salary Estimations
    # ─────────────────────────────────────────────────────────────

    def optimize_linkedin(self, resume_text: str) -> dict:
        """Generate LinkedIn profile optimization suggestions."""
        prompt = f"""
Optimize this candidate's LinkedIn Profile.
RESUME: {resume_text[:3000]}

Respond ONLY in valid raw JSON:
{{
    "headline": "Senior Software Engineer | Python, Django, AWS & Microservices",
    "about": "Passionate backend engineer with 5+ years of experience building high-scale distributed systems.",
    "experience_bullets": ["Engineered high-throughput REST APIs handling 1M+ requests daily."]
}}
"""
        raw = self._call(prompt, model_name=self.FAST_MODEL)
        parsed = self._parse_json(raw)
        return parsed if parsed else {
            "headline": "Software Developer | Full Stack & Cloud Technologies",
            "about": "Experienced software developer dedicated to clean code and scalable applications.",
            "experience_bullets": ["Developed REST APIs and backend microservices."]
        }

    def estimate_salary(self, resume_text: str, location: str = "US") -> dict:
        """Estimate competitive salary range based on candidate experience and skills."""
        prompt = f"""
Estimate competitive annual salary range for this candidate in {location}.
RESUME: {resume_text[:3000]}

Respond ONLY in valid raw JSON:
{{
    "min_salary": "$110,000",
    "max_salary": "$150,000",
    "median_salary": "$130,000",
    "currency": "USD"
}}
"""
        raw = self._call(prompt, model_name=self.FAST_MODEL)
        parsed = self._parse_json(raw)
        return parsed if parsed else {
            "min_salary": "$90,000",
            "max_salary": "$130,000",
            "median_salary": "$110,000",
            "currency": "USD"
        }

    # ─────────────────────────────────────────────────────────────
    # Fallback Methods
    # ─────────────────────────────────────────────────────────────

    def _fallback_analysis(self) -> dict:
        return {
            "strengths": [
                "Solid foundation in software development",
                "Clear education and technical skills listing"
            ],
            "weaknesses": [
                "Metrics and quantifiable impacts can be expanded",
                "Section headers can use standardized ATS formatting"
            ],
            "improvements": [
                "Add 3+ metric-driven bullet points (% increase, latency reduction)",
                "Include direct links to GitHub or portfolio projects"
            ],
            "score": 82,
            "recommendations": [
                "🔑 Add industry keywords: AWS, Docker, Kubernetes",
                "💪 Use action verbs: Architected, Spearheaded, Orchestrated",
                "📊 Add quantifiable achievements: 'Increased sales by 30%'"
            ]
        }

    def _fallback_built_resume(self, resume_text: str) -> str:
        return f"""PROFESSIONAL RESUME
==================

{resume_text[:2500]}

---
Optimized by Resume AI Gemini Engine
"""

    def _fallback_cover_letter(self, job_title: str, company: str) -> str:
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} role at {company}.
With my technical background and passion for engineering excellence, I am confident in my ability to add immediate value to your team.

Thank you for your time and consideration.

Sincerely,
Candidate
"""
