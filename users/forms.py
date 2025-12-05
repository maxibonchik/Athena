from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    """Упрощенная форма регистрации"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User  # Стандартная модель Django
        fields = ['username', 'email', 'password1', 'password2']