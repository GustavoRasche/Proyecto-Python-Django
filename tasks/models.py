from django.db import models

# Create your models here.
class Usuario(models.Model): 
    
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    rutC = models.CharField(max_length=12, null=False)
    nombre = models.CharField(max_length=100, null=False, unique=True )
    apellidoPaterno = models.CharField(max_length=45, null=False)
    correo = models.CharField(max_length=255, null=False)
    contraseña = models.CharField(max_length=50, null=False)
    
    
    def todo(self):
        return Usuario
    
    
class Empleado(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo Empleado')
    correo = models.CharField(max_length=50, null=False)
    contraseña = models.CharField(max_length=8)

class Pedido(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    estadoP = models.CharField(max_length=50, null=False)
    fechaIngreso = models.DateTimeField(null=False)
    descripcion = models.CharField(max_length=255)
    precio = models.IntegerField(null=False)

    
    
    def __str__(self):
        return self.estadoP
    

class Producto(models.Model):
   
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    dimensionado = models.CharField(max_length=45, null=False, default='2x3')
    descripcion = models.CharField(max_length=255)
    precio = models.IntegerField(null=False)
    

    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def mostrar(self):
        return Producto
    

class Envio(models.Model):
    id = models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo Envio')
    direccion = models.CharField(max_length=50)
    estado = models.IntegerField()
    

    class Meta:
        verbose_name = ("Envio")
        verbose_name_plural = ("Envios")

    def __str__(self):
        return self.idEnvio

class Historial(models.Model):
    id = models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Historial Pedidos')
    pedido = models.ForeignKey(Pedido, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Historial")
        verbose_name_plural = ("Historiales")

    def __str__(self):
        return self.name