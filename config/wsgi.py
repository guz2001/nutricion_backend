"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# config.settings es un paquete con __init__.py vacio: no contiene configuracion.
# Hay que apuntar al modulo concreto, si no el servidor WSGI/ASGI arranca sin settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
