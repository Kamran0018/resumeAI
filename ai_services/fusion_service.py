# ai_services/fusion_service.py
"""
AI Fusion Engine — merges Gemini and Grok outputs into a single authoritative report.

Workflow:
    Gemini Output + Grok Output
        → Normalize scores
        → Deduplicate skills/suggestions
        → Weighted average
        → FusionReport dict
"""


def _avg(a, b, w_a=0.5, w_b=0.5):
    """Weighted average of two numeric values."""
    try:
        return round(w_a * float(a) + w_b * float(b), 1)
    except (TypeError, ValueError):
        return round(float(a or b or 0), 1)


def _merge_list(list_a, list_b):
    """Merge two lists, remove duplicates, preserve order."""
    seen  = set()
    merged = []
    for item in list(list_a or []) + list(list_b or []):
        key = str(item).lower().strip()
        if key and key not in seen:
            seen.add(key)
            merged.append(item)
    return merged


class FusionEngine:
    """Merges Gemini (Resume Coach) and Grok (Recruiter Asst) outputs."""

    # ──────────────────────────────────────────
    # Resume Analysis Fusion
    # ──────────────────────────────────────────

    def fuse_resume_analysis(self, gemini: dict, grok: dict) -> dict:
        """
        Combine Gemini resume analysis + Grok technical analysis into one report.

        Args:
            gemini: Output of GeminiService.analyze_resume()
            grok:   Output of GrokService.analyze_technical()

        Returns:
            FusionReport dict
        """
        # Scores — Gemini weighted 60% for resume quality, Grok 40% for technical
        resume_score    = _avg(gemini.get('score', 0),          grok.get('technical_score', 0), 0.6, 0.4)
        grammar_score   = float(gemini.get('grammar_score', 0))
        ats_score       = float(gemini.get('ats_score', 0))
        technical_score = float(grok.get('technical_score', 0))
        hire_prob       = float(grok.get('hire_probability', 0))

        # Merged lists
        strengths  = _merge_list(gemini.get('strengths',  []), grok.get('technical_strengths',  []))
        weaknesses = _merge_list(gemini.get('weaknesses', []), grok.get('technical_weaknesses', []))
        suggestions= _merge_list(gemini.get('suggestions', []), [])
        keywords_missing = _merge_list(
            gemini.get('keywords_missing',  []),
            grok.get('trending_skills_missing', []),
        )
        keywords_found = _merge_list(
            gemini.get('keywords_found', []),
            grok.get('trending_skills_present', []),
        )
        interview_topics = _merge_list([], grok.get('interview_topics', []))
        certifications   = _merge_list([], grok.get('recommended_certifications', []))

        return {
            # Scores
            'resume_score'    : resume_score,
            'grammar_score'   : grammar_score,
            'ats_score'       : ats_score,
            'technical_score' : technical_score,
            'hire_probability': hire_prob,

            # Insights
            'rating'      : gemini.get('rating', 'Good'),
            'strengths'   : strengths[:6],
            'weaknesses'  : weaknesses[:6],
            'suggestions' : suggestions[:8],

            # Skills
            'keywords_found'  : keywords_found,
            'keywords_missing': keywords_missing[:10],

            # Career guidance
            'interview_topics': interview_topics,
            'certifications'  : certifications,
            'industry_alignment': grok.get('industry_alignment', ''),
            'experience_gap'    : grok.get('experience_gap', ''),

            # Summaries
            'gemini_summary'  : gemini.get('summary', ''),
            'grok_summary'    : grok.get('summary', ''),
            'recommendation'  : gemini.get('recommendation', '') or grok.get('summary', ''),

            # Source metadata
            'gemini_score'    : gemini.get('score', 0),
            'grok_score'      : grok.get('technical_score', 0),
            'sources'         : ['gemini', 'grok'] if (gemini and grok) else (['gemini'] if gemini else ['grok']),
        }

    # ──────────────────────────────────────────
    # Job Match Fusion
    # ──────────────────────────────────────────

    def fuse_match(self, gemini_match: dict, grok_match: dict) -> dict:
        """
        Combine Gemini semantic match + Grok technical match.

        Args:
            gemini_match: Output of GeminiService (or existing matcher)
            grok_match:   Output of GrokService.match_resume_to_jd()

        Returns:
            Fused match report
        """
        # Weighted: Grok is the technical expert (60%), Gemini adds semantic (40%)
        overall  = _avg(gemini_match.get('overall_score', 0), grok_match.get('overall_score', 0), 0.4, 0.6)
        skill_m  = _avg(gemini_match.get('skill_match',  0), grok_match.get('skill_match',  0), 0.4, 0.6)
        exp_m    = _avg(gemini_match.get('experience_match', 0), grok_match.get('experience_match', 0))
        sem_m    = float(gemini_match.get('semantic_match', 0) or grok_match.get('semantic_match', 0))
        hire_p   = float(grok_match.get('hire_probability', overall))

        matched  = _merge_list(gemini_match.get('matched_skills', []), grok_match.get('matched_skills', []))
        missing  = _merge_list(gemini_match.get('missing_skills', []), grok_match.get('missing_skills', []))
        questions= _merge_list([], grok_match.get('interview_questions', []))

        # Recommendation label from score
        if overall >= 85:
            rec = 'Highly Recommended'
        elif overall >= 70:
            rec = 'Recommended'
        elif overall >= 55:
            rec = 'Consider'
        else:
            rec = 'Not Recommended'

        return {
            'overall_score'      : overall,
            'skill_match'        : skill_m,
            'experience_match'   : exp_m,
            'semantic_match'     : sem_m,
            'keyword_match'      : grok_match.get('keyword_match', 0),
            'education_match'    : grok_match.get('education_match', 0),
            'matched_skills'     : matched,
            'missing_skills'     : missing[:10],
            'hire_probability'   : hire_p,
            'recommendation'     : rec,
            'interview_questions': questions[:5],
            'risk_factors'       : grok_match.get('risk_factors', []),
            'recruiter_notes'    : grok_match.get('recruiter_notes', ''),
            'salary_fit'         : grok_match.get('salary_fit', ''),
            'summary'            : grok_match.get('summary', ''),
        }
