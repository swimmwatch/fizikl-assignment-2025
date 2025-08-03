"""
Base test configurations and utilities for API testing.
"""

from typing import Any
from typing import Dict
from typing import Optional

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from tests.factories import UserFactory


@pytest.mark.django_db
class BaseAPITestCase(APITestCase):
    """Base test case for API tests with authentication support."""

    def setUp(self) -> None:
        """Set up test case with API client and helper methods."""
        super().setUp()
        self.client = APIClient()
        self.user = None

    def create_user(self, password: str = "testpassword123", **kwargs) -> None:  # noqa: S107
        """Create a user for testing and set it as the current user."""
        self.user = UserFactory(password=password, **kwargs)
        return self.user

    def authenticate(self) -> None:
        """Authenticate the test client with the current user."""
        if not self.user:
            self.create_user()
        self.client.force_authenticate(user=self.user)

    def get_token(self) -> Dict[str, str]:
        """Obtain JWT token for the current user."""
        if not self.user:
            self.create_user()

        response = self.client.post(
            reverse("token_obtain_pair"), data={"email": self.user.email, "password": "testpassword123"}, format="json"
        )
        return response.json()

    def api_call(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        authenticated: bool = True,
        format: str = "json",
    ):
        """Make an API call with the given method, URL, and data."""
        if authenticated and not self.client.handler._force_user:
            self.authenticate()

        method_map = {
            "get": self.client.get,
            "post": self.client.post,
            "put": self.client.put,
            "patch": self.client.patch,
            "delete": self.client.delete,
        }

        if method.lower() not in method_map:
            raise ValueError(f"Invalid method: {method}")

        return method_map[method.lower()](url, data=data, format=format)
