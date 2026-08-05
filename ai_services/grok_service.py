# ai_services/grok_service.py
"""
Grok Recruiter Assistant — handles technical analysis, JD matching,
candidate ranking, and interview question generation.

Uses xAI's OpenAI-compatible API via urllib (no extra package needed).
Endpoint: https://api.x.ai/v1/chat/completions
Model:    grok-beta
"""
import json
import os
import urllib.request
import urllib.error
from django.conf import settings
from .prompts import (
    GROK_TECHNICAL_ANALYSIS,
    GROK_JD_MATCH,
    GROK_RANK_CANDIDATE,
)


class GrokService:
    """Grok AI — Recruiter Assistant"""

    API_URL = 'https://api.x.ai/v1/chat/completions'
    MODEL   = 'grok-beta'

    def __init__(self):
        try:
            from django.conf import settings
            self.api_key = getattr(settings, 'GROK_API_KEY', os.environ.get("GROK_API_KEY", "")).strip()
        except Exception:
            self.api_key = os.environ.get("GROK_API_KEY", "").strip()

        self.available = bool(self.api_key and self.api_key != 'your-grok-api-key-here')
        self.client = None

        if self.available and OpenAI:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.x.ai/v1"
                )
            except Exception as e:
                print(f"[GrokService] OpenAI client init notice: {e}")

    # ──────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────

    def _call(self, prompt: str) -> str:
        """POST a chat completion request to xAI's Grok API."""
        if not self.available:
            return ''
        payload = json.dumps({
            'model': self.MODEL,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.3,
        }).encode('utf-8')

        req = urllib.request.Request(
            self.API_URL,
            data=payload,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            print(f"[GrokService] HTTP {e.code}: {e.reason}")
            return ''
        except Exception as e:
            print(f"[GrokService] Error: {e}")
            return ''

    def _parse_json(self, text: str) -> dict:
        try:
            start = text.find('{')
            end   = text.rfind('}') + 1
            if start == -1:
                return {}
            return json.loads(text[start:end])
        except Exception:
            return {}

    # ──────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────

    def analyze_technical(self, resume_text: str) -> dict:
        """
        Deep technical analysis of a resume.
        Returns: technical_score, trending gaps, hire_probability, interview_topics.
        """
        if not resume_text.strip():
            return self._fallback_technical()

        prompt = GROK_TECHNICAL_ANALYSIS.format(resume_text=resume_text[:6000])
        raw    = self._call(prompt)
        result = self._parse_json(raw)
        return result if result else self._fallback_technical()

    def match_resume_to_jd(self, resume_text: str, job) -> dict:
        """
        Match resume against a Job object.
        Returns: scores, matched/missing skills, hire_probability, interview_questions.
        """
        prompt = GROK_JD_MATCH.format(
            job_title       = job.title,
            company         = job.company,
            required_skills = job.required_skills,
            experience_level= job.get_experience_level_display(),
            jd_text         = f"{job.description}\n{job.requirements}"[:4000],
            resume_text     = resume_text[:4000],
        )
        raw    = self._call(prompt)
        result = self._parse_json(raw)
        return result if result else self._fallback_match()

    def rank_candidate(self, resume_text: str, job, match_score: float) -> dict:
        """
        Produce a hiring decision with interview questions.
        Returns: hire_recommendation, hire_probability, interview_questions.
        """
        prompt = GROK_RANK_CANDIDATE.format(
            job_title   = job.title,
            company     = job.company,
            resume_text = resume_text[:4000],
            match_score = round(match_score, 1),
        )
        raw    = self._call(prompt)
        result = self._parse_json(raw)
        return result if result else self._fallback_rank(match_score)

    def suggest_technologies(self, draft_text: str, target_role: str) -> dict:
        """
        Review a drafted resume and suggest modern technologies/rewrites.
        """
        from .prompts import GROK_RESUME_REVIEW_SUGGESTION
        prompt = GROK_RESUME_REVIEW_SUGGESTION.format(
            draft_text=draft_text[:5000],
            target_role=target_role or 'Software Developer'
        )
        raw    = self._call(prompt)
        result = self._parse_json(raw)
        return result if result else {
            'suggested_technologies': ['Docker', 'AWS', 'Pytest'],
            'rewriting_suggestions': ['Add more quantifiable achievements under experience.'],
            'summary': 'General fallback suggestions.'
        }

    # ──────────────────────────────────────────
    # Fallbacks
    # ──────────────────────────────────────────

    def _fallback_technical(self) -> dict:
        return {
            'technical_score'           : 65,
            'skills_depth'              : 'Mid-level',
            'trending_skills_present'   : [],
            'trending_skills_missing'   : ['Docker', 'Kubernetes', 'AWS'],
            'experience_gap'            : 'Unable to assess — add more experience details',
            'industry_alignment'        : 'General Software Development',
            'hire_probability'          : 60,
            'technical_strengths'       : ['Core programming skills present'],
            'technical_weaknesses'      : ['Cloud/DevOps skills missing'],
            'recommended_certifications': ['AWS Cloud Practitioner'],
            'interview_topics'          : ['Data structures', 'System design', 'APIs'],
            'summary'                   : 'Technical analysis requires Grok API key.',
        }

    def _fallback_match(self) -> dict:
        return {
            'overall_score'     : 50,
            'skill_match'       : 50,
            'experience_match'  : 50,
            'semantic_match'    : 50,
            'keyword_match'     : 50,
            'education_match'   : 50,
            'matched_skills'    : [],
            'missing_skills'    : [],
            'hire_probability'  : 50,
            'recommendation'    : 'Consider',
            'recruiter_notes'   : 'Detailed analysis requires Grok API key.',
            'interview_questions': [
                'Tell me about your most challenging project.',
                'How do you approach problem-solving?',
                'Where do you see yourself in 5 years?',
            ],
            'risk_factors'      : [],
            'salary_fit'        : 'Unknown',
            'summary'           : 'Basic match. Configure GROK_API_KEY for detailed analysis.',
        }

    def _fallback_rank(self, match_score: float) -> dict:
        tier = 'Tier 1' if match_score >= 80 else ('Tier 2' if match_score >= 60 else 'Tier 3')
        return {
            'hire_recommendation'          : 'Recommended' if match_score >= 70 else 'Consider',
            'hire_probability'             : match_score,
            'rank_tier'                    : tier,
            'interview_stage_recommendation': 'Phone Screen',
            'key_strengths'                : ['Candidate profile reviewed'],
            'key_concerns'                 : ['Detailed analysis requires Grok API key'],
            'interview_questions'          : [
                'Walk me through your background.',
                'What interests you about this role?',
                'Describe a challenging technical problem you solved.',
            ],
            'expected_onboarding_time'     : '2-4 weeks',
            'summary'                      : f'Score: {match_score}%. Configure GROK_API_KEY for full analysis.',
        }
