import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

logger = logging.getLogger(__name__)

from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"Error en la vista: {exception}")
        return JsonResponse({"error": "Error inesperado, por favor intente nuevamente más tarde."}, status=500)


class RequestCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        count = cache.get('request_count', 0)
        cache.set('request_count', count + 1, timeout=None)


class LogURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la dirección IP del cliente
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Registrar la URL solicitada y la IP del cliente
        logger.info(f"URL solicitada: {request.path} desde IP: {ip}")
        print(ip)

        response = self.get_response(request)
        return response


class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') and 'token' in request.GET:
            token = request.GET['token']
            try:
                token_obj = Token.objects.get(key=token)
                request.user = token_obj.user
            except ObjectDoesNotExist:
                return redirect('/admin/login/')  # Redirige si el token es inválido