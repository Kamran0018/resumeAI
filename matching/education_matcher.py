import re


EDUCATION_ALIASES = {
    "computer science": [
        "computer science",
        "computer science engineering",
        "cse",
        "cs"
    ],

    "information technology": [
        "information technology",
        "it"
    ],

    "electronics": [
        "electronics",
        "electronics and communication",
        "ece"
    ],

    "electrical": [
        "electrical engineering",
        "eee",
        "electrical"
    ],

    "mechanical": [
        "mechanical engineering",
        "mechanical"
    ],

    "civil": [
        "civil engineering",
        "civil"
    ],

    "business": [
        "business administration",
        "bba",
        "mba"
    ],

    "data science": [
        "data science",
        "data sciences"
    ],

    "mathematics": [
        "mathematics",
        "math"
    ],

    "physics": [
        "physics"
    ]
}


DEGREE_ALIASES = {
    "bachelor": [
        "bachelor",
        "b.tech",
        "btech",
        "b.e",
        "be",
        "bca",
        "b.sc",
        "bsc"
    ],

    "master": [
        "master",
        "m.tech",
        "mtech",
        "m.e",
        "me",
        "mca",
        "m.sc",
        "msc",
        "mba"
    ],

    "diploma": [
        "diploma",
        "polytechnic"
    ]
}


def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def find_field(text):
    """
    Identify the candidate's main education field.
    """

    text = normalize_text(text)

    for field, aliases in EDUCATION_ALIASES.items():

        for alias in aliases:

            if re.search(
                r"(?<!\w)" +
                re.escape(alias) +
                r"(?!\w)",
                text
            ):
                return field

    return None


def find_degree_level(text):
    """
    Identify bachelor/master/diploma level.
    """

    text = normalize_text(text)

    for level, aliases in DEGREE_ALIASES.items():

        for alias in aliases:

            if re.search(
                r"(?<!\w)" +
                re.escape(alias) +
                r"(?!\w)",
                text
            ):
                return level

    return None


def education_to_text(education):

    if not education:
        return ""

    parts = []

    for item in education:

        if isinstance(item, dict):

            parts.append(
                " ".join(
                    str(value)
                    for value in item.values()
                    if value
                )
            )

        else:
            parts.append(str(item))

    return " ".join(parts)


def match_education(
    job_requirements,
    candidate_education
):

    job_text = normalize_text(
        job_requirements
    )

    candidate_text = education_to_text(
        candidate_education
    )

    candidate_text = normalize_text(
        candidate_text
    )

    if not job_text:

        return {
            "score": 100.0,
            "status": "not_specified",
            "candidate_field": find_field(
                candidate_text
            ),
            "candidate_degree": find_degree_level(
                candidate_text
            )
        }

    required_field = find_field(job_text)
    required_degree = find_degree_level(job_text)

    candidate_field = find_field(
        candidate_text
    )

    candidate_degree = find_degree_level(
        candidate_text
    )

    field_match = False
    degree_match = False

    if required_field:

        field_match = (
            candidate_field == required_field
        )

    else:
        field_match = True

    if required_degree:

        degree_match = (
            candidate_degree == required_degree
        )

    else:
        degree_match = True

    # Both match
    if field_match and degree_match:

        score = 100.0
        status = "match"

    # Field matches but degree level differs
    elif field_match:

        score = 70.0
        status = "partial"

    # Degree matches but field differs
    elif degree_match:

        score = 50.0
        status = "partial"

    else:

        score = 0.0
        status = "no_match"

    return {
        "score": score,
        "status": status,

        "required_field": required_field,
        "required_degree": required_degree,

        "candidate_field": candidate_field,
        "candidate_degree": candidate_degree
    }