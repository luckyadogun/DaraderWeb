from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .manager import CustomUserManager


class User(AbstractUser):
    username = models.CharField(_("username"), max_length=100, unique=True)
    email = models.EmailField(_("email"), max_length=250, unique=True)
    password = models.CharField(_("password"), max_length=200)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_active = models.BooleanField(_("active user"), default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
