import os
import dj_database_url

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

ENVIRONMENT = "live"
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "darader.com",
    "www.darader.com",
    ]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
