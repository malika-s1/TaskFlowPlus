from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        
        errors = []
        
        # Валидация
        if not username:
            errors.append("Введите имя пользователя")
        elif len(username) < 3:
            errors.append("Имя пользователя должно быть не менее 3 символов")
        
        if not email:
            errors.append("Введите email")
        elif "@" not in email:
            errors.append("Введите корректный email")
        
        if not password1:
            errors.append("Введите пароль")
        elif len(password1) < 8:
            errors.append("Пароль должен быть не менее 8 символов")
        
        if password1 != password2:
            errors.append("Пароли не совпадают")
        
        if User.objects.filter(username=username).exists():
            errors.append("Пользователь с таким именем уже существует")
        
        if User.objects.filter(email=email).exists():
            errors.append("Пользователь с таким email уже существует")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            # АВТОМАТИЧЕСКИ ВХОДИМ ПОСЛЕ РЕГИСТРАЦИИ
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username}! Регистрация прошла успешно.")
                return redirect("home")
            else:
                messages.error(request, "Ошибка входа после регистрации. Попробуйте войти вручную.")
                return redirect("login")
    
    return render(request, "register.html")
