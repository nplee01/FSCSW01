# Development settings
import os

# Import everything from base
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CUBE_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# All static files to be copied to single folder for production
# Should be served by nginx or apache (not the wsgi appserver)
STATIC_ROOT = BASE_DIR / 'prod' / 'static'
