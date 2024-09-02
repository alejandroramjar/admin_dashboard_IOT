from django.core.management.base import BaseCommand
from accounts.utils import poblar_provincias, poblar_municipios


class Command(BaseCommand):
    help = 'Poblar la base de datos con provincias y municipios'

    def handle(self, *args, **kwargs):
        poblar_provincias()
        poblar_municipios()
        self.stdout.write(self.style.SUCCESS('Datos poblados exitosamente'))
