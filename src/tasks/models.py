from django.db import models

from utils.models import TimedMixin


class TaskStatusEnum(models.TextChoices):
    PENDING = "pending", "Запланировано"
    IN_PROGRESS = "in_progress", "Выполняется"
    COMPLETED = "completed", "Выполнено"
    ERROR = "error", "Ошибка"


class TaskTypeEnum(models.TextChoices):
    SUM = "sum", "Сумма двух чисел"
    COUNTDOWN = "countdown", "Обратный отсчёт"


class Task(
    TimedMixin,
    models.Model,
):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    task_type = models.CharField(
        max_length=20,
        choices=TaskTypeEnum.choices,
    )
    input_data = models.JSONField()
    status = models.CharField(
        max_length=20,
        choices=TaskStatusEnum.choices,
        default=TaskStatusEnum.PENDING,
    )
    result = models.JSONField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_task_type_display()} - {self.get_status_display()}"

    @property
    def is_active(self) -> bool:
        return self.status in [
            TaskStatusEnum.PENDING,
            TaskStatusEnum.IN_PROGRESS,
        ]
