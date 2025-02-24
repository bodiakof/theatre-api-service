from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from theatre.models import (
    TheatreHall,
    Performance,
    Reservation,
    Actor,
    Genre,
    Play,
)


User = get_user_model()


class GenreViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse("theatre:genre-list")
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", password="adminpass"
        )
        self.normal_user = User.objects.create_user(
            email="user@test.com", password="userpass"
        )

    def test_list_genres_as_authenticated_user(self) -> None:
        Genre.objects.create(name="Comedy")
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.count(), 1)

    def test_create_genre_as_admin(self) -> None:
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "Drama"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 1)

    def test_create_genre_as_non_admin(self) -> None:
        self.client.force_authenticate(user=self.normal_user)
        data = {"name": "Horror"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ActorViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse("theatre:actor-list")
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", password="adminpass"
        )
        self.normal_user = User.objects.create_user(
            email="user@test.com", password="userpass"
        )

    def test_list_actors_as_authenticated_user(self) -> None:
        Actor.objects.create(first_name="John", last_name="Doe")
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Actor.objects.count(), 1)

    def test_create_actor_as_admin(self) -> None:
        self.client.force_authenticate(user=self.admin_user)
        data = {"first_name": "Jane", "last_name": "Smith"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actor.objects.count(), 1)

    def test_create_actor_as_non_admin(self) -> None:
        self.client.force_authenticate(user=self.normal_user)
        data = {"first_name": "Tom", "last_name": "Hanks"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_actor_full_name_property(self) -> None:
        actor = Actor.objects.create(first_name="Robert", last_name="Downey")
        self.assertEqual(actor.full_name, "Robert Downey")


class ReservationViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse("theatre:reservation-list")
        self.user = User.objects.create_user(email="user@test.com", password="userpass")
        self.other_user = User.objects.create_user(
            email="other@test.com", password="otherpass"
        )
        self.hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=20
        )
        self.play = Play.objects.create(title="Epic Play")
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.hall, show_time=timezone.now()
        )

        self.reservation = Reservation.objects.create(user=self.user)

    def test_create_reservation_authenticated(self) -> None:
        self.client.force_authenticate(user=self.user)

        data = {
            "user": self.user.id,  # Provide the user ID
            "performance": self.performance.id,
            "tickets": [{"row": 1, "seat": 1, "performance": self.performance.id}],
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("user"), self.user.id)
        self.assertEqual(len(response.data.get("tickets")), 1)

    def test_create_reservation_without_tickets(self) -> None:
        self.client.force_authenticate(user=self.user)
        data = {"performance": self.performance.id}

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "This field is required.",
            str(response.data)
        )
