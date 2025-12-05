# courses/models.py - МИНИМАЛЬНАЯ ВЕРСИЯ
from django.db import models
from django.conf import settings  # Используем settings.AUTH_USER_MODEL

class Course(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем AUTH_USER_MODEL
        on_delete=models.CASCADE
    )
    stepik_url = models.URLField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title