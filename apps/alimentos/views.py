from rest_framework import viewsets
from  apps.alimentos.serializers import GrupoAlimentoSerializer,AlimentoListSerializer,AlimentoAllSerializer
from apps.alimentos.models import GrupoAlimento,Alimento
from apps.alimentos.filters import AlimentoFilter
from django.contrib.postgres.search import TrigramSimilarity

class GrupoAlimentoViewSet(viewsets.ModelViewSet):
    queryset= GrupoAlimento.objects.all()
    serializer_class=GrupoAlimentoSerializer



class AlimentoViewSet(viewsets.ModelViewSet):
    queryset=Alimento.objects.all()
    serializer_class=AlimentoAllSerializer
    filterset_class= AlimentoFilter

    def get_serializer_class(self):     # <- La lógica que necesitas es: "si la acción es 'list', usa el serializer corto(List); si no, usa el completo(All"
        if self.action == 'list':
            return AlimentoListSerializer
            
        return AlimentoAllSerializer
    
    def get_queryset(self):
        queryset=Alimento.objects.all()
        q=self.request.query_params.get('q')#Busca en el proyecto una variable con este nombre,

        if q:
            queryset=queryset.annotate(parecido=TrigramSimilarity('nombre',q)) #Calcular el puntaje de similitud hasta aca solo hace esto lo de abajo lo mostrar
            queryset =queryset.filter(parecido__gt=0.1)#Aca si lo  muestra por que le dice que dice que queryset es igual a solo mostrar los datos mayores a 0.1
            orderby=queryset.order_by('-parecido') 
            return orderby      # <- devuelve la lista de alimentos filtrados


        return queryset  #<- Si esta vacio devuelve todo los datos osea Alimento.objetcs.all()