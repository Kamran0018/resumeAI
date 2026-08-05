# ai_services/semantic_matcher.py
"""
Semantic Matcher Engine (Sentence Transformers + BERT Architecture)
Performs 384-dimensional vector embedding generation, PyTorch GPU acceleration,
cosine similarity scoring, caching, batch matching, and duplicate detection.
"""

import hashlib
import json
import logging
import numpy as np

# PyTorch & Sentence Transformers Imports
try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    torch = None
    DEVICE = "cpu"

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None

try:
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    cosine_similarity = None

# Optional Redis Cache
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=1)
    redis_client.ping()
except Exception:
    redis_client = None

logger = logging.getLogger(__name__)


class SemanticMatcher:
    """Production-grade Semantic Matcher using all-MiniLM-L6-v2 BERT embeddings."""

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM = 384

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.device = DEVICE
        self._memory_cache = {}
        self.model = None

        if SentenceTransformer:
            try:
                self.model = SentenceTransformer(self.model_name, device=self.device)
                logger.info(f"Loaded SentenceTransformer {self.model_name} on device: {self.device}")
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer: {e}. Falling back to statistical embedding mode.")

    # ─────────────────────────────────────────────────────────────
    # Core Embedding Generation with Caching
    # ─────────────────────────────────────────────────────────────

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generate 384-dimensional normalized vector embedding for text string.
        Uses Redis or in-memory cache to avoid recomputing embeddings.
        """
        text_clean = text.strip()
        if not text_clean:
            return np.zeros(self.EMBEDDING_DIM, dtype=np.float32)

        cache_key = f"emb:{hashlib.md5(text_clean.encode('utf-8')).hexdigest()}"

        # 1. Check Redis Cache
        if redis_client:
            try:
                cached_bytes = redis_client.get(cache_key)
                if cached_bytes:
                    return np.frombuffer(cached_bytes, dtype=np.float32)
            except Exception:
                pass

        # 2. Check Memory Cache
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]

        # 3. Compute Embedding
        if self.model:
            embedding = self.model.encode(text_clean, convert_to_numpy=True, normalize_embeddings=True)
        else:
            embedding = self._fallback_vector(text_clean)

        embedding = np.ascontiguousarray(embedding, dtype=np.float32)

        # Cache result
        self._memory_cache[cache_key] = embedding
        if redis_client:
            try:
                redis_client.set(cache_key, embedding.tobytes(), ex=86400)  # TTL 24h
            except Exception:
                pass

        return embedding

    def _fallback_vector(self, text: str) -> np.ndarray:
        """Deterministic pseudo-embedding fallback when transformer model is not loaded."""
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(self.EMBEDDING_DIM).astype(np.float32)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    # ─────────────────────────────────────────────────────────────
    # Cosine Similarity Calculation
    # ─────────────────────────────────────────────────────────────

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        sim = float(np.dot(vec1, vec2) / (norm1 * norm2))
        return max(0.0, min(1.0, sim))

    # ─────────────────────────────────────────────────────────────
    # Single Match Evaluation
    # ─────────────────────────────────────────────────────────────

    def match(self, resume_text: str, job_text: str) -> dict:
        """
        Evaluate semantic match between a resume and a job description.
        Returns match percentage, category, explanation, and 384-dim embedding vector.
        """
        emb_resume = self.get_embedding(resume_text)
        emb_job = self.get_embedding(job_text)

        similarity = self.compute_similarity(emb_resume, emb_job)
        score = round(similarity * 100, 1)

        category = self._classify_score(score)
        explanation = self._generate_explanation(score, resume_text, job_text)

        return {
            "semantic_score": score,
            "embedding_similarity": round(similarity, 4),
            "match_percentage": score,
            "match_category": category,
            "explanation": explanation,
            "embedding": emb_resume.tolist()
        }

    # ─────────────────────────────────────────────────────────────
    # Batch Processing (100+ Resumes)
    # ─────────────────────────────────────────────────────────────

    def batch_match(self, resume_texts: list, job_text: str) -> list:
        """
        Efficiently process 100+ resumes against a single job description.
        """
        emb_job = self.get_embedding(job_text)

        if self.model and SentenceTransformer:
            try:
                embeddings = self.model.encode(
                    resume_texts,
                    batch_size=64,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True
                )
                similarities = np.dot(embeddings, emb_job)
            except Exception:
                embeddings = [self.get_embedding(txt) for txt in resume_texts]
                similarities = [self.compute_similarity(emb, emb_job) for emb in embeddings]
        else:
            embeddings = [self.get_embedding(txt) for txt in resume_texts]
            similarities = [self.compute_similarity(emb, emb_job) for emb in embeddings]

        results = []
        for i, sim in enumerate(similarities):
            score = round(float(sim) * 100, 1)
            results.append({
                "index": i,
                "semantic_score": score,
                "embedding_similarity": round(float(sim), 4),
                "match_category": self._classify_score(score),
                "embedding": embeddings[i].tolist() if isinstance(embeddings[i], np.ndarray) else embeddings[i]
            })

        results.sort(key=lambda x: x["semantic_score"], reverse=True)
        return results

    # ─────────────────────────────────────────────────────────────
    # Use Case: Duplicate Resume Detection
    # ─────────────────────────────────────────────────────────────

    def find_duplicate_resumes(self, resume_texts: list, threshold: float = 0.92) -> list:
        """
        Detect near-identical or duplicate resumes using vector similarity.
        """
        embeddings = np.array([self.get_embedding(txt) for txt in resume_texts])
        duplicates = []

        num_resumes = len(embeddings)
        for i in range(num_resumes):
            for j in range(i + 1, num_resumes):
                sim = self.compute_similarity(embeddings[i], embeddings[j])
                if sim >= threshold:
                    duplicates.append({
                        "resume_index_1": i,
                        "resume_index_2": j,
                        "similarity": round(sim, 4),
                        "match_percentage": round(sim * 100, 1),
                        "status": "Potential Duplicate"
                    })

        return duplicates

    # ─────────────────────────────────────────────────────────────
    # Use Case: Job Recommendation Engine
    # ─────────────────────────────────────────────────────────────

    def recommend_jobs(self, resume_text: str, jobs_list: list) -> list:
        """
        Rank a list of job descriptions for a single candidate resume.
        """
        resume_emb = self.get_embedding(resume_text)
        recommendations = []

        for job in jobs_list:
            job_text = job.get("description", "") or job.get("text", "")
            job_emb = self.get_embedding(job_text)
            sim = self.compute_similarity(resume_emb, job_emb)
            score = round(sim * 100, 1)

            recommendations.append({
                "job_id": job.get("id"),
                "job_title": job.get("title", "Job Opportunity"),
                "company": job.get("company", ""),
                "match_score": score,
                "match_category": self._classify_score(score)
            })

        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations

    # ─────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────

    def _classify_score(self, score: float) -> str:
        if score >= 80.0:
            return "Excellent Match"
        elif score >= 65.0:
            return "Strong Match"
        elif score >= 50.0:
            return "Moderate Match"
        else:
            return "Low Match"

    def _generate_explanation(self, score: float, resume_text: str, job_text: str) -> str:
        if score >= 80.0:
            return "Strong semantic alignment in technical skills, experience level, and project domains."
        elif score >= 65.0:
            return "Good alignment in core technical requirements and relevant project context."
        elif score >= 50.0:
            return "Partial semantic match. Candidate shares foundational skills but has domain variations."
        else:
            return "Low semantic correlation between candidate experience and target job requirements."
