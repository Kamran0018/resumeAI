from .skill_normalizer import normalize_skill


def match_skills(required_skills, candidate_skills):

    required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    matched = sorted(
        required.intersection(candidate)
    )

    missing = sorted(
        required - candidate
    )

    if required:

        score = (
            len(matched) /
            len(required)
        ) * 100

    else:

        score = 0

    return {
        "score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing
    }