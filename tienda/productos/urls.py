from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    ProductoList,
    # ProductoDetail,
    ProductoCreation,
    ProductoUpdate,
    ProductoDelete
)
urlpatterns = [
    url(r'^$',views.principal, name='principal'),
    url(r'^inicio/',views.inicio, name='inicio'),
    url(r'^Lista/Productos/',views.ProductoList, name='producto_list'),
    # url(r'^Lista/Productos/', login_required(ProductoList.as_view()), name='list'),
    # url(r'^(?P<pk>\d+)', views.ProductoDetail, name='detail'),
    url(r'^Producto/(?P<pk>[0-9]+)/$',views.ProductoDetail,name='producto_detail'),
    url(r'^Producto/Nuevo',views.producto,name="producto"),
    url(r'^Categoria/Nueva',views.categoria,name="categoria"),
    url(r'^Venta/Nueva',views.venta,name="venta"),
    url(r'^Lista/Ventas/',views.listaventas,name="listaventas"),
    # url(r'^Pdf',views.pdf,name="pdf"),
    # url(r'^Grafica',views.grafica,name="grafica"),
    url(r'^Editar/(?P<pk>\d+)', login_required(ProductoUpdate.as_view()), name='edit'),
    url(r'^Borrar/(?P<pk>\d+)', login_required(ProductoDelete.as_view()), name='delete'),
    url(r'^Pdf/Dia',views.pdfdia,name="pdfdia"),
    url(r'^Pdf/General',views.pdfgen,name="pdfgen"),
    url(r'^Pdf/Grafica',views.grafica_pastel,name="pastel"),
    # url(r'^Venta/',views.venta,name="venta"),
    # url(r'^seller/$', views.seller_list, name='seller_list'),
    # url(r'^seller/(?P<id>[0-9]+)/$', views.seller_detail, name='seller_detail'),
]
