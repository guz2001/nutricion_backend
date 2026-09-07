from rest_framework import viewsets
from  apps.alimentos.serializers import GrupoAlimentoSerializer,AlimentoListSerializer,AlimentoAllSerializer
from apps.alimentos.models import GrupoAlimento,Alimento
from apps.alimentos.filters import AlimentoFilter
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

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
    """
     poblacion=''
    if poblacion== 'niños' or  poblacion== 'niños_y_adultos':
        queryset= GrupoAlimento.objects.filter(Q(poblacion='niños')|Q(poblacion='niños_y_adultos'))
    
        serializer_class=GrupoAlimentoSerializer

    elif poblacion== 'adultos' or  poblacion== 'niños_y_adultos':
        queryset= GrupoAlimento.objects.filter(Q(poblacion='adultos')|Q(poblacion='niños_y_adultos'))
        serializer_class=GrupoAlimentoSerializer
    elif poblacion== 'menores_de_dos_anios':
        queryset= GrupoAlimento.objects.filter(poblacion='menores_de_dos_anios')
        serializer_class=GrupoAlimentoSerializer
    """
    
    def get_queryset(self):
        queryset=Alimento.objects.all()
        poblacion=self.request.query_params.get('poblacion')
        q=self.request.query_params.get('q')#Busca en el proyecto una variable con este nombre,
        if poblacion== 'adultos':
            queryset=queryset.filter(Q(poblacion='adultos')|Q(poblacion='niños_y_adultos'))
            
        
        elif poblacion== 'niños':
            queryset=queryset.filter(Q(poblacion='niños')|Q(poblacion='niños_y_adultos'))

        elif poblacion== 'menores_de_dos_anios':
                    queryset=queryset.filter(poblacion='menores_de_dos_anios')


        elif poblacion== 'niños_y_adultos':
                    queryset=queryset.filter(poblacion='niños_y_adultos')
        if q:
            queryset=queryset.annotate(parecido=TrigramSimilarity('nombre',q)) #Calcular el puntaje de similitud hasta aca solo hace esto lo de abajo lo mostrar
            queryset =queryset.filter(parecido__gt=0.1)#Aca si lo  muestra por que le dice que dice que queryset es igual a solo mostrar los datos mayores a 0.1
            orderby=queryset.order_by('-parecido') 
            return orderby      # <- devuelve la lista de alimentos filtrados


        return queryset  #<- Si esta vacio devuelve todo los datos osea Alimento.objetcs.all()