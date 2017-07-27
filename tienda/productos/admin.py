# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Producto

# Register your models here.
@admin.register(Producto)
class AdminProducto(admin.ModelAdmin):
	list_display = ('codigo_p', 'nombre', 'descripcion', 'categoria', 'unidades', 'precio')
	list_filter = ('categoria',)
