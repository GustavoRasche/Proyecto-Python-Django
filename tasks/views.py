from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.db.models import Q
from .forms import *
from .models import Producto
from datetime import datetime


# Create your views here.
def inicio(request):
    return render(request, 'signup.html', {
        'form' : UserCreationForm
    })

def home(request):
    return render(request, 'home.html')
    

def catalogo(request):
    return render(request, 'catalogo.html')

def historial(request):
    return render(request, 'historial.html')

def dashboard(request):
    return render(request, 'dashboard.html')


def ingresarProducto(request):
    if request.method == 'GET':
        return render(request, 'ingresar_producto.html',{
            'form': FormAserradero
        })
    else:
        try:
            form = FormAserradero(request.POST)
            if form.is_valid():
                form.save()
            return redirect('/catalogo')
    
        except ValueError:
            return render(request, 'ingresar_producto.html',{
                'form' : FormAserradero,
                'error' :  'Porfavor envia los datos correctamente'
        })

def listadoProductos(request):
    busqueda = request.POST.get("buscar")
    productos = Producto.objects.all()
    
    if busqueda: 
        productos = Producto.objects.filter(
            Q(categoria__icontains = busqueda)|
            Q(dimensionado__icontains = busqueda )|
            Q(descripcion__icontains= busqueda)|
            Q(precio__icontains = busqueda)
        ).distinct()
        
    return render(request, 'catalogo.html', {'productos': productos})

def eliminarProducto(request, idproducto):
    prod = Producto.objects.get(idproducto = idproducto)   
    prod.delete()
    return redirect('/catalogo')


def actualizarProducto(request, idproducto):
    prod = Producto.objects.get(idproducto=idproducto)

    if request.method == 'POST':
        form = FormAserradero(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('/catalogo')
    else:
        form = FormAserradero(instance=prod)

    data = {'prod': prod, 'form': form}
    return render(request, 'actualizar_producto.html', data)

def ingresarUsuario(request):
    if request.method == 'GET':
        return render(request, 'ingresar_usuario.html',{
            'form': FormUsuario
        })
    else:
        try:
            form = FormUsuario(request.POST)
            if form.is_valid():
                form.save()
            return redirect('/ingresar/pedido')
        
        except ValueError:
            return render(request, 'ingresar_usuario.html',{
                'form': FormUsuario,
                'error': 'Ingrese datos correctamente'
            })

def ingresarPedido(request):
    ultimo_cliente = Usuario.objects.latest('idusuario')
    
    if request.method == 'POST':
        formulario = FormPedido(request.POST)
        if formulario.is_valid():
            pedido = formulario.save(commit=False)
            cliente_id = request.POST['cliente']
            cliente = Usuario.objects.get(idusuario=cliente_id)
            pedido.cliente = cliente
            pedido.save()
            return redirect('/home')
    else:
        formulario = FormPedido()

    return render(request, 'ingresar_pedido.html', {'ultimo_cliente': ultimo_cliente, 'formulario': formulario})

def listadoPedidos(request):
    busqueda = request.POST.get("buscar")
    pedidos = Pedido.objects.all()
    
    if busqueda:
        pedidos = Pedido.objects.filter(
            Q(fechaIngreso__icontains = busqueda)|
            Q(descripcion__icontains = busqueda)|
            Q(precio__icontains = busqueda)|
            Q(cliente__nombre__icontains = busqueda)|
            Q(cliente__rutC__icontains = busqueda)|
            Q(productos__categoria__icontains = busqueda)|
            Q(estadopedido__icontains = busqueda)|
            Q(reparto__icontains = busqueda)
        ).distinct()
    
       
    return render(request, 'home.html', {'pedidos': pedidos})


def historialPedidos(request):
    historial = Pedido.objects.all()
<<<<<<< HEAD
    datos = {}  # Initialize the datos dictionary
    
    if request.method == 'POST':
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        
        # Convertir las fechas de texto a objetos de fecha y hora
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        
        # Filtrar los pedidos por el rango de fecha
        historial = Pedido.objects.filter(fechaIngreso__range=[fecha_desde, fecha_hasta])
        count = len(historial)
        
        datos = {
            'pedidos': historial,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'count': count,
            'message': 'Pedidos entre las fechas: '
        }
    
    return render(request, 'historial.html', {'datos': datos})
    
=======
    return render(request, 'historial.html', {'historial': historial})



>>>>>>> 879e16c808e0c33062aa04f4f99bedc734c055a7
def eliminarPedido(request, idpedido):
    prod = Pedido.objects.get(idpedido = idpedido)   
    prod.delete()
    return redirect('/home')


def actualizarPedido(request, idpedido):
    ped = Pedido.objects.get(idpedido=idpedido)

    if request.method == 'POST':
        form = FormPedido(request.POST, instance=ped)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = FormPedido(instance=ped)

    data = {'ped': ped, 'form': form}
    return render(request, 'actualizar_pedido.html', data)


<<<<<<< HEAD
        
    
=======

>>>>>>> 879e16c808e0c33062aa04f4f99bedc734c055a7
