from django.apps import AppConfig


class PrintsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "prints"

    def ready(self):
        import prints.signals  # noqa
