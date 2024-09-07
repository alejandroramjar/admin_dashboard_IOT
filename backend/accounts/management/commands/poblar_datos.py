from django.core.management.base import BaseCommand
from accounts.utils import poblar_provincias, poblar_municipios, poblar_variables


class Command(BaseCommand):
    help = 'Poblar la base de datos con provincias, municipios y variables meteorologicas'

    def handle(self, *args, **kwargs):
        poblar_provincias()
        poblar_municipios()
        poblar_variables()
        self.stdout.write(self.style.SUCCESS('Datos poblados exitosamente'))
