from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class OTPBackend(ModelBackend):
    """Authenticate user by email, phone, or username (no password needed)."""
    def authenticate(self, request, username=None, email=None, phone_number=None, **kwargs):
        try:
            if email:
                return User.objects.get(email=email)
            elif phone_number:
                return User.objects.get(phone_number=phone_number)
            elif username:
                return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
