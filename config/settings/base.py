"""
Configuración base de Django — compartida por todos los entornos.
Importada por development.py y production.py.
"""

from pathlib import Path
from decouple import config

# Raíz del proyecto (la carpeta nutricion_backend/)
# __file__ es este archivo: config/settings/base.py
# .parent sube un nivel: config/settings/ → config/
# .parent otra vez: config/ → nutricion_backend/ (la raíz)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Clave secreta — viene del .env, nunca hardcodeada
SECRET_KEY = config('SECRET_KEY')

# Apps instaladas — Django nativo + las que agregamos
INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceros
    'rest_framework',
    'corsheaders',
    'django_filters',
    'apps.alimentos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS — debe ir alto en la lista
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo de URLs principal
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

# Base de datos PostgreSQL — credenciales vienen del .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Internacionalización
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'

# Campo PK por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}