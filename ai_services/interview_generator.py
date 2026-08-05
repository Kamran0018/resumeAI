# ai_services/interview_generator.py
"""
AI Interview Question Generator Engine
Uses Gemini LLM & Grok AI with fallback heuristics to generate 8 question categories,
difficulty levels, follow-up questions, sample candidate answers, and preparation tips.
"""

import json
from .gemini_service import GeminiService
from .grok_service import GrokService


class InterviewQuestionGenerator:
    """State-of-the-Art AI Interview Question Generator."""

    def __init__(self):
        self.gemini = GeminiService()
        self.grok = GrokService()

    def generate_interview_kit(
        self,
        resume_text: str,
        job_description: str = "",
        role_title: str = "Software Engineer",
        difficulty: str = "Medium"
    ) -> dict:
        """
        Generate a complete 360-degree interview preparation kit with 8 question categories.
        """
        if self.gemini.available or self.grok.available:
            ai_res = self._generate_with_ai(resume_text, job_description, role_title, difficulty)
            if ai_res and "interview_questions" in ai_res:
                return ai_res

        return self._generate_fallback(role_title, difficulty)

    def _generate_with_ai(self, resume_text: str, job_text: str, role_title: str, difficulty: str) -> dict:
        prompt = f"""
You are an Executive Hiring Lead and Senior Tech Interviewer.
Generate a comprehensive 360-degree interview preparation kit for a {role_title} candidate ({difficulty} level).

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_text[:2000] if job_text else 'Senior Software Developer role.'}

Respond ONLY in valid raw JSON with this exact structure:
{{
    "interview_questions": {{
        "hr_questions": [
            {{
                "question": "Tell me about yourself and your background.",
                "difficulty": "Easy",
                "sample_answer": "I am a passionate software engineer with 5+ years building scalable applications..."
            }}
        ],
        "technical_questions": [
            {{
                "question": "Explain your experience with Python, Django, and REST APIs.",
                "difficulty": "Medium",
                "follow_up": "Can you share a specific performance bottleneck you resolved?"
            }}
        ],
        "behavioral_questions": [
            {{
                "question": "Describe a challenge you faced with team disagreement and how you resolved it.",
                "difficulty": "Medium",
                "evaluation_criteria": ["Leadership", "Problem Solving", "Resilience"]
            }}
        ],
        "coding_questions": [
            {{
                "question": "Implement an LRU Cache with O(1) time complexity.",
                "difficulty": "Hard",
                "language": "Python",
                "estimated_time": "45 minutes"
            }}
        ],
        "system_design_questions": [
            {{
                "question": "Design a scalable URL Shortener service handling 100M daily active users.",
                "difficulty": "Hard",
                "evaluation_criteria": ["Scalability", "Database design", "Caching strategy", "API design"]
            }}
        ],
        "leadership_questions": [
            {{
                "question": "How do you mentor junior developers while delivering tight sprint goals?",
                "difficulty": "Medium",
                "sample_answer": "I institute weekly pair-programming sessions and clear code review guidelines..."
            }}
        ],
        "company_specific_questions": [
            {{
                "question": "Why do you want to work at our company specifically?",
                "difficulty": "Easy",
                "sample_answer": "Your work in scalable cloud engineering aligns directly with my career goals..."
            }}
        ],
        "resume_based_questions": [
            {{
                "question": "Walk me through the architecture of your recent project listed on your resume.",
                "difficulty": "Medium",
                "follow_up": "What would you re-architect if traffic doubled?"
            }}
        ]
    }},
    "interview_duration": "90 minutes",
    "difficulty_level": "{difficulty}",
    "focus_areas": ["System Design", "Data Structures", "Leadership", "Microservices"],
    "preparation_tips": [
        "Review system design concepts and database indexing",
        "Practice LeetCode medium/hard coding problems",
        "Prepare STAR method stories for behavioral questions"
    ]
}}
"""
        raw = self.gemini._call(prompt) if self.gemini.available else self.grok._call(prompt)
        parsed = self.gemini._parse_json(raw) if self.gemini.available else self.grok._parse_json(raw)
        return parsed

    def _generate_fallback(self, role_title: str, difficulty: str) -> dict:
        return {
            "interview_questions": {
                "hr_questions": [
                    {
                        "question": "Tell me about yourself and your professional journey.",
                        "difficulty": "Easy",
                        "sample_answer": f"I am a software professional specializing in {role_title} roles with strong technical and problem-solving skills."
                    }
                ],
                "technical_questions": [
                    {
                        "question": f"Explain your core technical experience relevant to {role_title}.",
                        "difficulty": "Medium",
                        "follow_up": "Can you provide an example project where you applied these skills under tight deadlines?"
                    }
                ],
                "behavioral_questions": [
                    {
                        "question": "Describe a major technical challenge you faced and how you overcame it.",
                        "difficulty": "Medium",
                        "evaluation_criteria": ["Leadership", "Problem Solving", "Resilience"]
                    }
                ],
                "coding_questions": [
                    {
                        "question": "Implement an LRU Cache with O(1) average lookup time.",
                        "difficulty": "Hard",
                        "language": "Python",
                        "estimated_time": "45 minutes"
                    }
                ],
                "system_design_questions": [
                    {
                        "question": "Design a scalable URL Shortener service (like bit.ly) handling 100M requests daily.",
                        "difficulty": "Hard",
                        "evaluation_criteria": ["Scalability", "Database design", "API design", "Caching strategy"]
                    }
                ],
                "leadership_questions": [
                    {
                        "question": "How do you handle technical debt while keeping project delivery on schedule?",
                        "difficulty": "Medium",
                        "sample_answer": "I advocate for allocating 15-20% of sprint capacity to refactoring critical paths."
                    }
                ],
                "company_specific_questions": [
                    {
                        "question": "Why are you interested in joining our engineering team?",
                        "difficulty": "Easy",
                        "sample_answer": "Your emphasis on high-impact products and technical innovation matches my passion."
                    }
                ],
                "resume_based_questions": [
                    {
                        "question": "Walk me through the system architecture of the top project listed on your resume.",
                        "difficulty": "Medium",
                        "follow_up": "What performance optimizations did you implement?"
                    }
                ]
            },
            "interview_duration": "90 minutes",
            "difficulty_level": difficulty,
            "focus_areas": ["System Design", "Data Structures", "Leadership", "Cloud Architecture"],
            "preparation_tips": [
                "Review system design principles (load balancing, caching, database sharding)",
                "Practice coding problems using the STAR technique for behavioral answers",
                "Brush up on core technical concepts and project architecture details"
            ]
        }
