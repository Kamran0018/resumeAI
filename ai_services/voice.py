# ai_services/voice.py
import os
from datetime import datetime
from django.conf import settings


class AIVoice:
    """Text to Speech - Free Voice"""
    
    def __init__(self):
        try:
            import pyttsx3  # lazy import — only fails here, not at module load
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
            self.available = True
        except Exception:
            self.engine = None
            self.available = False
            print("Voice engine not available. Using browser speech API as fallback.")

    
    def speak(self, text):
        """Text ko voice mein sunao (Legacy local speaker playback)"""
        if self.available and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        return False
        
    def save_to_file(self, text, filename):
        """Text ko audio file mein save karo"""
        if self.available and self.engine:
            media_dir = os.path.join(settings.MEDIA_ROOT, 'voice')
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)
            
            filepath = os.path.join(media_dir, filename)
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            
            return f"{settings.MEDIA_URL}voice/{filename}"
        return None
    
    def speak_suggestions(self, analysis):
        """Resume suggestions ko voice message mein convert karo"""
        message = f"""
Hello! Here is your resume analysis.

Your resume score is {analysis.get('score', 0)} out of 100.

{analysis.get('rating', 'Good')}

Your strengths are:
{'. '.join(analysis.get('strengths', [])[:3])}

Areas to improve:
{'. '.join(analysis.get('weaknesses', [])[:3])}

My suggestions for you:
{'. '.join(analysis.get('suggestions', [])[:4])}

{analysis.get('summary', 'Good luck with your job search!')}
        """
        message = message.strip()
        return message
    
    def speak_match(self, match_result):
        """Job match analysis ko voice message mein convert karo"""
        message = f"""
Job Match Analysis Complete!

Your resume matches this job by {match_result.get('overall_score', 0)} percent.

{match_result.get('recommendation', 'Consider')}

You have matched these skills:
{', '.join(match_result.get('matched_skills', [])[:5])}

You are missing these skills:
{', '.join(match_result.get('missing_skills', [])[:5])}

To improve your match, consider learning these missing skills.

{match_result.get('summary', '')}
        """
        message = message.strip()
        return message