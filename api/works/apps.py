from django.apps import AppConfig


class WorksConfig(AppConfig):
    name = 'works'

    def ready(self):
        from works import signals
