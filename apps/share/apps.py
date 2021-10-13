from django.apps import AppConfig

# flake8: noqa: F401


class ShareConfig(AppConfig):
    name = "apps.share"

    def ready(self):
        from apps.share import signals
