from django.db import models
from django import forms
from django.utils import timezone 
from django.contrib.auth.models import User, auth 
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals

# Create your models here.

    

class Task(models.Model):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (TODO, 'Todo'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),   
    ]
    taskTitle = models.CharField(max_length=255)
    taskDesc = models.TextField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default=TODO)
    due_date = models.DateTimeField(null=True, blank= True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'assigned_tasks' , null= True)  
    admin_assigned = models.BooleanField(default=False)
    submission = models.TextField(blank=True , null= True)

    def __str__(self):
        return self.taskTitle
    
    
        
class UserProfile(models.Model):
     
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('regular', 'Regular')], default='regular')
    notifications_enabled = models.BooleanField(default=True)
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)              


