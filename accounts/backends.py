# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that permits users to log in using 
    either their username or their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        login_identifier = username.strip()
        try:
            # Query by exact username or exact email (case insensitive)
            user = User.objects.get(
                Q(username__iexact=login_identifier) | Q(email__iexact=login_identifier)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Fallback if duplicate emails exist; pick the first active one
            user = User.objects.filter(
                Q(username__iexact=login_identifier) | Q(email__iexact=login_identifier)
            ).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
