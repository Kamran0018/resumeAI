# ai_services/matcher.py
"""
Resume–Job Matcher using dual AI (Gemini + Grok) with Fusion Engine.
"""
from .gemini_service import GeminiService
from .grok_service   import GrokService
from .fusion_service import FusionEngine


class ResumeJobMatcher:
    """Matches resumes to jobs using Gemini + Grok fusion."""

    def __init__(self):
        self.gemini  = GeminiService()
        self.grok    = GrokService()
        self.fusion  = FusionEngine()

    # ──────────────────────────────────────────
    # Single resume → single job
    # ──────────────────────────────────────────

    def match(self, resume, job) -> dict:
        """
        Full dual-AI match of a Resume object against a Job object.
        Returns a fused match report.
        """
        resume_text = resume.get_resume_text() if hasattr(resume, 'get_resume_text') else self._text_from_resume(resume)

        # Gemini: semantic / quality match (re-use existing rule-based as proxy)
        gemini_match = self._gemini_match(resume, job, resume_text)

        # Grok: technical match
        grok_match = self.grok.match_resume_to_jd(resume_text, job)

        # Fusion
        fused = self.fusion.fuse_match(gemini_match, grok_match)
        fused['gemini_match'] = gemini_match
        fused['grok_match'] = grok_match

        return fused

    # Alias used by existing jobs/views.py
    def match_resume_to_job(self, resume, job) -> dict:
        return self.match(resume, job)

    # ──────────────────────────────────────────
    # Rank multiple candidates for a job
    # ──────────────────────────────────────────

    def rank_candidates(self, job, applications) -> list:
        """
        Rank all applicants for a job using fusion scores.
        Returns sorted list of dicts with application + scores.
        """
        ranked = []

        for app in applications:
            if not app.resume:
                continue

            try:
                fused = self.match(app.resume, job)
                overall_score = fused.get('overall_score', 0)

                # Grok hiring decision
                resume_text = app.resume.get_resume_text() if hasattr(app.resume, 'get_resume_text') else ''
                grok_rank   = self.grok.rank_candidate(resume_text, job, overall_score)

                ranked.append({
                    'application'       : app,
                    'score'             : overall_score,
                    'hire_probability'  : grok_rank.get('hire_probability', overall_score),
                    'recommendation'    : grok_rank.get('hire_recommendation', fused.get('recommendation', 'Consider')),
                    'matched_skills'    : fused.get('matched_skills', []),
                    'missing_skills'    : fused.get('missing_skills', []),
                    'skill_match'       : fused.get('skill_match', 0),
                    'experience_match'  : fused.get('experience_match', 0),
                    'interview_questions': grok_rank.get('interview_questions', []),
                    'rank_tier'         : grok_rank.get('rank_tier', 'Tier 3'),
                    'key_concerns'      : grok_rank.get('key_concerns', []),
                })
            except Exception as e:
                print(f"[Matcher] Error ranking application {app.id}: {e}")

        ranked.sort(key=lambda x: x['score'], reverse=True)
        for i, item in enumerate(ranked, 1):
            item['rank'] = i

        return ranked

    # ──────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────

    def _text_from_resume(self, resume) -> str:
        """Fallback text reconstruction for older Resume objects."""
        parts = list(resume.skills or [])
        for exp in (resume.experience or []):
            if isinstance(exp, dict):
                parts.append(f"{exp.get('role','')} {exp.get('company','')}")
        for edu in (resume.education or []):
            if isinstance(edu, dict):
                parts.append(f"{edu.get('degree','')} {edu.get('institution','')}")
        return ' '.join(parts)

    def _gemini_match(self, resume, job, resume_text: str) -> dict:
        """
        Rule-based proxy for Gemini semantic matching.
        (Gemini resume match prompt would require extra API credits;
        using skill overlap as a lightweight semantic proxy.)
        """
        resume_skills = [s.lower() for s in (resume.skills or [])]
        job_skills    = [s.lower() for s in job.get_required_skills_list()]

        if job_skills:
            matched = [s for s in job_skills if s in resume_skills]
            score   = round((len(matched) / len(job_skills)) * 100, 1)
        else:
            matched, score = [], 50.0

        missing = [s for s in job_skills if s not in resume_skills]

        return {
            'overall_score'   : score,
            'skill_match'     : score,
            'experience_match': 50,
            'semantic_match'  : score * 0.9,
            'matched_skills'  : [s for s in job_skills if s in resume_skills],
            'missing_skills'  : missing,
        }