from typing import Type

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from theatre.models import Reservation


@receiver(pre_save, sender=Reservation)
def validate_reservation(
    sender: Type[Reservation], instance: Reservation, **kwargs
) -> None:
    """Ensure a reservation has at least one ticket before saving."""

    if not instance.pk:
        return

    if not instance.tickets.exists():
        raise ValidationError("Reservation must include at least one ticket.")
