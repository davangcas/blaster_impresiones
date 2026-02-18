from django.apps import AppConfig


class PrintratesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "printrates"

    def ready(self):
        import printrates.signals  # noqa
