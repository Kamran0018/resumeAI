import re


SKILL_ALIASES = {

    "python": [
        "python",
        "python3",
        "python 3"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "typescript": [
        "typescript",
        "ts"
    ],

    "react": [
        "react",
        "reactjs",
        "react.js"
    ],

    "node.js": [
        "node",
        "nodejs",
        "node.js"
    ],

    "django": [
        "django"
    ],

    "flask": [
        "flask"
    ],

    "sql": [
        "sql",
        "structured query language"
    ],

    "mysql": [
        "mysql"
    ],

    "postgresql": [
        "postgresql",
        "postgres",
        "postgres db"
    ],

    "mongodb": [
        "mongodb",
        "mongo db",
        "mongo"
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "data science": [
        "data science",
        "data-science"
    ],

    "data analysis": [
        "data analysis",
        "data analytics"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch",
        "torch"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "tableau": [
        "tableau"
    ],

    "excel": [
        "excel",
        "microsoft excel"
    ],

    "git": [
        "git"
    ],

    "github": [
        "github"
    ],

    "docker": [
        "docker"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "rest apis"
    ]
}


def normalize_text(text):
    """
    Converts text into a standard searchable format.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def normalize_skill(skill):
    """
    Converts a skill into its canonical name.
    """

    skill = normalize_text(skill)

    for canonical, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if skill == alias.lower():
                return canonical

    return skill


def extract_skills_from_text(text):
    """
    Finds known skills inside resume/JD text.
    """

    text = normalize_text(text)

    found_skills = set()

    for canonical, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = r"(?<!\w)" + re.escape(
                alias.lower()
            ) + r"(?!\w)"

            if re.search(pattern, text):

                found_skills.add(canonical)

                break

    return sorted(found_skills)