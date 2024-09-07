from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroUsuario, ProvinciaViewSet, MunicipioViewSet, UserDispositivosList, UserDispositivosCount, \
    VariableViewSet, ProvinciaViewSet, MunicipioViewSet, DispositivoViewSet, UsuarioViewSet, RegistroVariableViewSet

router = DefaultRouter()
app_name = 'accounts'

router.register(r'variables', VariableViewSet)
router.register(r'provincias', ProvinciaViewSet)
router.register(r'municipios', MunicipioViewSet)
router.register(r'dispositivos', DispositivoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'registros', RegistroVariableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('user/dispositivos/', UserDispositivosList.as_view(), name='user-dispositivos'),
    path('user/dispositivos/count/', UserDispositivosCount.as_view(), name='user-dispositivos-count'),

]
