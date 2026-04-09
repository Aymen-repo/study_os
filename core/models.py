from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name  = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def task_count(self):
        return self.tasks.count()

    @property
    def done_count(self):
        return self.tasks.filter(done=True).count()

    @property
    def progress(self):
        total = self.task_count
        return round(self.done_count / total * 100) if total else 0

    def __str__(self):
        return self.name


class Task(models.Model):
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tasks')
    title      = models.CharField(max_length=200)
    done       = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title