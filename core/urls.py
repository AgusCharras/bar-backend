from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet,
    ReservaViewSet,
    VoucherViewSet,
    RepresentanteViewSet,
    EntradaViewSet,
    AsistenciaRepresentanteViewSet
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'vouchers', VoucherViewSet)
router.register(r'representantes', RepresentanteViewSet)
router.register(r'entradas', EntradaViewSet)
router.register(r'asistencias', AsistenciaRepresentanteViewSet)

urlpatterns = router.urls