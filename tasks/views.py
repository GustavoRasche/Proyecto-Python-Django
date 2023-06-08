from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def inicio(request):
    return render(request, 'signup.html', {
        'form' : UserCreationForm
    })
