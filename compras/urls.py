from django.urls import path
from . import views

urlpatterns = [
    path('crear_proveedor', views.crear_proveedor, name='crear_proveedor'),
    path('registrar_compra/', views.registrar_compra, name='registrar_compra'),
    path('ticket/<int:compra_id>/', views.ticket_compra, name='ticket_compra'),
    path('reimprimir/<int:compra_id>/', views.ticket_compraa, name='ticket_compraa'),
    path('lista_compra', views.lista_compra, name='lista_compra'),
    path('compras_eliminar/', views.eliminar_compra, name='eliminar_compra'),
]


