import json

from pathlib import Path
from os import getenv, path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

if path.exists(env_path := path.join(BASE_DIR, ".env")):
    load_dotenv(env_path)

# Telegram bot data
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")

TELEGRAM_CHAT_ID = getenv("CHAT_ID")

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Moscow"

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "django-db"

# Celery task timeouts
SYNC_DB_GHEETS_TASK_TIMEOUT = 300.0

CHECK_DELIVERY_DATE = 300.0

# Dict or .json file for access to Google sheet
GOOGLE_ACCESS_JSON = json.loads(getenv("GOOGLE_ACCESS_JSON"))

# Google sheet ID
ORDERS_GOOGLE_SHEET = getenv("ORDERS_GOOGLE_SHEET")

ALLOWED_HOSTS = tuple(getenv("ALLOWED_HOSTS", "localhost").rsplit())

SECRET_KEY = getenv("DJANGO_SECRET", "django insecure")

DEBUG = getenv("DEBUG", "False") == "True"

ROOT_URLCONF = "OrderParser.urls"

TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/backend_static/"

STATIC_ROOT = path.join(BASE_DIR, "static")

MEDIA_URL = "/backend_media/"

MEDIA_ROOT = path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WSGI_APPLICATION = "OrderParser.wsgi.application"

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "api.apps.ApiConfig",
]

THIRD_PARTY_APPS = [
    "django_celery_beat",
    "django_celery_results",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": getenv("DB_NAME", "db.sqlite3"),
        "USER": getenv("DB_USER", "postgres"),
        "PASSWORD": getenv("DB_PASSWORD", "postgres"),
        "HOST": getenv("DB_HOST", "localhost"),
        "PORT": getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
