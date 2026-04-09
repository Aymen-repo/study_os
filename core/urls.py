from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # app
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subject/create/', views.create_subject, name='create_subject'),
    path('subject/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:pk>/add-task/', views.add_task, name='add_task'),
    path('subject/<int:subject_pk>/toggle/<int:task_pk>/', views.toggle_task, name='toggle_task'),
]