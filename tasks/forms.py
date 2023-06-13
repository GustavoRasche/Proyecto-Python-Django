from django import forms
from tasks.models import *


class FormAserradero(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
class FormUsuario(forms.ModelForm)    :   
    class Meta:
        model =  Usuario
        fields = '__all__'

class FormPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        

        