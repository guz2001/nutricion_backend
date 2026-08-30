"""
Configuración específica de desarrollo.
Extiende base.py con ajustes para desarrollo local.
"""

from .base import *

# En desarrollo: DEBUG True muestra errores detallados en el navegador
# NUNCA debe ser True en producción
DEBUG = True

# En desarrollo permitimos cualquier host local
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS: permite que el frontend Astro (puerto 4321) consuma la API
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4321',
    'http://127.0.0.1:4321',
]