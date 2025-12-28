import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlowPlus.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Project, Task

# Создаем тестового пользователя, если его нет
try:
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print(f'Создан пользователь: {user.username}')
except:
    user = User.objects.get(username='testuser')
    print(f'Пользователь уже существует: {user.username}')

# Создаем тестовые проекты
projects_data = [
    {
        'title': 'Разработка сайта',
        'description': 'Создание корпоративного сайта компании'
    },
    {
        'title': 'Маркетинговая кампания',
        'description': 'Запуск рекламной кампании в соцсетях'
    },
    {
        'title': 'Внутренняя документация',
        'description': 'Обновление внутренней документации команды'
    },
]

for i, data in enumerate(projects_data):
    project, created = Project.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'owner': user
        }
    )
    if created:
        print(f'Создан проект: {project.title}')
        
        # Создаем задачи для проекта
        tasks_data = [
            {
                'title': f'Задача {j+1} для {project.title}',
                'description': f'Описание задачи {j+1}',
                'status': 'todo' if j % 3 == 0 else 'in_progress' if j % 3 == 1 else 'done'
            }
            for j in range(3)
        ]
        
        for task_data in tasks_data:
            task = Task.objects.create(
                title=task_data['title'],
                description=task_data['description'],
                project=project,
                assigned_to=user,
                status=task_data['status'],
                created_by=user
            )
            print(f'  Создана задача: {task.title}')

print('Тестовые данные созданы успешно!')
