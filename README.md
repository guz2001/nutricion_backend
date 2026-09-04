
# NutriConsulta - Backend

## Descripción
Este proyecto es una api para conectar al frontend con el fin de consumir una base de datos de intercambios nutricionales, en estos datos se encuentran
macronutrientes,micronutrientes, poblacion, grupos alimenticios.

## Requisitos previos
- Python 3.9
- PostgreSQL con la base de datos nutricion_db ya existente o cualquier otra base de datos, tener encuenta configurarla en base.py en el diccionario
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
- Se usa python3.9 por que es una de las versiones mas estables para realizar apis ademas de esto se integra bien con django

## Instalación
1. Crear entorno virtual con Python 3.9
2. Activar entorno
3. Instalar dependencias (requirements.txt, incluye psycopg2-binary)

## Configuración
1. Copiar .env.example a .env
2. Completar las variables (nombre de BD, usuario, contraseña, host, puerto)
   [tu idea de "establecer las variables con los valores de acceso"]

## Ejecutar el proyecto
- python manage.py runserver
- La API queda disponible en http://127.0.0.1:8000/api/

## Endpoints disponibles
- GET /api/alimentos/ (con filtros: q, grupo_id, poblacion)
- GET /api/alimentos/:id/
- GET /api/grupos/

## Conexión con el frontend
Tener encuenta cual es la direccion ip y el puerto que tenemos en el frontend que usara esta api, de tenerlo claro lo configuramos en development.py:
En desarrollo permitimos cualquier host local
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS: permite que el frontend Astro (puerto 4321) consuma la API
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4321',
    'http://127.0.0.1:4321',
]

## Notas técnicas
- La base de datos es preexistente (managed=False en los modelos)
- Si se desea cambiar la zona horaria lo hacemos en base.py seccion:
    Internacionalización
    LANGUAGE_CODE = 'es-co'
    TIME_ZONE = 'America/Bogota'
    USE_I18N = True
    USE_TZ = True