from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.db.models import Q
from .forms import *
from .models import *
from datetime import datetime, timedelta
from django.http import FileResponse
from django.template.loader import get_template
from django.views import View
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.response import TemplateResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import Count
from django.db.models.functions import ExtractMonth





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
    prod = Producto.objects.get(idproducto=idproducto)   
    prod.delete()
    return HttpResponse("Producto eliminado correctamente")


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

    historial = []
    datos = {'pedidos': historial, 'message': 'Menores a: '}

    historial = Pedido.objects.all()
    total_pedidos = len(historial)
    datos = {'pedidos': historial, 'total_pedidos': total_pedidos, 'message': 'Menores a: '}

    
    if request.method == 'POST':
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        
        # Convertir las fechas desde y hasta en objetos datetime
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        
        # Incrementar la fecha hasta en un día adicional
        fecha_hasta += timedelta(days=1)
        
        historial = Pedido.objects.filter(fechaIngreso__range=[fecha_desde, fecha_hasta])
        count = len(historial)
        
        datos['pedidos'] = historial
        datos['fecha_desde'] = fecha_desde
        datos['fecha_hasta'] = fecha_hasta - timedelta(days=1)
        datos['count'] = count

        return render(request, 'historial.html', {'datos': datos})
    return render(request, 'historial.html', {'datos': datos})
    
def eliminarPedido(request, idpedido):
    prod = Pedido.objects.get(idpedido = idpedido)   
    prod.delete()
    return HttpResponse("Producto eliminado correctamente")

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
 
class PDFExportView(View):
    def get(self, request):
        historial = Pedido.objects.all()  # Obtén todos los registros de la base de datos

        if not historial:
            return HttpResponse("No hay registros disponibles.")
        
        # Crea un objeto de documento PDF
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)

        # Define el estilo del título
        styles = getSampleStyleSheet()
        estilo_titulo = styles['Title']
        estilo_titulo.alignment = 1

        # Agrega el título al contenido del PDF
        titulo = Paragraph("Historial de ventas Aserradero LM", estilo_titulo)
        content = [titulo]

        # Define el estilo de la tabla
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Crea la tabla y agrega los datos
        tabla_datos = []
        cabeceras = ['Código', 'Estado', 'Fecha de la venta', 'Descripción', 'Precio', 'Cliente', 'Reparto']
        tabla_datos.append(cabeceras)

        for pedido in historial:
            fecha_venta = pedido.fechaIngreso.strftime('%Y-%m-%d %H:%M') # Formatear solo la parte de la fecha
            fila = [
                str(pedido.idpedido),
                pedido.estadopedido,
                fecha_venta,
                pedido.descripcion,
                str(pedido.precio),
                pedido.cliente,
                pedido.reparto
            ]
            tabla_datos.append(fila)

        tabla = Table(tabla_datos)
        tabla.setStyle(estilo_tabla)

        # Agrega la tabla al contenido del PDF
        content.append(tabla)

        # Genera el PDF
        pdf.build(content)

        # Configura la respuesta HTTP con el archivo PDF generado
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, as_attachment=True, filename='historial_ventas.pdf')

    def post(self, request):
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']

        # Convertir las fechas desde y hasta en objetos datetime
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()

        # Incrementar la fecha hasta en un día adicional
        fecha_hasta += timedelta(days=1)

        historial = Pedido.objects.filter(fechaIngreso__range=[fecha_desde, fecha_hasta])
        count = len(historial)

        # Crea un objeto de documento PDF
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)

        # Define el estilo del título
        styles = getSampleStyleSheet()
        estilo_titulo = styles['Title']
        estilo_titulo.alignment = 1

        # Agrega el título al contenido del PDF
        titulo = Paragraph("Historial de ventas Aserradero LM", estilo_titulo)
        content = [titulo]

        # Define el estilo de la tabla
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Crea la tabla y agrega los datos
        tabla_datos = []
        cabeceras = ['Código', 'Estado', 'Fecha de la venta', 'Descripción', 'Precio', 'Cliente', 'Reparto']
        tabla_datos.append(cabeceras)

        for pedido in historial:
            fecha_venta = pedido.fechaIngreso.strftime('%Y-%m-%d %H:%M')  # Formatear solo la parte de la fecha
            fila = [
                str(pedido.idpedido),
                pedido.estadopedido,
                fecha_venta,
                pedido.descripcion,
                str(pedido.precio),
                pedido.cliente,
                pedido.reparto
            ]
            tabla_datos.append(fila)

        tabla = Table(tabla_datos)
        tabla.setStyle(estilo_tabla)

        # Agrega la tabla al contenido del PDF
        content.append(tabla)

        # Genera el PDF
        pdf.build(content)

        # Configura la respuesta HTTP con el archivo PDF generado
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, as_attachment=True, filename='historial_ventas.pdf')


def login(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        try:
            empleado = Empleado.objects.get(correo=correo, contraseña=contraseña)
            # Si se encontró el usuario en la base de datos, realiza las acciones necesarias y redirecciona a la página principal.
            return redirect('/home')
        except Empleado.DoesNotExist:
            # Si no se encontró el usuario, muestra un mensaje de error.
            error = 'Correo o contraseña incorrectos'
            return render(request, 'signup.html', {'error': error})
    else:
        return render(request, 'signup.html')

def dashboard(request):
    ventas_por_mes = Pedido.objects.annotate(mes=ExtractMonth('fechaIngreso')).values('mes').annotate(total=Count('idpedido')).order_by('mes')

    ventas_data = [0] * 12  # Inicializar una lista con 12 elementos (un elemento para cada mes) y establecer todos los valores en cero

    for venta in ventas_por_mes:
        mes = venta['mes']
        total = venta['total']
        ventas_data[mes - 1] = total  # Restar 1 al mes para que coincida con el índice de la lista (los meses comienzan desde 1)

    context = {
        'ventas_por_mes': ventas_data,
    }

    return render(request, 'dashboard.html', context)

