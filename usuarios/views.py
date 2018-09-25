# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# -*- encoding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from usuarios.models import *
#librerias necesarias para correos desde django
from email.mime.text import MIMEText
from smtplib import SMTP
from datetime import datetime, date
from django.core.urlresolvers import reverse


""" Autenticacion de programa """
def acceder(request):
	to = request.GET.get('next', '/')
	print 'entro almetrodo',to
	if request.method == 'POST':
		nombre_de_usuario = request.POST['nombre_de_usuario']
		ckeck_list = int(request.POST.get('checkdir_activo', False))
		print 'este es el valor que trae del check del login ',ckeck_list
		clave = request.POST['clave']
		# ckeck_list = request.POST['checkdir_activo']		
		print nombre_de_usuario,'mire el nombre que trae'
		print clave, 'mire la clave que trae'		
		#parte de la autenticacion 
		if ckeck_list != 1 : 
			usuario = authenticate(username=nombre_de_usuario, password=clave)
			print usuario,'resultado del autecticar'
			if usuario is not None and usuario.is_active:
				login(request, usuario)
				# return HttpResponseRedirect(to)
				""" parte que voy a utilizar para validar el primer login"""
				if not usuario.is_superuser and not validad_primero_login(usuario.pk):
					primer_login = True
					return HttpResponseRedirect('/usuarios/configuracion')
				else:	
					return HttpResponseRedirect(to)
			else:
				error = 'El usuario o contraseña es/son incorrectos, vuelva a intentar'
				print 'error'
		else:
			usuario = authenticate(username=nombre_de_usuario)
			print usuario,'resultado del autecticar por correo activo '
			if usuario is not None and usuario.is_active:
				login(request, usuario)				
			else:
				error = 'El usuario no esta en el directorio activo, vuelva a intentar'
				print 'error'
	elif request.user.is_authenticated():
		return HttpResponseRedirect(to)
	# return render(request,'usuarios/login.html', locals())
	return render(request,'dashboard/login.html', locals())

@login_required
def cerrar_sesion(request):
	logout(request)
	return HttpResponseRedirect('/usuarios/acceder')

def validad_primero_login(usuario_id):
	logion_n = True
	print usuario_id,'este es el valor que ingreso al metodo'
	usuario_s = Usuario.objects.get(usuario__id=usuario_id)
	if usuario_s.primer_login:
		logion_n = False

	return logion_n

""" Fin Autenticacion """

""" ADMINISTRACION PARA LA GESTION  DE LAS OPCIONES DEL NAVBAR """
@login_required
def ver_perfil_usuario(request):
	usuario_log = request.user
	is_admin = False
	if str(usuario_log.username) == "admin":
		is_admin = True 
	else:
		usuario = Usuario.objects.get(usuario__pk=usuario_log.pk)
	return render(request,'usuarios/ver_perfil_usuario.html', locals())

@login_required
def configuracion(request):
	
	if request.method == 'POST':
		print 'esta entrando'
		try:
			clave = request.POST['clave_actual']
			nueva_clave = request.POST['nue_contrasena']
			c_nueva_clave = request.POST['c_nueva_clave']
			usuario = request.user
			print 'tare los siguiente: ',clave,nueva_clave,c_nueva_clave
			if usuario.check_password(clave):
				print 'valido por el checkpass'
				if len(nueva_clave) < 6 or ' ' in nueva_clave:
					error = 'Use por lo menos 6 caracteres, sin espacios en blanco en la contraseña'
					print error
				else:
					if nueva_clave == c_nueva_clave:
						usuario.set_password(nueva_clave)						
						usuario.save()
						usuario_sistemas = Usuario.objects.get(usuario__id=usuario.pk)
						usuario_sistemas.primer_login = False
						usuario_sistemas.save()
						ok = 'la Contraseña actualizada correctamente.'
						# return HttpResponseRedirect('/usuarios/ver_perfil_usuario/?ok='+ok)
						print ok
						return render(request,'dashboard/cambio_contrasena.html', locals())	 
					else:
						error = 'Las contraseñas no coinciden verifique nuevamente'
						# return HttpResponseRedirect('/usuarios/ver_perfil_usuario/?error='+error)
						print error
						return render(request,'dashboard/cambio_contrasena.html', locals())	
			else:
				error = 'La contraseña que ingreso no es correcta, Vuelva  a ingresarla'
				print error
				return render(request,'dashboard/cambio_contrasena.html', locals())	

			return render(request,'dashboard/cambio_contrasena.html', locals({'ok':'La contraseña se modifico correctamente ver perfil'}))		
		except Exception:
			error = 'Ha ocurrido un error inesperado.'
			print error
	return render(request,'dashboard/cambio_contrasena.html', locals())


