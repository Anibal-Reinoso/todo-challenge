from rest_framework import viewsets, filters
from django.contrib.auth.decorators import login_required
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .forms import TaskForm
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
import logging

logger = logging.getLogger('tareas')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['created_at', 'completed']
    search_fields = ['title', 'description']

def index(request):
    tasks = Task.objects.all().order_by('-created_at')
    created_at = request.GET.get('created_at')
    q = request.GET.get('q')

    if created_at:
        tasks = tasks.filter(created_at__date=created_at)
    if q:
        tasks = tasks.filter(title__icontains=q)

    return render(request, 'task_manager/index.html', {'tasks': tasks})

def task_create_form_view(request):
    form = TaskForm()
    return render(request, 'task_manager/task_form.html', {'form': form})

@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            response = HttpResponse()
            response['HX-Redirect'] = '/'
            logger.info(f"Tarea creada por {request.user.username}, ID={task.id}, titulo={task.title}")
            return response
    else:
        form = TaskForm()

    return render(request, 'task_manager/task_form.html', {'form': form})

@require_POST
@login_required
def task_delete_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    logger.info(f"Tarea eliminada por {request.user.username}, ID={task_id}")
    response = HttpResponse()
    response['HX-Redirect'] = '/'
    logger.info(f"Tarea eliminada por {request.user.username}, ID={task_id}")
    return response

@require_http_methods(["GET", "POST"])
@login_required
def task_update_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            response = HttpResponse()
            response['HX-Redirect'] = '/'
            logger.info(f"Tarea actualizada por {request.user.username}, ID={task.id}")
            return response
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_manager/task_form.html', {'form': form, 'task': task})