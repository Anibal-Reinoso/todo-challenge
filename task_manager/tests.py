from django.test import TestCase
import logging
from pathlib import Path
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Task

User = get_user_model()

class LoggingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_crear_tarea(self):
        response = self.client.post('/tasks/create/', {
            'user': self.user.id,
            'title': 'Tarea de prueba',
            'description': 'Descripción de prueba',
            'completed': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title='Tarea de prueba').exists())

    def test_eliminar_tarea(self):
        tarea = Task.objects.create(
            title='eliminar',
            user=self.user,
            description='tarea a eliminar',
            completed=False
        )
        response = self.client.post(f'/tasks/{tarea.id}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=tarea.id).exists())

    def test_log_written_to_file(self):
        logger = logging.getLogger('tareas')
        test_message = 'Mensaje de prueba para validar funcionamiento de logging'
        logger.info(test_message)

        log_file = Path(settings.LOG_DIR) / 'tareas.log'
        self.assertTrue(log_file.exists(), "El archivo de log no existe.")

        with open(log_file, 'r') as f:
            logs = f.read()
        self.assertIn(test_message, logs, "El mensaje no se encontró en el log.")
