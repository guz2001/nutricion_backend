"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# config.settings es un paquete con __init__.py vacio: no contiene configuracion.
# Hay que apuntar al modulo concreto, si no el servidor WSGI/ASGI arranca sin settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_asgi_application()
