from .job_parser import parse_job
from .resume_parser import parse_resume
from .skill_matcher import match_skills
from .preferred_skill_matcher import match_preferred_skills
from .experience_matcher import match_experience
from .education_matcher import match_education
from .semantic_matcher import calculate_semantic_score
from .scoring_engine import calculate_final_score, get_match_category
from .models import ApplicationMatch
from .ranking import update_job_rankings


def calculate_application_match(application):
    """
    Calculate complete match result for one application.
    """

    # --------------------------------
    # Get Resume and Job
    # --------------------------------

    resume = application.resume
    job = application.job

    if not resume:
        raise ValueError(
            "This application has no resume."
        )

    if not job:
        raise ValueError(
            "This application has no job."
        )

    # --------------------------------
    # Parse Resume & Job
    # --------------------------------

    resume_data = parse_resume(resume)
    job_data = parse_job(job)

    # --------------------------------
    # Required Skills
    # --------------------------------

    skill_result = match_skills(
        job_data["required_skills"],
        resume_data["skills"]
    )

    # --------------------------------
    # Preferred Skills
    # --------------------------------

    preferred_result = match_preferred_skills(
        job_data["preferred_skills"],
        resume_data["skills"]
    )

    # --------------------------------
    # Experience
    # --------------------------------

    experience_result = match_experience(
        job_data["experience_years"],
        resume_data["experience_years"]
    )

    # --------------------------------
    # Education
    # --------------------------------

    education_result = match_education(
        job_data["requirements"],
        resume_data["education"]
    )

    # --------------------------------
    # Semantic Similarity
    # --------------------------------

    semantic_result = calculate_semantic_score(
        job_data["full_text"],
        resume_data["raw_text"]
    )

    # --------------------------------
    # Final Score
    # --------------------------------

    final_score = calculate_final_score(
        skill_score=skill_result["score"],
        experience_score=experience_result["score"],
        semantic_score=semantic_result["score"],
        education_score=education_result["score"],
        preferred_skill_score=preferred_result["score"],
    )

    category = get_match_category(
        final_score
    )

    # --------------------------------
    # Detailed Breakdown
    # --------------------------------

    breakdown = {
        "skill_score": skill_result["score"],
        "experience_score": experience_result["score"],
        "education_score": education_result["score"],
        "semantic_score": semantic_result["score"],
        "preferred_skill_score": preferred_result["score"],

        "category": category,

        "matched_skills": skill_result[
            "matched_skills"
        ],

        "missing_skills": skill_result[
            "missing_skills"
        ],

        "matched_preferred_skills":
            preferred_result[
                "matched_skills"
            ],

        "missing_preferred_skills":
            preferred_result[
                "missing_skills"
            ],

        "experience": experience_result,

        "education": education_result,

        "semantic": semantic_result,
    }

    # --------------------------------
    # Save ApplicationMatch
    # --------------------------------

    match, created = ApplicationMatch.objects.update_or_create(
        application=application,
        defaults={
            "skill_score": skill_result["score"],
            "experience_score": experience_result["score"],
            "education_score": education_result["score"],
            "semantic_score": semantic_result["score"],
            "preferred_skill_score": preferred_result["score"],

            "overall_score": final_score,

            "matched_skills": skill_result[
                "matched_skills"
            ],

            "missing_skills": skill_result[
                "missing_skills"
            ],

            "explanation": (
                f"{category}: "
                f"{final_score}% overall match."
            ),
        }
    )

    # --------------------------------
    # Update existing Application
    # --------------------------------

    application.match_score = final_score
    application.match_breakdown = breakdown
    application.save(
        update_fields=[
            "match_score",
            "match_breakdown",
            "updated_at",
        ]
    )

    # --------------------------------
    # Recalculate Ranking
    # --------------------------------
    update_job_rankings(application.job)

    return match