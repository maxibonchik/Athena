from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import CustomUserCreationForm, CognitiveTestForm

def signup_view(request):
    """Страница регистрации с когнитивным тестом"""
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    user_form = CustomUserCreationForm()
    
    if request.method == 'POST' and 'register' in request.POST:
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Регистрация успешна! Теперь пройдите когнитивный тест.')
            return redirect('cognitive_test')
    
    context = {
        'user_form': user_form,
        'user': request.user,
    }
    
    return render(request, 'users/signup.html', context)

@login_required
def cognitive_test_view(request):
    """Страница когнитивного теста"""
    # Упрощенная версия пока
    if request.method == 'POST':
        form = CognitiveTestForm(request.POST)
        if form.is_valid():
            # Пока просто редирект
            messages.success(request, 'Тест пройден!')
            return redirect('dashboard')
    else:
        form = CognitiveTestForm()
    
    return render(request, 'users/cognitive_test.html', {'form': form})