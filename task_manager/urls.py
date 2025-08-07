from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_update_view, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete_view, name='task_delete'),
]
