# ai_services/ats_engine.py
"""
Hybrid + ML ATS (Applicant Tracking System) Scoring Engine.
Calculates weighted ATS compatibility score (0-100%) across 8 parameters,
with industry keyword databases, role weights, location adjustments & custom recommendations.
"""

import re
import math


class ATSEngine:
    """State-of-the-Art Hybrid ATS Scoring Engine."""

    # ─────────────────────────────────────────────────────────────
    # Default Scoring Parameter Weights (Total = 100%)
    # ─────────────────────────────────────────────────────────────
    DEFAULT_WEIGHTS = {
        "keyword_score": 0.25,       # 25% Keyword Optimization
        "action_verb_score": 0.15,   # 15% Action Verbs
        "quantifier_score": 0.15,    # 15% Quantifiable Achievements
        "formatting_score": 0.10,    # 10% Formatting Quality
        "length_score": 0.10,        # 10% Resume Length (250-800 words)
        "education_score": 0.10,     # 10% Education Relevance
        "experience_score": 0.10,    # 10% Experience Relevance
        "project_score": 0.05,       # 5%  Project & Links Portfolio
    }

    # ─────────────────────────────────────────────────────────────
    # Taxonomies & Keywords
    # ─────────────────────────────────────────────────────────────
    ACTION_VERBS = [
        "led", "managed", "developed", "architected", "engineered", "built", "designed",
        "implemented", "spearheaded", "orchestrated", "automated", "optimized", "scaled",
        "improved", "delivered", "deployed", "launched", "streamlined", "increased",
        "reduced", "mentored", "created", "integrated", "analyzed", "formulated"
    ]

    INDUSTRY_KEYWORDS = {
        "software": [
            "python", "django", "react", "aws", "docker", "kubernetes", "sql", "git",
            "microservices", "rest api", "ci/cd", "node.js", "graphql", "typescript",
            "postgresql", "redis", "linux", "cloud", "agile", "scrum", "unit testing"
        ],
        "data_science": [
            "python", "machine learning", "deep learning", "pytorch", "tensorflow",
            "pandas", "numpy", "scikit-learn", "sql", "spark", "nlp", "transformers",
            "data visualization", "a/b testing", "statistics", "feature engineering"
        ],
        "product_management": [
            "product strategy", "roadmap", "user research", "agile", "scrum",
            "jira", "kpis", "okrs", "wireframing", "stakeholder management",
            "data analytics", "customer discovery", "growth", "a/b testing"
        ],
        "devops": [
            "aws", "docker", "kubernetes", "terraform", "jenkins", "ansible",
            "github actions", "linux", "bash", "prometheus", "grafana", "ci/cd",
            "cloudformation", "security", "infrastructure as code"
        ]
    }

    ROLE_WEIGHT_MODIFIERS = {
        "software": {"keyword_score": 0.30, "project_score": 0.10, "education_score": 0.05},
        "management": {"action_verb_score": 0.20, "experience_score": 0.15, "project_score": 0.05},
        "entry_level": {"education_score": 0.20, "project_score": 0.15, "experience_score": 0.05}
    }

    def score(
        self,
        resume_text: str,
        job_description: str = "",
        role_type: str = "software",
        company_preset: str = "standard",
        location: str = "global"
    ) -> dict:
        """
        Calculate comprehensive ATS score and breakdown for a resume.
        """
        if not resume_text or not resume_text.strip():
            return self._empty_result()

        # 1. Parameter Calculations
        kw_score, missing_kw = self._calc_keyword_score(resume_text, job_description, role_type)
        verb_score, missing_verbs = self._calc_action_verb_score(resume_text)
        quant_score, quant_examples = self._calc_quantifier_score(resume_text)
        fmt_score, fmt_tips = self._calc_formatting_score(resume_text)
        len_score, word_count = self._calc_length_score(resume_text)
        edu_score = self._calc_education_score(resume_text)
        exp_score = self._calc_experience_score(resume_text)
        proj_score = self._calc_project_score(resume_text)

        breakdown = {
            "keyword_score": round(kw_score, 1),
            "action_verb_score": round(verb_score, 1),
            "quantifier_score": round(quant_score, 1),
            "formatting_score": round(fmt_score, 1),
            "length_score": round(len_score, 1),
            "education_score": round(edu_score, 1),
            "experience_score": round(exp_score, 1),
            "project_score": round(proj_score, 1),
        }

        # 2. Apply Custom Role & Company Weights
        weights = self._get_adjusted_weights(role_type, company_preset)
        raw_ats = sum(breakdown[param] * weight for param, weight in weights.items())

        # 3. Location Modifier
        location_adj = self._get_location_adjustment(location, resume_text)
        final_ats = round(min(100.0, max(0.0, raw_ats + location_adj)), 1)

        # 4. Generate Recommendations & Urgency
        recommendations = self._generate_recommendations(
            breakdown, missing_kw, missing_verbs, quant_examples, fmt_tips, word_count
        )
        compatibility_label = self._classify_compatibility(final_ats)
        urgency = self._classify_urgency(final_ats)

        return {
            "ats_score": final_ats,
            "breakdown": breakdown,
            "recommendations": recommendations,
            "ats_compatibility": f"{compatibility_label} - {final_ats}% ATS Friendly",
            "improvement_urgency": urgency
        }

    # ─────────────────────────────────────────────────────────────
    # Parameter Calculation Methods
    # ─────────────────────────────────────────────────────────────

    def _calc_keyword_score(self, text: str, job_description: str, role_type: str) -> tuple:
        text_lower = text.lower()
        target_keywords = set()

        if job_description and len(job_description.strip()) > 30:
            words = re.findall(r"\b[a-zA-Z]{3,}\b", job_description.lower())
            stop_words = {"with", "from", "that", "this", "have", "your", "will", "team", "work", "must", "they"}
            target_keywords = {w for w in words if w not in stop_words and len(w) > 3}
        else:
            domain_kws = self.INDUSTRY_KEYWORDS.get(role_type, self.INDUSTRY_KEYWORDS["software"])
            target_keywords = set(domain_kws)

        if not target_keywords:
            return 80.0, []

        found = [kw for kw in target_keywords if kw in text_lower]
        missing = list(target_keywords - set(found))[:5]
        score = min(100.0, (len(found) / len(target_keywords)) * 100 * 1.3)
        return round(score, 1), missing

    def _calc_action_verb_score(self, text: str) -> tuple:
        text_lower = text.lower()
        found_verbs = [v for v in self.ACTION_VERBS if re.search(r"\b" + v + r"\b", text_lower)]
        ratio = len(found_verbs) / 10.0  # benchmark: 10 distinct action verbs
        score = min(100.0, ratio * 100)

        missing = [v.title() for v in self.ACTION_VERBS if v not in text_lower][:4]
        return round(score, 1), missing

    def _calc_quantifier_score(self, text: str) -> tuple:
        # Check for numbers with %, $, k+, X+, 2x, etc.
        metric_matches = re.findall(r"\b(?:\d+%\b|\$\d+|\d+\+|\d+x|\d+\s*(?:k|million|users|clients|requests))\b", text, re.IGNORECASE)
        count = len(metric_matches)
        score = min(100.0, count * 20.0)  # 5 metrics = 100%
        return round(score, 1), metric_matches[:3]

    def _calc_formatting_score(self, text: str) -> tuple:
        score = 60.0
        tips = []

        # Bullet points
        bullets = len(re.findall(r"^[•\-\*\s]+", text, re.MULTILINE))
        if bullets >= 5:
            score += 20
        else:
            tips.append("📄 Improve formatting: Use bullet points for skills and experience section")

        # Clear section headers
        headers = ["experience", "education", "skills", "projects", "summary"]
        found_headers = sum(1 for h in headers if h in text.lower())
        score += min(20, found_headers * 4)

        return min(100.0, score), tips

    def _calc_length_score(self, text: str) -> tuple:
        words = len(re.findall(r"\b\w+\b", text))
        if 350 <= words <= 750:
            score = 100.0
        elif 250 <= words < 350 or 750 < words <= 1000:
            score = 80.0
        elif 150 <= words < 250 or 1000 < words <= 1500:
            score = 60.0
        else:
            score = 40.0
        return score, words

    def _calc_education_score(self, text: str) -> float:
        text_lower = text.lower()
        degree_keywords = ["b.tech", "bachelor", "master", "m.tech", "phd", "b.s.", "m.s.", "bca", "mca", "degree"]
        found = sum(1 for d in degree_keywords if d in text_lower)
        if found >= 2:
            return 100.0
        elif found == 1:
            return 85.0
        else:
            return 50.0

    def _calc_experience_score(self, text: str) -> float:
        year_matches = re.findall(r"\b(19|20)\d{2}\b", text)
        if len(year_matches) >= 4:
            return 100.0
        elif len(year_matches) >= 2:
            return 80.0
        elif "experience" in text.lower():
            return 70.0
        else:
            return 50.0

    def _calc_project_score(self, text: str) -> float:
        text_lower = text.lower()
        score = 40.0

        if "github.com" in text_lower or "linkedin.com" in text_lower or "http" in text_lower:
            score += 30
        if "project" in text_lower or "portfolio" in text_lower:
            score += 30

        return min(100.0, score)

    # ─────────────────────────────────────────────────────────────
    # Helpers & Adjustments
    # ─────────────────────────────────────────────────────────────

    def _get_adjusted_weights(self, role_type: str, company_preset: str) -> dict:
        weights = dict(self.DEFAULT_WEIGHTS)
        if role_type in self.ROLE_WEIGHT_MODIFIERS:
            for k, v in self.ROLE_WEIGHT_MODIFIERS[role_type].items():
                weights[k] = v
        # Normalize sum to 1.0
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}

    def _get_location_adjustment(self, location: str, text: str) -> float:
        loc = location.lower()
        if "us" in loc or "usa" in loc:
            # US ATS favors metrics and action verbs
            return 2.0 if "%" in text or "$" in text else -2.0
        return 0.0

    def _generate_recommendations(
        self, breakdown: dict, missing_kw: list, missing_verbs: list, quant_examples: list, fmt_tips: list, word_count: int
    ) -> list:
        recs = []

        if breakdown["keyword_score"] < 75 and missing_kw:
            recs.append(f"🔑 Add more industry keywords: {', '.join(missing_kw[:4]).upper()}")

        if breakdown["action_verb_score"] < 75 and missing_verbs:
            recs.append(f"💪 Use more action verbs: {', '.join(missing_verbs[:4])}")

        if breakdown["quantifier_score"] < 70:
            recs.append("📊 Add quantifiable achievements: 'Increased sales by 30%', 'Reduced latency by 40%'")

        if fmt_tips:
            recs.extend(fmt_tips)

        if word_count < 300:
            recs.append(f"📄 Expand resume details (current: {word_count} words, optimal: 350-750 words)")

        if not recs:
            recs.append("✨ Resume layout and keyword optimization look strong for ATS screening!")

        return recs

    def _classify_compatibility(self, score: float) -> str:
        if score >= 85.0:
            return "Excellent"
        elif score >= 70.0:
            return "Good"
        elif score >= 55.0:
            return "Moderate"
        else:
            return "Needs Improvement"

    def _classify_urgency(self, score: float) -> str:
        if score >= 80.0:
            return "Low"
        elif score >= 65.0:
            return "Medium"
        else:
            return "High"

    def _empty_result(self) -> dict:
        return {
            "ats_score": 0.0,
            "breakdown": {p: 0.0 for p in self.DEFAULT_WEIGHTS},
            "recommendations": ["Upload a non-empty resume document."],
            "ats_compatibility": "Needs Improvement - 0.0% ATS Friendly",
            "improvement_urgency": "High"
        }
