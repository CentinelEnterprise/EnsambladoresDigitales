from django.conf.urls import include, url

from . import views

urlpatterns = [
    
    #parte para la gestion de proyectos
    url(r'^administrar_proyectos/$', views.administracion_proyectos, name='administracion_proyectos'),
    url(r'^agregar_proyectos/$', views.agregar_proyectos, name='agregar_proyecto'),
    url(r'^modificar_proyectos/(?P<proyecto_id>\d+)/$', views.modificar_proyecto, name='modificar_proyecto'),
    url(r'^eliminar_proyectos/(?P<proyecto_id>\d+)/$', views.eliminar_proyecto, name='eliminar_proyecto'),
    url(r'^ver_modal_proyectos/(?P<proyecto_id>\d+)/$', views.ver_modal_proyectos, name='ver_modal_proyectos'),
    url(r'^reactivar_proyectos/(?P<proyecto_id>\d+)/$', views.reactivar_proyecto, name='reactivar_proyecto'),
    

]