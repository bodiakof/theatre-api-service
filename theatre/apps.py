from django.apps import AppConfig


class TheatreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "theatre"

    def ready(self) -> None:
        import theatre.signals
