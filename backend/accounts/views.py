from django.shortcuts import render
from rest_framework import viewsets, generics, status
# from django.core.mail import send_mail
from rest_framework import viewsets
from .models import Variable, Provincia, Municipio, Dispositivo, Usuario, RegistroVariable
from .serializer import RegisterSerializer, ProvinciaSerializer, MunicipioSerializer, UsuarioSerializer, \
    DispositivoSerializer, VariableSerializer, ProvinciaSerializer, MunicipioSerializer, DispositivoSerializer, \
    UsuarioSerializer, RegistroVariableSerializer
from rest_framework import viewsets
from .models import Dispositivo, RegistroVariable
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .models import Usuario
from .serializer import UsuarioSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'is_admin': user.is_staff,  # o user.is_superuser
        })

class RegistroUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()
            user.is_active = True  # Establecer el usuario como inactivo
            user.save()

            # Enviar correo electrónico al usuario
            # self.send_registration_email(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ProvinciaList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class ProvinciaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        provincia_id = self.request.query_params.get('provincia')
        if provincia_id:
            return self.queryset.filter(provincia_id=provincia_id)
        return self.queryset


class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer


class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Devuelve los dispositivos solo para el usuario autenticado
        return Dispositivo.objects.filter(user=self.request.user)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class RegistroVariableViewSet(viewsets.ModelViewSet):
    queryset = RegistroVariable.objects.all()
    serializer_class = RegistroVariableSerializer


#    def send_registration_email(self, user):
#        try:
#            send_mail(
#                'Registro exitoso',
#                f'Hola {user.username}, tu registro ha sido exitoso. El administrador del sistema tiene 72 horas para autorizar tu cuenta.',
#                settings.DEFAULT_FROM_EMAIL,
#                [user.email],
#                fail_silently=False,
#            )
#            send_mail(
#                'Nuevo registro de usuario',
#                f'El usuario {user.username} se ha registrado y está pendiente de autorización. Tienes 72 horas para autorizar el registro.',
#                settings.DEFAULT_FROM_EMAIL,
#                [settings.ADMIN_EMAIL],
#                fail_silently=False,
#            )
#        except Exception as e:
#            logger.error(f"Error al enviar correos: {e}")


@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDispositivosList(generics.ListAPIView):
    serializer_class = DispositivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.dispositivos.all()


class UserDispositivosCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        count = user.dispositivos.count()
        return Response({'count': count})


class DispositivoDataViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        dispositivo = Dispositivo.objects.get(pk=pk)

        # Obtén los registros de las variables del dispositivo (últimos 10)
        registros = RegistroVariable.objects.filter(dispositivo=dispositivo).order_by('-timestamp')[:20]
        print(registros.count())

        # Estructura para almacenar los datos
        data = {}

        # Recorre los registros y agrupa por variable
        for registro in registros:
            variable_nombre = registro.variable.nombre  # Asegúrate de tener un campo 'variable' en RegistroVariable
            timestamp = registro.timestamp.strftime('%H:%M')
            valor = registro.valor

            if variable_nombre not in data:
                data[variable_nombre] = {'labels': [], 'values': []}

            data[variable_nombre]['labels'].insert(0, timestamp)  # Insertar al inicio para mantener el orden
            data[variable_nombre]['values'].insert(0, valor)  # Insertar al inicio para mantener el orden

        # Construye la respuesta
        response_data = {
            'labels': data[list(data.keys())[0]]['labels'],  # Usar las etiquetas de la primera variable
            'data': {variable: values for variable, values in data.items()}
        }
        print(response_data)

        return Response(response_data)



class UsuarioDetail(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print(self.request.user.municipio)
        # Devuelve el usuario autenticado
        return self.request.user


class UsuarioDetailMunicipio(generics.RetrieveUpdateAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Obtiene el usuario autenticado
        user = self.request.user

        # Verifica si el usuario tiene un municipio asociado
        if hasattr(user, 'municipio'):
            return user.municipio  # Devuelve el objeto Municipio asociado al usuario
        else:
            return Response("Municipio no encontrado para el usuario autenticado.")