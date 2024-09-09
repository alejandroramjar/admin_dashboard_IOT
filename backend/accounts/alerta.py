from django.core.mail import send_mail
from django.conf import settings

def enviar_aviso(variable, valor):
    subject = f'Aviso: {variable.nombre} ha alcanzado un límite'
    message = f'La variable {variable.nombre} ha alcanzado un valor de {valor}, que supera los límites establecidos.'
    recipient_list = settings.ADMIN_EMAIL  # Cambia esto por la lista de destinatarios

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)