""" Metodo para generar la recuperacion de la contraseña """

def recuperar_contrasena(request):	
	
	if request.method == 'POST':
		try:
			print 'esta ingresando'
			if request.POST['usu_recuperacion_usr']:
				dato_recuperacion_usr = request.POST['usu_recuperacion_usr']
				print dato_recuperacion_usr
				user_valida = User.objects.get(username=dato_recuperacion_usr)
				print 'ingreso por la opcion 1'
				# if enviar_correo_contrasena(user_valida):
					
				ok="El correo se envio correctamente"	
				HttpResponseRedirect('/usuarios/acceder/?ok='+ok)			
			
			elif request.POST['usu_recuperacion_id']:
				print 'entro por la parte dos',request.POST['usu_recuperacion_id']
				dato_recuperacion_id = request.POST['usu_recuperacion_id']
				print dato_recuperacion_id
				usario_valida_mail=Usuario.objects.get(identificacion=dato_recuperacion_id)
				print 'ingreso por la opcion 2'
				if enviar_correo_contrasena(usario_valida_mail):
					ok="El correo se envio correctamente"
					HttpResponseRedirect('/usuarios/acceder/?ok='+ok)
			else:
				error = "Se ha generado un error con el usuario o la cedula ingresada por favor verificar"
		except Exception:
			error = 'Ha ocurrido un error inesperado.'
			print error
			HttpResponseRedirect('/usuarios/acceder/?error='+error)
	
	return render(request,'dashboard/recuperar_contrasena.html',locals())

# parte del correo electronico de recuperacion
def enviar_correo_contrasena(usuario_id):
	try:
		import os
		from django.core.mail import EmailMultiAlternatives
		print 'llego a la primera parte del corre'		
		link='http://127.0.0.1:8000/usuarios/administrar_usuarios/'		
		correo_destino = 'camancera@indracompany.com'
		observaciones = 'si envio las observaciones'
		# cargo_a = cargo_aprobacion
		subject = 'Prueba de correo recuperacion contraseña' 
		origen = 'testenelirene@gmail.com'		
		html_content = '<a href='+link+'>Ingrese aqui para validar la contraseña<br>'
		print 'llego a la segunda parte del corre'	
		msg = EmailMultiAlternatives(subject,observaciones, origen, [correo_destino])
		msg.attach_alternative(html_content, "text/html")
		print 'llego a la tercera parte del corre'		
		# msg.send()
		print 'envio el correo compadre'	
		valido = True
	except Exception:
		valido = False	
""" Fin Usuario """

""" Administracion de Usuarios ------------------------------------------------------------ """

@login_required
# def administracion_usuarios(request):
# 	if request.method == 'POST':
# 		print 'hizo el post por lo menos'
# 		try:
# 			usuarios_seleccionados = request.POST.getlist('filas_seleccionadas')
# 			for pk in usuarios_seleccionados:
# 				usuario = Usuario.objects.get(pk=pk)
# 				user = User.objects.get(pk=usuario.usuario.pk)
# 				usuario.activo = False
# 				usuario.save()
# 				user.is_active= False
# 				user.save()
# 			ok = 'Los usuarios han sido eliminados correctamente.'
# 			return HttpResponseRedirect('/usuarios/administrar_usuarios/')
# 		except Exception:
# 			error = 'Ha ocurrido un error inesperado al intentar eliminar el/los usuarios.'
# 			return render(request,'usuarios/administrar_usuarios.html', locals())	
# 	usuarios = Usuario.objects.all()
# 	if len(usuarios) == 0:
# 		advertencia = "No hay usuarios registrados"
# 	return render(request,'usuarios/administrar_usuarios.html', locals())						
			
			

