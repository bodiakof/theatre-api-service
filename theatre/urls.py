from django.urls import path, include

from rest_framework.routers import DefaultRouter

from theatre.views import (
    GenreViewSet,
    ActorViewSet,
    TheatreHallViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)


app_name = "theatre"

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("actors", ActorViewSet, basename="actor")
router.register("theatre-halls", TheatreHallViewSet, basename="theatrehall")
router.register("plays", PlayViewSet, basename="play")
router.register("performances", PerformanceViewSet, basename="performance")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]
