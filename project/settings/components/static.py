import os

import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR + "staticfiles")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', "static"),
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, '..', "mediafiles")

if os.environ.get("ENVIRONMENT") != "local":
    STATICFILES_STORAGE = 'whitenoise.storage.GzipManifestStaticFilesStorage'
