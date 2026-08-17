try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    cosine_similarity = None


# Load model only once
_model = None


def get_model():
    global _model

    if SentenceTransformer is None:
        raise RuntimeError(
            "sentence-transformers is not installed. "
            "Run: pip install sentence-transformers"
        )

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


def calculate_semantic_score(
    job_text,
    resume_text
):
    """
    Calculate semantic similarity between
    job description and resume.

    Returns score from 0 to 100.
    """

    if cosine_similarity is None:
        raise RuntimeError(
            "scikit-learn is not installed. "
            "Run: pip install scikit-learn"
        )

    if not job_text or not resume_text:
        return {
            "score": 0.0,
            "similarity": 0.0
        }

    model = get_model()

    job_embedding = model.encode(
        [job_text]
    )

    resume_embedding = model.encode(
        [resume_text]
    )

    similarity = cosine_similarity(
        job_embedding,
        resume_embedding
    )[0][0]

    # similarity is in [0, 1] for normalized text embeddings
    score = float(similarity) * 100

    return {
        "score": round(score, 2),
        "similarity": round(
            float(similarity),
            4
        )
    }