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
             return render(request, '/catalogo', {'productos': productos})
        
