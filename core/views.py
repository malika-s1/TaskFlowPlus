from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Project, Task, UserProfile
from django.utils import timezone

# ===== DASHBOARD =====
@login_required
def dashboard(request):
    """Дашборд пользователя"""
    projects = Project.objects.filter(owner=request.user)[:5]
    tasks = Task.objects.filter(assigned_to=request.user)[:10]
    
    total_projects = Project.objects.filter(owner=request.user).count()
    total_tasks = Task.objects.filter(assigned_to=request.user).count()
    completed_tasks = Task.objects.filter(assigned_to=request.user, status='done').count()
    
    context = {
        'projects': projects,
        'tasks': tasks,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'core/dashboard.html', context)

# ===== PROJECTS =====
@login_required
def projects_list(request):
    """Список проектов"""
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'core/projects.html', {'projects': projects})

@login_required
def create_project(request):
    """Создание нового проекта"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', 'medium')
        color = request.POST.get('color', '#3B82F6')
        
        if title:
            project = Project.objects.create(
                title=title,
                description=description,
                owner=request.user,
                priority=priority,
                color=color
            )
            messages.success(request, f'Проект "{title}" успешно создан!')
            return redirect('projects_list')
        else:
            messages.error(request, 'Название проекта обязательно')
    
    return render(request, 'core/create_project.html')

@login_required
def edit_project(request, project_id):
    """Редактирование проекта"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        project.title = request.POST.get('title', '').strip()
        project.description = request.POST.get('description', '').strip()
        project.priority = request.POST.get('priority', 'medium')
        project.color = request.POST.get('color', '#3B82F6')
        project.save()
        
        messages.success(request, 'Проект успешно обновлен!')
        return redirect('projects_list')
    
    return render(request, 'core/edit_project.html', {'project': project})

@login_required
def delete_project(request, project_id):
    """Удаление проекта"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Проект "{project_title}" удален!')
        return redirect('projects_list')
    
    return render(request, 'core/delete_project.html', {'project': project})

# ===== PROFILE =====
@login_required
def profile(request):
    """Страница профиля пользователя"""
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    projects_count = Project.objects.filter(owner=user).count()
    tasks_count = Task.objects.filter(assigned_to=user).count()
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'projects_count': projects_count,
        'tasks_count': tasks_count,
    }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    """Редактирование профиля"""
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Обновляем данные пользователя
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        # Обновляем настройки профиля
        user_profile.theme = request.POST.get('theme', 'light')
        user_profile.email_notifications = 'email_notifications' in request.POST
        user_profile.task_notifications = 'task_notifications' in request.POST
        user_profile.deadline_notifications = 'deadline_notifications' in request.POST
        user_profile.save()
        
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')
    
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'core/edit_profile.html', context)

@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно: обновляем сессию
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'core/change_password.html', {'form': form})

@login_required
def delete_account(request):
    """Удаление аккаунта"""
    if request.method == 'POST':
        user = request.user
        username = user.username
        user.delete()
        messages.success(request, f'Аккаунт {username} удален.')
        return redirect('home')
    
    return render(request, 'core/delete_account.html')
