from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/create/form/', views.TaskCreateFormView.as_view(), name='task_create_form'),
    path('tasks/<int:task_id>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # login modal
    path('login/form/', views.LoginView.as_view(), name='login_form'),
    path('login-submit/', views.LoginView.as_view(), name='login_submit'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
]
