# ai_services/skill_matcher.py
"""
Skill Matching Engine (RapidFuzz + Synonym Normalization + Fuzzy Matching)
Handles variations in skill representation ("React" vs "ReactJS", "ML" vs "Machine Learning"),
skill level detection, missing skill discovery, fuzzy match scoring, and skill coverage guidance.
"""

import re
import numpy as np

# RapidFuzz / Levenshtein & difflib fallback
try:
    from rapidfuzz import fuzz, process
except ImportError:
    fuzz = None
    process = None

import difflib


class SkillMatcher:
    """Production-grade Skill Matching Engine."""

    # ─────────────────────────────────────────────────────────────
    # Synonym Database
    # ─────────────────────────────────────────────────────────────
    SYNONYMS = {
        "react": ["reactjs", "react.js", "react js"],
        "node.js": ["nodejs", "node js", "node"],
        "vue.js": ["vuejs", "vue js", "vue"],
        "next.js": ["nextjs", "next js"],
        "express.js": ["expressjs", "express js", "express"],
        "python": ["python3", "py"],
        "postgresql": ["postgres", "postgresql", "pgsql"],
        "mongodb": ["mongo", "mongodb"],
        "kubernetes": ["k8s", "k8"],
        "amazon web services": ["aws"],
        "google cloud platform": ["gcp"],
        "machine learning": ["ml"],
        "artificial intelligence": ["ai"],
        "deep learning": ["dl"],
        "natural language processing": ["nlp"],
        "ci/cd": ["cicd", "continuous integration"],
        "rest api": ["restful api", "rest", "restful apis"],
    }

    SKILL_CATEGORIES = {
        "technical": [
            "python", "react", "django", "sql", "aws", "docker", "kubernetes",
            "java", "javascript", "typescript", "node.js", "mongodb", "postgresql",
            "c++", "c#", "go", "ruby", "php", "html", "css", "git", "linux"
        ],
        "soft": [
            "leadership", "communication", "problem solving", "teamwork",
            "time management", "critical thinking", "agile", "scrum"
        ],
        "domain": [
            "fintech", "e-commerce", "healthcare", "cybersecurity", "saas",
            "data engineering", "devops", "cloud infrastructure"
        ]
    }

    def __init__(self, fuzzy_threshold: float = 85.0):
        self.fuzzy_threshold = fuzzy_threshold
        self._reverse_synonyms = {}
        for canonical, syn_list in self.SYNONYMS.items():
            self._reverse_synonyms[canonical] = canonical
            for syn in syn_list:
                self._reverse_synonyms[syn] = canonical

    # ─────────────────────────────────────────────────────────────
    # Public Entry Point
    # ─────────────────────────────────────────────────────────────

    def match(self, candidate_skills: list, job_required_skills: list) -> dict:
        """
        Perform exact, synonym, and fuzzy skill matching.
        """
        if not job_required_skills:
            return self._empty_result(candidate_skills)

        candidate_norm = [self._normalize(s) for s in candidate_skills]
        job_norm = [self._normalize(s) for s in job_required_skills]

        matched_job_skills = []
        missing_job_skills = []
        fuzzy_matches = []

        for original_job_skill in job_required_skills:
            norm_j = self._normalize(original_job_skill)
            canonical_j = self._reverse_synonyms.get(norm_j, norm_j)

            matched_c_skill = None
            highest_sim = 0.0

            for original_c_skill in candidate_skills:
                norm_c = self._normalize(original_c_skill)
                canonical_c = self._reverse_synonyms.get(norm_c, norm_c)

                # 1. Exact or Synonym Match
                if norm_j == norm_c or canonical_j == canonical_c:
                    matched_c_skill = original_c_skill
                    highest_sim = 100.0
                    break

                # 2. Fuzzy Match via RapidFuzz / Levenshtein
                sim = self._calculate_similarity(norm_j, norm_c)
                if sim > highest_sim:
                    highest_sim = sim
                    if sim >= self.fuzzy_threshold:
                        matched_c_skill = original_c_skill

            if matched_c_skill and highest_sim >= self.fuzzy_threshold:
                matched_job_skills.append(original_job_skill)
                fuzzy_matches.append({
                    "skill": original_job_skill,
                    "matched": matched_c_skill,
                    "similarity": round(highest_sim, 1)
                })
            else:
                missing_job_skills.append(original_job_skill)
                fuzzy_matches.append({
                    "skill": original_job_skill,
                    "matched": None,
                    "similarity": round(highest_sim, 1) if highest_sim > 0 else 0
                })

        total_req = len(job_required_skills)
        matched_count = len(matched_job_skills)
        match_pct = round((matched_count / total_req) * 100, 1) if total_req > 0 else 100.0

        coverage_label = self._classify_coverage(match_pct, missing_job_skills)
        recommendation = self._generate_recommendation(missing_job_skills)

        return {
            "candidate_skills": candidate_skills,
            "job_required_skills": job_required_skills,
            "matched_skills": matched_job_skills,
            "missing_skills": missing_job_skills,
            "matched_count": matched_count,
            "total_required": total_req,
            "skill_match_percentage": match_pct,
            "fuzzy_matches": fuzzy_matches,
            "skill_coverage": coverage_label,
            "recommendation": recommendation
        }

    # ─────────────────────────────────────────────────────────────
    # Categorization & Skill Level Detection
    # ─────────────────────────────────────────────────────────────

    def categorize_skill(self, skill: str) -> str:
        """Classify a skill into Technical, Soft, or Domain category."""
        norm = self._normalize(skill)
        for cat, skills in self.SKILL_CATEGORIES.items():
            if any(s in norm for s in skills):
                return cat.title()
        return "Technical"

    def detect_skill_level(self, skill: str, resume_context: str = "") -> str:
        """Detect skill proficiency level (Beginner, Intermediate, Expert)."""
        ctx_lower = resume_context.lower()
        norm = self._normalize(skill)

        if f"expert in {norm}" in ctx_lower or f"senior {norm}" in ctx_lower or f"5+ years {norm}" in ctx_lower:
            return "Expert"
        elif f"intermediate {norm}" in ctx_lower or f"3+ years {norm}" in ctx_lower or f"proficient in {norm}" in ctx_lower:
            return "Intermediate"
        elif f"basic {norm}" in ctx_lower or f"familiar with {norm}" in ctx_lower:
            return "Beginner"
        else:
            return "Intermediate"

    # ─────────────────────────────────────────────────────────────
    # Similarity Calculation Helper
    # ─────────────────────────────────────────────────────────────

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate fuzzy similarity using RapidFuzz or difflib fallback."""
        if fuzz:
            return float(fuzz.token_sort_ratio(str1, str2))
        else:
            return difflib.SequenceMatcher(None, str1, str2).ratio() * 100.0

    def _normalize(self, skill_name: str) -> str:
        clean = re.sub(r"[^\w\s\.-]", "", skill_name.strip().lower())
        return clean.replace(" ", "")

    def _classify_coverage(self, match_pct: float, missing: list) -> str:
        if match_pct >= 90.0:
            return "Excellent - Candidate covers all core required skills"
        elif match_pct >= 70.0:
            missing_str = ", ".join(missing[:2]) if missing else "minor tools"
            return f"Good - Missing {missing_str}"
        elif match_pct >= 50.0:
            return "Moderate - Partial skill match, additional training recommended"
        else:
            return "Low - Significant skill gaps relative to target job"

    def _generate_recommendation(self, missing: list) -> str:
        if not missing:
            return "Great match! Candidate possesses all required technical skills."
        top_missing = ", ".join(missing[:3])
        return f"Learn {top_missing} to improve match percentage."

    def _empty_result(self, candidate_skills: list) -> dict:
        return {
            "candidate_skills": candidate_skills,
            "job_required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "matched_count": 0,
            "total_required": 0,
            "skill_match_percentage": 100.0,
            "fuzzy_matches": [],
            "skill_coverage": "No skills required by job posting",
            "recommendation": "Ready to apply."
        }
