from django.shortcuts import render, redirect, get_object_or_404 
from .forms import TaskForm, SignupForm, PasswordResetForm , AssignedTasks
from .models import Task , UserProfile, Notification 
from home import views 
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout as auth_logout , login as auth_login , get_user_model
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required , user_passes_test, permission_required 
from django.db import IntegrityError
from django.core.mail import send_mail 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.core.exceptions import ValidationError

# Create your views here.


@login_required
def home(request):
    context = {'success': False}


    # Task Form for creating tasks
    task_form = TaskForm(request.POST or None)

    # Assign Task Form for assigning tasks to users
    assign_task_form = AssignedTasks(request.POST or None)

    if request.method == "POST":
        if 'create_task' in request.POST:
            # Handle the TaskForm submission for creating tasks
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.user = request.user
                task.save()
                context = {'success': True}
                messages.success(request, "Task has been saved successfully")
            else:
                for field, errors in task_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        elif 'assign_task' in request.POST:
            # Handle the AssignTaskForm submission for assigning tasks to users
            if assign_task_form.is_valid():
                task = assign_task_form.save(commit=False)
                task.user = request.user
                task.admin_assigned = True
                task.save()
                context = {'success': True}
                messages.success(request, "Task has been assigned successfully")
                notify_assigned_user(request, task)
            else:
                for field, errors in assign_task_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    
    context['task_form'] = task_form
    context['assign_task_form'] = assign_task_form

    return render(request, 'index.html', context)


@login_required
def task(request):
    
    tasks = Task.objects.filter(Q(user=request.user) | Q(assigned_to=request.user)).order_by('-time')

    page = request.GET.get('page', 1)
    paginator = Paginator(tasks, 5)  # Show 10 tasks per page
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'task.html', {'tasks': tasks})

      
@login_required
@permission_required('home.can_add_task', raise_exception=True)
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Assign the task to the current user
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            
            messages.success(request, 'Task added successfully.')
            return redirect('tasks')
    else:
        form = TaskForm()

    return render(request, 'index.html', {'form': form})


@login_required
@permission_required('home.change_task', raise_exception=True)
def change_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    print("User Permissions:", request.user.get_all_permissions())  # users has permission or not 


    if request.method == 'POST':
        # Handle form submission and update task details
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request,"Task edited successfully")

            return redirect('tasks')
    else:

        initial_data =  {

           'new_task_title': task.taskTitle,
            'new_task_desc': task.taskDesc,

        }

    
        form = TaskForm (initial=initial_data)
        
    return render(request, 'change_task.html', {'form': form, 'task': task})  


@login_required
@permission_required('home.delete_task', raise_exception=True)
def delete_task(request, pk):
    print("User Permissions:", request.user.get_all_permissions())  # users have permission or not 

    task= Task.objects.get(pk=pk)
    task.delete()
    messages.success(request,"Task Deleted Successfully")
    return redirect('tasks')


def change_status(request,pk):

    task=get_object_or_404(Task, pk=pk)


    if request.method =="POST":
        new_status= request.POST.get('new_status')
        task.status = new_status
        task.save()
        
       
    return redirect('tasks')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if form.is_valid():
            user = User.objects.create_user(username=username, email=email, password=password)
            user_profile = UserProfile(user=user, role='regular')
            user_profile.save()
            messages.success(request, "Your account has been created successfully. You can log in here.")
            return redirect('login_view')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('signup')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method =="POST":
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')

        user = authenticate(username=loginusername, password=loginpassword)
        
        if user is not None:
            auth.login(request,user)
            messages.success(request, "you're logged in successfully")

            return redirect('tasks')
        else:
            messages.error(request, "Please Enter Valid Credentials")
    return render (request,'login.html')

def logout_view(request):
    
    if request.method =="POST":
      auth.logout(request)
      messages.success(request,"you're successfully logged out")
      
      return redirect ('home')
    
    return render(request, 'logout.html')



def search_feature(request):
    search_query = request.POST.get('search[value]', '')
    
    user_tasks = Task.objects.filter(user=request.user)
    assigned_by_admin = Task.objects.filter(assigned_to=request.user)

    if search_query:
        tasks = Task.objects.filter(
            Q(taskTitle__icontains=search_query) |
            Q(taskDesc__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(assigned_to__username__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).filter(Q(user=request.user) | Q(id__in=assigned_by_admin))
    else:
        tasks = user_tasks.none()
     
    data = []
    for task in tasks:
        data.append({
            'id': task.id,
            'user': task.user.username,
            'taskTitle': task.taskTitle,
            'taskDesc': task.taskDesc,
            'status': task.status,
            'assigned_to': task.assigned_to.username if task.assigned_to else '',
        }) 

    response_data = {
        'draw': 1,
        'recordsTotal': len(data),
        'recordsFiltered': len(data),
        'data': data,
    }

    return JsonResponse(response_data)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/reset_password_sent/'
   
   
@login_required
@user_passes_test(lambda u: u.userprofile.role == 'admin', login_url='/login/')
def admin_task(request):
        print(f"User role: {request.user.userprofile.role}")

        if request.user.userprofile.role == 'admin':
    
            all_tasks = Task.objects.all()  # Fetch all tasks, not just tasks of the current user
            return render(request, 'admin_task.html', {'all_tasks': all_tasks})
        else:
            assigned_tasks = Task.objects.filter(assigned_tasks=request.user)
            return render(request, 'admin_task.html', {'assigned_tasks': assigned_tasks})   


@login_required
def create_admin_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.admin_assigned = True
            task.save()

            if request.user.userprofile.role == 'regular':
                # Update the submission field for regular users
                task.submission = request.POST.get('submission', '')
                task.save()

                # Notify the admin about the submission
                notify_admin_submission(request, task)

            messages.success(request, 'Task Created Successfully')

            return redirect('admin_tasks')
    else:
        form = TaskForm()

    return render(request, 'create_admin_task.html', {'form': form})


User = get_user_model()
    
def notify_assigned_user(request, task):
    if task.assigned_to and task.assigned_to.userprofile.notifications_enabled and not task.assigned_to.is_staff   and not request.user.userprofile.role == 'admin':
        message= f" You have been assigned a new task: {task.taskTitle} - {task.taskDesc} - Due Date: {task.due_date}"
        messages.info(request,message)
        
            # save the notification to database
        notification = Notification(user=task.assigned_to, message=message)
        notification.save()
        
@login_required
def view_notifications(request):
    # fetch notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user)
    print("Notifications:", notifications)  
    return render(request, 'notifications.html', {'notifications': notifications})


def notify_admin_submission(request, task):
    admin_users = User.objects.filter(userprofile__role='admin')
    message = f"User {task.user.username} has submitted a task: {task.taskTitle} - {task.submission}"

    for admin_user in admin_users:
        messages.info(request, f"Task submitted by {task.user.username} - {task.taskTitle}")
        # Save the notification to the database 
        notification = Notification(user=admin_user, message=message)
        notification.save()


