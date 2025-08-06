from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.task_list_view, name='task-list'),
    path('tasks/create-form/', views.task_create_form_view, name='task-create-form'),
    path('tasks/create/', views.task_create_view, name='task-create'),
]
