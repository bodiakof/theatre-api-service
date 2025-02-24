from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class UserViewsTests(APITestCase):
    def test_register_user(self) -> None:
        """Ensure a new user can register using only email and password."""

        url = reverse("user:register")
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_manage_user_retrieve_authenticated(self) -> None:
        """Ensure an authenticated user can retrieve their own details."""

        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        url = reverse("user:manage")
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "test@example.com")

    def test_manage_user_update_authenticated(self) -> None:
        """Ensure an authenticated user can update their own details."""

        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        url = reverse("user:manage")
        self.client.force_authenticate(user=user)
        data = {"email": "updated@example.com"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")

    def test_manage_user_unauthenticated(self) -> None:
        """Ensure unauthenticated users cannot access the manage endpoint."""

        url = reverse("user:manage")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
