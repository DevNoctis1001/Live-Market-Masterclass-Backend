import os
from .base import *

DEBUG  = False

ALLOWED_HOSTS = ['yourdomain.com']

DATABASES  = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql',
        'NAME' : os.getenv('DB_NAME'),
        'USER' : os.getenv('DB_USER'),
        'PASSWORD' : os.getenv('DB_PASSWORD'),
        'HOST' : os.getenv('DB_HOST', 'localhost'),
        'PORT' : os.getenv('DB_PORT', 5432),
    }
}

# Production-specific security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE  = True
CSRF_COOKIE_SECURE = True