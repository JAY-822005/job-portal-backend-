"""
Celery configuration for Job Portal Backend API
"""

import os
from celery import Celery

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app
app = Celery('job_portal')

# Configure from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Configuration
app.conf.update(
    # Broker settings
    broker_url=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    
    # Serialization
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task settings
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    
    # Retry policy
    task_autoretry_for=(Exception,),
    task_max_retries=3,
    task_default_retry_delay=60,
    
    # Worker settings
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    
    # Beat scheduler
    beat_schedule={
        # Run daily cleanup at midnight
        'cleanup-expired-tokens': {
            'task': 'accounts.tasks.cleanup_expired_tokens',
            'schedule': 86400.0,  # 24 hours
        },
        # Send job recommendations weekly
        'send-job-recommendations': {
            'task': 'jobs.tasks.send_job_recommendations',
            'schedule': 604800.0,  # 7 days
        },
        # Close expired job listings daily
        'close-expired-jobs': {
            'task': 'jobs.tasks.close_expired_jobs',
            'schedule': 86400.0,  # 24 hours
        },
    },
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
