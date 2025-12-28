from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Projects
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
]
