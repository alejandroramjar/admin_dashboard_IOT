from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Provincia, Municipio, Usuario, Variable, Dispositivo, RegistroVariable


# Registro del modelo Provincia en el panel de administración
@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Campos que se mostrarán en la lista de administración
    search_fields = ('nombre',)  # Campos por los que se puede buscar
    ordering = ('nombre',)  # Orden de los registros


# Registro del modelo Municipio en el panel de administración
@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia')  # Campos que se mostrarán en la lista de administración
    search_fields = ('nombre', 'provincia__nombre')  # Campos por los que se puede buscar
    list_filter = ('provincia',)  # Filtros en la barra lateral
    ordering = ('provincia', 'nombre')  # Orden de los municipios


# Personalización del modelo Usuario en el panel de administración
class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('carnet_identidad', 'phone', 'municipio', 'dispositivos')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('carnet_identidad', 'phone', 'municipio', 'dispositivos')}),
    )
    list_display = (
        'is_active', 'username', 'email', 'get_full_name', 'is_staff', 'carnet_identidad', 'phone', 'get_provincia',
        'municipio', 'get_dispositivos_count')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'carnet_identidad', 'phone', 'municipio__nombre')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'municipio')
    ordering = ('username',)


# Registro del modelo Usuario en el panel de administración
admin.site.register(Usuario, CustomUserAdmin)


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')


@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'descripcion', 'get_variables', 'municipio', 'protocolo', 'latitud', 'longitud')
    list_filter = ('municipio__provincia', 'municipio', 'protocolo', 'variables__nombre')
    search_fields = ('identificador', 'descripcion')
    filter_horizontal = ['variables']
    fieldsets = (
        (None, {
            'fields': ('descripcion', 'municipio', 'protocolo', 'identificador', 'variables')
        }),
        ('Coordenadas', {
            'fields': ('latitud', 'longitud')
        }),
    )

    def get_variables(self, obj):
        return ", ".join([variable.nombre for variable in obj.variables.all()])

    get_variables.short_description = 'Variables'


@admin.register(RegistroVariable)
class RegistroVariableAdmin(admin.ModelAdmin):
    list_display = ('dispositivo', 'variable', 'valor', 'timestamp')
    list_filter = ('dispositivo', 'variable', 'timestamp')
    search_fields = ('dispositivo__identificador', 'variable__nombre')
