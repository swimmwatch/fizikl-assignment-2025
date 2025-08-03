from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager
from users.managers import UserQuerySet
from utils.models import TimedMixin


class User(
    AbstractUser,
    PermissionsMixin,
    TimedMixin,
):
    first_name = models.CharField(
        blank=False,
        null=True,
        verbose_name=_("Имя"),
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        verbose_name=_("Фамилия"),
    )
    username = models.CharField(
        unique=True,
        blank=False,
        null=True,
        verbose_name=_("Никнейм"),
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=True,
        verbose_name=_("Email"),
    )

    REQUIRED_FIELDS = ()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "email"
