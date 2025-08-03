from django.http import HttpRequest
from rest_framework import permissions

from .models import Task
from .models import TaskStatusEnum


# TODO: pass the number as parameter
class ActiveTaskLimitPermission(permissions.BasePermission):
    message = "You can't have more than 5 active tasks at the same time"

    def has_permission(self, request: HttpRequest, view):
        user = request.user
        active_tasks_count = Task.objects.filter(
            user=user,
            status__in=[TaskStatusEnum.PENDING, TaskStatusEnum.IN_PROGRESS],
        ).count()
        return active_tasks_count < 5
