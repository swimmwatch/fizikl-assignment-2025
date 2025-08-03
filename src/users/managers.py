import typing

import structlog
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

if typing.TYPE_CHECKING:
    from users.models import User


logger = structlog.get_logger(__name__)


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


class UserQuerySet(models.QuerySet):
    pass
