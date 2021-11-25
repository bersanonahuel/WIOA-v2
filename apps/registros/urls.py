from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import  CrearRegistro, ListarRegistro, CrearRegistroDetalle, EliminarRegistroDetalle, CrearFactura

urlpatterns = [
    path('listarRegistro/', login_required(ListarRegistro.as_view()), name = 'listarRegistro'),
    path('crearRegistro/', login_required(CrearRegistro.as_view()), name = 'crearRegistro'),
    
    path('crearRegistroDetalle/<int:registropk>', login_required(CrearRegistroDetalle.as_view()), name = 'crearRegistroDetalle'),
    path('eliminarRegistroDetalle/<int:pk>', login_required(EliminarRegistroDetalle.as_view()), name = 'eliminarRegistroDetalle'),

    path('crearFactura/', login_required(CrearFactura.as_view()), name = 'crearFactura'),
]