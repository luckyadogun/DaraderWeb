from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model managers where email is the unique identifiers
    for authentication instead of username
    """
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User must have a username.")

        if email is None:
            raise TypeError("User must have an email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and save a Superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)

        return user
