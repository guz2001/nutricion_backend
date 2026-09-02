from rest_framework import serializers
from apps.alimentos.models import Alimento
from apps.alimentos.models import GrupoAlimento

class GrupoAlimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model=GrupoAlimento
        fields=['id','nombre','descripcion']






class AlimentoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Alimento

        fields=['id','grupo','subgrupo','nombre','poblacion','porcion_g','unidad_medida','kcal',
            'proteina_g','grasa_total_g','ags_g','agm_g','agp_g','colesterol_mg','cho_g',
            'fibra_g','calcio_mg','fosforo_mg','hierro_mg','sodio_mg']
        #Cambiar esta clase mas tarde