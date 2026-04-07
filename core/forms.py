from django import forms
from .models import Subject, Task


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]