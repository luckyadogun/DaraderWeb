from datetime import timedelta
AUTHENTICATION_BACKENDS = (
    'users.auth.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Rest framework authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=52),
}