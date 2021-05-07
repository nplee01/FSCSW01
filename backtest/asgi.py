"""
ASGI config for backtest project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import dotenv

from django.core.asgi import get_asgi_application

# Load .env from parent directory
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
# Default is fot development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backtest.settings.dev')

# Allow .env to override for production
if os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE')

application = get_asgi_application()
