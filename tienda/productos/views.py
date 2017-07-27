# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Producto, Categoria, Venta
from .forms import ProductoForm, CategoriaForm, VentaForm

from django.db.models import Sum, Count
import pprint
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
import os
from reportlab.pdfgen import canvas
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from io import BytesIO
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from django.db.models import Q
#pastel
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
import time


def ProductoList(request):
    latest_alcohol_list = Producto.objects.order_by('id')[:9]
    context = {
        'latest_alcohol_list':latest_alcohol_list
    }
    print (latest_alcohol_list)
    return render(request, 'productos/producto_list.html', context)

def ProductoDetail(request,pk):
    producto = get_object_or_404(Producto, pk=pk)
    template = loader.get_template('productos/producto_detail.html')
    forma = VentaForm(request.POST, request.FILES)
    if forma.is_valid():
        cantidad_vendida = forma.cleaned_data['cantidad_vendida']
        venta = Venta()
        producto.unidades = producto.unidades - cantidad_vendida
        venta.producto = producto
        venta.cantidad_vendida = cantidad_vendida
        producto.save()
        venta.save()
    context = {
    'forma': forma,
    'producto': producto
    }
    if request.user.is_authenticated():
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(reverse('productos/producto_detail.html', args=(producto.id,)))

class ProductoCreation(CreateView):
    model = Producto
    success_url = reverse_lazy('productos:producto_list')
    fields = ['codigo_p', 'nombre', 'descripcion', 'categoria', 'unidades', 'precio']
class ProductoUpdate(UpdateView):
    model = Producto
    success_url = reverse_lazy('productos:producto_list')
    fields = ['codigo_p', 'nombre', 'descripcion', 'categoria', 'unidades', 'precio']
class ProductoDelete(DeleteView):
    model = Producto
    success_url = reverse_lazy('productos:producto_list')
    fields = ['codigo_p', 'nombre', 'descripcion', 'categoria', 'unidades', 'precio']

def principal(request):
    playera = Producto.objects.order_by('id')
    template = loader.get_template('home.html')
    context = {
        'playera': playera
    }
    return HttpResponse(template.render(context, request))

def inicio(request):
    playera = Producto.objects.order_by('id')
    template = loader.get_template('inicio.html')
    context = {
        'playera': playera
    }
    return HttpResponse(template.render(context, request))

def producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            playera = form.save()
            playera.save()
            return HttpResponseRedirect('/productos/Lista/Productos/')
    else:
        form = ProductoForm()
    template = loader.get_template('productos/new_producto.html')
    context = {
        'form': form
    }
    if request.user.is_authenticated():
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('productos:producto_list')

def categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            playera = form.save()
            playera.save()
            return HttpResponseRedirect('/productos/Lista/Productos/')
    else:
        form = CategoriaForm()
    template = loader.get_template('productos/new_categoria.html')
    context = {
        'form': form
    }
    if request.user.is_authenticated():
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('productos:productos_list')


def venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST, request.FILES)
        if form.is_valid():
            playera = form.save()
            playera.save()
            return HttpResponseRedirect('/productos/Lista/Productos/')
    else:
        form = VentaForm()
    template = loader.get_template('productos/new_venta.html')
    context = {
        'form': form
    }
    if request.user.is_authenticated():
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('producto:detail')

def listaventas(request):
    playera = Venta.objects.order_by('id')
    template = loader.get_template('productos/venta_list.html')
    context = {
        'playera': playera
    }
    return HttpResponse(template.render(context, request))

# def grafica(request):
#     print "Genero el PDF[grafica]"
#     response = HttpResponse(content_type='application/pdf')
#     pdf_name = "Grafica.pdf"  # llamado clientes
#     # la linea 26 es por si deseas descargar el pdf a tu computadora
#     response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
#     buff = BytesIO()
#     doc = SimpleDocTemplate(buff,
#                             pagesize=letter,
#                             rightMargin=40,
#                             leftMargin=40,
#                             topMargin=60,
#                             bottomMargin=18,
#                             )
#     courses = []
#     styles = getSampleStyleSheet()
#     header = Paragraph("Total de Cursos", styles['Heading2'])
#     courses.append(header)
#     styles = getSampleStyleSheet()
#     d = Drawing(600, 300)
#     conteo = Course.objects.count()
#     # for i in Course.objects.all():
#     # print conteo
#     data = [(conteo,)]
#     bc = VerticalBarChart()
#     bc.x = 50
#     bc.y = 50
#     bc.height = 200
#     bc.width = 300
#     bc.data = data
#     bc.strokeColor = colors.blue
#     bc.valueAxis.valueMin = 0
#     bc.valueAxis.valueMax = 10
#     bc.valueAxis.valueStep = 1  #paso de distancia entre punto y punto
#     bc.categoryAxis.labels.boxAnchor = 'ne'
#     bc.categoryAxis.labels.dx = 8
#     bc.categoryAxis.labels.dy = -2
#     bc.categoryAxis.labels.angle = 30
#     bc.categoryAxis.categoryNames = ['Cursos']
#     bc.groupSpacing = 10
#     bc.barSpacing = 2
#     d.add(bc)
#     pprint.pprint(bc.getProperties())
#     courses.append(d)
#     doc.build(courses)
#     response.write(buff.getvalue())
#     buff.close()
#     return response
#
# def pdf(request):
#     print "Genero el PDF"
#     response = HttpResponse(content_type='application/pdf')
#     pdf_name = "Lista de Cursos.pdf"  # llamado clientes
#     # la linea 26 es por si deseas descargar el pdf a tu computadora
#     response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
#     buff = BytesIO()
#     doc = SimpleDocTemplate(buff,
#                             pagesize=letter,
#                             rightMargin=40,
#                             leftMargin=40,
#                             topMargin=60,
#                             bottomMargin=18,
#                             )
#     courses = []
#     styles = getSampleStyleSheet()
#     header = Paragraph("Lista de Cursos", styles['Heading2'])
#     courses.append(header)
#     headings = ('Nombre', 'Fecha de Inicio', 'Fecha de fin', 'Imagen')
#     allcourses = [(p.Nombre, p.Fecha_inicio, p.Fecha_fin,  p.Imagen) for p in Course.objects.all()]
#     print allcourses
#     t = Table([headings] + allcourses)
#     t.setStyle(TableStyle(
#         [
#             ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
#             ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
#         ]
#     ))
#
#     courses.append(t)
#     doc.build(courses)
#     response.write(buff.getvalue())
#     buff.close()
#     return response

