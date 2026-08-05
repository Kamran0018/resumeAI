# ai_services/jd_parser.py
"""
Job Description Parser — Uses Dual AI (Gemini / Grok) with Rule-Based NLP Fallback
to extract structured fields (title, company, location, skills, salary, etc.) from PDF, DOCX, or TXT JDs.
"""
import os
import re
import json
from django.conf import settings
from resumes.services import ResumeParser
from .gemini_service import GeminiService
from .prompts import GEMINI_JD_PARSING


class JDParser:
    """Parses JD files and extracts structured fields for form auto-population."""

    def __init__(self):
        self.file_parser = ResumeParser()  # Text extractor (PDF, DOCX, TXT)
        self.gemini = GeminiService()

    def parse_file(self, file_path: str) -> dict:
        """
        Extract text from file and send to Gemini, with robust NLP heuristic fallback.
        """
        try:
            # 1. Extract raw text from file
            raw_text = self.file_parser._extract_text(file_path)
            if not raw_text or not raw_text.strip():
                return {}

            # 2. Try Gemini AI parsing if available
            if self.gemini.available:
                try:
                    prompt = GEMINI_JD_PARSING.format(jd_text=raw_text[:6000])
                    raw_response = self.gemini._call(prompt)
                    parsed = self.gemini._parse_json(raw_response)
                    if parsed and isinstance(parsed, dict) and parsed.get("title"):
                        return self._clean_result(parsed)
                except Exception as e:
                    print(f"[JDParser] Gemini parse error: {e}")

            # 3. Rule-Based NLP Fallback (Always returns structured data)
            return self._fallback_parse(raw_text)

        except Exception as e:
            print(f"[JDParser] Error parsing file: {e}")
            return {}

    def _clean_result(self, data: dict) -> dict:
        """Ensure default fields exist and are formatted correctly."""
        return {
            "title": data.get("title", "Software Engineer"),
            "company": data.get("company", "Company Name"),
            "location": data.get("location", "Remote"),
            "job_type": data.get("job_type", "full_time"),
            "experience_level": data.get("experience_level", "mid"),
            "description": data.get("description", ""),
            "requirements": data.get("requirements", ""),
            "responsibilities": data.get("responsibilities", ""),
            "benefits": data.get("benefits", ""),
            "required_skills": data.get("required_skills", "Python, Django, SQL"),
            "preferred_skills": data.get("preferred_skills", "AWS, Docker, CI/CD"),
            "salary_min": data.get("salary_min", None),
            "salary_max": data.get("salary_max", None),
        }

    def _fallback_parse(self, text: str) -> dict:
        """Rule-based NLP parser when LLM API is offline or unconfigured."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text_lower = text.lower()

        # 1. Job Title Extraction
        roles = [
            "Senior Software Engineer", "Software Engineer", "Full Stack Developer",
            "Backend Developer", "Frontend Developer", "Python Developer", "Java Developer",
            "Data Scientist", "DevOps Engineer", "Product Manager", "Project Manager",
            "Software Architect", "UI/UX Designer", "Data Analyst", "Engineering Manager"
        ]

        extracted_title = "Software Engineer"
        for line in lines[:10]:
            for role in roles:
                if role.lower() in line.lower():
                    extracted_title = role
                    break
            if extracted_title != "Software Engineer":
                break

        if extracted_title == "Software Engineer" and lines:
            extracted_title = lines[0][:60]

        # 2. Company Name Extraction
        company = "Tech Solutions"
        company_match = re.search(r"(?:at|company:?|for)\s+([A-Z][a-zA-Z0-9\s&]+(?:Inc|Corp|Ltd|Technologies|Solutions|Systems|Labs|Pvt))", text, re.IGNORECASE)
        if company_match:
            company = company_match.group(1).strip()

        # 3. Location Extraction
        location = "Remote"
        if "remote" in text_lower:
            location = "Remote"
        elif "hybrid" in text_lower:
            location = "Hybrid"
        else:
            loc_match = re.search(r"\b(San Francisco|New York|London|Berlin|Bangalore|Mumbai|Seattle|Austin|Chicago)\b", text, re.IGNORECASE)
            if loc_match:
                location = loc_match.group(0)

        # 4. Job Type & Experience Level
        job_type = "full_time"
        if "part-time" in text_lower or "part time" in text_lower:
            job_type = "part_time"
        elif "contract" in text_lower:
            job_type = "contract"
        elif "internship" in text_lower:
            job_type = "internship"
        elif "remote" in text_lower:
            job_type = "remote"

        experience_level = "mid"
        if "senior" in text_lower or "sr." in text_lower:
            experience_level = "senior"
        elif "junior" in text_lower or "jr." in text_lower or "entry" in text_lower:
            experience_level = "entry"
        elif "lead" in text_lower or "principal" in text_lower:
            experience_level = "lead"
        elif "manager" in text_lower or "head" in text_lower:
            experience_level = "manager"

        # 5. Skills Extraction
        known_skills = [
            "Python", "Django", "Flask", "React", "Node.js", "JavaScript", "TypeScript",
            "SQL", "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes", "Git", "Linux",
            "HTML", "CSS", "C++", "Java", "REST APIs", "GraphQL", "Redis", "CI/CD"
        ]

        found_skills = [skill for skill in known_skills if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text_lower)]
        req_skills = ", ".join(found_skills[:4]) if found_skills else "Python, Django, SQL"
        pref_skills = ", ".join(found_skills[4:]) if len(found_skills) > 4 else "AWS, Docker, CI/CD"

        # 6. Salary Extraction
        salary_min, salary_max = None, None
        nums = re.findall(r"\d{1,3}(?:,\d{3})+|\b\d{2,3}\s*k\b|\b\d{4,6}\b", text)
        if len(nums) >= 2:
            try:
                s1 = nums[0].lower().replace(",", "").replace("k", "000").strip()
                s2 = nums[1].lower().replace(",", "").replace("k", "000").strip()
                salary_min = int(s1)
                salary_max = int(s2)
            except Exception:
                pass

        # 7. Sections (Description, Requirements, Responsibilities)
        sections = self._split_sections(lines)

        return {
            "title": extracted_title,
            "company": company,
            "location": location,
            "job_type": job_type,
            "experience_level": experience_level,
            "description": sections.get("description", "\n".join(lines[:4])),
            "requirements": sections.get("requirements", "• 3+ years of relevant experience.\n• Strong technical & problem solving skills."),
            "responsibilities": sections.get("responsibilities", "• Develop and maintain scalable software applications.\n• Collaborate with cross-functional teams."),
            "benefits": sections.get("benefits", "• Competitive salary & Remote work options."),
            "required_skills": req_skills,
            "preferred_skills": pref_skills,
            "salary_min": salary_min,
            "salary_max": salary_max
        }

    def _split_sections(self, lines: list) -> dict:
        sections = {}
        curr = "description"
        sections[curr] = []

        headers = {
            "requirements": ["requirement", "qualification", "what you need", "who you are"],
            "responsibilities": ["responsibility", "duty", "what you will do", "role overview"],
            "benefits": ["benefit", "perk", "what we offer"]
        }

        for line in lines:
            line_clean = line.lower()
            found = False
            for sec, kws in headers.items():
                if any(kw in line_clean for kw in kws) and len(line_clean) < 40:
                    curr = sec
                    sections[curr] = []
                    found = True
                    break
            if not found:
                sections.setdefault(curr, []).append(line)

        return {k: "\n".join(v[:8]) for k, v in sections.items()}
