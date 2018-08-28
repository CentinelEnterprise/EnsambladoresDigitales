from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def menu_aplicaciones(request):
	usuario = request.user
	principal = request.user.has_module_perms('principal')
	usuarios = request.user.has_module_perms('usuarios')
	return render(request,'dashboard/panel_de_control.html', locals())


def pagina_blanco(request):
	error =  'la pagina se encuentra en desarrollo'
	return render(request,'dashboard/blank.html', locals())
