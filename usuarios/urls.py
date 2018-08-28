from django.conf.urls import include, url

from . import views

urlpatterns = [

    url(r'^acceder/', views.acceder, name='acceder_usuarios'),
    url(r'^ver_perfil/$', views.ver_perfil_usuario, name='ver_perfil_usuario'),
    url(r'^configuracion/$', views.configuracion, name='configuracion_usuarios'),
    url(r'^recuperar_contrasena/$', views.recuperar_contrasena, name='recuperar_contrasena'),
    url(r'^cerrar_sesion/$', views.cerrar_sesion, name='cerrar_sesion_usuarios'),
    
    #parte para la gestion de usuarios
    url(r'^administrar_usuarios/$', views.administracion_usuarios, name='administracion_usuarios'),
    url(r'^agregar_usuarios/$', views.agregar_usuarios, name='agregar_usuario'),
    url(r'^modificar_usuario/(?P<usuario_id>\d+)/$', views.modificar_usuario, name='modificar_usuario'),
    url(r'^eliminar_usuario/(?P<usuario_id>\d+)/$', views.eliminar_usuario, name='eliminar_usuario'),
    url(r'^ver_modal_usuarios/(?P<usuario_id>\d+)/$', views.ver_modal_usuarios, name='ver_modal_usuarios'),
    url(r'^reactivar_usuario/(?P<usuario_id>\d+)/$', views.reactivar_usuario, name='reactivar_usuario'),
    
    # parte para la gestion de perfiles
    url(r'^administrar_perfiles/$', views.administrar_perfiles, name='administracion_perfiles'),
    url(r'^agregar_perfiles/$', views.agregar_perfiles, name='agregar_perfiles'),
    url(r'^modificar_perfil/(?P<perfil_id>\d+)/$', views.modificar_perfiles, name='modificar_perfil'), 
    url(r'^eliminar_perfil/(?P<perfil_id>\d+)/$', views.eliminar_perfil, name='eliminar_perfil'),
    url(r'^ver_modal_perfiles/(?P<perfil_id>\d+)/$', views.ver_modal_perfiles, name='ver_modal_perfiles'),
    url(r'^reactivar_perfile/(?P<perfil_id>\d+)/$', views.reactivar_perfil, name='reactivar_perfil'),

    #parte para la gestion de empresas
    url(r'^administrar_empresas/$', views.administracion_empresas, name='administracion_empresas'),
    url(r'^agregar_empresas/$', views.agregar_empresa, name='agregar_empresas'),
     url(r'^modificar_empresa/(?P<empresa_id>\d+)/$', views.modificar_empresa, name='modificar_empresa'), 
    url(r'^eliminar_empresa/(?P<empresa_id>\d+)/$', views.eliminar_empresa, name='eliminar_empresa'),
    url(r'^ver_modal_empresas/(?P<empresa_id>\d+)/$', views.ver_modal_empresas, name='ver_modal_empresas'),
    url(r'^reactivar_empresa/(?P<empresa_id>\d+)/$', views.reactivar_empresa, name='reactivar_empresa'),

    #Administracion de Grupos
    url(r'^grupos/$', views.administracion_grupos, name='administracion_grupos_usuarios'),
    url(r'^ver-grupo/(?P<grupo_id>[0-9]+)/$', views.ver_grupo, name='ver_grupo_usuarios'),
    url(r'^agregar-grupo/$', views.agregar_grupo, name='agregar_grupo_usuarios'),
    url(r'^modificar-grupo/(?P<grupo_id>[0-9]+)/$', views.modificar_grupo, name='modificar_grupo_usuarios'),
    url(r'^eliminar-grupo/(?P<grupo_id>[0-9]+)/$', views.eliminar_grupo, name='eliminar_grupo_usuarios'),
    url(r'^ver_modal_grupos/(?P<empresa_id>\d+)/$', views.ver_modal_grupos, name='ver_modal_grupos'),



]
