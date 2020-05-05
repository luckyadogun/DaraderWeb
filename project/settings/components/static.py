import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

if os.environ.get("ENVIRONMENT") != "local":
    AWS_ACCESS_KEY_ID = os.environ.get(AWS_ACCESS_KEY_ID)
    AWS_SECRET_ACCESS_KEY = os.environ.get(AWS_ACCESS_KEY_ID)
    AWS_STORAGE_BUCKET_NAME = 'darader-assets'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amamzonaws' % AWS_STORAGE_BUCKET_NAME

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_LOCATION = 'static'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

    DEFAULT_FILE_STORAGE = 'storage_backend.MediaStorage'
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'