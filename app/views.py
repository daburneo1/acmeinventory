from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Proveedor, Producto, Pedido
from .serializers import ProveedorSerializer, ProductoSerializer, PedidoSerializer
from decimal import Decimal
from django.db.models import F


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Hacemos una copia de los datos para no modificar el objeto original
        data['precio'] = Decimal(data['precio'])  # Convertimos el precio a decimal
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stock_bajo(self, request, *args, **kwargs):
        productos_bajo_stock = Producto.objects.filter(stock__lt=F('stock_minimo'))
        serializer = self.get_serializer(productos_bajo_stock, many=True)
        return Response(serializer.data)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # Obtén el pedido que se desea actualizar
        pedido = self.get_object()

        # Deserializa los datos de la solicitud y valida los datos
        serializer = self.get_serializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            # Si los datos son válidos, actualiza el pedido
            serializer.save()

            # Devuelve una respuesta con los datos del pedido actualizado
            return Response(serializer.data)

        # Si los datos no son válidos, devuelve una respuesta con los errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pedidos_con_proveedor(self, request, *args, **kwargs):
        pedidos_con_proveedor = Pedido.objects.select_related('proveedor')
        serializer = self.get_serializer(pedidos_con_proveedor, many=True)
        return Response(serializer.data)
