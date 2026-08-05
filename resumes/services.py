# resumes/services.py
import os
import re
import json
from ai_services.nlp_parser import AdvancedResumeParser

class ResumeParser:
    """Wrapper using AdvancedResumeParser for backward compatibility."""

    def __init__(self):
        self.nlp_parser = AdvancedResumeParser()
        self.skill_keywords = list(self.nlp_parser.tech_skills_map.values())

    def parse(self, file_path):
        """Parse resume file and extract structured data"""
        raw_text = self._extract_text(file_path)
        parsed_data = self.nlp_parser.parse(file_path)

        # Merge raw_text and flattened skills list for backward compatibility with Django templates & views
        all_skills = (
            parsed_data.get("skills", {}).get("technical", []) +
            parsed_data.get("skills", {}).get("soft", []) +
            parsed_data.get("skills", {}).get("domain", [])
        )

        return {
            'raw_text': raw_text or parsed_data.get('summary', ''),
            'skills': all_skills,
            'experience': parsed_data.get('experience', []),
            'education': parsed_data.get('education', []),
            'contact_info': {
                'email': parsed_data.get('email', ''),
                'phone': parsed_data.get('phone', ''),
                'linkedin': parsed_data.get('linkedin', ''),
                'github': parsed_data.get('github', '')
            },
            'summary': parsed_data.get('summary', ''),
            'full_nlp_json': parsed_data
        }

    def _extract_text(self, file_path):
        """Extract text from different file types"""
        return self.nlp_parser.extract_text_from_file(file_path)