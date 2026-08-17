from .skill_normalizer import (
    extract_skills_from_text,
    normalize_skill
)


def calculate_experience_years(experience):

    if not experience:
        return 0

    total_years = 0

    for item in experience:

        if not isinstance(item, dict):
            continue

        years = item.get("years", 0)

        try:
            total_years += float(years)
        except (ValueError, TypeError):
            continue

    return total_years


def parse_resume(resume):

    # --------------------------------
    # Resume text
    # --------------------------------

    raw_text = resume.get_resume_text()

    # --------------------------------
    # Skills stored in Resume model
    # --------------------------------

    stored_skills = [
        normalize_skill(skill)
        for skill in (resume.skills or [])
    ]

    # --------------------------------
    # Detect additional skills
    # --------------------------------

    detected_skills = extract_skills_from_text(
        raw_text
    )

    # Combine both sources
    all_skills = sorted(
        set(
            stored_skills +
            detected_skills
        )
    )

    # --------------------------------
    # Experience
    # --------------------------------

    experience_years = calculate_experience_years(
        resume.experience
    )

    # --------------------------------
    # Education
    # --------------------------------

    education = resume.education or []

    return {

        "resume_id": resume.id,

        "user_id": resume.user_id,

        "skills": all_skills,

        "stored_skills": stored_skills,

        "detected_skills": detected_skills,

        "experience": resume.experience or [],

        "experience_years": experience_years,

        "education": education,

        "contact_info": resume.contact_info or {},

        "raw_text": raw_text,

    }