# File: apps/authentication/models.py

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    foto_profile = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
