from django.shortcuts import render

def index(request):
    """Главная страница для неавторизованных пользователей"""
    
    # Пример данных для шаблона (можно расширить)
    context = {
        'title': 'Афина — Ваш ИИ-наставник для обучения',
        'features': [
            {
                'icon': '🎯',
                'title': 'Персонализация',
                'description': 'План под ваш тип восприятия и памяти'
            },
            {
                'icon': '🎮',
                'title': 'Геймификация',
                'description': 'XP, уровни и ачивки для мотивации'
            },
            {
                'icon': '🧠',
                'title': 'Научный подход',
                'description': 'Интервальные повторения и мнемотехники'
            },
            {
                'icon': '📊',
                'title': 'Аналитика прогресса',
                'description': 'Детальная статистика вашего обучения'
            }
        ],
        'steps': [
            {
                'number': '1',
                'title': 'Тест и анализ',
                'description': 'Пройдите когнитивный тест и добавьте ссылку на курс Stepik'
            },
            {
                'number': '2',
                'title': 'Стратегия',
                'description': 'ИИ создаст персональный план с повторениями и дедлайнами'
            },
            {
                'number': '3',
                'title': 'Обучение',
                'description': 'Выполняйте задания, зарабатывайте XP и отслеживайте прогресс'
            }
        ]
    }
    return render(request, 'main/index.html', context)
# main/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

# Обработчики ошибок
def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)

def custom_500(request):
    return render(request, 'main/500.html', status=500)