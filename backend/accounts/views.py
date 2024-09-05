from django.shortcuts import render
from rest_framework import viewsets, generics, status
# from django.core.mail import send_mail
from .models import Usuario, Municipio, Provincia
from .serializer import RegisterSerializer, ProvinciaSerializer, MunicipioSerializer, UsuarioSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.

class RegistroUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.is_active = False  # Establecer el usuario como inactivo
        user.save()

        # Enviar correo electrónico al usuario
        # self.send_registration_email(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    permission_classes = [AllowAny]


class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        provincia_id = self.request.query_params.get('provincia')
        if provincia_id:
            return self.queryset.filter(provincia_id=provincia_id)
        return self.queryset

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


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)