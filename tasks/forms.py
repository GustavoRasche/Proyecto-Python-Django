from django import forms
from tasks.models import Producto

class FormAserradero(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'