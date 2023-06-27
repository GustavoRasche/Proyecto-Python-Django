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
    
    fechaIngreso = forms.DateTimeField(label='Fecha de Ingreso')
    descripcion = forms.CharField(label='Descripcion')
    precio = forms.IntegerField(label='Precio')
    estadopedido = forms.CharField(label='Estado', widget=forms.Select(choices=estado_pedido))
    reparto = forms.CharField(label='Reparto', widget=forms.Select(choices=delivery))
    cliente = forms.ModelChoiceField(queryset=Usuario.objects.all(), label='Cliente')
    class Meta:
        model = Pedido
        fields = '__all__'
        
        

        