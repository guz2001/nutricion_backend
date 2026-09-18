from rest_framework import serializers
from apps.alimentos.models import Alimento
from apps.alimentos.models import GrupoAlimento
from apps.alimentos.models import AlimentoGuardado

class GrupoAlimentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=GrupoAlimento
        fields=['id','nombre']


class AlimentoListSerializer(serializers.ModelSerializer):
    grupo=GrupoAlimentoSerializer(read_only=True)#Lo que hace esto es decirle a django que no solo me de el id del grupo alimento,
    class Meta:
        
        #Necesito que me de todo lo relacionado a ese GrupoAlimento por que cada numero corresponde a un grupo ya sea lacteos etc
        model=Alimento
        fields=['id','nombre','porcion_g','kcal','cho_g','grasa_total_g','proteina_g','unidad_medida','grupo','fibra_g']


class AlimentoAllSerializer(serializers.ModelSerializer):
    grupo=GrupoAlimentoSerializer(read_only=True)#Lo que hace esto es decirle a django que no solo me de el id del grupo alimento,
    class Meta:
        model=Alimento
        fields='__all__'


class AlimentoGuardadoSerializer(serializers.ModelSerializer):
    """
    Hay dos campos para el mismo alimento porque leer y escribir necesitan formas distintas:

    - alimento    (lectura):  serializer anidado, devuelve el objeto completo para que el
                              frontend tenga nombre, kcal, etc. sin una segunda consulta.
    - alimento_id (escritura): al hacer POST el frontend solo manda el id.
                              PrimaryKeyRelatedField valida que ese id exista y
                              source='alimento' le dice a DRF que ese valor va al
                              campo alimento del modelo. Es write_only porque el id
                              ya viene dentro del objeto anidado en las respuestas.
    """
    alimento = AlimentoListSerializer(read_only=True)
    alimento_id = serializers.PrimaryKeyRelatedField(
        queryset=Alimento.objects.all(),
        source='alimento',
        write_only=True
    )

    class Meta:
        model = AlimentoGuardado
        fields = ['id', 'alimento', 'alimento_id', 'cantidad', 'creado_en']
        read_only_fields = ['id', 'creado_en']
