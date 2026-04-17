from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse

from .models import Subject, Task, Profile
from .forms import SubjectForm, TaskForm


# ================= HOME =================
def home(request):
    return render(request, 'home.html')


# ================= AUTH =================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ================= DASHBOARD =================
@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)

    tasks = Task.objects.filter(subject__user=request.user)

    return render(request, 'dashboard.html', {
        'subjects': subjects,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(done=True).count(),
        'remaining_tasks': tasks.filter(done=False).count(),
    })


# ================= SUBJECT =================
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

    tasks = subject.tasks.all()

    return render(request, 'subject_details.html', {
        'subject': subject,
        'tasks': tasks,
        'incomplete_tasks': tasks.filter(done=False),
        'completed_tasks': tasks.filter(done=True),
        'progress': subject.progress,
        'task_form': TaskForm(),
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

    return JsonResponse({
        'success': True,
        'done': task.done,
        'progress': subject.progress,
    })


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, subject__user=request.user)
    task.delete()
    return JsonResponse({'success': True})


@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)

    if request.method == "POST":
        subject.delete()
        return redirect('dashboard')

    return redirect('subject_detail', pk=pk)


# ================= PROFILE =================
@login_required
def profile_view(request):
    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)

    subjects_count = Subject.objects.filter(user=user).count()
    tasks = Task.objects.filter(subject__user=user)

    completed_tasks = tasks.filter(done=True).count()
    total_tasks = tasks.count()

    progress = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    if request.method == "POST":
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()

        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
            profile.save()

        return redirect('profile')

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'subjects_count': subjects_count,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'progress': progress,
    })