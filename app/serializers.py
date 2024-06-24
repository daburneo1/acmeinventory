from rest_framework import serializers
from .models import Proveedor, Producto, Pedido


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'direccion', 'telefono', 'correo']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'stock', 'stock_minimo', 'precio', 'proveedor']


class PedidoSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'producto', 'proveedor', 'cantidad_solicitada', 'fecha_entrega', 'estado_entrega']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        estado_entrega = representation['estado_entrega']
        if estado_entrega == 'PEN':
            representation['estado_entrega'] = 'PENDIENTE'
        elif estado_entrega == 'ENT':
            representation['estado_entrega'] = 'ENTREGADO'
        return representation

    def to_internal_value(self, data):
        if 'estado_entrega' in data:
            if data['estado_entrega'] == 'PENDIENTE':
                data['estado_entrega'] = 'PEN'
            elif data['estado_entrega'] == 'ENTREGADO':
                data['estado_entrega'] = 'ENT'
        return super().to_internal_value(data)