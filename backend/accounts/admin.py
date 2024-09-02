from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Provincia, Municipio, Usuario


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
    ordering = ('provincia', 'nombre')  # Orden de los registros


# Personalización del modelo Usuario en el panel de administración
class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('carnet_identidad', 'phone', 'municipio', 'provincia')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('carnet_identidad', 'phone', 'municipio', 'provincia')}),
    )
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'carnet_identidad', 'phone', 'municipio',
        'provincia')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'carnet_identidad', 'phone', 'municipio__nombre',
                     'provincia__nombre')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'municipio', 'provincia')
    ordering = ('username',)


# Registro del modelo Usuario en el panel de administración
admin.site.register(Usuario, CustomUserAdmin)
