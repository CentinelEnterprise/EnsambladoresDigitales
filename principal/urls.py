from django.conf.urls import * 
from . import views

urlpatterns = [
    url(r'^$', views.menu_aplicaciones,name='menu_aplicaciones'),
    url(r'^en_construccion/$', views.pagina_blanco, name='pagina_construccion'),
   
]

