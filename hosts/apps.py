from django.apps import AppConfig
from octoxlabscase import hosts_container


class VeryCoolAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hosts'

    def ready(self):
        hosts_container.wire(
            modules=[
                "hosts.selectors"
            ]
        )
