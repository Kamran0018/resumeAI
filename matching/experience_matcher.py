
def match_experience(required_years, candidate_years):
    """
    Compare required experience with candidate experience.

    Returns a score from 0 to 100.
    """

    try:
        required_years = float(required_years or 0)
    except (ValueError, TypeError):
        required_years = 0

    try:
        candidate_years = float(candidate_years or 0)
    except (ValueError, TypeError):
        candidate_years = 0

    # No experience required
    if required_years <= 0:
        return {
            "score": 100.0,
            "required_years": 0,
            "candidate_years": candidate_years,
            "status": "meets_requirement"
        }

    # Candidate meets or exceeds requirement
    if candidate_years >= required_years:
        return {
            "score": 100.0,
            "required_years": required_years,
            "candidate_years": candidate_years,
            "status": "meets_requirement"
        }

    # Partial experience
    score = (
        candidate_years / required_years
    ) * 100

    return {
        "score": round(min(score, 100), 2),
        "required_years": required_years,
        "candidate_years": candidate_years,
        "status": "partial"
    }