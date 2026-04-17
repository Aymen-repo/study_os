from django import forms
from .models import Subject, Task, Profile
from django.contrib.auth.models import User


# ================= SUBJECT FORM =================
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'color']


# ================= TASK FORM =================
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']


# ================= USER UPDATE FORM =================
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# ================= PROFILE UPDATE FORM =================
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']