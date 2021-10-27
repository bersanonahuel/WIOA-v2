from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import  CrearRegistro

urlpatterns = [
    path('crearRegistro/', login_required(CrearRegistro.as_view()), name = 'crearRegistro'),
]