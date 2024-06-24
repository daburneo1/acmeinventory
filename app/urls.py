from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProveedorViewSet, ProductoViewSet, PedidoViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]