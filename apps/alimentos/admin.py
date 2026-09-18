from django.contrib import admin

from apps.alimentos.models import GrupoAlimento, Alimento, AlimentoGuardado


class SoloLecturaAdmin(admin.ModelAdmin):
    """
    Base para las tablas preexistentes (alimentos y grupos_alimentos):
    se pueden consultar desde el admin pero no crear, editar ni borrar.
    Es la misma decisión que en la API, donde esos dos ViewSets son
    ReadOnlyModelViewSet: son datos reales de producción que Django no administra.
    """
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GrupoAlimento)
class GrupoAlimentoAdmin(SoloLecturaAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


@admin.register(Alimento)
class AlimentoAdmin(SoloLecturaAdmin):
    list_display = ['id', 'nombre', 'grupo', 'poblacion', 'porcion_g', 'kcal']
    list_filter = ['poblacion', 'grupo']
    search_fields = ['nombre', 'subgrupo']
    list_select_related = ['grupo']  # evita una consulta por fila al mostrar el grupo


@admin.register(AlimentoGuardado)
class AlimentoGuardadoAdmin(admin.ModelAdmin):
    """Esta sí es editable: la tabla la administra Django."""
    list_display = ['id', 'alimento', 'cantidad', 'creado_en']
    list_select_related = ['alimento']
    autocomplete_fields = ['alimento']  # selector con búsqueda, no un <select> de 553 opciones
