from django.db import transaction

from rest_framework import serializers

from theatre.models import (
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
    Actor,
    Genre,
    Play,
)


class TheatreHallSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    play_image = serializers.ImageField(source="play.image", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(
        source="available_seats", read_only=True
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play_title",
            "play_image",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "tickets_available",
        )


class TicketSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = serializers.StringRelatedField(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)
    taken_places = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time", "taken_places")


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, validated_data: dict) -> dict:
        ticket = Ticket(**validated_data)
        ticket.clean()
        return validated_data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(read_only=True)

    class Meta(TicketSerializer.Meta):
        fields = TicketSerializer.Meta.fields


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSeatsSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ("id", "user", "created", "tickets")

    def validate_tickets(self, value: list[dict]) -> list[dict]:
        if not value:
            raise serializers.ValidationError(
                "Reservation must include at least one ticket."
            )
        return value

    def create(self, validated_data: dict) -> Reservation:
        tickets_data = validated_data.pop("tickets", [])
        user = self.context["request"].user
        validated_data.pop("user", None)

        with transaction.atomic():
            reservation = Reservation.objects.create(user=user, **validated_data)

            seen_combinations = set()
            unique_tickets = []

            for ticket in tickets_data:
                if "performance" in ticket:
                    ticket["performance_id"] = ticket.pop("performance")
                elif "performance_id" not in ticket:
                    raise serializers.ValidationError(
                        "Ticket must have an associated performance."
                    )

                ticket_combination = (
                    ticket["performance_id"],
                    ticket["row"],
                    ticket["seat"],
                )

                if ticket_combination not in seen_combinations:
                    if not Ticket.objects.filter(
                        performance_id=ticket["performance_id"],
                        row=ticket["row"],
                        seat=ticket["seat"],
                    ).exists():
                        unique_tickets.append(Ticket(reservation=reservation, **ticket))
                        seen_combinations.add(ticket_combination)

            if not unique_tickets:
                raise serializers.ValidationError(
                    "All requested tickets are already taken."
                )

            Ticket.objects.bulk_create(unique_tickets)

        return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketSeatsSerializer(many=True, read_only=True)

    class Meta(ReservationSerializer.Meta):
        fields = ReservationSerializer.Meta.fields


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    image = serializers.ImageField()

    class Meta(PlaySerializer.Meta):
        fields = PlaySerializer.Meta.fields + ("image",)


class PlayDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "image")


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")
