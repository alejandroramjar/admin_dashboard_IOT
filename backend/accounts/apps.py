from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # def ready(self):
    #   import accounts.signals
    def ready(self):
        from .mqtt_client import start_mqtt_client
        start_mqtt_client()  # Iniciar el cliente MQTT al cargar la aplicación
