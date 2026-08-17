import re

from .skill_normalizer import (
    extract_skills_from_text,
    normalize_skill
)


def get_experience_years(experience_level):
    """
    Convert Job experience level into minimum years.
    """

    experience_map = {
        "entry": 0,
        "junior": 2,
        "mid": 4,
        "senior": 7,
        "lead": 10,
        "manager": 10,
    }

    return experience_map.get(
        experience_level,
        0
    )


def parse_job(job):
    """
    Convert existing Job model into
    structured data for matching.
    """

    # --------------------------------
    # Required skills
    # --------------------------------

    required_skills = [
        normalize_skill(skill)
        for skill in job.get_required_skills_list()
    ]

    # --------------------------------
    # Preferred skills
    # --------------------------------

    preferred_skills = [
        normalize_skill(skill)
        for skill in job.get_preferred_skills_list()
    ]

    # --------------------------------
    # Combine JD text
    # --------------------------------

    full_text = "\n".join(
        filter(
            None,
            [
                job.title,
                job.description,
                job.responsibilities,
                job.requirements,
                job.preferred_qualifications,
            ]
        )
    )

    # --------------------------------
    # Detect additional skills
    # --------------------------------

    detected_skills = extract_skills_from_text(
        full_text
    )

    # Add detected skills to required
    # only when explicitly listed in
    # required_skills is not necessary.
    #
    # We keep them separate for now
    # to avoid accidentally treating
    # every mentioned skill as required.

    return {
        "job_id": job.id,

        "title": job.title,

        "company": job.company,

        "required_skills": sorted(
            set(required_skills)
        ),

        "preferred_skills": sorted(
            set(preferred_skills)
        ),

        "detected_skills": detected_skills,

        "experience_years": get_experience_years(
            job.experience_level
        ),

        "experience_level": job.experience_level,

        "requirements": job.requirements,

        "preferred_qualifications":
            job.preferred_qualifications,

        "full_text": full_text,
    }