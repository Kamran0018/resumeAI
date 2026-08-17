WEIGHTS = {
    "skill": 0.40,
    "experience": 0.20,
    "semantic": 0.20,
    "education": 0.10,
    "preferred_skill": 0.10,
}


def calculate_final_score(
    skill_score,
    experience_score,
    semantic_score,
    education_score,
    preferred_skill_score,
):
    """
    Calculate transparent overall match score.
    """

    final_score = (
        (skill_score * WEIGHTS["skill"])
        + (experience_score * WEIGHTS["experience"])
        + (semantic_score * WEIGHTS["semantic"])
        + (education_score * WEIGHTS["education"])
        + (preferred_skill_score * WEIGHTS["preferred_skill"])
    )

    return round(final_score, 2)


def get_match_category(score):
    """
    Convert score into a human-readable category.
    """

    if score >= 90:
        return "Excellent Match"

    if score >= 80:
        return "Strong Match"

    if score >= 70:
        return "Good Match"

    if score >= 60:
        return "Moderate Match"

    if score >= 40:
        return "Weak Match"

    return "Poor Match"