from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroUsuario, ProvinciaViewSet, MunicipioViewSet

router = DefaultRouter()
app_name = 'accounts'

router.register(r'provincias', ProvinciaViewSet)
router.register(r'municipios', MunicipioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistroUsuario.as_view(), name='registro_usuario'),
]
