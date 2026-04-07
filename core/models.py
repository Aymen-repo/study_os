from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_tasks(self):
        return self.tasks.count()

    def done_tasks(self):
        return self.tasks.filter(is_done=True).count()

    def progress(self):
        total = self.total_tasks()
        if total == 0:
            return 0
        return int((self.done_tasks() / total) * 100)


class Task(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title