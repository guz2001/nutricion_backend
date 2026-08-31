"""
Configuración específica de producción.
Extiende base.py con ajustes de seguridad para el servidor real.
"""

from .base import *

DEBUG = False

# En producción: solo el dominio real del servidor
ALLOWED_HOSTS = ['*']
# CORS: solo el dominio real del frontend
""" no se usa por ahora
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
"""