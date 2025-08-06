from rest_framework import viewsets, filters
from django.contrib.auth.decorators import login_required
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .forms import TaskForm

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['created_at', 'completed']
    search_fields = ['title']

def index(request):
    return render(request, 'task_manager/index.html')

def task_list_view(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})

def task_create_form_view(request):
    form = TaskForm()
    return render(request, 'task_manager/task_form.html', {'form': form})

@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # ✅ Asignamos el usuario autenticado
            task.save()
            return render(request, 'task_manager/task_item.html', {'task': task})
    else:
        form = TaskForm()

    return render(request, 'task_manager/task_form.html', {'form': form})
