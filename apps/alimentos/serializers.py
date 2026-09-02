from rest_framework import serializers
from apps.alimentos.models import Alimento
from apps.alimentos.models import GrupoAlimento

class GrupoAlimentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=GrupoAlimento
        fields=['id','nombre']


class AlimentoListSerializer(serializers.ModelSerializer):
    grupo=GrupoAlimentoSerializer(read_only=True)#Lo que hace esto es decirle a django que no solo me de el id del grupo alimento,
    class Meta:
        
        #Necesito que me de todo lo relacionado a ese GrupoAlimento por que cada numero corresponde a un grupo ya sea lacteos etc
        model=Alimento
        fields=['id','nombre','porcion_g','kcal','cho_g','grasa_total_g','proteina_g','unidad_medida','grupo']


class AlimentoAllSerializer(serializers.ModelSerializer):
    grupo=GrupoAlimentoSerializer(read_only=True)#Lo que hace esto es decirle a django que no solo me de el id del grupo alimento,
    class Meta:
        model=Alimento
        fields='__all__'
        