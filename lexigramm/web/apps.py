from django.apps import AppConfig
from django.conf import settings
from django.templatetags.static import static


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

    def ready(self):
        if hasattr(settings, "BOOTSTRAP5"):
            settings.BOOTSTRAP5["css_url"]["href"] = static(settings.BOOTSTRAP5["css_url"]["href"])
            settings.BOOTSTRAP5["javascript_url"]["url"] = static(settings.BOOTSTRAP5["javascript_url"]["url"])