def administracion_usuarios(request):
	error = request.GET.get('error', False)
	ok = request.GET.get('ok', False)
	usuarios = Usuario.objects.filter(activo=True)
	usuarios_inactivos = Usuario.objects.filter(activo=False)
	if len(usuarios) == 0:
		advertencia = "No hay Usuarios registrados"
	return render(request,'usuarios/administrar_usuarios.html', locals())


def agregar_usuarios(request):
	perfiles = TipoPerfil.objects.filter(activo=True)
	empresas = Empresa.objects.filter(activo=True)
	print perfiles,'esta entrando'
	if not perfiles:
		advertencia = 'No se encuentran perfiles registrados. No podra agregar un usuario nuevo mientras no exitan perfiles.'
	
	if request.method == 'POST':
		login_usuario = request.POST['nombre_de_usuario']
		clave = request.POST['clave']
		c_clave = request.POST['c_clave']
		numero_documento = request.POST['numero_documento']
		nombre_de_usuario = request.POST['primer_nombre']
		correo_n =  request.POST['correo']
		empresa_n  = int(request.POST['empresa_usuario'])
		tipo_perfil  = int(request.POST['sel_tipo_perfil'])
		tipo_usuario  = int(request.POST['sel_tipo_usuario'])
		# grupos_seleccionados = request.POST.getlist('grupos_seleccionados')
		if clave == c_clave:
			usuario_sys = User()
			usuario_sys.username=login_usuario
			usuario_sys.set_password(clave)
			usuario_sys.email=correo_n
			usuario_sys.first_name=nombre_de_usuario
			usuario_sys.last_name="n.a"
			usuario_sys.save()

			nuevo_usuario = Usuario()
			usuario_sistemas = User.objects.get(username=login_usuario)
			nuevo_usuario.usuario = usuario_sistemas
			nuevo_usuario.password = usuario_sistemas.password
			nuevo_usuario.identificacion = numero_documento
			nuevo_usuario.nombre = nombre_de_usuario
			nuevo_usuario.email = correo_n
			nuevo_usuario.empresa = Empresa.objects.get(id=empresa_n)
			nuevo_usuario.tipo_perfil = TipoPerfil.objects.get(id=tipo_perfil)
			nuevo_usuario.fecha_modificacion = datetime.now()
			nuevo_usuario.tipo_empresa = tipo_usuario
			nuevo_usuario.save()
			ok = 'El usuario ha sido creado.'
			return HttpResponseRedirect('/usuarios/administrar_usuarios/?ok='+ok)		
		
	return render(request,'usuarios/nuevo_usuario.html', locals())


def modificar_usuario(request, usuario_id):
	modificar =True
	try:
		usuario_mod = Usuario.objects.get(pk=usuario_id)
		perfiles_usuario = TipoPerfil.objects.filter(pk=usuario_mod.tipo_perfil.pk)
	except Exception:
		return HttpResponse('/usuarios/administrar_usuarios/')	
	if request.method == 'POST':
		try:
			# login_usuario = request.POST['nombre_de_usuario']
			# clave = request.POST['clave']
			# c_clave = request.POST['c_clave']
			numero_documento = request.POST['numero_documento']
			nombre_de_usuario = request.POST['primer_nombre']
			correo_n =  request.POST['correo']
			empresa_n  = int(request.POST['empresa_usuario'])
			tipo_perfil  = int(request.POST['sel_tipo_perfil'])
			try:
				usuario_sys = User.objects.get(username=usuario_mod.usuario)
				# usuario_sys.username=login_usuario
				# usuario_sys.set_password(clave)
				usuario_sys.email=correo_n
				usuario_sys.first_name=nombre_de_usuario
				usuario_sys.last_name="n.a"
				usuario_sys.save()

				usuario_mod.usuario = User.objects.get(username=usuario_mod.usuario)
				# usuario_mod.password = clave
				usuario_mod.identificacion = numero_documento
				# usuario_mod.nombre = nombre_de_usuario
				usuario_mod.email = correo_n
				usuario_mod.empresa = Empresa.objects.get(id=empresa_n)
				usuario_mod.tipo_perfil = TipoPerfil.objects.get(id=tipo_perfil)
				usuario_mod.fecha_modificacion = datetime.now()
				usuario_mod.save()
			
				ok = 'Datos actualizados exitosamente'
				return HttpResponse('/usuarios/administrar_usuarios/?ok='+ok)
				print 'fue ok'	
			except Exception:
				error = 'Ha ocurrido un error con el usuario.'
				print 'fue por el error'
		except Exception:
			error = 'Ha ocurrido un error inesperado.'
			print 'fue por ultimo'
	return render(request,'usuarios/nuevo_usuario.html', locals())



