from datetime import datetime

from typing import Any, Type

from django.db.models import F, Count, QuerySet

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from theatre.serializers import (
    PerformanceDetailSerializer,
    ReservationListSerializer,
    PerformanceListSerializer,
    TheatreHallSerializer,
    ReservationSerializer,
    PerformanceSerializer,
    PlayDetailSerializer,
    PlayImageSerializer,
    PlayListSerializer,
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
)
from theatre.models import (
    Reservation,
    TheatreHall,
    Performance,
    Genre,
    Actor,
    Play,
)
from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly


class PlayAndReservationPaginator(PageNumberPagination):
    """Paginator for Play and Reservation views."""

    page_size = 5
    page_size_query_param = "per_page"
    max_page_size = 50

    def get_paginated_response(self, data: Any) -> Response:
        return Response(
            {
                "pages": self.page.paginator.num_pages,
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class BaseCreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    """Base viewset for endpoints that allow creation and listing
    with read-only access for non-admins."""

    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class BaseRetrieveCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """Base viewset for endpoints that allow creation, listing, and retrieving
    with read-only access for non-admins."""

    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class GenreViewSet(BaseCreateListViewSet):
    """Viewset for managing genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(BaseCreateListViewSet):
    """Viewset for managing actors."""

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class TheatreHallViewSet(BaseCreateListViewSet):
    """Viewset for managing theatre halls."""

    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayViewSet(BaseRetrieveCreateListViewSet):
    """Viewset for managing plays, including filtering and image uploads."""

    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer
    pagination_class = PlayAndReservationPaginator

    @staticmethod
    def _params_to_ints(params: str) -> list[int]:
        return [int(str_id) for str_id in params.split(",")]

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genres:
            genre_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genre_ids)
        if actors:
            actor_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actor_ids)
        return queryset.distinct()

    def get_serializer_class(self) -> Type[Any]:
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "upload_image":
            return PlayImageSerializer
        return super().get_serializer_class()

    @action(
        detail=True,
        methods=["POST"],
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request: Any, pk: Any = None) -> Response:
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "genres",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by genre id (ex. ?genres=2,5)",
            ),
            OpenApiParameter(
                "actors",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by actor id (ex. ?actors=2,5)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by play title (ex. ?title=fiction)",
            ),
        ]
    )
    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)


class PerformanceViewSet(viewsets.ModelViewSet):
    """Viewset for managing performances with filtering capabilities."""

    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    queryset = Performance.objects.select_related("play", "theatre_hall").annotate(
        tickets_available=(
            F("theatre_hall__rows") * F("theatre_hall__seats_in_row") - Count("tickets")
        )
    )
    serializer_class = PerformanceSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        date_str = self.request.query_params.get("date")
        play_id_str = self.request.query_params.get("play")

        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(show_time__date=date_obj)
            except ValueError:
                raise ValidationError(
                    {"date": "Invalid date format, should be YYYY-MM-DD."}
                )
        if play_id_str:
            queryset = queryset.filter(play_id=int(play_id_str))
        return queryset

    def get_serializer_class(self) -> Type[Any]:
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "play",
                type=OpenApiTypes.INT,
                description="Filter by play id (ex. ?play=3)",
            ),
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description="Filter by date (ex. ?date=2025-01-01)",
            ),
        ]
    )
    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)


class ReservationViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    """Viewset for managing reservations, accessible only to authenticated users."""

    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play",
        "tickets__performance__theatre_hall",
    )
    serializer_class = ReservationSerializer
    pagination_class = PlayAndReservationPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> Type[Any]:
        if self.action == "list":
            return ReservationListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer: Any) -> None:
        serializer.save(user=self.request.user)
