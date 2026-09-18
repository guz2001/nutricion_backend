from rest_framework import viewsets
from  apps.alimentos.serializers import GrupoAlimentoSerializer,AlimentoListSerializer,AlimentoAllSerializer,AlimentoGuardadoSerializer
from apps.alimentos.models import GrupoAlimento,Alimento,AlimentoGuardado
from apps.alimentos.filters import AlimentoFilter
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from rest_framework.response import Response

# ReadOnlyModelViewSet y no ModelViewSet: grupos_alimentos es una tabla preexistente
# con datos reales. Solo expone GET (list y retrieve); nunca POST, PUT, PATCH ni DELETE.
class GrupoAlimentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= GrupoAlimento.objects.all()
    serializer_class=GrupoAlimentoSerializer
    
    def get_queryset(self):
        queryset= GrupoAlimento.objects.all()
        poblacion=self.request.query_params.get('poblacion')
        
        
        if poblacion:
            # aqui distinct() SI hace falta: el filtro cruza hacia alimento y un
            # grupo aparece una vez por cada alimento suyo que coincida
            queryset=queryset.filter(alimento__poblacion=poblacion).distinct()

        # order_by explicito por el mismo motivo que en alimentos: sin ORDER BY
        # PostgreSQL no garantiza un orden estable y la paginacion se vuelve poco fiable
        return queryset.order_by('nombre','id')

# ReadOnlyModelViewSet: la tabla alimentos es preexistente y de solo consulta.
# Con ModelViewSet la API quedaba abierta a escritura publica sobre los 553 registros reales.
class AlimentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Alimento.objects.all()
    serializer_class=AlimentoAllSerializer
    filterset_class= AlimentoFilter

    def get_serializer_class(self):     # <- La lógica que necesitas es: "si la acción es 'list', usa el serializer corto(List); si no, usa el completo(All"
        if self.action == 'list':
            return AlimentoListSerializer
            
        return AlimentoAllSerializer
    def get_queryset(self):
        # select_related trae el grupo en el mismo JOIN. Sin esto, como el serializer
        # anida GrupoAlimentoSerializer, listar 20 alimentos disparaba 20 consultas
        # extra (problema N+1): 22 consultas por pagina en vez de 2.
        queryset=Alimento.objects.select_related('grupo')
        poblacion=self.request.query_params.get('poblacion')
        q=self.request.query_params.get('q')#Busca en el proyecto una variable con este nombre,
        if poblacion:
            # sin distinct(): poblacion es columna de la propia tabla, el filtro no
            # puede generar duplicados y DISTINCT solo agregaba un ordenamiento inutil
            queryset=queryset.filter(poblacion=poblacion)

        if q:
            queryset=queryset.annotate(parecido=TrigramSimilarity('nombre',q)) #Calcular el puntaje de similitud hasta aca solo hace esto lo de abajo lo mostrar
            queryset =queryset.filter(parecido__gt=0.1)#Aca si lo  muestra por que le dice que dice que queryset es igual a solo mostrar los datos mayores a 0.1
            # 'id' como segundo criterio: si dos alimentos empatan en similitud el
            # orden seria arbitrario y la paginacion podria repetirlos u omitirlos
            return queryset.order_by('-parecido','id')

        # order_by explicito: PostgreSQL no garantiza un orden estable sin ORDER BY,
        # asi que al paginar un mismo alimento podia salir dos veces o ninguna.
        return queryset.order_by('nombre','id')


class AlimentoGuardadoViewSet(viewsets.ModelViewSet):
    # select_related trae el alimento y su grupo en el mismo JOIN.
    # Sin esto, listar 20 guardados dispararia 20 consultas extra por el alimento
    # y otras 20 por el grupo (problema N+1).
    queryset = AlimentoGuardado.objects.select_related('alimento', 'alimento__grupo').all()
    serializer_class = AlimentoGuardadoSerializer

    # @action agrega una ruta propia al ViewSet, aparte de las que ya crea el router.
    # detail=False -> actua sobre toda la coleccion (/api/guardados/total/)
    # y no sobre un registro puntual (/api/guardados/5/total/).
    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Devuelve la suma de los valores nutricionales de todos los
        alimentos guardados, multiplicados por su cantidad.
        Ruta: GET /api/guardados/total/
        """
        campos = {
            'porcion_g': 'alimento__porcion_g',
            'kcal': 'alimento__kcal',
            'proteina_g': 'alimento__proteina_g',
            'grasa_total_g': 'alimento__grasa_total_g',
            'cho_g': 'alimento__cho_g',
            'fibra_g': 'alimento__fibra_g',
        }

        # F() referencia columnas dentro de la consulta, asi la multiplicacion
        # cantidad * valor se hace en SQL y no en Python.
        # Coalesce(..., 0) es necesario porque Sum() devuelve None cuando no hay
        # ningun registro; sin el, el frontend recibiria null en vez de 0.
        agregaciones = {
            nombre: Coalesce(
                Sum(
                    F('cantidad') * F(ruta),
                    output_field=DecimalField(max_digits=14, decimal_places=3)
                ),
                0,
                output_field=DecimalField(max_digits=14, decimal_places=3)
            )
            for nombre, ruta in campos.items()
        }

        # aggregate ejecuta las 6 sumas en una sola consulta
        totales = AlimentoGuardado.objects.aggregate(**agregaciones)
        totales['items'] = AlimentoGuardado.objects.count()

        return Response(totales)