def pdfgen(request):
    print "Genero el PDF Ventas en General"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte_de_Ventas_General.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    courses = []
    styles = getSampleStyleSheet()
    header = Paragraph("Reporte General de Ventas.", styles['Heading2'])
    courses.append(header)
    headings = ('Id', 'Producto', 'Cantidad Vendida', 'Fecha')
    allcourses = [(p.id, p.producto, p.cantidad_vendida, p.fecha) for p in Venta.objects.all()]
    # print allcourses
    t = Table([headings] + allcourses)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.green),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.green),
            ('BACKGROUND', (0, 0), (-1, 0), colors.green)
        ]
    ))

    courses.append(t)
    doc.build(courses)
    response.write(buff.getvalue())
    buff.close()
    return response


def pdfdia(request):
    # print "Genero el PDF Ventas del Dia"
    date = request.GET.get('date','2017-05-04')
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte del Dia"+date+".pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    courses = []
    styles = getSampleStyleSheet()
    header = Paragraph("Reporte de Ventas de "+date, styles['Heading2'])
    courses.append(header)
    headings = ('Id', 'Producto', 'Cantidad Vendida','Subtotal')
    allcourses = [(p.id, p.producto, p.cantidad_vendida,(p.producto.precio*p.cantidad_vendida)) for p in Venta.objects.filter(fecha = date)]
    totalfinal = 0
    saldos = 0
    for p in Venta.objects.filter(fecha = date):
        saldos = saldos + p.cantidad_vendida
        totalfinal = totalfinal + (p.producto.precio*p.cantidad_vendida)
        # print (saldos)
    total = ('','Total', saldos, totalfinal)
    # print allcourses

    allcourses.append(total)
    t = Table([headings] + allcourses)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.green),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.green),
            ('BACKGROUND', (0, 0), (-1, 0), colors.green)
        ]
    ))

    courses.append(t)
    doc.build(courses)
    response.write(buff.getvalue())
    buff.close()
    return response


def grafica_pastel(request):


    response = HttpResponse(content_type='application/pdf')
    pdf_name = "ventas.pdf"

    buff = BytesIO()

    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=200,
                            bottomMargin=18,
                            )
    story = []
    estilo = getSampleStyleSheet()


    d = Drawing(300, 200)
    pc = Pie()
    pc.x = 65
    pc.y = 15
    pc.width = 170
    pc.height = 170
    # pc.data = [11,20,30,40,50]
    # pc.labels = ['IE','Kopete','Chrome','Firefox','Opera']
    datos = []
    etiquetas = []

    for key in Venta.objects.values('producto').annotate(suma=Sum('cantidad_vendida')):
        producto = get_object_or_404(Producto, pk=key['producto'])
        etiquetas.append(producto.nombre)
        datos.append(key['suma'])
    pc.data = datos
    pc.labels = etiquetas

    pc.slices.strokeWidth=0.5
    pc.slices[3].popout = 10
    pc.slices[3].strokeWidth = 2
    pc.slices[3].strokeDashArray = [2,2]
    pc.slices[3].labelRadius = 1.75
    pc.slices[3].fontColor = colors.red
    pc.sideLabels = 1  # Con 0 no se muestran líneas hacia las etiquetas
    #~ pc.slices.labelRadius = 0.65  # Para mostrar el texto dentro de las tajadas

    #Insertamos la legenda

    legend = Legend()
    legend.x               = 370
    legend.y               = 0
    legend.dx              = 8
    legend.dy              = 8
    legend.fontName        = 'Helvetica'
    legend.fontSize        = 7
    legend.boxAnchor       = 'n'
    legend.columnMaximum   = 10
    legend.strokeWidth     = 1
    legend.strokeColor     = colors.black
    legend.deltax          = 75
    legend.deltay          = 10
    legend.autoXPadding    = 5
    legend.yGap            = 0
    legend.dxTextSpace     = 5
    legend.alignment       = 'right'
    legend.dividerLines    = 1|2|4
    legend.dividerOffsY    = 4.5
    legend.subCols.rpad    = 30

    #Insertemos nuestros propios colores
    colores  = [colors.blue, colors.red, colors.green, colors.yellow, colors.pink]
    for i, color in enumerate(colores):
        pc.slices[i].fillColor = color

    legend.colorNamePairs  = [(
                                pc.slices[i].fillColor,
                                (pc.labels[i][0:20], '%0.2f' % pc.data[i])
                               ) for i in xrange(len(pc.data))]

    d.add(pc)
    d.add(legend)
    story.append(d)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response
