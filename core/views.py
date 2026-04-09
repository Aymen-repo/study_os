from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Subject, Task
from .forms  import SubjectForm, TaskForm


def home(request):
    return render(request, 'home.html')



def dashboard(request):
    # SAFE FIX: fallback user if not logged in
    user = request.user if request.user.is_authenticated else None

    subjects = Subject.objects.filter(user=user).prefetch_related('tasks')
    all_tasks = Task.objects.filter(subject__user=user)

    total_tasks     = all_tasks.count()
    completed_tasks = all_tasks.filter(done=True).count()
    remaining_tasks = all_tasks.filter(done=False).count()

    return render(request, 'dashboard.html', {
        'subjects':        subjects,
        'total_tasks':     total_tasks,
        'completed_tasks': completed_tasks,
        'remaining_tasks': remaining_tasks,
    })



def create_subject(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = form.save(commit=False)
        subject.user = request.user
        subject.save()
        return redirect('subject_detail', pk=subject.pk)
    return render(request, 'create_subject.html', {'form': form})



def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    tasks   = subject.tasks.all().order_by('created_at')

    incomplete_tasks = tasks.filter(done=False)
    completed_tasks  = tasks.filter(done=True)
    done_count       = completed_tasks.count()
    progress         = subject.progress

    task_form = TaskForm()

    return render(request, 'subject_detail.html', {
        'subject':          subject,
        'tasks':            tasks,
        'incomplete_tasks': incomplete_tasks,
        'completed_tasks':  completed_tasks,
        'done_count':       done_count,
        'progress':         progress,
        'task_form':        task_form,
    })




def add_task(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    task_form = TaskForm(request.POST)
    if task_form.is_valid():
        task = task_form.save(commit=False)
        task.subject = subject
        task.save()
    return redirect('subject_detail', pk=pk)




def toggle_task(request, subject_pk, task_pk):
    subject = get_object_or_404(Subject, pk=subject_pk, user=request.user)
    task    = get_object_or_404(Task, pk=task_pk, subject=subject)
    task.done = not task.done
    task.save()

    # Return JSON for the AJAX toggle in subject_detail.html
    tasks       = subject.tasks.all()
    total_count = tasks.count()
    done_count  = tasks.filter(done=True).count()
    progress    = round(done_count / total_count * 100) if total_count else 0

    return JsonResponse({
        'success':     True,
        'done':        task.done,
        'progress':    progress,
        'done_count':  done_count,
        'total_count': total_count,
    })