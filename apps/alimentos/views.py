from rest_framework import viewsets
from  apps.alimentos.serializers import GrupoAlimentoSerializer,AlimentoListSerializer,AlimentoAllSerializer
from apps.alimentos.models import GrupoAlimento,Alimento


class GrupoAlimentoViewSet(viewsets.ModelViewSet):
    queryset= GrupoAlimento.objects.all()
    serializer_class=GrupoAlimentoSerializer



class AlimentoViewSet(viewsets.ModelViewSet):
    queryset=Alimento.objects.all()
    serializer_class=AlimentoAllSerializer

    def get_serializer_class(self):     # <- La lógica que necesitas es: "si la acción es 'list', usa el serializer corto(List); si no, usa el completo(All"
        if self.action == 'list':
            return AlimentoListSerializer
            
        return AlimentoAllSerializer