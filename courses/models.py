from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Module"            # одно название
        verbose_name_plural = "Modules"    # множественное число

    def __str__(self):
        return self.title

class CourseLesson(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.title