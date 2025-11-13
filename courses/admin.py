from django.contrib import admin
from .models import Course, CourseModule, CourseLesson

class CourseLessonInline(admin.TabularInline):
    model = CourseLesson
    extra = 1
    fields = ('title', 'order')
    ordering = ('order',)

class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    fields = ('title', 'order')
    ordering = ('order',)

@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')

@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module',)
    ordering = ('module', 'order')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    ordering = ('created_at',)

    inlines = [CourseModuleInline]