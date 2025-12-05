# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course
from users.models import CustomUser

def home(request):
    """Главная страница для неавторизованных пользователей"""
    context = {
        'title': 'Афина - Персонализированная платформа обучения',
        'description': 'Интеллектуальная система, которая создает индивидуальные стратегии обучения на основе вашего когнитивного профиля.'
    }
    
    # Если пользователь уже авторизован, перенаправляем на dashboard
    if request.user.is_authenticated:
        return redirect('main:dashboard')
    
    return render(request, 'main/home.html', context)


@login_required
def dashboard(request):
    """Личный кабинет пользователя"""
    user = request.user
    
    # Получаем курсы пользователя
    user_courses = Course.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Статистика пользователя
    user_stats = {
        'total_courses': Course.objects.filter(user=user).count(),
        'completed_courses': Course.objects.filter(user=user, status='completed').count(),
        'total_xp': user.total_xp if hasattr(user, 'total_xp') else 0,
        'level': user.level if hasattr(user, 'level') else 1,
        'streak': getattr(user, 'current_streak', 0),
    }
    
    context = {
        'title': 'Мой кабинет',
        'user': user,
        'courses': user_courses,
        'stats': user_stats,
    }
    return render(request, 'main/dashboard.html', context)


def about(request):
    """Страница "О проекте" """
    context = {
        'title': 'О проекте Афина',
    }
    return render(request, 'main/about.html', context)


@login_required
def settings_view(request):
    """Настройки пользователя"""
    context = {
        'title': 'Настройки',
    }
    return render(request, 'main/settings.html', context)