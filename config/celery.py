import os
from celery import Celery
from celery.schedules import crontab

# Указываем стандартный модуль настроек Django для 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('job_market_analytics')

# Используем строку настроек из django.conf:settings, имеющую префикс 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружаем модули tasks.py из всех зарегистрированных приложений Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')