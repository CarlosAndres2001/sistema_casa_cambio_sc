from django.urls import path
from . import views

urlpatterns = [

    path('gestionar_categorias', views.gestionar_categorias, name='gestionar_categorias'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear-subcategoria/', views.crear_subcategoria, name='crear_subcategoria'),
    path('listar_categorias', views.listar_categorias, name="listar_categorias"),
    path('registrar_traspaso/', views.registrar_traspaso, name='registrar_traspaso'),
    path('registrar_egreso/', views.registrar_egreso, name='registrar_egreso'),
    path('reporte-egresos/', views.reporte_egresos, name='reporte_egresos'),
    path('reporte-traspasos/', views.reporte_traspasos, name='reporte_traspasos'),
    path('eliminar_traspaso', views.eliminar_traspaso, name='eliminar_traspaso'),
    path('eliminar_egreso', views.eliminar_egreso, name='eliminar_egreso')
]

