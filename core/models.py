from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    color = models.CharField(max_length=7, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В процессе'),
        ('review', 'На проверке'),
        ('done', 'Выполнено'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, choices=[('light', 'Светлая'), ('dark', 'Темная'), ('auto', 'Авто')], default='light')
    email_notifications = models.BooleanField(default=True)
    task_notifications = models.BooleanField(default=True)
    deadline_notifications = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Профиль {self.user.username}'
