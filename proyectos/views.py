# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from proyectos.models import *


""" PARTE PARA LA GESTION DE LOS PROYECTOS ------------------------------------------------------------"""

def administracion_proyectos(request):
	# error = request.GET.get('error', False)
	# ok = request.GET.get('ok', False)	
	# perfiles = TipoPerfil.objects.filter(activo=True)
	# perfiles_inactivos = TipoPerfil.objects.filter(activo=False)
	# if len(perfiles) == 0:
	advertencia = "No hay proyectos registrados"
	return render(request,'proyectos/administrar_proyectos.html',locals())


def agregar_proyectos(request):	
	if request.method == 'POST':
		nombre_p = request.POST['nombre']
		observaciones_p = request.POST['observaciones']						
		nuevo_perfil = TipoPerfil()
		nuevo_perfil.nombre_tipo_perfil = nombre_p
		nuevo_perfil.descripcion_tipo_perfil = observaciones_p
		nuevo_perfil.fecha_modificacion = datetime.now()
		
		print 'algo paso en el guardar'
		nuevo_perfil.save()
		print 'gaurdo el usuario'
		
		ok = 'El perfil ha sido creado.'
		return HttpResponseRedirect('/usuarios/administrar_perfiles/?ok='+ok)		
		
	return render(request,'usuarios/nuevo_perfil.html', locals())

def modificar_proyecto(request,perfil_id):	
	modificar = True
	mod_perfil = TipoPerfil.objects.get(pk=perfil_id)
	if request.method == 'POST':
		nombre_p = request.POST['nombre']
		observaciones_p = request.POST['observaciones']						
		
		mod_perfil.nombre_tipo_perfil = nombre_p
		mod_perfil.descripcion_tipo_perfil = observaciones_p
		mod_perfil.fecha_modificacion = datetime.now()
		
		print 'algo paso en el guardar'
		mod_perfil.save()
		print 'gaurdo el usuario'
		
		ok = 'El perfil ha sido modificado correctamente.'
		return HttpResponse('/usuarios/administrar_perfiles/?ok='+ok)		
		
	return render(request,'usuarios/nuevo_perfil.html', locals())

def eliminar_proyecto(request,perfil_id):
	try:
		perfil = TipoPerfil.objects.get(pk=perfil_id)
		
		if perfil.activo:
			perfil.activo = False
			perfil.fecha_desactivacion = datetime.now()
			perfil.save()			
			ok="Perfil eliminado exitosamente."
			return HttpResponseRedirect('/usuarios/administrar_perfiles/?ok='+ok)
		return HttpResponseRedirect('/usuarios/administrar_perfiles/?ok='+ok)
	except:
		error="Ha ocurrido un error inesperado al intentar eliminar el Perfil"
		return HttpResponseRedirect('/usuarios/administrar_perfiles/?error='+error)


def reactivar_proyecto(request, perfil_id):
	try:
		perfil = TipoPerfil.objects.get(pk=perfil_id)
		if perfil.activo == False:
			perfil.activo = True
			perfil.fecha_modificacion = datetime.now()
			perfil.save()
			ok ="Se ha reactivado el perfil correctamente"
			return HttpResponseRedirect('/usuarios/administrar_perfiles/?ok='+ok)
		return HttpResponseRedirect('/usuarios/administrar_perfiles/?ok='+ok)	
	except:
		error="se ha generado un error al reactivar el perfil"
		return HttpResponseRedirect('/usuarios/administrar_perfiles/?error='+error)

def ver_modal_proyectos(request,perfil_id):
	print "vino al metodo"
	accion = request.GET['accion_r']
	eliminar_m = False
	reactivar_m = False
	editar_m = False
	detalles_m = False
	perfil_s = TipoPerfil.objects.get(pk=perfil_id)
	if accion == "editar":
	 	editar_m=True	 	
	elif accion == "detalles":
		detalles_m = True
	elif accion == "eliminar":
		eliminar_m = True
		advertencia = "Esta a punto de eliminar el perfil"
	elif accion == "reactivar":
		reactivar_m = True
		advertencia = "Esta a punto de reactivarvar el perfil"

	return render(request,'usuarios/modal_perfiles.html',locals())
 
