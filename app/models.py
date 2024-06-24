# En el archivo models.py
from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    correo = models.EmailField()

    class Meta:
        db_table = 'Proveedor'


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    stock = models.IntegerField()
    stock_minimo = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Producto'

    def necesita_reabastecimiento(self):
        return self.stock <= self.stock_minimo


class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad_solicitada = models.IntegerField()
    fecha_entrega = models.DateTimeField()
    ENTREGADO = 'ENT'
    PENDIENTE = 'PEN'
    ESTADOS_ENTREGA = [
        (ENTREGADO, 'Entregado'),
        (PENDIENTE, 'Pendiente'),
    ]
    estado_entrega = models.CharField(
        max_length=3,
        choices=ESTADOS_ENTREGA,
        default=PENDIENTE,
    )

    class Meta:
        db_table = 'Pedido'


class Alerta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()

    class Meta:
        db_table = 'Alerta'
