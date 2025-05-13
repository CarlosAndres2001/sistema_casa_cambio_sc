from django.db import models
from usuarios.models import Usuario, Moneda,Sucursal

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)  # AutoIncremental
    nombre_categoria = models.CharField(max_length=50)

    class Meta:
        db_table = 'categoria'


class Subcategoria(models.Model):
    id_subcategoria = models.AutoField(primary_key=True)  # AutoIncremental
    nombre_subcategoria = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subcategoria'


class Traspaso(models.Model):
    id_traspaso = models.AutoField(primary_key=True)  # AutoIncremental
    fecha_hora = models.DateTimeField()
    observaciones = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sucursal_destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='traspasos_destino')
    estado = models.IntegerField()
    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='traspasos_origen')
    nota_anulacion = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'traspaso'


class Egreso(models.Model):
    id_egreso = models.AutoField(primary_key=True)  # AutoIncremental
    fecha_hora = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    estado = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nota_anulacion = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'egreso'
