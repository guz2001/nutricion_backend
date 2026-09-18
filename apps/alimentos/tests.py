"""
Pruebas de la API de NutriConsulta.

Cubren los criterios de aceptación de la funcionalidad de alimentos guardados
y las protecciones sobre las tablas preexistentes.
"""

from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.alimentos.models import GrupoAlimento, Alimento, AlimentoGuardado


def crear_alimento(grupo, nombre, **valores):
    """Crea un alimento de prueba con valores nutricionales por defecto."""
    campos = dict(
        poblacion='adultos',
        porcion_g=Decimal('100.000'),
        kcal=Decimal('200.000'),
        proteina_g=Decimal('10.000'),
        grasa_total_g=Decimal('5.000'),
        cho_g=Decimal('30.000'),
        fibra_g=Decimal('2.000'),
    )
    campos.update(valores)
    return Alimento.objects.create(
        grupo=grupo,
        nombre=nombre,
        unidad_medida='1 porción',
        creado_en=timezone.now(),
        **campos,
    )


class TablasPreexistentesSoloLecturaTests(APITestCase):
    """Las tablas alimentos y grupos_alimentos no deben aceptar escritura."""

    @classmethod
    def setUpTestData(cls):
        cls.grupo = GrupoAlimento.objects.create(nombre='Lácteos')
        cls.alimento = crear_alimento(cls.grupo, 'Kumis')

    def test_no_se_puede_crear_un_alimento(self):
        r = self.client.post('/api/alimentos/', {'nombre': 'Inventado'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_se_puede_modificar_un_alimento(self):
        r = self.client.patch(f'/api/alimentos/{self.alimento.id}/',
                              {'nombre': 'Modificado'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.alimento.refresh_from_db()
        self.assertEqual(self.alimento.nombre, 'Kumis')

    def test_no_se_puede_borrar_un_alimento(self):
        r = self.client.delete(f'/api/alimentos/{self.alimento.id}/')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Alimento.objects.filter(id=self.alimento.id).exists())

    def test_no_se_puede_escribir_en_grupos(self):
        r = self.client.post('/api/grupos/', {'nombre': 'Inventado'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_la_lectura_sigue_funcionando(self):
        self.assertEqual(self.client.get('/api/alimentos/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/grupos/').status_code, status.HTTP_200_OK)


class ListadoAlimentosTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.grupo = GrupoAlimento.objects.create(nombre='Cereales')
        for i in range(25):
            crear_alimento(cls.grupo, f'Alimento {i:02d}')

    def test_el_listado_no_dispara_consultas_por_cada_grupo(self):
        """Sin select_related esto serían 22 consultas en vez de 2 (problema N+1)."""
        with self.assertNumQueries(2):
            self.client.get('/api/alimentos/')

    def test_la_paginacion_no_repite_ni_omite_registros(self):
        vistos, pagina = [], 1
        while True:
            datos = self.client.get('/api/alimentos/', {'page': pagina}).json()
            vistos += [a['id'] for a in datos['results']]
            if not datos['next']:
                break
            pagina += 1
        self.assertEqual(len(vistos), 25)
        self.assertEqual(len(set(vistos)), 25, 'la paginación devolvió duplicados')

    def test_filtro_por_poblacion(self):
        crear_alimento(self.grupo, 'Solo niños', poblacion='niños')
        datos = self.client.get('/api/alimentos/', {'poblacion': 'niños'}).json()
        self.assertEqual(datos['count'], 1)
        self.assertEqual(datos['results'][0]['nombre'], 'Solo niños')


class AlimentoGuardadoTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.grupo = GrupoAlimento.objects.create(nombre='Leguminosas')
        cls.alimento = crear_alimento(
            cls.grupo, 'Arveja seca cocida',
            porcion_g=Decimal('157.000'), kcal=Decimal('190.000'),
            proteina_g=Decimal('13.000'), grasa_total_g=Decimal('0.600'),
            cho_g=Decimal('33.100'), fibra_g=Decimal('13.000'),
        )

    def test_guardar_devuelve_201_con_el_alimento_anidado(self):
        r = self.client.post('/api/guardados/',
                             {'alimento_id': self.alimento.id, 'cantidad': 2},
                             format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['alimento']['nombre'], 'Arveja seca cocida')
        self.assertEqual(r.data['alimento']['grupo']['nombre'], 'Leguminosas')
        self.assertEqual(Decimal(r.data['cantidad']), Decimal('2.00'))

    def test_guardar_con_un_alimento_inexistente_devuelve_400(self):
        r = self.client.post('/api/guardados/',
                             {'alimento_id': 999999, 'cantidad': 1}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_la_cantidad_por_defecto_es_uno(self):
        r = self.client.post('/api/guardados/', {'alimento_id': self.alimento.id},
                             format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(r.data['cantidad']), Decimal('1.00'))

    def test_el_listado_trae_el_alimento_anidado(self):
        AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('2'))
        datos = self.client.get('/api/guardados/').json()
        self.assertEqual(datos['count'], 1)
        self.assertEqual(datos['results'][0]['alimento']['nombre'], 'Arveja seca cocida')

    def test_el_listado_no_dispara_consultas_por_cada_alimento(self):
        for _ in range(5):
            AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('1'))
        with self.assertNumQueries(2):
            self.client.get('/api/guardados/')

    def test_eliminar_devuelve_204(self):
        g = AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('1'))
        r = self.client.delete(f'/api/guardados/{g.id}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AlimentoGuardado.objects.filter(id=g.id).exists())

    def test_totales_multiplican_por_la_cantidad(self):
        AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('2'))
        AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('2'))
        datos = self.client.get('/api/guardados/total/').json()

        # el alimento dos veces con cantidad 2 = cuatro porciones
        self.assertEqual(Decimal(str(datos['porcion_g'])), Decimal('628.0'))
        self.assertEqual(Decimal(str(datos['kcal'])), Decimal('760.0'))
        self.assertEqual(Decimal(str(datos['proteina_g'])), Decimal('52.0'))
        self.assertEqual(Decimal(str(datos['grasa_total_g'])), Decimal('2.4'))
        self.assertEqual(Decimal(str(datos['cho_g'])), Decimal('132.4'))
        self.assertEqual(Decimal(str(datos['fibra_g'])), Decimal('52.0'))
        self.assertEqual(datos['items'], 2)

    def test_totales_con_media_porcion(self):
        AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('0.5'))
        datos = self.client.get('/api/guardados/total/').json()
        self.assertEqual(Decimal(str(datos['kcal'])), Decimal('95.0'))

    def test_totales_sin_registros_devuelven_cero_y_no_null(self):
        datos = self.client.get('/api/guardados/total/').json()
        for campo in ('porcion_g', 'kcal', 'proteina_g', 'grasa_total_g', 'cho_g', 'fibra_g'):
            self.assertIsNotNone(datos[campo], f'{campo} llegó como null')
            self.assertEqual(Decimal(str(datos[campo])), Decimal('0'))
        self.assertEqual(datos['items'], 0)

    def test_borrar_el_alimento_arrastra_sus_guardados(self):
        """on_delete=CASCADE: los guardados no deben quedar huérfanos."""
        g = AlimentoGuardado.objects.create(alimento=self.alimento, cantidad=Decimal('1'))
        self.alimento.delete()
        self.assertFalse(AlimentoGuardado.objects.filter(id=g.id).exists())
