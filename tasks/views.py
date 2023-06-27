from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .forms import *
from .models import Producto


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
    if request.method == 'GET':
        return render(request, 'ingresar_pedido.html',{
            'form': FormPedido
        })
    else:
        try:
            form = FormPedido(request.POST)
            if form.is_valid():
                form.save()
            return redirect('/home')
        
        except ValueError:
            return render(request, 'ingresar_pedido.html',{
                'form': FormPedido,
                'error': 'Ingrese datos correctamente'
            })

def listadoPedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'home.html', {'pedidos': pedidos})

def historialPedidos(request):
    historial = Pedido.objects.all()
    return render(request, 'historial.html', {'historial': historial})

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