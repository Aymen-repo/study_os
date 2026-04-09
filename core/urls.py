from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.home,            name='home'),
    path('dashboard/',                    views.dashboard,       name='dashboard'),
    path('subjects/create/',              views.create_subject,  name='create_subject'),
    path('subjects/<int:pk>/',            views.subject_detail,  name='subject_detail'),
    path('subjects/<int:pk>/tasks/add/',  views.add_task,        name='add_task'),
    path('subjects/<int:subject_pk>/tasks/<int:task_pk>/toggle/',
                                          views.toggle_task,     name='toggle_task'),
]