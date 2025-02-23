from django.contrib import admin
from theatre.models import (
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
    Actor,
    Genre,
    Play,
)


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    pass


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    pass
