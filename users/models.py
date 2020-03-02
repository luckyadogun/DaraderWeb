from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from .abstract import TimeStampedModel
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


class Agent(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    fullname = models.CharField(
        _("fullname or company name"), max_length=200)
    company_name = models.CharField(
        _("company name"), max_length=200, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the "
                "format: '+999999999'. Up to 15 digits allowed.")
    office_phone = models.CharField(validators=[phone_regex], max_length=17)
    mobile_phone = models.CharField(validators=[phone_regex], max_length=17)
    about_me = models.TextField(_("about"), blank=True, null=True)

    def _get_agent(self):
        return "{0} {1}".format(self.fullname, self.company_name)

    def __str__(self):
        return self._get_agent()
