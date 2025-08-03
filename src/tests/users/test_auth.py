"""
Tests for user authentication endpoints.
"""

from django.urls import reverse
from rest_framework import status

from tests.base import BaseAPITestCase
from tests.factories import UserFactory
from users.models import User


class TestUserRegistration(BaseAPITestCase):
    """Tests for user registration endpoint."""

    def test_register_user_success(self) -> None:
        """Test successful user registration."""
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.api_call("post", url, data=data, authenticated=False)

        assert response.status_code == status.HTTP_201_CREATED

        assert "id" in response.data
        assert response.data["username"] == data["username"]
        assert response.data["email"] == data["email"]
        assert "password" not in response.data

        # Verify user was created in database
        user = User.objects.filter(email=data["email"]).first()
        assert user is not None
        assert user.username == data["username"]

    def test_register_user_duplicate_email(self) -> None:
        """Test user registration with an existing email."""
        existing_user = UserFactory(email="existing@example.com")

        url = reverse("register")
        data = {
            "username": "newuser",
            "email": existing_user.email,
            "password": "StrongPassword123!",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.api_call("post", url, data=data, authenticated=False)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_register_user_duplicate_username(self) -> None:
        """Test user registration with an existing username."""
        existing_user = UserFactory(username="existinguser")

        url = reverse("register")
        data = {
            "username": existing_user.username,
            "email": "new@example.com",
            "password": "StrongPassword123!",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.api_call("post", url, data=data, authenticated=False)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data


class TestTokenAuthentication(BaseAPITestCase):
    """Tests for token authentication endpoints."""

    def test_token_obtain_success(self) -> None:
        """Test successful token generation."""
        self.create_user(email="user@example.com", password="StrongPassword123!")

        url = reverse("token_obtain_pair")
        data = {"email": "user@example.com", "password": "StrongPassword123!"}

        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_token_obtain_invalid_credentials(self) -> None:
        """Test token generation with invalid credentials."""
        self.create_user(email="user@example.com", password="StrongPassword123!")

        url = reverse("token_obtain_pair")
        data = {"email": "user@example.com", "password": "WrongPassword123!"}  # Wrong password

        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self) -> None:
        """Test refreshing an access token."""
        self.create_user()
        tokens = self.get_token()

        url = reverse("token_refresh")
        data = {"refresh": tokens["refresh"]}

        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_refresh_invalid(self) -> None:
        """Test refreshing with an invalid refresh token."""
        url = reverse("token_refresh")
        data = {"refresh": "invalid-token"}

        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
