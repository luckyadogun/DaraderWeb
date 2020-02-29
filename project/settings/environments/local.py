DEBUG = True
SECRET_KEY = "SECRET"
ENVIRONMENT = "tests"

ALLOWED_HOSTS = ("localhost", "127.0.0.1")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": "rentalapp",
        "PASSWORD": "rentalapp",
        "PORT": 5432,
        "NAME": "rentalapp",
        "HOST": "localhost",
        "ATOMIC_REQUESTS": True,
    }
}