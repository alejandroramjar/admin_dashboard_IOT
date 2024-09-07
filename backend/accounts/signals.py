from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Provincia, Municipio
from .utils import poblar_provincias, poblar_municipios


# no usado de momento por problemas a la hora de migrar la base de datos
@receiver(post_migrate)
def ejecutar_poblar_datos(sender, **kwargs):
    if sender.name == 'accounts':
        poblar_provincias()
        poblar_municipios()


# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dispositivo  # Asegúrate de importar el modelo


# Señales
@receiver(post_save, sender=Dispositivo)
def subscribe_to_device(sender, instance, created, **kwargs):
    if created:
        instance.subscribe()
