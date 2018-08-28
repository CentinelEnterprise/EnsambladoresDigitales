# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

TIPO_EMPRESA =((1,'Sin Definir'),(2,'Natural'),(3,'Juridica'))
# ocpiones para validacion de usuario interno o externo
TIPO_USUARIO_APP =((1,'Sin Asignar'),(2,'Aplicacion'),(3,'Directorio Activo'))

class Empresa(models.Model):
	class Meta:
		permissions = (("view_empresas", "Puede Ver Empresas"),)

	identificacion_empresa = models.CharField(max_length=200,unique=True)
	razon_social_empresa = models.CharField(max_length=200)
	nombre_comercial_empresa = models.CharField(max_length=200, null=True, blank=True)
	tipo_empresa = models.SmallIntegerField(choices=TIPO_EMPRESA,default=1) # Persona Natural o Juridica
	estado_empresa= models.BooleanField(default=True) # Activo o inactivo
	observaciones_empresa = models.CharField(max_length=3000,null=True)
	#fecha_inicio_empresa = models.DateField() // deshabilito el campo por reemplazo de nuevos proporcionados por el cliente.
	# campos solicitados en reunion 17/08/2018
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateField(null=True)
	fecha_desactivacion = models.DateField(null=True)
	activo =  models.BooleanField(default=True, verbose_name='Activo')
  
	def __unicode__(self):
		return '%s' % (self.razon_social_empresa)

class TipoPerfil(models.Model):
	class Meta:
		permissions = (
			("view_tipoperfil", "Can view Tipo perfiles"),
		)
	nombre_tipo_perfil = models.CharField(max_length=200)
	descripcion_tipo_perfil = models.CharField(max_length=200, null=True, blank=True)
	# campos solicitados en reunion 17/08/2018
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateField(null=True)
	fecha_desactivacion = models.DateField(null=True)
	activo =  models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre_tipo_perfil

class Usuario(models.Model):
	usuario = models.OneToOneField(User, verbose_name="Usuario")
	password = models.CharField(max_length=200)
	identificacion = models.PositiveIntegerField()
	nombre = models.CharField(max_length=350)
	# correo = models.CharField(max_length=100)
	email = models.EmailField()
	empresa = models.ForeignKey(Empresa)
	tipo_perfil = models.ForeignKey(TipoPerfil)	
	# campos solicitados en reunion 17/08/2018
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateField(null=True)
	fecha_desactivacion = models.DateField(null=True)	
	#capo para validar si es el primer login de ususario
	primer_login = models.BooleanField(default=True)
	tipo_empresa = models.SmallIntegerField(choices=TIPO_USUARIO_APP,default=1)
	activo =  models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.usuario.username

	class Meta:
		permissions = (
			("view_usuarios", "Can view usuario"),
		)

	def __unicode__(self):
		return self.usuario.username

class Perfil(models.Model):
	class Meta:
		permissions = (
			("view_perfil", "Can view perfiles"),
		)
	nombre_perfil = models.CharField(max_length=200)
	tipo_perfil = models.ForeignKey(TipoPerfil)
	observaciones = models.CharField(max_length=200, null=True, blank=True)
	activo =  models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre_perfil


class PerfilUsuario(models.Model):

	id_usuario = models.ForeignKey(Usuario)
	id_perfil = models.ForeignKey(Perfil)
	fecha_reporte = models.DateTimeField(auto_now_add=True)
	activo =  models.BooleanField(default=True)