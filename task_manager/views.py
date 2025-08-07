from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .forms import TaskForm
from .models import Task
from .serializers import TaskSerializer
import logging
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

logger = logging.getLogger('tareas')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['created_at', 'completed']
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

def htmx_redirect(path):
    response = HttpResponse()
    response['HX-Redirect'] = path
    return response

def handle_task_form(request, form, log_template):
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        logger.info(log_template.format(
            user=request.user.username,
            id=task.id,
            title=task.title
        ))
        return htmx_redirect('/')
    return None

def index(request):
    tasks = Task.objects.filter(user=request.user.id).order_by('-created_at')
    created_at = request.GET.get('created_at')
    q = request.GET.get('q')

    if created_at:
        tasks = tasks.filter(created_at__date=created_at)
    if q:
        tasks = tasks.filter(title__icontains=q)

    return render(request, 'task_manager/index.html', {'tasks': tasks})

class TaskCreateFormView(LoginRequiredMixin, TemplateView):
    template_name = 'task_manager/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        logger.info(f"Tarea creada por {self.request.user.username}, ID={task.id}, titulo={task.title}")
        return htmx_redirect('/')

class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        logger.info(f"Tarea eliminada por {request.user.username}, ID={task_id}")
        return htmx_redirect('/')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        task = form.save()
        logger.info(f"Tarea actualizada por {self.request.user.username}, ID={task.id}, titulo={task.title}")
        return htmx_redirect('/')

@require_http_methods(["GET"])
def login_form_view(request):
    form = AuthenticationForm()
    return render(request, 'task_manager/login_form.html', {'form': form})

@require_http_methods(["POST"])
def login_submit_view(request):
    form = AuthenticationForm(data=request.POST)

    if form.is_valid():
        login(request, form.get_user())

        if request.headers.get('Hx-Request') == 'true':
            html = render_to_string('task_manager/login_success.html', {'user': form.get_user()})
            return HttpResponse(html)
        return redirect('index')
    return render(request, 'task_manager/login_form.html', {'form': form})

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    if request.headers.get("Hx-Request") == "true":
        html = render_to_string('task_manager/login_button.html')
        return HttpResponse(html)
    return redirect('index')