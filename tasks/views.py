from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def inicio(request):
    return render(request, 'signup.html', {
        'form' : UserCreationForm
    })

def home(request):
    return render(request, 'home.html')
    

def catalogo(request):
    return render(request, 'catalogo.html')

def ventas(request):
    return render(request, 'ventas.html')

def historial(request):
    return render(request, 'historial.html')