def eliminar_usuario(request, usuario_id):
	try:
		usuario = Usuario.objects.get(pk=usuario_id)
		user = User.objects.get(pk=usuario.usuario.pk)
		if usuario.activo:
			usuario.activo = False
			usuario.fecha_desactivacion = datetime.now()
			usuario.save()
			user.is_active= False
			user.save()
			ok ="Se ha eliminado el usuario correctamente"
			# return render(request,'usuarios/administrar_usuarios.html', locals())
			# url = reverse('administrar_usuarios', kwargs={'ok': ok})
			# return HttpResponseRedirect(url)
			return HttpResponseRedirect('/usuarios/administrar_usuarios/?ok='+ok)	
		return HttpResponseRedirect('/usuarios/administrar_usuarios/?ok='+ok)
		# return HttpResponseRedirect(url)
		# return render(request,'usuarios/administrar_usuarios.html', locals())	
	except:
		error="se ha generado un error al eliminar el usuario"
		return HttpResponseRedirect('/usuarios/administrar_usuarios/?error='+error)

def reactivar_usuario(request, usuario_id):
	try:
		usuario = Usuario.objects.get(pk=usuario_id)
		user = User.objects.get(pk=usuario.usuario.pk)
		if usuario.activo == False:
			usuario.activo = True
			usuario.fecha_modificacion = datetime.now()
			usuario.save()
			user.is_active= True
			user.save()
			ok ="Se ha reactivado el usuario correctamente"
			return HttpResponseRedirect('/usuarios/administrar_usuarios/?ok='+ok)
		return HttpResponseRedirect('/usuarios/administrar_usuarios/?ok='+ok)	
	except:
		error="se ha generado un error al reactivar el usuario"
		return HttpResponseRedirect('/usuarios/administrar_usuarios/?error='+error)

def ver_modal_usuarios(request,usuario_id):
	print "vino al metodo"
	accion = request.GET['accion_r']
	reactivar_m = False
	eliminar_m = False
	modificar = False
	detalles_m = False
	usuario_mod = Usuario.objects.get(pk=usuario_id)
	if accion == "editar":
	 	modificar=True	
	 	perfiles = TipoPerfil.objects.all()
		empresas = Empresa.objects.all() 	
	elif accion == "detalles":
		detalles_m = True
	elif accion == "eliminar":
		eliminar_m = True
		advertencia = "Esta a punto de eliminar el usuario"
	elif accion == "reactivar":
		reactivar_m = True
		advertencia = "Esta a punto de reactivarvar el usuario"

	return render(request,'usuarios/modal_usuarios.html',locals())

""" PARTE PARA LA GESTION DE LOS PERFILES ------------------------------------------------------------"""

def administrar_perfiles(request):
	error = request.GET.get('error', False)
	ok = request.GET.get('ok', False)	
	perfiles = TipoPerfil.objects.filter(activo=True)
	perfiles_inactivos = TipoPerfil.objects.filter(activo=False)
	if len(perfiles) == 0:
		advertencia = "No hay perfiles registrados"
	return render(request,'usuarios/administrar_perfiles.html',locals())


def agregar_perfiles(request):	
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

def modificar_perfiles(request,perfil_id):	
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

def eliminar_perfil(request,perfil_id):
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


def reactivar_perfil(request, perfil_id):
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

def ver_modal_perfiles(request,perfil_id):
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
""" PARTE PARA LA GESTION DE LAS EMPRESAS """


