import json
import time

import structlog
from celery import shared_task
from django.db import transaction

from .models import Task
from .models import TaskStatusEnum

logger = structlog.get_logger(__name__)


@shared_task
@transaction.atomic
def sum_two_numbers(task_id: int) -> None:
    """
    Task to sum two numbers.
    """
    log = logger.bind(task_id=task_id)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        log.warning("Task with id %s does not exist", task_id)
        return

    try:
        # Update task status to in progress
        task.status = TaskStatusEnum.IN_PROGRESS
        task.save()

        # Extract input data
        data = json.loads(task.input_data)
        num1 = float(data.get("num1", 0))
        num2 = float(data.get("num2", 0))

        # Calculate sum
        result = num1 + num2

        # Update task with result
        task.result = {"sum": result}
        task.status = TaskStatusEnum.COMPLETED
        task.save()
    except Exception as e:
        # Handle any errors
        task.status = "error"
        task.result = {"error": str(e)}
        task.save()


@shared_task
def countdown(task_id: int) -> None:
    """
    Task to perform a countdown for a specified number of seconds.
    """
    log = logger.bind(task_id=task_id)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        log.warning("Task with id %s does not exist", task_id)
        return

    try:
        # Update task status to in progress
        task.status = TaskStatusEnum.IN_PROGRESS
        task.save()

        # Extract input data
        data = task.input_data
        seconds = float(data.get("seconds", 0))

        # Perform countdown (sleep)
        time.sleep(seconds)

        # Update task with result
        message = "Обратный отсчёт завершён"
        task.result = {"message": message}
        task.status = TaskStatusEnum.COMPLETED
        task.save()
    except Exception as e:
        # Handle any errors
        task.status = TaskStatusEnum.ERROR
        task.result = {"error": str(e)}
        task.save()
