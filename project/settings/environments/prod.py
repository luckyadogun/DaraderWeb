import os

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')

ENVIRONMENT = "live"
DEBUG = False
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "darader.com",
    ]

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

SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
