# Proyecto Django + Vue.js

Este proyecto es una aplicación web que utiliza Django para el backend y Vue.js para el frontend. El frontend está
ubicado en la carpeta `frontend` en la raíz del proyecto y el backend está ubicado en la carpeta `backend` de la raíz del proyecto.

## Requisitos

- Python 3.8.10
- Node.js y npm
- PostgreSQL server

## Dependencias y Bibliotecas
### Backend
- asgiref==3.8.1
- backports.zoneinfo==0.2.1
- Django==4.2.15
- django-4-jet==1.0.9
- django-cors-headers==4.4.0
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- psycopg2==2.9.9
- psycopg2-binary==2.9.9
- PyJWT==2.9.0
- six==1.16.0
- sqlparse==0.5.1
- typing_extensions==4.12.2
- tzdata==2024.1
### Frontend
- @vue/cli-plugin-babel@3.12.1
- @vue/cli-plugin-eslint@3.12.1
- @vue/cli-plugin-pwa@3.12.1
- @vue/cli-service@3.12.1
- axios@1.7.3
- bindings@1.5.0 extraneous
- bootstrap@4.6.0
- cache-loader@4.1.0
- chartist@0.11.0
- cross-env@7.0.3
- file-uri-to-path@1.0.0 extraneous
- google-maps@3.2.1
- jwt-decode@4.0.0
- nan@2.20.0 extraneous
- register-service-worker@1.7.2
- sass-loader@10.1.1
- sass@1.56.2
- v-tooltip@2.0.0-rc.33
- vue-router@3.0.2
- vue-template-compiler@2.7.14
- vue@2.7.14
- vue2-google-maps@0.10.7
- vuex@4.1.0


## Funcionalidades
- API para gestión de usuarios (CRUD).
- Autenticación y autorización de usuarios. (Autenticación por token)
- Validaciones necesarias para garantizar la integridad de los datos.
- Registro de la actividad de la aplicación.
- Notificación de registro exitoso de usuario via Email

## Configuración del Entorno

### Backend (Django)

1. Clona el repositorio:
    ```bash
    git clone https://github.com/alejandroramjar/admin_dashboard_IOT.git
    cd meteoro
    ```

2. Crea y activa un entorno virtual:
    ```bash
    pip install virtualenv
    virtualenv .env
    ./.env/scripts/activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables(refente a la configuración del
   servidor de base de datos postgresql):
    ```env
    DB_NAME=database_name
    DB_USER=postgres
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5433
    ```

5. Realiza las migraciones de la base de datos y se crea el súper usuario:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

    ```

6. Ejecuta el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

### Frontend (Vue.js)

1. Navega a la carpeta `frontend`:
    ```bash
    cd frontend
    ```

2. Instala las dependencias:
    ```bash
    npm install
    npm install axios
    ```

3. Ejecuta el servidor de desarrollo:
    ```bash
    npm run serve
    ```

## Estructura del Proyecto

meteoro/
├── .idea/ 
├── .venv/ 
├── admin_panel/ 
├── config/ 
├── frontend/ 
│ ├── .github/ 
│ ├── documentation/ 
│ ├── node_modules/ 
│ ├── public/ 
│ ├── src/ 
│ ├── .babelrc 
│ ├── .editorconfig 
│ ├── .eslintrc 
│ ├── .gitignore 
│ ├── .npmrc 
│ ├── .postcssrc.js 
│ ├── CHANGELOG.md 
│ ├── CODE_OF_CONDUCT.md 
│ ├── CONTRIBUTING.md 
│ ├── genezio.yaml 
│ ├── intelij.webpack.js 
│ ├── ISSUE_TEMPLATE.md 
│ ├── LICENSE 
│ ├── package-lock.json 
│ ├── package.json 
│ ├── README.md 
│ └── vue.config.js 
├── pycache/ 
├── .gitignore 
├── db.sqlite3 
├── debug.log 
├── manage.py 
├── README.md 
├── requirements.txt 
└── Test_koredata.txt

## Despliegue

### Backend

1. Configura las variables de entorno para producción en el archivo `.env`.
2. Realiza las migraciones de la base de datos:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
3. Recoge los archivos estáticos:
    ```bash
    python manage.py collectstatic
    ```
4. Configura un servidor web (por ejemplo, Gunicorn, Nginx) para servir la aplicación.

### Frontend

1. Construye la aplicación para producción:
    ```bash
    npm run build
    ```
2. Sirve los archivos estáticos generados en la carpeta `dist` con un servidor web.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, sigue los pasos a continuación para contribuir:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT.

---

¡Gracias por usar este proyecto! Si tienes alguna pregunta o problema, no dudes en abrir un issue o contactarme.