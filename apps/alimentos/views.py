from rest_framework import viewsets
from  apps.alimentos.serializers import GrupoAlimentoSerializer
from apps.alimentos.models import GrupoAlimento


class GrupoAlimentoViewSet(viewsets.ModelViewSet):
    queryset= GrupoAlimento.objects.all()
    serializer_class=GrupoAlimentoSerializer



