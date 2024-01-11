from django import forms 
from .models import Task
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['taskTitle', 'taskDesc', 'status', 'submission']
        widgets = {
            'taskTitle': forms.TextInput(attrs={'class': 'TaskTitle'}),
            'taskDesc': forms.Textarea(attrs={'class': 'TaskDesc'}),
            'status': forms.Select(attrs={'class': 'Status'}),
            'submission': forms.TextInput(attrs={'class': 'Submission'}),
        }
    
    def clean_taskTitle(self):
        task_title = self.cleaned_data['taskTitle']

        if len(task_title) < 5:
            raise ValidationError("Task title must be at least 5 characters long.")
   
        if not any(char.islower() for char in 'taskTitle'):
            raise ValidationError("Password must contain lowercase letter.")


        return task_title
        
    def clean_taskDesc(self):
        task_Desc = self.cleaned_data['taskDesc']

        if not task_Desc:
            raise ValidationError("taskDesc cannot blank")
        
        if len(task_Desc)< 10 :
            raise ValidationError("TaskDesc must be more than 10 characters long ")
        
        return task_Desc


class AssignedTasks(forms.ModelForm):
    class Meta:
        model = Task 
        fields = ['taskTitle','taskDesc', 'assigned_to','due_date']
        widgets = {
            'taskTitle': forms.TextInput(attrs={'class': 'tasktitle'}),
            'taskDesc': forms.Textarea(attrs={'class': 'taskDesc'}),
            'assigned_to': forms.Select(attrs={'class': 'assigned_to'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'DueDate'}),
        
        }

    def clean_taskTitle(self):
        task_title = self.cleaned_data['taskTitle']

        if len(task_title) < 5:
            raise ValidationError("Task title must be at least 5 characters long.")
   
        if not any(char.islower() for char in 'taskTitle'):
            raise ValidationError("Password must contain lowercase letter.")


        return task_title
        
    def clean_taskDesc(self):
        task_Desc = self.cleaned_data['taskDesc']

        if not task_Desc:
            raise ValidationError("taskDesc cannot blank")
        
        if len(task_Desc)< 10 :
            raise ValidationError("TaskDesc must be more than 10 characters long ")
        
        return task_Desc

    

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)

    
    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.match(r'^[A-Z][a-z0-9]*$', username):
            raise ValidationError("Username should start with a capital letter and only contain lowercase letters, numbers, and no spaces.")

        return username 
    

    def clean_password(self):
        password = self.cleaned_data['password']

        # Check if the password contains at least one capital letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one capital letter.")

        # Check if the password contains at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Check if the password contains at least one digit
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")

        # Check if the password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if password and password_confirm match
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

class PasswordResetForm(forms.Form):
    email =forms.EmailField( required=True)
