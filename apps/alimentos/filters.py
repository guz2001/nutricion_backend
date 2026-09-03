import django_filters
from apps.alimentos.models import Alimento


class AlimentoFilter(django_filters.FilterSet):
    grupo_id= django_filters.NumberFilter(field_name='grupo') 
    """
    → esto crea un filtro nuevo que se llama grupo_id (así es como aparecerá en la URL: ?grupo_id=1),
      pero por dentro, cuando ejecute la consulta, va a buscar en el campo real del modelo que es grupo 
      (field_name='grupo' es la traducción entre el nombre de la URL y 
      el nombre real de la columna).
    """
    class Meta:
        model = Alimento
        fields =  ['poblacion','grupo_id']