"""
Django settings for backtest project.

Any settings with "our" in comments are ours.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/

7 May 2021 - Using dotenv to load some security sensitive settings.
             Split into base + dev or prod settings which is decided by
             the env.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Our Vendor apps
    'django.contrib.sites', # Needed by allauth
    'crispy_forms',
    # AllAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Allow oauth2 with google (example only)
    # 'allauth.socialaccount.providers.google',
    # Calculation
    'mathfilters',
    # Our Apps
    'runtest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Our Middlewares
    'runtest.threadlocals.ThreadLocals', # stash login user for own use
]

ROOT_URLCONF = 'backtest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Ours: Allow project wide templates too
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Our Vendor: `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'backtest.wsgi.application'

# django 3.2 requires this
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    # django default
    'django.contrib.auth.backends.ModelBackend',
    # Our Vendor: `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Our settings follows...
APP_NAME = 'theCube'

# allauth needs this
SITE_ID = 1

# Our Vendor settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Allow project wide static files (else default is app static files only)
STATICFILES_DIRS = [BASE_DIR / 'static']

# Stock Price Data directory
STOCK_DIR = BASE_DIR / 'stockdata'
# Directory for result files from backtest runs
RESULTS_DIR = BASE_DIR / 'results'

# allauth settings
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_AUTHENTICATION_METHOD = 'username' # username, email, username_email
# Implement email login later
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'optional' # optional, mandatory, none

# Auth settings
LOGIN_URL = 'accounts/login'
LOGIN_REDIRECT_URL = 'home' # Redirect to home after login

# End our settings
