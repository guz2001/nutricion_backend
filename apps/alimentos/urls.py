from rest_framework.routers import DefaultRouter
from apps.alimentos.views import GrupoAlimentoViewSet, AlimentoViewSet, AlimentoGuardadoViewSet

router= DefaultRouter()
router.register(r'alimentos',AlimentoViewSet)
router.register(r'grupos',GrupoAlimentoViewSet)
router.register(r'guardados',AlimentoGuardadoViewSet)
urlpatterns= router.urls