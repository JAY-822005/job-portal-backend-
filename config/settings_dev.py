"""
Development settings for Job Portal Backend API.
"""

from .settings_base import *

DEBUG = True
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# Development database (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Development email backend (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS for development
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:5173',
]

# Development secret key (NOT FOR PRODUCTION)
SECRET_KEY = 'django-insecure-@xo$8@-ihpd8fb$o$#gbzwq8(skv0wtn+(iufjs9@h-8sbjuv*'

# Celery for development (synchronous execution)
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
