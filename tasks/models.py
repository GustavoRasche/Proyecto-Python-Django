from django.db import models

# Create your models here.



delivery = [
    ('Envío','Envío'),
    ('Sin Envío', 'Sin Envío')
]

estado_pedido = [
    ('Activo','En curso'),
    ('Entregado','Finalizado'),
]


categoria_producto = [
    ('Dimensionado','Dimensionado'),
    ('Forro','Forro'),
    ('Traslapo','Traslapo'),
    ('Molduras','Molduras')
]

cliente = [
    ('Ingresado', ' Ingresado'),
]



class Empleado(models.Model):
    idempleado = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo Empleado')
    nombreEmpleado = models.CharField(max_length=50, null= False)
    correo = models.CharField(max_length=50, null=False)
    contraseña = models.CharField(max_length=8)
  
    
class Usuario(models.Model): 
    
    idusuario = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    rutC = models.CharField(max_length=12, null=False, verbose_name='Rut Cliente')
    nombre = models.CharField(max_length=100, null=False, unique=True )
    apellidoPaterno = models.CharField(max_length=45, null=False, verbose_name='Apellido')
    correo = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"{self.nombre} {self.apellidoPaterno}"
    
class Producto(models.Model):
    
    idproducto = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    categoria = models.CharField(null=False, blank=False, choices=categoria_producto, default='Dimensionado')
    dimensionado = models.CharField(max_length=45, null=False, default='2x3')
    descripcion = models.CharField(max_length=255)
    precio = models.IntegerField(null=False)
    
    
class Envio(models.Model):
    idenvio = models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo Envio')
    direccion = models.CharField(max_length=50)
    estado = models.IntegerField()
    

class Pedido(models.Model):
    idpedido = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    fechaIngreso = models.DateTimeField(null=False)
    descripcion = models.CharField(max_length=255)
    precio = models.IntegerField(null=False)
    cliente = models.ForeignKey(Usuario, null=True, blank=False, on_delete=models.CASCADE)
    productos = models.ForeignKey(Producto, null=True, blank=False, on_delete=models.CASCADE)
    estadopedido = models.CharField(max_length=30, choices=estado_pedido, default='Activo',)
    reparto = models.CharField(max_length=30, choices=delivery, default='Sin Envío')

class Historial(models.Model):
    idhistorial = models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Historial Pedidos')
    pedido = models.ForeignKey(Pedido, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name