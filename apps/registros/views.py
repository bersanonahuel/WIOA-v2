from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from .models import *
from django.urls.base import reverse_lazy
from .forms import RegistroForm, RegistroDetalleForm, FacturaForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime, timedelta

from apps.proyecto.models import ServiciosProyecto, Proyecto
#Filtro
from .filters import RegistroFilter

CREAR_REGISTRO_FILE  = 'registros/crearRegistro.html'
LISTAR_REGISTRO_FILE = 'registros/listarRegistro.html'

class CrearRegistro(CreateView):
    models=Registro
    form_class=RegistroForm
    template_name= 'registros/crearRegistro.html'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                action = request.POST['action']
                
                if action == 'getAlumnosDelProyecto':

                    serviciosProyecto = ServiciosProyecto.objects.get(id=request.POST['servicioProyectoId'])

                    print('**** PROYECTO')
                    p = Proyecto.objects.get(id=serviciosProyecto.proyecto.id)
                    alumnos = p.alumnos.values('id', 'nombre', 'apellidoPaterno', 'apellidoMaterno')
                    print(alumnos)
                    
                    if alumnos:
                        data = { 'alumnos': list(alumnos) }
                    else:
                        data['error'] = 'No se encontró ningún alumno asignado a este Proyecto y Servicio'
                else:
                    data['error'] = 'Ha ocurrido un error'

            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        
        if request.method == 'POST':
            form = RegistroForm(request.POST)
            registro = form.save(commit=False)
            registro.save()
            
            self.kwargs['registropk'] = registro.id

            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        kwargs['titulo'] = 'Crear registro'
        return  super(CrearRegistro,self).get_context_data(**kwargs)
    
    def get_success_url(self):
        return reverse_lazy('registros:crearRegistroDetalle',args=[self.kwargs['registropk']])


class ListarRegistro(ListView):
    model = Registro
    template_name = LISTAR_REGISTRO_FILE
    
    def get(self, request, *args, **kwargs):
        registro_filter = RegistroFilter(request.GET, queryset=Registro.objects.all())
        
        return render(request, LISTAR_REGISTRO_FILE, {'filter': registro_filter})

class CrearRegistroDetalle(CreateView):
    models = RegistroDetalle
    form_class = RegistroDetalleForm
    template_name = 'registros/crearRegistroDetalle.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            request.POST._mutable = True

            #Pruebas convertir time AM/PM
            format = '%Y-%m-%d %H:%M'
            date_string_inicio = request.POST['fechaHoraInicio']  #'2009-11-29 03:17:00.0000'
            inicio = datetime.strptime(date_string_inicio, format)
    
            date_string_fin = request.POST['fechaHoraFin']
            fin = datetime.strptime(date_string_fin, format)

            form = RegistroDetalleForm()
            regDet = form.save(commit=False)
            regDet.fechaHoraInicio = inicio.strftime(format)
            regDet.fechaHoraFin = fin.strftime(format)
            regDet.registro = Registro.objects.get(id=self.kwargs['registropk'])
            
            regDet.save()
            
            return super().form_valid(regDet)
    
    def get_context_data(self, *args, **kwargs):
        kwargs['titulo'] = 'Crear registro de horas'
        kwargs['registro'] = Registro.objects.get(id=self.kwargs['registropk'])
        kwargs['registrosDet'] = RegistroDetalle.objects.filter(registro=self.kwargs['registropk'])
        
        return super(CrearRegistroDetalle,self).get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registros:crearRegistroDetalle',args=[self.kwargs['registropk']])

class EliminarRegistroDetalle(DeleteView):
    model = RegistroDetalle

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            registroDetalle = self.get_object()

            registroDetalle.delete()
            
            res = {
                'mensaje': 'El detalle se elimino con éxito.'
            }
            return JsonResponse(res, safe=False)

class CrearFactura(CreateView):
    models = Factura
    form_class = FacturaForm
    template_name = 'registros/crearFactura.html'

    def get_context_data(self, *args, **kwargs):
        kwargs['facturas'] = Factura.objects.all()
        
        return super(CrearFactura,self).get_context_data(**kwargs)
    
    def get_success_url(self):
        return reverse_lazy('factura:crearFactura')