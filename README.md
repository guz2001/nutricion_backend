
# NutriConsulta - Backend

## Descripción
Este proyecto es una api para conectar al frontend con el fin de consumir una base de datos de intercambios nutricionales, en estos datos se encuentran
macronutrientes,micronutrientes, poblacion, grupos alimenticios.

## Qué se hizo en esta versión (explicado sin tecnicismos)

Esta sección está escrita para cualquier persona, sin necesidad de saber de
programación. Si solo quieres entender qué cambió y por qué importaba, lee esto.

### Primero: qué es este proyecto, en una frase

Es la "bodega" del sistema. Guarda la tabla de 553 alimentos con sus valores
nutricionales y se la entrega a la pantalla que ve el nutricionista. La pantalla
es bonita pero no sabe nada; cada vez que necesita un dato se lo pide a esta
bodega.

---

### 1. Lo nuevo: guardar alimentos y ver la suma

Antes el nutricionista podía consultar alimentos uno por uno, pero no había
manera de armar una lista.

Ahora puede ir agregando alimentos a una "lista de trabajo" y el sistema le
muestra el total sumado: cuántas calorías, cuánta proteína, cuánta grasa, etc.
Si agrega dos porciones de arroz, cuenta el doble que una. También puede quitar
alimentos de la lista, y el total se recalcula solo.

Detalle importante: **la suma la hace la bodega, no la pantalla**. Es como pedirle
la cuenta al mesero en vez de sumar los precios uno mismo en una servilleta: hay
un solo lugar donde se hacen las cuentas, así que no puede haber dos resultados
distintos.

**Limitación que conviene tener presente:** por ahora esa lista es **una sola y
compartida**. No hay usuarios ni contraseñas todavía, así que si dos personas
usan el sistema al mismo tiempo, las dos ven y modifican la misma lista. Fue una
decisión deliberada para poder probar la idea rápido con nutricionistas reales
antes de construir todo un sistema de cuentas.

---

### 2. El problema grave que se encontró y se corrigió

Este es el hallazgo más importante de toda la revisión.

**Qué pasaba:** la bodega estaba entregando los datos, pero también había quedado
con la puerta de atrás abierta. Cualquier persona que conociera la dirección del
sistema podía **cambiar o dañar los 553 alimentos reales**. No hacía falta ser
experto: bastaba abrir cierta página en el navegador y llenar un formulario.

Piénsalo así: es como una biblioteca donde se supone que la gente entra a
consultar libros, pero por descuido quedó permitido que cualquiera tachara y
reescribiera las páginas de los libros.

**Por qué era serio:** esos alimentos son información nutricional real que usan
profesionales para atender pacientes. Un dato alterado sin que nadie se dé
cuenta es un dato en el que ya no se puede confiar.

**Qué lo hacía peor:** en el momento de la revisión, el sistema estaba publicado
en internet para hacer una demostración. O sea, la puerta no solo estaba abierta:
estaba abierta hacia la calle.

**Qué se hizo:** se dejó la tabla de alimentos y la de grupos en modo *solo
lectura*. Ahora se pueden consultar todas las veces que se quiera, pero cualquier
intento de modificarlas se rechaza. Se probó de verdad, intentando modificar un
alimento: el sistema lo rechazó y el dato quedó intacto.

La única lista que sí se puede modificar es la de alimentos guardados, que es
justamente la que debe poder cambiar.

---

### 3. El sistema no habría podido publicarse

Había un error de dirección: el archivo encargado de arrancar el sistema en un
servidor real apuntaba a una carpeta de configuración vacía. Es como un sobre con
la dirección incompleta: nunca llega.

En el computador de desarrollo no se notaba, porque ahí se arranca por otro
camino que sí estaba bien. Pero el día que se intentara publicar de verdad, no
habría arrancado. Ya está corregido y comprobado.

---

### 4. Protecciones para cuando salga a internet

La configuración pensada para el servidor real venía sin candados. Se activaron:

- Que todo el tráfico viaje **cifrado** (el candadito del navegador). Sin esto,
  quien esté en la misma red wifi puede leer lo que se envía.
- Que el sistema **solo responda a su dirección oficial**. Antes respondía a
  cualquiera que preguntara, lo que permite ciertos engaños.
- Que el sistema **no se pueda incrustar dentro de otra página**, un truco que se
  usa para hacer que la gente haga clic donde no quiere.

Django trae un examen de seguridad propio. Antes reprobaba con 5 observaciones;
ahora queda 1, que se explica más abajo en "Pendiente".

---

### 5. La lista de ingredientes estaba mal

Todo proyecto lleva una lista de los componentes que necesita para funcionar, para
que otra persona pueda instalarlo en su computador.

Esa lista se había generado por equivocación copiando **todos los programas del
computador entero**, incluidos programas del sistema operativo Fedora que no
tienen nada que ver. Eran 134 cosas cuando en realidad hacían falta 9. Siguiendo
las instrucciones del proyecto, nadie de afuera habría podido instalarlo.

