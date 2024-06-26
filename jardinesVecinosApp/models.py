import datetime
from django.db import models


# Create your models here.
class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='Id Categoria') 
    nombreCategoria= models.CharField(max_length=40, verbose_name='Nombre Categoria')

    def __str__(self):
        return self.nombreCategoria


class Producto(models.Model):
    idProducto = models.CharField(primary_key=True, max_length=5, verbose_name='Id Producto')
    stock = models.IntegerField(verbose_name='Stock')
    nombre = models.CharField(max_length=40, verbose_name='Nombre')
    descripcion= models.CharField(max_length=40, verbose_name='Descripcion')
    precio = models.IntegerField(verbose_name='Precio')
    imagen= models.ImageField(upload_to="imagenes", null=True, verbose_name='Imagen')
    categoria= models.ForeignKey('Categoria', on_delete=models.CASCADE, verbose_name='Categoria')

    def __str__(self):
        return self.idProducto

class Boleta(models.Model):
    idBoleta=models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False, null=False, default = datetime.datetime.now)

    def __str__(self):
        return str(self.idBoleta)
    
class detalle_boleta(models.Model):
    idBoleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)