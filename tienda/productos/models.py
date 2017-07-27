# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Venta(models.Model):
	fecha = models.DateField(auto_now_add=True)
	producto = models.ForeignKey('Producto', null=True, blank=True, on_delete=models.CASCADE)
	cantidad_vendida = models.IntegerField()

	def __str__(self):
		return self.producto

class Categoria(models.Model):
	categoria = models.CharField(max_length=255)

	def __str__(self):
		return self.categoria


class Producto(models.Model):
	codigo_p = models.IntegerField(null=False, blank=False, unique=True)
	nombre = models.CharField(max_length=255, null=False, blank=False)
	descripcion = models.CharField(max_length=255)
	categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
	unidades = models.IntegerField(null=False, blank=False)
	precio = models.DecimalField(max_digits=9,decimal_places=2, null=False, blank=False)

	def __str__(self):
		return self.nombre
