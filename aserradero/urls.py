"""
URL configuration for aserradero project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio),
    path('historial/', views.historial),
    path('dashboard/', views.dashboard),
    path('ingresar/producto', views.ingresarProducto),
    path('catalogo/', views.listadoProductos),
    path('ingresar/usuario', views.ingresarUsuario),
    path('eliminarProducto/<int:idproducto>', views.eliminarProducto),
    path('actualizar/producto/<int:idproducto>', views.actualizarProducto, name='actualizar_producto'),
    path('ingresar/pedido', views.ingresarPedido),
    path('home/', views.listadoPedidos),
    path('eliminarPedido/<int:idpedido>',views.eliminarPedido),
    path('actualizar/pedido/<int:idpedido>', views.actualizarPedido, name='actualizar_pedido'),
    

    
]
