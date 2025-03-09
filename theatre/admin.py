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

admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Reservation)
admin.site.register(Ticket)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Play)
