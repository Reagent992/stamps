from django.apps import AppConfig


class PrintyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "printy"
    verbose_name = "Оснастки"

    def ready(self):
        """Добавление signals.py."""
        import printy.signals  # noqa
