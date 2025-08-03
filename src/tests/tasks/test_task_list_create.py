"""
Tests for task list and creation endpoints.
"""

import json

from django.urls import reverse
from rest_framework import status

from tasks.models import Task
from tasks.models import TaskStatusEnum
from tasks.models import TaskTypeEnum
from tests.base import BaseAPITestCase
from tests.factories import TaskFactory
from tests.factories import UserFactory


class TestTaskListCreate(BaseAPITestCase):
    """Tests for task listing and creation endpoint."""

    def setUp(self) -> None:
        """Set up test data for each test."""
        super().setUp()
        self.url = reverse("task-list-create")
        self.create_user()
        self.authenticate()

    def test_list_tasks_empty(self) -> None:
        """Test listing tasks when user has no tasks."""
        response = self.api_call("get", self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_list_tasks_with_tasks(self) -> None:
        """Test listing tasks when user has existing tasks."""
        # Create tasks for the user
        tasks = [TaskFactory(user=self.user) for _ in range(3)]

        # Create tasks for another user (should not be returned)
        another_user = UserFactory()
        TaskFactory(user=another_user)

        response = self.api_call("get", self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        # Verify task IDs match
        task_ids = [task.id for task in tasks]
        response_ids = [task["id"] for task in response.data]
        for task_id in response_ids:
            assert task_id in task_ids

    def test_list_tasks_filter_by_status(self) -> None:
        """Test filtering tasks by status."""
        # Create tasks with different statuses
        TaskFactory(user=self.user, status=TaskStatusEnum.PENDING)
        TaskFactory(user=self.user, status=TaskStatusEnum.IN_PROGRESS)
        TaskFactory(user=self.user, status=TaskStatusEnum.COMPLETED)

        url = f"{self.url}?status={TaskStatusEnum.COMPLETED}"
        response = self.api_call("get", url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["status"] == TaskStatusEnum.COMPLETED

    def test_create_task_sum_success(self) -> None:
        """Test creating a sum task successfully."""
        data = {"task_type": TaskTypeEnum.SUM, "input_data": json.dumps({"num1": 5, "num2": 7})}

        response = self.api_call("post", self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["task_type"] == TaskTypeEnum.SUM
        assert response.data["status"] == TaskStatusEnum.PENDING
        assert response.data["user"] == self.user.username

        # Verify task was created in database
        task = Task.objects.get(id=response.data["id"])
        assert task.task_type == TaskTypeEnum.SUM
        assert json.loads(task.input_data) == {"num1": 5, "num2": 7}

    def test_create_task_countdown_success(self) -> None:
        """Test creating a countdown task successfully."""
        data = {"task_type": TaskTypeEnum.COUNTDOWN, "input_data": json.dumps({"seconds": 10})}

        response = self.api_call("post", self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["task_type"] == TaskTypeEnum.COUNTDOWN
        assert response.data["status"] == TaskStatusEnum.PENDING

        # Verify task was created in database
        task = Task.objects.get(id=response.data["id"])
        assert task.task_type == TaskTypeEnum.COUNTDOWN
        assert json.loads(task.input_data) == {"seconds": 10}

    def test_create_task_invalid_input_data(self) -> None:
        """Test creating a task with invalid input data."""
        data = {"task_type": TaskTypeEnum.SUM, "input_data": json.dumps({"num1": 5})}  # Missing num2

        response = self.api_call("post", self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_invalid_json(self) -> None:
        """Test creating a task with invalid JSON input."""
        data = {"task_type": TaskTypeEnum.SUM, "input_data": "{invalid json}"}

        response = self.api_call("post", self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_unauthenticated(self) -> None:
        """Test creating a task when not authenticated."""
        self.client.logout()

        data = {"task_type": TaskTypeEnum.SUM, "input_data": json.dumps({"num1": 5, "num2": 7})}

        response = self.api_call("post", self.url, data=data, authenticated=False)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_task_limit_reached(self) -> None:
        """Test creating a task when user has reached the active task limit."""
        # Create 5 active tasks (the limit)
        for _ in range(5):
            TaskFactory(user=self.user, status=TaskStatusEnum.PENDING)

        data = {"task_type": TaskTypeEnum.SUM, "input_data": json.dumps({"num1": 5, "num2": 7})}

        response = self.api_call("post", self.url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        # Verify the error message matches what's defined in the permission class
        assert "You can't have more than 5 active tasks at the same time" in str(response.data)
