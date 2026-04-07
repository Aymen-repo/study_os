from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("subject/new/", views.create_subject, name="create_subject"),
    path("subject/<int:pk>/", views.subject_detail, name="subject_detail"),
    path("task/toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),
]