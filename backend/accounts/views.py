from django.shortcuts import render
from rest_framework import viewsets, generics, status
# from django.core.mail import send_mail
from .models import Usuario
from .serializer import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


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
