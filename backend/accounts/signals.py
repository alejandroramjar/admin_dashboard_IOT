from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Provincia, Municipio
from .utils import poblar_municipios


@receiver(post_migrate)
def ejecutar_poblar_municipios(sender, **kwargs):
    poblar_municipios()
