import os
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import now

from django_extensions.db.models import TimeStampedModel


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    seats_in_row = models.IntegerField(validators=[MinValueValidator(1)])

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


def create_custom_path(instance: "Play", filename: str) -> str:
    _, extension = os.path.splitext(filename)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    if extension not in allowed_extensions:
        raise ValidationError("Unsupported file extension.")
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads", "play", filename)


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, blank=True, related_name="plays")
    actors = models.ManyToManyField(Actor, blank=True, related_name="plays")
    image = models.ImageField(null=True, upload_to=create_custom_path)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    @property
    def available_seats(self) -> int:
        total_seats = self.theatre_hall.capacity
        reserved_seats = self.tickets.count()
        return total_seats - reserved_seats

    def can_reserve(self, ticket_count: int) -> bool:
        return self.available_seats >= ticket_count

    def clean(self) -> None:
        if self.show_time < now():
            raise ValidationError(
                {"show_time": "Performance cannot be scheduled in the past."}
            )

        if not self.can_reserve(ticket_count=1):
            raise ValidationError(
                {"show_time": "Not enough seats available for this performance."}
            )

    class Meta:
        ordering = ["-show_time"]

    def __str__(self) -> str:
        return (f"{self.play} at {self.theatre_hall} on "
                f"{self.show_time.strftime('%Y-%m-%d %H:%M')}")


class Reservation(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )

    def clean(self) -> None:
        if not self.tickets.exists():
            raise ValidationError("Reservation must include at least one ticket.")

    def __str__(self) -> str:
        return f"Reservation by {self.user} on {self.created}"

    class Meta:
        ordering = ["-created"]


class Ticket(models.Model):
    row = models.IntegerField(validators=[MinValueValidator(1)])
    seat = models.IntegerField(validators=[MinValueValidator(1)])
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_seat_in_range(value: int, max_value: int, field_name: str) -> None:
        if not (1 <= value <= max_value):
            raise ValidationError(
                {
                    field_name: f"{field_name.capitalize()} must be in the range: "
                                f"(1, {max_value})."
                }
            )

    def clean(self) -> None:
        if not self.performance:
            raise ValidationError("Performance must be set before validating seats.")

        theatre_hall = self.performance.theatre_hall
        self.validate_seat_in_range(self.row, theatre_hall.rows, "row")
        self.validate_seat_in_range(self.seat, theatre_hall.seats_in_row, "seat")

    def save(self, *args: tuple, **kwargs: dict) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.performance} (row: {self.row}, seat: {self.seat})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["performance", "row", "seat"],
                name="unique_ticket_per_performance",
            )
        ]
        ordering = ["row", "seat"]
