from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet,
    ReservaViewSet,
    VoucherViewSet,
    RepresentanteViewSet
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'vouchers', VoucherViewSet)
router.register(r'representantes', RepresentanteViewSet)

urlpatterns = router.urls