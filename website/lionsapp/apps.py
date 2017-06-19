from django.apps import AppConfig


class LionsappConfig(AppConfig):
    name = 'lionsapp'
    def ready(self):
        import lionsapp.signals  # noqa
