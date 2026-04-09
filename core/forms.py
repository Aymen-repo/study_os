from django import forms
from .models import Subject, Task


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter subject name...',
                'class': 'input'
            })
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Add a task...',
                'class': 'input'
            })
        }