"""
Runner de pruebas para un proyecto con modelos managed=False.

Alimento y GrupoAlimento apuntan a tablas preexistentes en PostgreSQL. Eso hace
que, en la base de datos de pruebas, Django no cree esas tablas y cualquier test
que las use falle con "no existe la relación".

Hacen falta dos cosas, y ninguna sirve sin la otra:

1. Marcar esos modelos como managed=True mientras corren los tests, para que
   Django sepa que debe crear su esquema.
2. Desactivar las migraciones de la app durante los tests. Si no, Django arma la
   base de pruebas aplicando la migración, y ahí los modelos están registrados
   con managed=False, así que no crearía nada. Con las migraciones desactivadas
   Django crea las tablas directamente a partir de los modelos.

La base de datos real nunca se toca: todo esto ocurre sobre test_nutricion_db,
que Django crea al empezar y borra al terminar.
"""

from django.test.runner import DiscoverRunner


class ManagedModelTestRunner(DiscoverRunner):
    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        from django.conf import settings

        self.modelos_no_gestionados = [
            m for m in apps.get_models() if not m._meta.managed
        ]
        for m in self.modelos_no_gestionados:
            m._meta.managed = True

        settings.MIGRATION_MODULES = {'alimentos': None}

        super().setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super().teardown_test_environment(*args, **kwargs)
        # Restaurar el estado real para no afectar a nada posterior
        for m in self.modelos_no_gestionados:
            m._meta.managed = False
