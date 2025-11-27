from django.db import models
from django.conf import settings
import json

class UserProfile(models.Model):
    LEARNING_STYLES = [
        ('visual', 'Визуал'),
        ('auditory', 'Аудиал'),
        ('kinesthetic', 'Кинестет'),
        ('reading', 'Чтение/Письмо'),
    ]
    DISCIPLINE_LEVELS = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    MEMORY_LEVELS = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='learning_profile'
    )
    learning_style = models.CharField('Стиль обучения', max_length=20, choices=LEARNING_STYLES)
    discipline_level = models.CharField('Уровень самодисциплины', max_length=10, choices=DISCIPLINE_LEVELS)
    memory_capacity = models.CharField('Объем памяти', max_length=10, choices=MEMORY_LEVELS, default='medium')
    weekly_hours = models.IntegerField('Часов в неделю', default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль обучения {self.user.username}"

class Course(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    source_url = models.URLField('Ссылка на Stepik', blank=True, null=True)  # НОВОЕ ПОЛЕ
    parsed_data = models.JSONField('Данные анализа', null=True, blank=True)  # НОВОЕ ПОЛЕ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # НОВОЕ ПОЛЕ

    def __str__(self):
        return self.title

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Название', max_length=200)
    order = models.PositiveIntegerField('Порядок', default=0)
    complexity = models.CharField('Сложность', max_length=15, choices=[  # НОВОЕ ПОЛЕ
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый')
    ], default='beginner')
    estimated_hours = models.FloatField('Часов на изучение', default=2.0)  # НОВОЕ ПОЛЕ

    class Meta:
        ordering = ['order']
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return self.title

class CourseLesson(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название', max_length=200)
    content = models.TextField('Содержание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    key_concepts = models.JSONField('Ключевые концепции', default=list)  # НОВОЕ ПОЛЕ

    class Meta:
        ordering = ['order']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.title

# НОВАЯ МОДЕЛЬ: Учебный план
class StudyPlan(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('paused', 'Приостановлен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_plans'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='study_plans'
    )
    strategy_data = models.JSONField('Данные стратегии')  # Результат работы StrategyGenerator
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    total_xp = models.IntegerField('Всего XP', default=0)  # НОВОЕ ПОЛЕ
    current_level = models.IntegerField('Текущий уровень', default=1)  # НОВОЕ ПОЛЕ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'course']  # Один план на пользователя и курс
        verbose_name = "Study Plan"
        verbose_name_plural = "Study Plans"

    def __str__(self):
        return f"План {self.user.username} для {self.course.title}"

# НОВАЯ МОДЕЛЬ: Прогресс изучения
class StudyProgress(models.Model):
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    lesson = models.ForeignKey(
        CourseLesson,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    completed = models.BooleanField('Завершено', default=False)
    completed_at = models.DateTimeField('Завершено в', null=True, blank=True)
    xp_earned = models.IntegerField('Заработано XP', default=0)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Study Progress"
        verbose_name_plural = "Study Progress Records"
        unique_together = ['study_plan', 'lesson']

    def __str__(self):
        status = "Завершено" if self.completed else "В процессе"
        return f"Прогресс: {self.study_plan.user.username} - {self.lesson.title} ({status})"

# НОВАЯ МОДЕЛЬ: Достижения
class Achievement(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    icon = models.CharField('Иконка', max_length=50, help_text="Название иконки или emoji")
    xp_reward = models.IntegerField('Награда XP', default=100)
    condition = models.JSONField('Условие получения', help_text="Логика получения в формате JSON")

    def __str__(self):
        return self.name

# НОВАЯ МОДЕЛЬ: Полученные достижения
class UserAchievement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='earned_achievements'
    )
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    study_plan = models.ForeignKey(  # Связь с планом, в котором получено
        StudyPlan,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ['user', 'achievement']

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
    
# courses/models.py (дополнение)
class CognitiveTest(models.Model):
    """Модель для хранения вопросов когнитивного теста"""
    QUESTION_SECTIONS = [
        ('learning_style', 'Стиль обучения'),
        ('memory', 'Память'),
        ('discipline', 'Самодисциплина'),
    ]
    
    section = models.CharField('Раздел', max_length=20, choices=QUESTION_SECTIONS)
    question_number = models.IntegerField('Номер вопроса')
    question_text = models.TextField('Текст вопроса')
    option_a = models.CharField('Вариант A', max_length=200)
    option_b = models.CharField('Вариант B', max_length=200)
    option_c = models.CharField('Вариант C', max_length=200)
    option_d = models.CharField('Вариант D', max_length=200)
    
    class Meta:
        ordering = ['section', 'question_number']
        unique_together = ['section', 'question_number']
    
    def __str__(self):
        return f"{self.get_section_display()} - Вопрос {self.question_number}"

class TestResult(models.Model):
    """Результаты прохождения когнитивного теста"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    learning_style = models.CharField('Стиль обучения', max_length=20, choices=[
        ('visual', 'Визуал'),
        ('auditory', 'Аудиал'),
        ('reading', 'Чтение/Письмо'),
        ('kinesthetic', 'Кинестет'),
        ('mixed', 'Смешанный'),
    ])
    memory_score = models.IntegerField('Оценка памяти (1-10)')
    discipline_score = models.IntegerField('Оценка самодисциплины (1-10)')
    raw_answers = models.JSONField('Сырые ответы')  # {question_id: 'a'/'b'/'c'/'d'}
    calculated_scores = models.JSONField('Рассчитанные баллы')  # Детальная аналитика
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Результаты теста {self.user.username}"