from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True,unique=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

   

    def __str__(self):
        return self.username


class OTPVerification(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.username} - {'Used' if self.is_used else 'Unused'}"

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)


    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])

    def is_valid(self):
        return not self.is_used and not self.is_expired
