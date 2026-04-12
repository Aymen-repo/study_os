from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .models import Subject, Task
from .forms import SubjectForm, TaskForm


def home(request):
    return render(request, 'home.html')


# ================= AUTH ================= #

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully 🎉")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below")

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back 👋")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ================= APP ================= #

@login_required
def dashboard(request):
    user = request.user

    subjects = Subject.objects.filter(user=user).prefetch_related('tasks')
    all_tasks = Task.objects.filter(subject__user=user)

    return render(request, 'dashboard.html', {
        'subjects': subjects,
        'total_tasks': all_tasks.count(),
        'completed_tasks': all_tasks.filter(done=True).count(),
        'remaining_tasks': all_tasks.filter(done=False).count(),
    })


@login_required
def create_subject(request):
    form = SubjectForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        subject = form.save(commit=False)
        subject.user = request.user
        subject.save()
        return redirect('subject_detail', pk=subject.pk)

    return render(request, 'create_subject.html', {'form': form})


@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    tasks = subject.tasks.all().order_by('created_at')

    done_count = tasks.filter(done=True).count()

    return render(request, 'subject_details.html', {
        'subject': subject,
        'tasks': tasks,
        'incomplete_tasks': tasks.filter(done=False),
        'completed_tasks': tasks.filter(done=True),
        'progress': subject.progress,
        'task_form': TaskForm(),
        'done_count': done_count,
    })


@login_required
def add_task(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)

    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.subject = subject
        task.save()

    return redirect('subject_detail', pk=pk)


@login_required
def toggle_task(request, subject_pk, task_pk):
    subject = get_object_or_404(Subject, pk=subject_pk, user=request.user)
    task = get_object_or_404(Task, pk=task_pk, subject=subject)

    task.done = not task.done
    task.save()

    tasks = subject.tasks.all()
    total = tasks.count()
    done = tasks.filter(done=True).count()

    return JsonResponse({
        'success': True,
        'done': task.done,
        'progress': round(done / total * 100) if total else 0,
        'done_count': done,
        'total_count': total,
    })


# ================= DELETE TASK ================= #

@login_required
def delete_task(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk, subject__user=request.user)
        task.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


# ================= DELETE SUBJECT (FIXED) ================= #

@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)

    if request.method == "POST":
        subject.delete()
        return redirect('dashboard')

    return redirect('subject_detail', pk=pk)