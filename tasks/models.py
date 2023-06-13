from django.db import models

# Create your models here.
categoria_producto = [
    (1,'Dimensionado'),
    (2,'Forro'),
    (3,'Traslapo'),
    (4,'Molduras')
]

class Empleado(models.Model):
    idempleado = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo Empleado')
    correo = models.CharField(max_length=50, null=False)
    contraseña = models.CharField(max_length=8)
   
    def __str__(self):
       return self.idempleado
    
class Usuario(models.Model): 
    
    idusuario = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    rutC = models.CharField(max_length=12, null=False)
    nombre = models.CharField(max_length=100, null=False, unique=True )
    apellidoPaterno = models.CharField(max_length=45, null=False)
    correo = models.CharField(max_length=255, null=False)
    contraseña = models.CharField(max_length=50, null=False)
    empleado = models.ForeignKey(Empleado, null=True, blank=False, on_delete=models.CASCADE)
    
    def todo(self):
        return Usuario
    
class Producto(models.Model):
    
    idproducto = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    categoria = models.IntegerField(null=False, blank=False, choices=categoria_producto,default=1)
    dimensionado = models.CharField(max_length=45, null=False, default='2x3')
    descripcion = models.CharField(max_length=255)
    precio = models.IntegerField(null=False)
    

    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def mostrar(self):
        return Producto
    
    
class Envio(models.Model):
    idenvio = models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo Envio')
    direccion = models.CharField(max_length=50)
    estado = models.IntegerField()
    

    class Meta:
        verbose_name = ("Envio")
        verbose_name_plural = ("Envios")

    def __str__(self):
        return self.idEnvio

class Pedido(models.Model):
    idpedido = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    estadoP = models.CharField(max_length=50, null=False)
    fechaIngreso = models.DateTimeField(null=False)
    descripcion = models.CharField(max_length=255)
    precio = models.IntegerField(null=False)
    estado = models.ForeignKey(Envio, null=True, blank=False, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, null=True, blank=False, on_delete=models.CASCADE)
    productos = models.ForeignKey(Producto, null=True, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.estadoP
    
class Historial(models.Model):
    idhistorial = models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Historial Pedidos')
    pedido = models.ForeignKey(Pedido, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name