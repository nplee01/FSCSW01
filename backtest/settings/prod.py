# Production settings
import os

# Import everything from base
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CUBE_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', 'web', 'minikube.local', 'thecube.atsc.org.my']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('CUBE_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('CUBE_DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('CUBE_DB_USER', 'user'),
        'PASSWORD': os.environ.get('CUBE_DB_PASSWORD', 'password'),
        'HOST': os.environ.get('CUBE_DB_HOST', 'localhost'),
        'PORT': os.environ.get('CUBE_DB_PORT', ''),
    }
}

# Our Vendor: Allauth social Provider specific settings
"""
Note: Either create a row in socialaccount model or add the key here.

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}
"""

# Later: In production, must use https
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
