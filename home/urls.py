"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home, task, delete_task, change_status, change_task , login_view, logout_view, signup, search_feature, CustomPasswordResetView, admin_task, create_admin_task, notify_assigned_user, view_notifications
from home import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.signup, name='signup'),
    path('login/', views.login_view , name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', views.home, name='home'),
    path('tasks/', views.task, name='tasks'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
    path('search/ ', search_feature, name= 'search_feature'),
    path('change-status/<int:pk>/', change_status, name='change_status'),   
    path('change-task/<int:task_id>/', change_task, name='change_task'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/login/'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin-tasks/', views.admin_task, name='admin_tasks'),
    path('create-admin-task/', views.create_admin_task, name='create_admin_task'),
    path('notify-assigned-user', views.notify_assigned_user, name='notify_assigned_user'),
    path('view-notifications', views.view_notifications, name='view_notifications'),


]