def administracion_empresas(request):
	error = request.GET.get('error', False)
	ok = request.GET.get('ok', False)
	empresas = Empresa.objects.filter(activo=True)
	empresas_inactivos = Empresa.objects.filter(activo=False)
	if len(empresas) == 0:
		advertencia = "No hay empresas registradas"
	return render(request,'usuarios/administrar_empresas.html',locals())


def agregar_empresa(request):	
	if request.method == 'POST':
		nit_n = request.POST['identificacion']
		razon_social = request.POST['razon']
		nombre_c = request.POST['comercial']
		tipo_e = request.POST['tipo']
		observaciones_p = request.POST['TextareaObservacion']						
		
		nueva_empresa = Empresa()
		nueva_empresa.identificacion_empresa = nit_n
		nueva_empresa.razon_social_empresa = razon_social
		nueva_empresa.nombre_comercial_empresa = nombre_c
		nueva_empresa.tipo_empresa = tipo_e
		nueva_empresa.observaciones_empresa = observaciones_p
		# nueva_empresa.fecha_inicio_empresa = "2018-08-10"
		nueva_empresa.fecha_modificacion = datetime.now()
		
		print 'algo paso en el guardar'
		nueva_empresa.save()
		print 'gaurdo el usuario'
		
		ok = 'El usuario ha sido creado.'
		return HttpResponseRedirect('/usuarios/administrar_empresas/?ok='+ok)		
		
	return render(request,'usuarios/nueva_empresa.html', locals())

def modificar_empresa(request,empresa_id):	
	modificar = True
	mod_empresa = Empresa.objects.get(pk=empresa_id)
	if request.method == 'POST':
		
		nit_n = request.POST['identificacion']
		razon_social = request.POST['razon']
		nombre_c = request.POST['comercial']
		tipo_e = int(request.POST['tipo'])
		observaciones_p = request.POST['TextareaObservacion']						
		
		mod_empresa.identificacion_empresa = nit_n
		mod_empresa.razon_social_empresa = razon_social
		mod_empresa.nombre_comercial_empresa = nombre_c
		mod_empresa.tipo_empresa = tipo_e
		mod_empresa.observaciones_empresa = observaciones_p
		mod_empresa.fecha_modificacion = datetime.now()
		
		
		print 'algo paso en el guardar'
		mod_empresa.save()
		print 'gaurdo el usuario'
		
		ok = 'El usuario ha sido creado.'
		return HttpResponse('/usuarios/administrar_empresas/?ok='+ok)		
		
	return render(request,'usuarios/nueva_empresa.html', locals())

def eliminar_empresa(request,empresa_id):
	try:
		empresa = Empresa.objects.get(pk=empresa_id)
		
		if empresa.activo:
			empresa.activo = False
			empresa.fecha_modificacion = datetime.now()
			empresa.save()			
			ok="Se Elimino correctamente la empresa"
			return HttpResponseRedirect('/usuarios/administrar_empresas/?ok='+ok)
		return HttpResponseRedirect('/usuarios/administrar_empresas/?ok='+ok)
	except:
		error="se ha generado un error al eliminar la empresa"
		return HttpResponseRedirect('/usuarios/administrar_empresas/?error='+error)

def reactivar_empresa(request, empresa_id):
	try:
		empresa = Empresa.objects.get(pk=empresa_id)
		if empresa.activo == False:
			empresa.activo = True
			empresa.fecha_modificacion = datetime.now()
			empresa.save()
			ok ="Se ha reactivado la empresa correctamente"
			return HttpResponseRedirect('/usuarios/administrar_empresas/?ok='+ok)
		return HttpResponseRedirect('/usuarios/administrar_empresas/?ok='+ok)	
	except:
		error="se ha generado un error al reactivar la empresa"
		return HttpResponseRedirect('/usuarios/administrar_empresas/?error='+error)

def ver_modal_empresas(request,empresa_id):
	accion = request.GET['accion_r']
	modificar = False
	eliminar_m = False
	reactivar_m = False
	detalles_m = False
	mod_empresa = Empresa.objects.get(pk=empresa_id)
	if accion == "editar":
	 	modificar=True	 	
	elif accion == "detalles":
		detalles_m = True
	elif accion == "eliminar":
		eliminar_m = True
		advertencia = "Esta a punto de eliminar la empresa"
	elif accion == "reactivar":
		reactivar_m = True
		advertencia = "Esta a punto de reactivarvar la empresa"

	return render(request,'usuarios/modal_empresas.html',locals())

