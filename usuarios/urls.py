from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.usuarios, name='usuarios_usuario'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('crear_rol/', views.crear_rol, name='crear_rol'),
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios_eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios_editar/', views.editar_usuario, name='editar_usuario'),
    path('editar_empresa', views.editar_empresa, name='editar_empresa'),
    path('crear_sucursal', views.crear_sucursal, name='crear_sucursal'),
    path('editar_sucursal', views.editar_sucursal, name='editar_sucursal'),
    path('lista_sucursal', views.lista_sucursal, name='lista_sucursal'),
]

