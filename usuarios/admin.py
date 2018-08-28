# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuarios.models import * 

# Register your models here.
admin.site.register(Empresa)
admin.site.register(Usuario)
admin.site.register(TipoPerfil)
admin.site.register(Perfil)
admin.site.register(PerfilUsuario)