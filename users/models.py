# users/models.py - МИНИМАЛЬНАЯ ВЕРСИЯ
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # ТОЛЬКО ОДНО поле для начала
    # learning_style = models.CharField(max_length=100, blank=True)
    # memory_type = models.CharField(max_length=100, blank=True)
    # discipline_score = models.IntegerField(default=0)
    # total_xp = models.IntegerField(default=0)
    # level = models.IntegerField(default=1)
    pass  # Пустой класс для начала

    def __str__(self):
        return self.username