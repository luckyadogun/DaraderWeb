import os
import dj_database_url

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET')
ENVIRONMENT = "tests"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

