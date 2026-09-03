from rest_framework.routers import DefaultRouter
from apps.alimentos.views import GrupoAlimentoViewSet, AlimentoViewSet

router= DefaultRouter()
router.register(r'alimentos',AlimentoViewSet)
router.register(r'grupos',GrupoAlimentoViewSet)
urlpatterns= router.urls