Se reescribió con los 9 componentes reales y se comprobó instalándolo desde cero
en un entorno limpio.

---

### 6. Se volvió once veces más eficiente al listar

Para mostrar 20 alimentos en pantalla, el sistema le hacía **22 preguntas** a la
base de datos: una por la lista, y luego una pregunta aparte por cada alimento
solo para averiguar a qué grupo pertenecía.

Es como ir al mercado y volver a la casa 22 veces porque olvidaste algo cada vez,
en lugar de llevar la lista completa y hacer un solo viaje.

Ahora son **2 preguntas** en total. Está medido, no es una estimación.

---

### 7. Un error que el usuario sí alcanzaba a ver

Los alimentos se muestran de a 20 por página. El problema es que nadie le había
dicho a la base de datos en qué orden entregarlos, y cuando no se especifica, no
garantiza dar siempre el mismo orden.

El efecto práctico: al pasar de página, un alimento podía **aparecer dos veces, o
no aparecer nunca**. Con 126 alimentos en la categoría "adultos" son 7 páginas,
así que era perfectamente posible que a un nutricionista se le perdiera un
alimento sin que él supiera por qué.

Se corrigió ordenándolos alfabéticamente y se verificó recorriendo las 7 páginas:
126 alimentos, ninguno repetido, ninguno faltante.

**Cambio visible:** los alimentos y los grupos ahora salen en orden alfabético.

---

### 8. Pruebas automáticas

Antes no había ninguna. Cada vez que alguien tocaba algo, la única forma de saber
si se había roto era probarlo a mano y confiar en no haber olvidado nada.

Ahora hay **18 pruebas automáticas** que se ejecutan con un comando y revisan en
segundos que todo siga funcionando: que guardar funcione, que la suma dé el
número correcto, que quitar un alimento recalcule el total, que la lista vacía
muestre ceros y no un espacio en blanco, y sobre todo **que la puerta de atrás
siga cerrada**.

Esto último es lo valioso: si en el futuro alguien vuelve a abrir el agujero de
seguridad sin darse cuenta, las pruebas avisan de inmediato.

Ejecutándolas se descubrió, además, que el listado de grupos tenía el mismo
problema de orden del punto 7. También quedó corregido.

---

### 9. Orden y limpieza

- Se borró un bloque de código viejo, desactivado y contradictorio que estorbaba
  la lectura.
- El panel de administración ahora muestra los alimentos, pero **sin permitir
  editarlos**, por la misma razón del punto 2.
- El archivo de ejemplo que sirve de plantilla para configurar el proyecto estaba
  **completamente vacío**, aunque las instrucciones decían copiarlo. Se llenó.

---

### Pendiente: una cosa que falta hacer

Queda **una** tarea, y requiere una decisión humana, no código.

El sistema usa una "llave" secreta para proteger la información. La que está
puesta hoy es la de práctica que genera Django automáticamente, y viene marcada
con la palabra *insecure* (insegura) en su propio nombre.

Para desarrollo está bien. **Antes de publicar el sistema de verdad hay que
generar una llave propia.** El comando exacto está escrito dentro del archivo
`.env.example`. Es un solo comando y toma diez segundos, pero no puede olvidarse.

---

### Resumen

| Qué | Antes | Ahora |
|---|---|---|
| Modificar los alimentos reales desde fuera | Cualquiera podía | Bloqueado |
| Arrancar en un servidor real | No habría arrancado | Funciona |
| Examen de seguridad de Django | 5 observaciones | 1 (la llave) |
| Instalar el proyecto desde cero | Imposible | Verificado |
| Preguntas a la base por cada listado | 22 | 2 |
| Alimentos repetidos o perdidos al pasar página | Posible | Imposible |
| Pruebas automáticas | 0 | 18 |

---

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
1. Crear entorno virtual con Python 3.9:  `python3.9 -m venv venv`
2. Activar entorno:  `source venv/bin/activate`
3. Instalar dependencias:  `pip install -r requirements.txt`

requirements.txt lista SOLO las 9 dependencias del proyecto. Si se regenera con
`pip freeze`, hacerlo con el entorno virtual activado; con el Python del sistema
se cuelan paquetes de la distribución que nadie más puede instalar.

## Configuración
1. Copiar .env.example a .env
2. Completar las variables. El .env.example documenta cada una, incluido el
   comando para generar una SECRET_KEY propia.

Variables usadas: SECRET_KEY, DEBUG, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST,
DB_PORT y —solo en producción— ALLOWED_HOSTS y CORS_ALLOWED_ORIGINS.

## Permisos necesarios en PostgreSQL
El usuario de la aplicación necesita, además de leer y escribir:

    -- para crear la tabla alimentos_guardados con las migraciones
    GRANT CREATE ON SCHEMA public TO nutricion_app;
    -- para que esa tabla pueda referenciar a alimentos (llave foránea)
    GRANT REFERENCES ON TABLE alimentos TO nutricion_app;
    -- solo en desarrollo, para poder ejecutar las pruebas
    ALTER ROLE nutricion_app CREATEDB;

