from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from .models import *
from django.urls.base import reverse_lazy
from .forms import RegistroForm, RegistroDetalleForm, FacturaForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime, timedelta

from apps.proyecto.models import ServiciosProyecto, Proyecto
#Para PDF
from io import BytesIO # nos ayuda a convertir un html en pdf
import os
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
#Filtro
from .filters import RegistroFilter, FacturaFilter

from weasyprint import HTML
from weasyprint import CSS

CREAR_REGISTRO_FILE  = 'registros/crearRegistro.html'
LISTAR_REGISTRO_FILE = 'registros/listarRegistro.html'
LISTAR_FACTURA_FILE  = 'registros/factura/listarFactura.html'
CREAR_FACTURA_FILE   = 'registros/factura/crearFactura.html'

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
            regDet.usuario = request.user
            
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
    template_name = CREAR_FACTURA_FILE

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            request.POST._mutable = True

            print('**** post factura')
            print(request.POST)

            #Pruebas convertir time AM/PM
            format = '%Y-%m-%d'
            date_string_inicio = request.POST['fechaInicio']
            inicio = datetime.strptime(date_string_inicio, format)
    
            date_string_fin = request.POST['fechaFin']
            fin = datetime.strptime(date_string_fin, format)
            
            form = FacturaForm(request.POST)
            factura = form.save(commit=False)
            factura.fechaInicio = inicio.strftime(format)
            factura.fechaFin = fin.strftime(format)
            factura.fechaCreacion = fin.strftime(format)
            factura.cliente = Cliente.objects.get(id=request.POST['cliente'])
            factura.proveedor = Proveedor.objects.get(id=request.POST['proveedor'])
                        
            factura.save()
            
            return super().form_valid(factura)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registros:crearFactura')

class EditarFactura(UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = CREAR_FACTURA_FILE
    success_url = reverse_lazy('registros:listarFactura')

    def get_context_data(self, **kwargs):
        kwargs['boton'] = 'Modificar'
        kwargs['titulo'] = 'Editar Factura'
        return super(EditarFactura,self).get_context_data(**kwargs)

class ListarFactura(ListView):
    model = Factura
    template_name = LISTAR_FACTURA_FILE
    
    def get(self, request, *args, **kwargs):
        factura_filter = FacturaFilter(request.GET, queryset=Factura.objects.all())
        
        return render(request, LISTAR_FACTURA_FILE, {'filter': factura_filter})

class ListarFacturaPdf(TemplateView):
    model = Factura
    template_name = 'registros/documentos/factura.html'
    def get_context_data(self, **kwargs):
        facturaInstance = Factura.objects.get(id=self.kwargs['pk'])
        kwargs['facturaInstance'] = facturaInstance
        kwargs['registrosDetalle'] = RegistroDetalle.objects.filter(factura=facturaInstance.id)

        return super(ListarFacturaPdf,self).get_context_data(**kwargs)


class ImprimirFactura(View):
    def link_callback(self,uri,rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT
    
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl,""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl,""))
        else:
            return uri
        
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl,mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        path = request.path
        
        template = get_template('registros/documentos/factura.html')

        facturaInstance = Factura.objects.get(id=self.kwargs['pk'])
        
        registrosDetalle = RegistroDetalle.objects.filter(factura=facturaInstance.id)

        context = {
            'factura': facturaInstance,
            'registrosDetalle': registrosDetalle,
            'logoCgi':'{}{}'.format(settings.STATIC_URL, 'img/logo-cgi.png'),
            'logoUno':'{}{}'.format(settings.STATIC_URL, 'img/logo-uno.png'),
            'logoAmsi':'{}{}'.format(settings.STATIC_URL, 'img/logo-amsi.png'),
            'logoGobPr':'{}{}'.format(settings.STATIC_URL, 'img/logo-gob-pr.png')
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response, link_callback = self.link_callback
        )
        return response


class PrintPdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template("registros/documentos/imprimirFactura.html")
        
        facturaInstance = Factura.objects.get(id=self.kwargs['pk'])
        registrosDetalle = RegistroDetalle.objects.filter(factura=facturaInstance.id)

        context = {
            'factura': facturaInstance,
            'registrosDetalle': registrosDetalle
        }

        html_template = template.render(context)
        css_url = os.path.join(settings.BASE_DIR, 'static/lib/adminlte-3.1.0/css/adminlte.css')
        pdf = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])

        #return super(PrintPdf,self).get_context_data(**kwargs)
        return HttpResponse(pdf, content_type='application/pdf')