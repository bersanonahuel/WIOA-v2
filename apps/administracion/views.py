from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Alumno, Maestro ,CentroGestion, Servicio
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
class Inicio(TemplateView):
    template_name = 'index.html'

# ALUMNO
class ListarAlumno(ListView):
    model=Alumno
    template_name = 'administracion/alumno/listarAlumno'
    context_object_name = 'alumnos' #Nombre que le doy al objeto que contiene tod o lo que devuelve la query y se usa en la vista
    queryset = Alumno.objects.all()

class CreateAlumno(CreateView):
    model=Alumno
    template_name = 'administracion/alumno/crearAlumno'
    success_url = reverse_lazy('administracion:listarAlumno')

class EditarAlumno(UpdateView):
    model=Alumno
    template_name = 'administracion/alumno/crearAlumno'
    success_url = reverse_lazy('administracion:listarAlumno')

class EliminarAlumno(DeleteView):
    model=Alumno
    success_url = reverse_lazy('administracion:listarAlumno')

# MAESTRO
class ListarMaestro(ListView):
    model=Maestro
    template_name = 'administracion/maestro/listarMaestro'
    context_object_name = 'maestros' #Nombre que le doy al objeto que contiene tod o lo que devuelve la query y se usa en la vista
    queryset = Maestro.objects.all()

class CreateMaestro(CreateView):
    model=Maestro
    template_name = 'administracion/maestro/crearMaestro'
    queryset = Maestro.objects.all()


class EditarMaestro(UpdateView):
    model=Maestro
    template_name = 'administracion/maestro/crearMaestro'
    queryset = Maestro.objects.all()

class EliminarMaestro(DeleteView):
    model=Maestro
    success_url = reverse_lazy('administracion:listarMaestro')

# CENTRO DE GESTION
class ListarCentroGestion(ListView):
    model=CentroGestion
    template_name = 'administracion/centroGestion/listarCentroGestion'
    context_object_name = 'centroGestion' #Nombre que le doy al objeto que contiene tod o lo que devuelve la query y se usa en la vista
    queryset = CentroGestion.objects.all()

class CreateCentroGestion(CreateView):
    model=CentroGestion
    template_name = 'administracion/centroGestion/crearCentroGestion'
    success_url = reverse_lazy('administracion:listarCentroGestion')

class EditarCentroGestion(UpdateView):
    model=CentroGestion
    template_name = 'administracion/centroGestion/crearCentroGestion'
    success_url = reverse_lazy('administracion:listarCentroGestion')

class EliminarCentroGestion(DeleteView):
    model=CentroGestion
    success_url = reverse_lazy('administracion:listarCentroGestion')

# SERVICIOS

class ListarServicio(ListView):
    model=CentroGestion
    template_name = 'administracion/servicio/listarServicio'
    context_object_name = 'servicio' #Nombre que le doy al objeto que contiene tod o lo que devuelve la query y se usa en la vista
    queryset = Servicio.objects.all()

class CreateServicio(CreateView):
    model=Servicio
    template_name = 'administracion/servicio/crearServicio'
    success_url = reverse_lazy('administracion:listarServicio')

class EditarServicio(UpdateView):
    model=Servicio
    template_name = 'administracion/servicio/crearServicio'
    success_url = reverse_lazy('administracion:listarServicio')

class EliminarServicio(DeleteView):
    model=Servicio
    success_url = reverse_lazy('administracion:listarServicio')