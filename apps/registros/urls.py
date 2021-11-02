from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import  CrearRegistro, ListarRegistro

urlpatterns = [
    path('listarRegistro/', login_required(ListarRegistro.as_view()), name = 'listarRegistro'),
    path('crearRegistro/', login_required(CrearRegistro.as_view()), name = 'crearRegistro'),
]