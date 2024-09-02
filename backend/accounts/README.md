# Documentación del admin.py

Este archivo `admin.py` gestiona la configuración del panel de administración de Django para los
modelos `Provincia`, `Municipio` y `Usuario`.

## Modelos Registrados

### Provincia

- **list_display**: Muestra el nombre de la provincia en la lista de administración.
- **search_fields**: Permite buscar provincias por nombre.
- **ordering**: Ordena las provincias por nombre.

### Municipio

- **list_display**: Muestra el nombre del municipio y su provincia en la lista de administración.
- **search_fields**: Permite buscar municipios por nombre y por nombre de la provincia.
- **list_filter**: Añade un filtro por provincia en la barra lateral.
- **ordering**: Ordena los municipios por provincia y nombre.

### Usuario

- **CustomUserAdmin**: Extiende `UserAdmin` para incluir los campos
  personalizados `carnet_identidad`, `phone`, `municipio` y `provincia`.
- **list_display**: Muestra los campos personalizados en la lista de administración de usuarios.
- **search_fields**: Permite buscar usuarios por los campos personalizados.
- **list_filter**: Añade filtros por municipio y provincia en la barra lateral.
- **ordering**: Ordena los usuarios por nombre de usuario.

## Cómo usar

1. Asegúrate de que `admin.py` esté en el directorio de tu aplicación Django.
2. Registra los modelos en el panel de administración para gestionarlos fácilmente.

