"""
Tests for task detail endpoint.
"""

from django.urls import reverse
from rest_framework import status

from tasks.models import TaskStatusEnum
from tests.base import BaseAPITestCase
from tests.factories import TaskFactory
from tests.factories import UserFactory


class TestTaskDetail(BaseAPITestCase):
    """Tests for retrieving individual task details."""

    def setUp(self) -> None:
        """Set up test data for each test."""
        super().setUp()
        self.create_user()
        self.authenticate()

        # Create a task owned by the authenticated user
        self.task = TaskFactory(user=self.user)
        self.url = reverse("task-detail", kwargs={"pk": self.task.id})

        # Create a task owned by another user
        self.other_user = UserFactory()
        self.other_task = TaskFactory(user=self.other_user)
        self.other_task_url = reverse("task-detail", kwargs={"pk": self.other_task.id})

    def test_retrieve_task_success(self) -> None:
        """Test successfully retrieving a task's details."""
        response = self.api_call("get", self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == self.task.id
        assert response.data["user"] == self.user.username
        assert response.data["task_type"] == self.task.task_type
        assert response.data["status"] == self.task.status

    def test_retrieve_task_not_found(self) -> None:
        """Test retrieving a task that doesn't exist."""
        non_existent_id = 9999
        url = reverse("task-detail", kwargs={"pk": non_existent_id})

        response = self.api_call("get", url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_task_not_owned(self) -> None:
        """Test retrieving a task owned by another user."""
        response = self.api_call("get", self.other_task_url)

        # Should return 404 for privacy/security reasons rather than 403
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_task_details_include_all_fields(self) -> None:
        """Test that all expected fields are included in the task detail response."""
        # Create a task with all fields populated
        task = TaskFactory(user=self.user, status=TaskStatusEnum.COMPLETED, result={"result": 42})
        url = reverse("task-detail", kwargs={"pk": task.id})

        response = self.api_call("get", url)

        assert response.status_code == status.HTTP_200_OK

        # Check that all expected fields are present
        expected_fields = [
            "id",
            "user",
            "task_type",
            "task_type_display",
            "status",
            "status_display",
            "input_data",
            "result",
            "created_at",
        ]

        for field in expected_fields:
            assert field in response.data
