import os
import logging
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&zu@2a2%s80nh2th38!-qpw&_vjy-^09div7eag4rr@l0pa$!5'

DEBUG = True

# Application definition

DJANGO_APPS = [
    'jet.dashboard',
    'jet',
    'corsheaders',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # 'rest_framework.authtoken',
    # 'rest_auth',
    # 'rest_auth.registration',
    # 'rest_framework.authtoken',

    # 'jet',
    # 'dj_rest_auth',
    # 'dj_rest_auth.registration',
    # 'dj_rest_auth.registration.login_redirect',
    # 'dj_rest_auth.registration.profile_redirect',
    # 'dj_rest_auth.socialaccount',
    # 'dj_rest_auth.tokens',

]
LOCAL_APPS = [
    'accounts',

]
INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Middelware del corsheaders
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middelware.LogURLMiddleware',  # middleware para registro de solicitudes y eventos por dirección e IP

]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8082',
    'http://localhost:8082',
]
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

AUTH_USER_MODEL = 'accounts.Usuario'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         },
#         'console': {
#             'level': 'INFO',  # Cambia a INFO para reducir la cantidad de logs
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['file', 'console'],
#         'level': 'DEBUG',
#         'propagate': True,
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file', 'console'],  # Incluye la consola para ver los logs en tiempo real
#             'level': 'DEBUG',  # Cambia a INFO para reducir la cantidad de logs
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file', 'console'],
#             'level': 'DEBUG',  # Cambia a INFO para reducir la cantidad de logs
#             'propagate': True,
#         },
#     },
# }


# ***********************CONFIG EMAIL********************************************
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'koredatatesting@gmail.com'  # koredatatesting@gmail.com
EMAIL_HOST_PASSWORD = 'audj ucrj qlbk xmon'  # audj ucrj qlbk xmon
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_EMAIL = 'ramjar2107@gmail.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# *********************** END CONFIG EMAIL***************************************
JET_DEFAULT_THEME = 'light-gray'
JET_SIDE_MENU_COMPACT = False
JET_CHANGE_FORM_SIBLING_LINKS = True
JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultIndexDashboard'
JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'


SITE_ID = 1
