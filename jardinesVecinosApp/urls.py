from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('acercaDe/', views.acercaDe, name="acercaDe"),
    path('feriados/', views.feriados, name="feriados"),
    path('filtrar/', views.filtrar, name="filtrar"),
    path('login/', views.login, name="login"),
    path('productos/', views.productos, name="productos"),
    path('crear/', views.crear, name="crear"),
    path('detalle/<id>/', views.detalle_producto, name="detalle"),
    path('modificar/<id>/', views.modificar, name="modificar"),
    path('eliminar/<id>/', views.eliminar, name="eliminar"),
    path('registro/', views.registro, name="registro"),
    path('logout/', views.cerrar, name="cerrar"),
    path('modificarPerfil/<str:username>', views.modificarPerfil, name="modificarPerfil"),
    path('tienda/',views.tienda, name="tienda"),
    path('agregar/<id>/', views.agregar_producto, name="agregar"),
    path('eliminarProducto/<id>', views.eliminar_producto, name="eliminarProducto"),
    path('restar/<id>', views.restar_producto, name="restar"),
    path('limpiar/', views.limpiar_carrito, name="limpiar"),
    path('generarBoleta/', views.generarBoleta,name="generarBoleta"),
]