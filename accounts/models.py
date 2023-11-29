from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you want
    # For example, a profile picture, bio, etc.
    # Example: profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    # Optional: add any custom methods you need

    def __str__(self):
        return self.username