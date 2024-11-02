from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroUsuario, ProvinciaViewSet, MunicipioViewSet, UserDispositivosList, UserDispositivosCount, \
    VariableViewSet, ProvinciaViewSet, MunicipioViewSet, DispositivoViewSet, UsuarioViewSet, RegistroVariableViewSet, \
    DispositivoDataViewSet, ProvinciaList, UserView, UsuarioDetail, UsuarioDetailMunicipio, DispositivoList, CustomTokenObtainPairView, \
    LogoutView

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
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user-info'),
    path('userD/', UsuarioDetail.as_view(), name='user-detail'),
    path('userD/municipio', UsuarioDetailMunicipio.as_view(), name='user-detail-municipio'),
    path('api/dispositivos/', DispositivoList.as_view(), name='dispositivo-list'),
    #path('provincias_/', ProvinciaList.as_view(), name='provincias_list'),
    path('user/dispositivos/', UserDispositivosList.as_view(), name='user-dispositivos'),
    path('user/dispositivo/<int:pk>/data/', DispositivoDataViewSet.as_view({'get': 'retrieve'}), name='dispositivo-data'),
    path('user/dispositivos/count/', UserDispositivosCount.as_view(), name='user-dispositivos-count'),

]