# parte para el envio de correo 


""" Administracion Grupos/Permisos """
@login_required
@permission_required('auth.add_group')
def administracion_grupos(request):
	error = request.GET.get('error', False)
	ok = request.GET.get('ok', False)
	grupos = Group.objects.all()
	if len(grupos) == 0:
		advertencia = "No hay datos registrados"	
	return render(request,'usuarios/administrar_grupos.html', locals())

@login_required
@permission_required('auth.add_group')
def agregar_grupo(request):
	permisos = Permission.objects.all()
	if request.method == 'POST':
		try:
			nombre_grupo = request.POST['nombre_grupo']
			permisos_seleccionados = request.POST.getlist('permisos_seleccionados')
			grupo = Group.objects.create(name=nombre_grupo)
			try:
				for pk in permisos_seleccionados:
					permiso = Permission.objects.get(pk=pk)
					grupo.permissions.add(permiso)
					ok= 'Se ha creado el grupo correctamente'
				return HttpResponseRedirect('/usuarios/grupos/?ok='+ok)
			except Exception:
				if grupo is not None:
					grupo.delete()
		except:
			error = 'Ha ocurrido un error inesperado.'
	return render(request,'usuarios/agregar_permisos_grupos.html', locals())


@login_required
@permission_required('auth.add_group')
def ver_grupo(request, grupo_id):
	permisos = Permission.objects.all()
	try:
		grupo = Group.objects.get(pk=grupo_id)
		grupo_permisos = grupo.permissions
	except Exception:
		return HttpResponseRedirect('/usuarios/grupos?error=No se pudo encontrar el grupo.')
	return render_to_response('ver_grupo_usuarios.html', locals(), context_instance=RequestContext(request))

@login_required
@permission_required('auth.change_group')
def modificar_grupo(request, grupo_id):
	permisos = Permission.objects.all()
	try:
		grupo = Group.objects.get(pk=grupo_id)
		grupo_permisos = grupo.permissions
	except Exception:
		return HttpResponseRedirect('/usuarios/grupos?error=No se pudo encontrar el grupo.')
	if request.method == 'POST':
		try:
			nombre_grupo = request.POST['nombre_grupo']
			permisos_seleccionados = request.POST.getlist('permisos_seleccionados')
			grupo.name = nombre_grupo
			grupo.permissions.clear()
			for pk in permisos_seleccionados:
				permiso = Permission.objects.get(pk=pk)
				grupo.permissions.add(permiso)
			grupo.save()
			return HttpResponseRedirect('/usuarios/grupos?ok=Datos actualizados exitosamente.')
		except:
			error = "Ha ocurrido un error inesperado al intentar modificar el grupo."
	return render_to_response('modificar_grupo_usuarios.html', locals(), context_instance=RequestContext(request))

@login_required
@permission_required('auth.delete_group')
def eliminar_grupo(request, grupo_id):
	try:
		grupo = Group.objects.get(pk=grupo_id)
		grupo.delete()
		return HttpResponseRedirect('/usuarios/grupos?ok=Grupo eliminado exitosamente.')
	except:
		return HttpResponseRedirect('/usuarios/grupos?ok=Ha ocurrido un error inesperado al intentar eliminar el Grupo.')


def ver_modal_grupos(request,empresa_id):
	accion = request.GET['accion_r']
	modificar = False
	eliminar_m = False
	reactivar_m = False
	detalles_m = False
	mod_empresa = Empresa.objects.get(pk=empresa_id)
	if accion == "editar":
	 	modificar=True	 	
	elif accion == "detalles":
		detalles_m = True
	elif accion == "eliminar":
		eliminar_m = True
		advertencia = "Esta a punto de eliminar la empresa"
	elif accion == "reactivar":
		reactivar_m = True
		advertencia = "Esta a punto de reactivarvar la empresa"

	return render(request,'usuarios/modal_empresas.html',locals())
""" Fin Administracion Grupos/Permisos """