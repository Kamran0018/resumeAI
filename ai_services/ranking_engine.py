# ai_services/ranking_engine.py
"""
Candidate Ranking Engine (ML-based Multi-Factor Scorer)
Normalizes candidate scores (MinMaxScaler), applies configurable feature weights,
ranks candidates, calculates aggregate metrics (top, avg, median, histogram),
and generates recruiter recommendations.
"""

import numpy as np

# scikit-learn MinMaxScaler fallback
try:
    from sklearn.preprocessing import MinMaxScaler
except ImportError:
    MinMaxScaler = None


class CandidateRankingEngine:
    """State-of-the-Art Multi-Factor Candidate Ranking Engine."""

    DEFAULT_WEIGHTS = {
        "ats_score": 0.25,
        "semantic_score": 0.35,  # Highest priority
        "skill_score": 0.20,
        "experience_score": 0.15,
        "education_score": 0.05
    }

    def __init__(self, custom_weights: dict = None):
        self.weights = dict(self.DEFAULT_WEIGHTS)
        if custom_weights:
            self.weights.update(custom_weights)
        self._normalize_weights()

    def _normalize_weights(self):
        """Ensure weights sum up to 1.0"""
        total = sum(self.weights.values())
        if total > 0:
            self.weights = {k: v / total for k, v in self.weights.items()}

    # ─────────────────────────────────────────────────────────────
    # Public Ranking API
    # ─────────────────────────────────────────────────────────────

    def rank_candidates(self, candidates_data: list, weights_override: dict = None) -> dict:
        """
        Rank a list of candidates based on multi-factor scores.
        Input: list of dicts with 'name', 'email', and 'scores' dict.
        """
        if not candidates_data:
            return self._empty_result()

        active_weights = dict(self.weights)
        if weights_override:
            active_weights.update(weights_override)
            total = sum(active_weights.values())
            if total > 0:
                active_weights = {k: v / total for k, v in active_weights.items()}

        raw_scores_matrix = []
        candidates_meta = []

        for candidate in candidates_data:
            scores_dict = candidate.get("score_breakdown", candidate.get("scores", {}))
            row = [
                float(scores_dict.get("ats_score", 60.0)),
                float(scores_dict.get("semantic_score", 60.0)),
                float(scores_dict.get("skill_score", 60.0)),
                float(scores_dict.get("experience_score", 60.0)),
                float(scores_dict.get("education_score", 60.0)),
            ]
            raw_scores_matrix.append(row)
            candidates_meta.append({
                "name": candidate.get("name", "Candidate"),
                "email": candidate.get("email", ""),
            })

        matrix = np.array(raw_scores_matrix, dtype=np.float32)

        # 1. MinMaxScaler Normalization (0 - 1)
        if len(matrix) > 1 and MinMaxScaler:
            scaler = MinMaxScaler(feature_range=(0, 1))
            normalized_matrix = scaler.fit_transform(matrix)
        else:
            normalized_matrix = matrix / 100.0

        # 2. Weighted Score Calculation
        weight_vec = np.array([
            active_weights["ats_score"],
            active_weights["semantic_score"],
            active_weights["skill_score"],
            active_weights["experience_score"],
            active_weights["education_score"]
        ], dtype=np.float32)

        # Matrix multiplication for weighted normalized score
        weighted_scores = np.dot(matrix, weight_vec)

        # 3. Build Candidates Output
        processed_candidates = []
        overall_scores_list = []

        for i, meta in enumerate(candidates_meta):
            score_val = round(float(weighted_scores[i]), 1)
            overall_scores_list.append(score_val)

            breakdown_dict = {
                "ats_score": round(float(matrix[i][0]), 1),
                "semantic_score": round(float(matrix[i][1]), 1),
                "skill_score": round(float(matrix[i][2]), 1),
                "experience_score": round(float(matrix[i][3]), 1),
                "education_score": round(float(matrix[i][4]), 1),
            }

            recommendation = self._classify_recommendation(score_val)
            summary = self._generate_summary(score_val, breakdown_dict)

            processed_candidates.append({
                "name": meta["name"],
                "email": meta["email"],
                "overall_score": score_val,
                "rank": 0,  # set in next step
                "score_breakdown": breakdown_dict,
                "recommendation": recommendation,
                "summary": summary
            })

        # 4. Sort and Rank Candidates
        processed_candidates.sort(key=lambda x: x["overall_score"], reverse=True)
        for rank_idx, cand in enumerate(processed_candidates, 1):
            cand["rank"] = rank_idx

        # 5. Calculate Aggregate Ranking Metrics
        metrics = self._calculate_ranking_metrics(overall_scores_list, processed_candidates)

        return {
            "candidates": processed_candidates,
            "ranking_metrics": metrics
        }

    # ─────────────────────────────────────────────────────────────
    # Metrics & Summaries
    # ─────────────────────────────────────────────────────────────

    def _calculate_ranking_metrics(self, scores: list, candidates: list) -> dict:
        if not scores:
            return {}

        scores_arr = np.array(scores)
        top_score = round(float(np.max(scores_arr)), 1)
        avg_score = round(float(np.mean(scores_arr)), 1)
        median_score = round(float(np.median(scores_arr)), 1)

        # Histogram Distribution
        dist = {
            "0-20": int(np.sum((scores_arr >= 0) & (scores_arr < 20))),
            "20-40": int(np.sum((scores_arr >= 20) & (scores_arr < 40))),
            "40-60": int(np.sum((scores_arr >= 40) & (scores_arr < 60))),
            "60-80": int(np.sum((scores_arr >= 60) & (scores_arr < 80))),
            "80-100": int(np.sum((scores_arr >= 80) & (scores_arr <= 100))),
        }

        rec_count = sum(1 for c in candidates if c["recommendation"] in ["Highly Recommended", "Recommended"])
        consider_count = sum(1 for c in candidates if c["recommendation"] == "Consider")

        rec_summary = f"🌟 {rec_count} candidates recommended, {consider_count} candidates to consider"

        return {
            "top_score": top_score,
            "average_score": avg_score,
            "median_score": median_score,
            "score_distribution": dist,
            "recommendation_summary": rec_summary
        }

    def _classify_recommendation(self, score: float) -> str:
        if score >= 85.0:
            return "Highly Recommended"
        elif score >= 72.0:
            return "Recommended"
        elif score >= 55.0:
            return "Consider"
        else:
            return "Not Recommended"

    def _generate_summary(self, overall_score: float, breakdown: dict) -> str:
        sem = breakdown.get("semantic_score", 0)
        skills = breakdown.get("skill_score", 0)

        if overall_score >= 85.0:
            return f"Excellent candidate with strong semantic alignment ({sem}%) and skill coverage ({skills}%)."
        elif overall_score >= 72.0:
            return f"Solid candidate with good technical qualifications ({skills}%) and relevant experience."
        elif overall_score >= 55.0:
            return "Moderate match. Candidate meets basic requirements but has skill or experience gaps."
        else:
            return "Low match. Candidate profile lacks key technical alignment for this position."

    def _empty_result(self) -> dict:
        return {
            "candidates": [],
            "ranking_metrics": {
                "top_score": 0.0,
                "average_score": 0.0,
                "median_score": 0.0,
                "score_distribution": {"0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0},
                "recommendation_summary": "No candidates evaluated"
            }
        }
