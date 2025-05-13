from django.db import models
from usuarios.models import Usuario,Empresa, Sucursal,Moneda

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)  # AutoIncremental
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'proveedor'


class Almacen(models.Model):
    id_almacen = models.AutoField(primary_key=True)  # AutoIncremental
    nombre_almacen = models.CharField(max_length=100)

    class Meta:
        db_table = 'Almacen'


class CasaCambioCompra(models.Model):
    id_operacion_compra = models.AutoField(primary_key=True)  # AutoIncremental
    fecha = models.DateTimeField()
    corte_100 = models.IntegerField()
    corte_50 = models.IntegerField()
    corte_20 = models.IntegerField()
    corte_10 = models.IntegerField()
    corte_5 = models.IntegerField()
    corte_1 = models.IntegerField()
    total_calculado = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField()
    id_moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)  # Recomendación: usar ForeignKey a una tabla 'Moneda'
    observaciones = models.CharField(max_length=255)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    total_ganado = models.DecimalField(max_digits=10, decimal_places=2)
    nota_anulacion = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'casa_cambio_compra'
