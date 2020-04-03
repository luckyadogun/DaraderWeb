import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(value):
    pattern = re.compile(r'^\+?1?\d{9,15}$')
    if not bool(pattern.match(value)):
        raise ValidationError(
            _("Invalid! Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
            params={'value': value},)
