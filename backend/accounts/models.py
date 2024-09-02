from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class Provincia(models.Model):
    PROVINCIAS_CHOICES = [
        ('Pinar del Río', 'Pinar del Río'),
        ('Artemisa', 'Artemisa'),
        ('La Habana', 'La Habana'),
        ('Mayabeque', 'Mayabeque'),
        ('Matanzas', 'Matanzas'),
        ('Cienfuegos', 'Cienfuegos'),
        ('Villa Clara', 'Villa Clara'),
        ('Sancti Spíritus', 'Sancti Spíritus'),
        ('Ciego de Ávila', 'Ciego de Ávila'),
        ('Camagüey', 'Camagüey'),
        ('Las Tunas', 'Las Tunas'),
        ('Holguín', 'Holguín'),
        ('Granma', 'Granma'),
        ('Santiago de Cuba', 'Santiago de Cuba'),
        ('Guantánamo', 'Guantánamo'),
        ('Isla de la Juventud', 'Isla de la Juventud'),
    ]

    nombre = models.CharField(max_length=100, choices=PROVINCIAS_CHOICES)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='municipios')

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    carnet_identidad = models.CharField(max_length=11, help_text="Máximo 11 caracteres", unique=True)
    phone_regex = RegexValidator(regex=r'^\d{8}$')
    phone = models.CharField(validators=[phone_regex], max_length=8, blank=True,
                             help_text="Ingrese el número de teléfono en el formato: '5x-xx-xx-xx'", unique=True)
    municipio = models.OneToOneField(Municipio, on_delete=models.SET_NULL, related_name='usuario', blank=True,
                                     null=True)
    provincia = models.OneToOneField(Provincia, on_delete=models.SET_NULL, related_name='usuario', blank=True,
                                     null=True)

    def __str__(self):
        return f'{self.get_full_name()}'
