from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import FormAserradero
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
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

def eliminarProducto(request, idproducto):
    prod = Producto.objects.get(idproducto = idproducto)   
    prod.delete()
    return redirect('/catalogo')

def actualizarProducto(request, idproducto):
     if request.method == 'GET':
        prod = Producto.objects.get(idproducto = idproducto)
        form = FormAserradero(instance = prod)
        return render(request, 'ingresar_producto.html', {'prod': prod, 'form' : form})
      
     else:
         prod = Producto.objects.get(producto = idproducto)
         form = FormAserradero(request.POST, instance=prod)
         if form.is_valid():
            form.save()
         return redirect('/catalogo')
         data = {'form' : form}
         return render(request, 'ingresar_producto.html', data)

def igresarUsuario(request):
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

