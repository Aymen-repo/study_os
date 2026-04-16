from django import forms
from .models import Subject, Task


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'color']  # color enabled

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter subject name...',
                'class': 'input'
            }),

            # 🎨 improved color picker
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'color-input',
                'style': 'width: 50px; height: 40px; padding: 0; border: none; background: none; cursor: pointer;'
            }),
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