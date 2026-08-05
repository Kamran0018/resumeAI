from django.apps import AppConfig
import sys
import os

class ResumesConfig(AppConfig):
    name = 'resumes'

    def ready(self):
        # Run database migrations automatically when starting django server
        if 'runserver' in sys.argv:
            # Ensure it runs once in the main reloaded process, not the wrapper
            if os.environ.get('RUN_MAIN') == 'true':
                try:
                    from django.core.management import call_command
                    print("🤖 [Resume AI Config] Checking and running schema migrations...")
                    call_command('makemigrations', interactive=False)
                    call_command('migrate', interactive=False)
                    print("🤖 [Resume AI Config] Schema up to date!")
                except Exception as e:
                    print(f"🤖 [Resume AI Config] Migration warning: {e}")

