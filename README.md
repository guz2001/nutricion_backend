
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
   En el proyecto tenemos que tener encuenta configurar las credenciales para conectar el backend de django con la base de datos que tenemos creada y tambien la secret key de django
   Para esto tenemos que tener claro 6 datos de la base de datos que son:
   1-Que motor de base de datos estamos utilizando, debido a que en este espacio se organizara la variable ENGINE que le damos el valor del motod de base de datos, para postgresql quedaria asi "'ENGINE': 'django.db.backends.postgresql'"
   2-Nombre de la base de datos, en este caso como usamos postgresql la db se llama nutricion_db sera postgres pero puede ser otro creado e iria de la siguiente manera 'NAME': config('DB_NAME')

   3-Nombre del usuario que accede a la base de datos, puede ser el admin de postgresql que en este caso se llama postgres,
   
   4-Configuramos la contraseña que le asignamos a la base de datos para acceder
   
   5-Para este apartado buscamos la ubicacion de donde esta corriendo la base de datos de postgresq, local host 
   
   6-Por ultimo tendriamos que saber exactamente el puerto donde corre el postgresq

   Al tener claro estos dato nos dirigimos al archivo env, donde se ubicaran las variables a rellenar con la informacion anteriormente recopilada, por si se olvida serian las siguiente:
SECRET_KEY

DEBUG
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

3. Para evitar errores al correr la aplicacion con python manage.py runserver se debe de crear las tablas no existentes para poder asociar los datos, para realizarlas desde cero esas tablas habria que ejecturar el comando python manage.py migrate


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