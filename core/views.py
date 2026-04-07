from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Task
from .forms import SubjectForm, TaskForm
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"subjects": subjects})


@login_required
def create_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect("dashboard")
    else:
        form = SubjectForm()
    return render(request, "create_subject.html", {"form": form})


@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, id=pk, user=request.user)
    tasks = subject.tasks.all()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.subject = subject
            task.save()
            return redirect("subject_detail", pk=pk)
    else:
        form = TaskForm()

    return render(request, "subject_detail.html", {
        "subject": subject,
        "tasks": tasks,
        "form": form
    })


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, subject__user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect("subject_detail", pk=task.subject.id)
