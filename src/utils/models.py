import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


class TimedMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Дата "ленивого" удаления',
    )

    class Meta:
        abstract = True


@deconstructible
class RandomFileName:
    def __init__(self, path):
        self.path = os.path.join(path, "%s_%s")

    def __call__(self, _, filename) -> str:
        return self.path % (uuid.uuid4().hex, filename)
