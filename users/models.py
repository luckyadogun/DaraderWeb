from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .manager import CustomUserManager


class User(AbstractUser):
    username = models.CharField(_("username"), max_length=100, unique=True)
    email = models.EmailField(_("email"), max_length=250, unique=True)
    is_staff = models.BooleanField(_("staff"), default=False, blank=True)
    is_admin = models.BooleanField(_("admin"), default=False, blank=True)
    is_account_manager = models.BooleanField(_("account manager"), default=False, blank=True, null=True)
    is_active = models.BooleanField(_("active user"), default=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
