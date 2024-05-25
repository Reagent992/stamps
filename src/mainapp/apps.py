from django.apps import AppConfig


class MainappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mainapp"
    verbose_name = "Печати"

    def ready(self):
        """Добавление signals.py."""
        import mainapp.signals  # noqa
