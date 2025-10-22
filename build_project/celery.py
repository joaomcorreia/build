import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'build_project.settings')

app = Celery('build_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure Celery to work with multi-tenant setup
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    
    # Task routing for tenant-specific tasks
    task_routes={
        'ai_tools.tasks.*': {'queue': 'ai_processing'},
        'media_library.tasks.*': {'queue': 'media_processing'},
        'websites.tasks.*': {'queue': 'website_operations'},
    },
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    
    # Rate limiting
    task_annotations={
        'ai_tools.tasks.generate_content': {'rate_limit': '10/m'},
        'ai_tools.tasks.generate_image': {'rate_limit': '5/m'},
        'media_library.tasks.optimize_image': {'rate_limit': '20/m'},
    }
)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')