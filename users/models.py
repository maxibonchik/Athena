from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Расширенная модель пользователя для Афины"""
    
    # Данные когнитивного теста
    learning_style = models.CharField(
        max_length=50,
        choices=[
            ('visual', 'Визуал'),
            ('auditory', 'Аудиал'),
            ('kinesthetic', 'Кинестетик'),
            ('mixed', 'Смешанный'),
        ],
        blank=True,
        null=True
    )
    
    memory_score = models.IntegerField(
        default=50,
        help_text="Оценка памяти (0-100)"
    )
    
    discipline_score = models.IntegerField(
        default=50,
        help_text="Оценка самодисциплины (0-100)"
    )
    
    concentration_span = models.IntegerField(
        default=25,
        help_text="Продолжительность концентрации в минутах"
    )
    
    preferred_study_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Утро (6-12)'),
            ('afternoon', 'День (12-18)'),
            ('evening', 'Вечер (18-24)'),
            ('night', 'Ночь (24-6)'),
        ],
        blank=True,
        null=True
    )
    
    test_completed = models.BooleanField(default=False)
    test_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Статистика обучения
    total_xp = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'