"""
Configuración específica de producción.
Extiende base.py con ajustes de seguridad para el servidor real.
"""

from .base import *
from decouple import config, Csv

DEBUG = False

# Dominios reales del servidor, separados por coma en el .env.
# NUNCA usar ['*']: anula la validación de la cabecera Host y habilita
# ataques de Host header poisoning (enlaces de recuperación envenenados,
# envenenamiento de caché).
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# CORS: solo el dominio real del frontend, también desde el .env
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())

# ─── Seguridad HTTPS ───────────────────────────────────────────────────────
# Redirige todo el tráfico HTTP a HTTPS
SECURE_SSL_REDIRECT = True

# HSTS: indica al navegador que solo use HTTPS para este dominio.
# Se arranca en 1 hora a propósito. Subirlo a 31536000 (1 año) SOLO cuando
# el certificado esté confirmado y estable: si se activa un valor alto y el
# HTTPS falla, los navegadores siguen rechazando el sitio hasta que expire
# y no hay forma de revertirlo del lado del servidor.
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Si hay un proxy inverso (nginx, Caddy) terminando el TLS, esta cabecera le
# dice a Django que la petición original venía por HTTPS.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ─── Cookies ───────────────────────────────────────────────────────────────
# Solo viajan por HTTPS, así no se pueden capturar en tráfico plano
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ─── Cabeceras de protección ───────────────────────────────────────────────
SECURE_CONTENT_TYPE_NOSNIFF = True  # impide que el navegador adivine el tipo MIME
X_FRAME_OPTIONS = 'DENY'            # impide incrustar el sitio en un iframe (clickjacking)
