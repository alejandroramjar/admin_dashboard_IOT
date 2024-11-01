from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import paho.mqtt.client as mqtt
import json


class Variable(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    limite_superior = models.FloatField(null=True, blank=True)
    limite_inferior = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, related_name='municipios')

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    PROTOCOLO_CHOICES = [
        ('mqtt', 'MQTT'),
        ('http', 'HTTP'),
    ]

    descripcion = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING, related_name='dispositivos')
    protocolo = models.CharField(max_length=200, choices=PROTOCOLO_CHOICES, null=True, blank=True)
    identificador = models.CharField(max_length=200, unique=True)
    variables = models.ManyToManyField(Variable)
    latitud = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return self.identificador

    def subscribe(self):
        client = mqtt.Client()
        client.on_message = on_message
        client.connect("localhost", 1883, 60)
        topic = f"dispositivo/{self.identificador}/data"
        client.subscribe(topic)
        client.loop_start()
        print(f"Suscrito a {topic}")


def on_message(client, userdata, message):
    # Implementación de la función para manejar mensajes MQTT
    pass


class Usuario(AbstractUser):
    dispositivos = models.ManyToManyField(Dispositivo, related_name='usuarios', blank=True)
    carnet_identidad = models.CharField(max_length=11, unique=True)
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="El número de teléfono debe tener exactamente 8 dígitos.")
    phone = models.CharField(validators=[phone_regex], max_length=8, blank=True, unique=True)
    municipio = models.OneToOneField(Municipio, on_delete=models.SET_NULL, related_name='usuario', blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    def get_municipio(self):
        return self.municipio.nombre

    def get_provincia(self):
        if self.municipio:
            return self.municipio.provincia
        return None

    def get_dispositivos_count(self):
        return self.dispositivos.count()


class RegistroVariable(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.DO_NOTHING)
    variable = models.ForeignKey(Variable, on_delete=models.DO_NOTHING)
    valor = models.FloatField()
    unidad = models.CharField(default='C', max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Registro: {self.dispositivo} - {self.variable} - {self.valor} en {self.timestamp}'

    def save(self, *args, **kwargs):
        if not RegistroVariable.objects.filter(
                dispositivo=self.dispositivo,
                variable=self.variable,
                valor=self.valor,
                timestamp__date=self.timestamp.date()
        ).exists():
            super().save(*args, **kwargs)
        else:
            print(f'Registro duplicado: {self}')