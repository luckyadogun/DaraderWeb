import os

DEBUG = True
SECRET_KEY = os.environ.get('DJANGO_SECRET')
ENVIRONMENT = "tests"

ALLOWED_HOSTS = ["*"]

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "PORT": 5432,
        "NAME": DB_NAME,
        "HOST": "localhost",
        "ATOMIC_REQUESTS": True,
    }
}