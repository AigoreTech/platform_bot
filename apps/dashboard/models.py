# File: apps/dashboard/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relasi ke model User
    action = models.CharField(max_length=255)  # Deskripsi aktivitas
    timestamp = models.DateTimeField(default=timezone.now)  # Waktu aktivitas terjadi

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
