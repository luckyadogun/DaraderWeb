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