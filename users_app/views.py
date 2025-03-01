from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    next_page = 'main'

def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('main')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Проверяем совпадение паролей
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')
        
        # Проверяем существование пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')
        
        # Проверяем существование email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'register.html')
        
        # Создаем пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Авторизуем пользователя
        login(request, user)
        messages.success(request, f'Добро пожаловать, {user.username}!')
        return redirect('main')
        
    return render(request, 'register.html')

def profile_user(request):
    pass