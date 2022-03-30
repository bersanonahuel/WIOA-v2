from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import  CrearRegistro, ListarRegistro, ListarRegistroPorProyecto, CrearRegistroDetalle, EliminarRegistroDetalle, CrearFactura, EditarFactura, ListarFactura, PrintPdf #, ListarFacturaPdf, ImprimirFactura

urlpatterns = [
    path('crearRegistro/', login_required(CrearRegistro.as_view()), name = 'crearRegistro'),
    path('listarRegistro/', login_required(ListarRegistro.as_view()), name = 'listarRegistro'),
    path('listarRegistroPorProyecto/', login_required(ListarRegistroPorProyecto.as_view()), name = 'listarRegistroPorProyecto'),
    
    path('crearRegistroDetalle/<int:registropk>', login_required(CrearRegistroDetalle.as_view()), name = 'crearRegistroDetalle'),
    path('eliminarRegistroDetalle/<int:pk>', login_required(EliminarRegistroDetalle.as_view()), name = 'eliminarRegistroDetalle'),

    path('crearFactura/', login_required(CrearFactura.as_view()), name = 'crearFactura'),
    path('editarFactura/<int:pk>', login_required(EditarFactura.as_view()), name = 'editarFactura'),
    path('listarFactura/', login_required(ListarFactura.as_view()), name = 'listarFactura'),
    
    path('printPdf/<int:pk>', PrintPdf.as_view(), name = 'printPdf'),
]