En PostgreSQL 15 y superiores el permiso CREATE sobre el esquema public está
revocado por defecto, así que el primero es obligatorio aunque antes no hiciera falta.

## Ejecutar el proyecto
- `python manage.py migrate`  (la primera vez, y en cada despliegue)
- `python manage.py runserver`
- La API queda disponible en http://127.0.0.1:8000/api/

## Ejecutar las pruebas
- `python manage.py test apps.alimentos`

Son 18 pruebas que cubren los endpoints de guardados, los totales y —importante—
que las tablas preexistentes sigan siendo de solo lectura.

Como Alimento y GrupoAlimento son managed=False, Django no crearía sus tablas en
la base de pruebas. Por eso config/test_runner.py las marca temporalmente como
gestionadas y desactiva las migraciones de la app mientras corren los tests.
Todo ocurre sobre test_nutricion_db, que Django crea y borra; nunca sobre la real.

## Desplegar en producción
Usar la configuración de producción, que ya trae HTTPS forzado, HSTS, cookies
seguras y las cabeceras de protección activadas:

    DJANGO_SETTINGS_MODULE=config.settings.production

wsgi.py y asgi.py ya apuntan ahí por defecto. Verificar antes con:

    DJANGO_SETTINGS_MODULE=config.settings.production python manage.py check --deploy

Debe quedar sin advertencias. Si reporta la SECRET_KEY, es que falta generar una
propia para producción (ver .env.example).

## Endpoints disponibles

Alimentos y grupos son de SOLO LECTURA (ReadOnlyModelViewSet): son tablas
preexistentes con datos reales. Cualquier POST, PUT, PATCH o DELETE sobre ellas
devuelve 405. Solo /api/guardados/ acepta escritura.

- GET /api/alimentos/ (con filtros: q, grupo_id, poblacion)
- GET /api/alimentos/:id/
- GET /api/grupos/ (con filtro: poblacion)
- GET /api/guardados/ — lista los alimentos guardados
- POST /api/guardados/ — guarda un alimento. Body: {"alimento_id": int, "cantidad": decimal}
- DELETE /api/guardados/:id/ — elimina un alimento guardado
- GET /api/guardados/total/ — devuelve la suma de valores nutricionales de todos los guardados

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
- Los listados llevan order_by explícito: sin ORDER BY, PostgreSQL no garantiza
  un orden estable y la paginación puede repetir u omitir registros
- AlimentoViewSet usa select_related('grupo'): sin eso, listar 20 alimentos
  disparaba 22 consultas en vez de 2 (problema N+1)
- La tabla `alimentos_guardados` SÍ es administrada por Django (sin managed=False),
  a diferencia de `alimentos` y `grupos_alimentos` que son preexistentes.
  Requiere ejecutar migraciones al desplegar:
      python manage.py migrate
  El usuario de base de datos necesita permiso CREATE sobre el esquema public:
      GRANT CREATE ON SCHEMA public TO nutricion_app;
- Si se desea cambiar la zona horaria lo hacemos en base.py seccion:
    Internacionalización
    LANGUAGE_CODE = 'es-co'
    TIME_ZONE = 'America/Bogota'
    USE_I18N = True
    USE_TZ = True

## Decisiones de diseño — alimentos guardados

Se deja constancia del "por qué" de cada decisión, porque en una iteración
futura habrá que revisarlas y la razón original se pierde si no queda escrita.

1. **Granularidad: alimentos sueltos con cantidad, no agrupados por consulta.**
   Cada registro guardado es "este alimento, esta cantidad de porciones, en este
   momento". Agrupar en consultas o planes por paciente se dejó para después
   porque obligaba a modelar paciente y consulta antes de poder validar lo
   básico con nutricionistas reales.

2. **Sin autenticación por ahora.** Los alimentos guardados no pertenecen a
   ningún usuario. Esto permite validar la funcionalidad sin bloquearla detrás
   de un sistema de login completo. Implicación conocida: la lista es global y
   compartida por todos los que abran la app. Agregar autenticación más adelante
   significa añadir un ForeignKey a User en AlimentoGuardado (con su migración),
   filtrar el queryset del ViewSet y el endpoint /total/ por request.user, y
   proteger las rutas con permission_classes.

3. **Cantidad como DecimalField.** Permite medias porciones (0.5, 1.5) y hace
   que la suma sea real: 2 porciones de arroz cuentan el doble que 1.

4. **La suma se calcula en el backend, no en el frontend.** Razones: la lógica
   vive en un solo lugar (si mañana se agregan más campos a sumar solo se toca
   el backend); se usa agregación SQL (Sum, F) en una sola consulta en vez de
   traer todos los registros y sumarlos en JavaScript; y el frontend no recibe
   más datos de los que necesita, igual que en el resto del proyecto.

5. **AlimentoGuardado no lleva managed=False.** A diferencia de `alimentos` y
   `grupos_alimentos`, que existían en PostgreSQL antes de Django, esta tabla
   nace con el proyecto y por eso Django sí la crea y administra por migraciones.
