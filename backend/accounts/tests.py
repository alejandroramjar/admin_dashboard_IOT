from django.test import TestCase
from .models import Variable, Provincia, Municipio, Dispositivo
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Variable, Provincia, Municipio, Dispositivo, Usuario, RegistroVariable
class ModelsTestCase(TestCase):

    def setUp(self):
        # Crear instancias de prueba para las variables
        self.variable1 = Variable.objects.create(
            nombre="Temperatura",
            descripcion="Temperatura ambiente",
            limite_superior=50.0,
            limite_inferior=-10.0
        )
        self.variable2 = Variable.objects.create(
            nombre="Humedad",
            descripcion="Humedad relativa",
            limite_superior=100.0,
            limite_inferior=0.0
        )

        # Crear instancias de prueba para las provincias
        self.provincia = Provincia.objects.create(nombre="La Habana")

        # Crear instancias de prueba para los municipios
        self.municipio = Municipio.objects.create(
            nombre="Centro Habana",
            provincia=self.provincia
        )

        # Crear instancias de prueba para los dispositivos
        self.dispositivo = Dispositivo.objects.create(
            descripcion="Dispositivo de prueba",
            municipio=self.municipio,
            protocolo="mqtt",
            identificador="disp001",
            latitud=23.135,
            longitud=-82.358
        )
        self.dispositivo.variables.add(self.variable1, self.variable2)

    def test_variable_creation(self):
        self.assertEqual(self.variable1.nombre, "Temperatura")
        self.assertEqual(self.variable2.limite_superior, 100.0)

    def test_provincia_creation(self):
        self.assertEqual(self.provincia.nombre, "La Habana")

    def test_municipio_creation(self):
        self.assertEqual(self.municipio.nombre, "Centro Habana")
        self.assertEqual(self.municipio.provincia.nombre, "La Habana")

    def test_dispositivo_creation(self):
        self.assertEqual(self.dispositivo.descripcion, "Dispositivo de prueba")
        self.assertEqual(self.dispositivo.municipio.nombre, "Centro Habana")
        self.assertEqual(self.dispositivo.protocolo, "mqtt")
        self.assertEqual(self.dispositivo.identificador, "disp001")
        self.assertEqual(self.dispositivo.latitud, 23.135)
        self.assertEqual(self.dispositivo.longitud, -82.358)
        self.assertIn(self.variable1, self.dispositivo.variables.all())
        self.assertIn(self.variable2, self.dispositivo.variables.all())




class UsuarioRegistroVariableTestCase(TestCase):

    def setUp(self):
        # Crear instancias de prueba para las variables
        self.variable = Variable.objects.create(
            nombre="Temperatura",
            descripcion="Temperatura ambiente",
            limite_superior=50.0,
            limite_inferior=-10.0
        )

        # Crear instancias de prueba para las provincias
        self.provincia = Provincia.objects.create(nombre="La Habana")

        # Crear instancias de prueba para los municipios
        self.municipio = Municipio.objects.create(
            nombre="Centro Habana",
            provincia=self.provincia
        )

        # Crear instancias de prueba para los dispositivos
        self.dispositivo = Dispositivo.objects.create(
            descripcion="Dispositivo de prueba",
            municipio=self.municipio,
            protocolo="mqtt",
            identificador="disp001",
            latitud=23.135,
            longitud=-82.358
        )
        self.dispositivo.variables.add(self.variable)

        # Crear instancia de prueba para el usuario
        self.usuario = Usuario.objects.create_user(
            username="testuser",
            password="testpass123",
            carnet_identidad="12345678901",
            phone="51234567",
            municipio=self.municipio
        )
        self.usuario.dispositivos.add(self.dispositivo)

        # Crear instancia de prueba para el registro de variables
        self.registro_variable = RegistroVariable.objects.create(
            dispositivo=self.dispositivo,
            variable=self.variable,
            valor=25.5,
            unidad="C"
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.username, "testuser")
        self.assertEqual(self.usuario.carnet_identidad, "12345678901")
        self.assertEqual(self.usuario.phone, "51234567")
        self.assertEqual(self.usuario.municipio.nombre, "Centro Habana")
        self.assertIn(self.dispositivo, self.usuario.dispositivos.all())

    def test_get_provincia(self):
        self.assertEqual(self.usuario.get_provincia(), self.provincia)

    def test_get_dispositivos_count(self):
        self.assertEqual(self.usuario.get_dispositivos_count(), 1)

    def test_registro_variable_creation(self):
        self.assertEqual(self.registro_variable.dispositivo, self.dispositivo)
        self.assertEqual(self.registro_variable.variable, self.variable)
        self.assertEqual(self.registro_variable.valor, 25.5)
        self.assertEqual(self.registro_variable.unidad, "C")


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Variable, Provincia, Municipio, Dispositivo, Usuario, RegistroVariable

class ViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Crear instancias de prueba para las variables
        self.variable = Variable.objects.create(
            nombre="Temperatura",
            descripcion="Temperatura ambiente",
            limite_superior=50.0,
            limite_inferior=-10.0
        )

        # Crear instancias de prueba para las provincias
        self.provincia = Provincia.objects.create(nombre="La Habana")

        # Crear instancias de prueba para los municipios
        self.municipio = Municipio.objects.create(
            nombre="Centro Habana",
            provincia=self.provincia
        )

        # Crear instancias de prueba para los dispositivos
        self.dispositivo = Dispositivo.objects.create(
            descripcion="Dispositivo de prueba",
            municipio=self.municipio,
            protocolo="mqtt",
            identificador="disp001",
            latitud=23.135,
            longitud=-82.358
        )
        self.dispositivo.variables.add(self.variable)

        # Crear instancia de prueba para el usuario
        self.usuario = Usuario.objects.create_user(
            username="testuser",
            password="testpass123",
            carnet_identidad="12345678901",
            phone="51234567",
            municipio=self.municipio
        )
        self.usuario.dispositivos.add(self.dispositivo)

        # Crear instancia de prueba para el registro de variables
        self.registro_variable = RegistroVariable.objects.create(
            dispositivo=self.dispositivo,
            variable=self.variable,
            valor=25.5,
            unidad="C"
        )

    def test_registro_usuario(self):
        url = reverse('accounts:registro_usuario')
        data = {
            "username": "newuser",
            "password": "newpass123",
            "carnet_identidad": "10987654321",
            "phone": "52345678",
            # "municipio": self.municipio.id
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  # Imprimir los errores de validación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 2)

    def test_provincia_viewset(self):
        self.client.force_authenticate(user=self.usuario)  # Autenticación
        url = reverse('accounts:provincia-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_municipio_viewset(self):
        self.client.force_authenticate(user=self.usuario)  # Autenticación
        url = reverse('accounts:municipio-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_variable_viewset(self):
        self.client.force_authenticate(user=self.usuario)  # Autenticación
        url = reverse('accounts:variable-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_dispositivo_viewset(self):
        self.client.force_authenticate(user=self.usuario)  # Autenticación
        self.client.force_authenticate(user=self.usuario)
        url = reverse('accounts:user-dispositivos')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_usuario_viewset(self):
        self.client.force_authenticate(user=self.usuario)  # Autenticación
        url = reverse('accounts:usuario-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_registro_variable_viewset(self):
        self.client.force_authenticate(user=self.usuario)  # Autenticación
        url = reverse('accounts:registrovariable-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
