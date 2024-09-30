from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator
from django.db import models
import paho.mqtt.client as mqtt
import json
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Variable(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # nombre de la variable meteorológica
    descripcion = models.TextField()  # Descripción de la variable
    limite_superior = models.FloatField(null=True, blank=True)  # Límite superior de la variable
    limite_inferior = models.FloatField(null=True, blank=True)  # Límite inferior de la variable

    def __str__(self):
        return self.nombre


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


# Modelo para los municipios
class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre único del municipio
    provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, related_name='municipios')

    def __str__(self):
        return self.nombre


# Modelo para los dispositivos
class Dispositivo(models.Model):
    PROTOCOLO_CHOICES = [
        ('mqtt', 'MQTT'),
        ('http', 'HTTP'),
    ]

    descripcion = models.CharField(max_length=200)  # Descripción del dispositivo
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING,
                                  related_name='dispositivos')  # Relación con el municipio
    protocolo = models.CharField(max_length=200, choices=PROTOCOLO_CHOICES, null=True,
                                 blank=True)  # Protocolo del dispositivo
    identificador = models.CharField(max_length=200, unique=True)  # Identificador único del dispositivo
    variables = models.ManyToManyField(Variable)  # Variables meteorológicas asociadas al dispositivo
    latitud = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)  # Latitud del dispositivo
    longitud = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)  # Longitud del dispositivo

    def __str__(self):
        return f'{self.identificador}'

    def variables_dict(self):
        return json.loads(self.variables.__str__())

    def subscribe(self):
        client = mqtt.Client()
        client.on_message = on_message  # Referencia a la función de manejo de mensajes

        # Conectar al broker
        client.connect("localhost", 1883, 60)

        # Crear el tema y suscribirse
        topic = f"dispositivo/{self.identificador}/data"
        client.subscribe(topic)

        # Iniciar el bucle de escucha
        client.loop_start()

        print(f"Suscrito a {topic}")

####
def on_message(client, userdata, message):
    from datetime import datetime
    from .alerta import enviar_aviso
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)

    dispositivo_id = data.get('dispositivo_id')
    variable_nombre = data.get('variable_nombre')
    valor = data.get('valor')

    try:
        dispositivo = Dispositivo.objects.get(identificador=dispositivo_id)
        variable = Variable.objects.get(nombre=variable_nombre)

        # Verifica si ya existe un registro para evitar duplicados
        if not RegistroVariable.objects.filter(dispositivo=dispositivo, variable=variable, valor=valor,
                                               timestamp__date=datetime.today()).exists():
            registro = RegistroVariable(dispositivo=dispositivo, variable=variable, valor=valor)
            registro.save()

            # Verificar límites
            if (variable.limite_superior is not None and valor > variable.limite_superior) or \
                    (variable.limite_inferior is not None and valor < variable.limite_inferior):
                enviar_aviso(variable, valor)

            print(f'Registro guardado: {registro}')
        else:
            print(f'Registro duplicado: {dispositivo} - {variable} - {valor}')

    except (Dispositivo.DoesNotExist, Variable.DoesNotExist) as e:
        print(f'Error al guardar registro: {e}')


# Modelo para los usuarios
class Usuario(AbstractUser):
    dispositivos = models.ManyToManyField(Dispositivo, related_name='usuarios')  # Dispositivos asociados al usuario
    carnet_identidad = models.CharField(max_length=11, unique=True,
                                        help_text="Máximo 11 caracteres")  # Carnet de identidad único
    phone_regex = RegexValidator(regex=r'^\d{8}$')  # Validador para el número de teléfono
    phone = models.CharField(validators=[phone_regex], max_length=8, blank=True,
                             help_text="Ingrese el número de teléfono en el formato: '5x-xx-xx-xx'",
                             unique=True)  # Número de teléfono único
    municipio = models.OneToOneField(Municipio, on_delete=models.SET_NULL, related_name='usuario', blank=True,
                                     null=True)  # Municipio del usuario

    def __str__(self):
        return f'{self.get_full_name()}'

    def get_provincia(self):
        """Retorna la provincia del municipio asociado."""
        if self.municipio:
            return self.municipio.provincia
        return None

    def get_dispositivos_count(self):
        """Retorna la cantidad de dispositivos asociados al usuario."""
        return self.dispositivos.count()


# Modelo para el registro de variables
class RegistroVariable(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.DO_NOTHING)  # Dispositivo que registra la variable
    variable = models.ForeignKey(Variable, on_delete=models.DO_NOTHING)  # Variable registrada
    valor = models.FloatField()  # Valor de la variable registrada
    unidad = models.CharField(default='C', max_length=10)  # Unidad en la que se registra la variable
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora del registro

    def __str__(self):
        return f'Registro: {self.dispositivo} - {self.variable} - {self.valor} en {self.timestamp}'

    def save(self, *args, **kwargs):
        # Verifica si ya existe un registro con los mismos valores
        if not RegistroVariable.objects.filter(
                dispositivo=self.dispositivo,
                variable=self.variable,
                valor=self.valor,
                timestamp__date=self.timestamp
        ).exists():
            super().save(*args, **kwargs)  # Llama al método de la clase base para guardar
        else:
            print(f'Registro duplicado: {self}')


# Señales
# @receiver(post_save, sender=Dispositivo)
# def subscribe_to_device(sender, instance, created, **kwargs):
#     if created:
#         instance.subscribe()
