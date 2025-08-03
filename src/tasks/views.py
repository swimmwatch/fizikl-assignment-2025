from http import HTTPMethod

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework import permissions

from .models import Task
from .models import TaskTypeEnum
from .permissions import ActiveTaskLimitPermission
from .serializers import TaskSerializer
from .tasks import countdown
from .tasks import sum_two_numbers


class TaskListCreateView(generics.ListCreateAPIView):
    """
    View for listing all tasks and creating new tasks.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filterset_fields = ["status"]

    def get_permissions(self):
        if self.request.method == HTTPMethod.POST:
            return [
                permissions.IsAuthenticated(),
                ActiveTaskLimitPermission(),
            ]
        return [permissions.IsAuthenticated()]

    def get_queryset(self) -> QuerySet[Task]:
        user = self.request.user

        # Filter tasks by current user
        queryset = self.queryset.filter(user=user)

        return queryset

    def perform_create(self, serializer: TaskSerializer) -> None:
        task_map = {
            TaskTypeEnum.SUM: sum_two_numbers,
            TaskTypeEnum.COUNTDOWN: countdown,
        }

        # Save the task with the current user
        task = serializer.save(user=self.request.user)

        # Start the appropriate Celery task based on task_type
        task_map.get(task.task_type).delay(task.id)


class TaskDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a specific task.
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Task]:
        # Filter tasks by current user
        user = self.request.user
        return Task.objects.filter(user=user)
