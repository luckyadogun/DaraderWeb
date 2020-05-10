import os
import dj_database_url

DEBUG = True
SECRET_KEY = os.environ.get('DJANGO_SECRET')

ENVIRONMENT = "live"
DEBUG = False
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "darader.herokuapp.com",
    "infinite-mountain-88972.herokuapp.com",
    "darader.com",
    ]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
