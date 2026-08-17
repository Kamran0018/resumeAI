from .skill_normalizer import normalize_skill


def match_preferred_skills(preferred_skills, candidate_skills):
    """
    Match preferred (nice-to-have) skills from
    the job against the candidate's skills.

    Returns a score from 0 to 100.
    Scoring is more lenient than required skills:
    - Having no preferred skills listed → 100 (not penalised)
    - Partial match still awards proportional score
    """

    preferred = {
        normalize_skill(skill)
        for skill in preferred_skills
    }

    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    # No preferred skills specified — full score
    if not preferred:
        return {
            "score": 100.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = sorted(
        preferred.intersection(candidate)
    )

    missing = sorted(
        preferred - candidate
    )

    score = (
        len(matched) /
        len(preferred)
    ) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }
