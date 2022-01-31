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
from decimal import Decimal
from django.db.models import Count

from apps.proyecto.models import ServiciosProyecto, Proyecto, Servicio
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

from django.db.models import F, Q

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
            print('comentario:::: ', request.POST['comentario'])
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
            regDet.comentario = request.POST['comentario']
            
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
        if request.is_ajax():
            data = {}
            try:
                action = request.POST['action']
                
                if action == 'getServiciosDelProyecto':

                    p = Proyecto.objects.get(id=request.POST['proyectoId'])
                    serviciosProyecto = ServiciosProyecto.objects.filter(proyecto=p.id)
                    
                    servicioIds = serviciosProyecto.values_list('servicio_id', flat=True) #.values('id', 'nombre')
                    servicios = Servicio.objects.filter(pk__in=servicioIds).values('id', 'nombre')
                    print(servicios)
                    
                    if servicios:
                        data = { 'servicios': list(servicios) }
                    else:
                        data['error'] = 'No se encontró ningún Servicio asignado a este Proyecto.'
                else:
                    data['error'] = 'Ha ocurrido un error'

            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)

        if request.method == 'POST':
            request.POST._mutable = True

            #Pruebas convertir time AM/PM
            format = '%Y-%m-%d'
            date_string_inicio = request.POST['fechaInicio']
            inicio = datetime.strptime(date_string_inicio, format)
    
            date_string_fin = request.POST['fechaFin']
            fin = datetime.strptime(date_string_fin, format)
            

            request.POST['proyectosServicios'] = 1
            
            form = FacturaForm(request.POST)
            
            if form.is_valid():
                factura = form.save(commit=False)
                factura.fechaInicio = inicio.strftime(format)
                factura.fechaFin = fin.strftime(format)
                factura.fechaCreacion = fin.strftime(format)
                factura.cliente = Cliente.objects.get(id=request.POST['cliente'])
                factura.proveedor = Proveedor.objects.get(id=request.POST['proveedor'])

                factura.save()
                
                #Guardar tabla intermedia Factura-ProyectoServicios
                proyectoSelId = request.POST['proyectoSelId']
                #print('PROY: ',proyectoSelId)
                for serv in request.POST.getlist('serviciosCheck'):
                    sp = ServiciosProyecto.objects.filter(proyecto=proyectoSelId, servicio=serv).first()
                    
                    factura.proyectosServicios.add(sp)
                
                factura.save()

                #Buscar todos los registros de hs que se incluyan en el periodo ingresado.
                detalles = RegistroDetalle.objects.filter( fechaHoraInicio__gte=inicio, fechaHoraFin__lte=fin, factura=None )

                listaProyServFactura = factura.proyectosServicios.values_list('id',flat=True)
                for det in detalles:
                    if det.registro.proyecto_servicio.id in listaProyServFactura:
                        det.factura = factura
                        det.save()
                
                return super().form_valid(factura)
            else:
                print('NO SE GUARDO, ERROR: ', form.errors)
                return super().form_valid(form)


    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registros:crearFactura')
    
    def get_context_data(self, **kwargs):
        kwargs['proyectos'] = Proyecto.objects.all()
        return super(CrearFactura,self).get_context_data(**kwargs)

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
        

class PrintPdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template("registros/documentos/imprimirFactura.html")
        
        facturaInstance = Factura.objects.get(id=self.kwargs['pk'])
        
        registrosDetalle = dict()
        registrosDetalle = RegistroDetalle.objects.filter(factura=facturaInstance.id).order_by('usuario', 'registro', 'fechaHoraInicio')
        usuariosList = RegistroDetalle.objects.filter(factura=facturaInstance.id).values('usuario', 'usuario__first_name', 'usuario__last_name').distinct()
        
        # ······ Total y subtotal Factura
        subtotal = Decimal(0.0)
        total = Decimal(0.0)

        for proyServ in facturaInstance.proyectosServicios.all():
            subtotal = subtotal + (proyServ.precio_por_hora * proyServ.cantidad_participantes)
            
        
        tax = Decimal(0.0)
        tax = facturaInstance.impuesto.porcentaje

        precioTax = round(subtotal * (tax/100), 2)
        total = subtotal + precioTax
        
        totalParticipantes = facturaInstance.proyectosServicios.all().aggregate(total=models.Sum('cantidad_participantes'))


        # ······ Detalle de Hs por MES
        registrosPorMes = dict()
        nro = 1
        tutoriaHsTotal = 0
        mentoriaHsTotal = 0
        conserjeriaHsTotal = 0
        jsHsTotal = 0
        totalHorasServicios = 0
        
        for i in range(1, 13): 
            #regDetMes = RegistroDetalle.objects.filter(factura=facturaInstance.id, fechaHoraInicio__month = i).values('fechaHoraInicio__month', servicioId=F('registro__proyecto_servicio__servicio')).annotate(cant=Count('registro', distinct=True)).order_by('fechaHoraInicio__month', '-registro__proyecto_servicio__servicio')
            #cantParticipantes = ([regDet.registro_id for regDet in regDetMes])
            regDetMes = RegistroDetalle.objects.filter(factura=facturaInstance.id, fechaHoraInicio__month = i).values('fechaHoraInicio__month').aggregate(
                tutoria=Count('registro', distinct=True, filter=Q(registro__proyecto_servicio__servicio=1)),
                mentoria=Count('registro', distinct=True, filter=Q(registro__proyecto_servicio__servicio=2)),
                conserjeria=Count('registro', distinct=True, filter=Q(registro__proyecto_servicio__servicio=3)),
                js=Count('registro', distinct=True, filter=Q(registro__proyecto_servicio__servicio=4)),
            )
            
            if regDetMes:
                if regDetMes['tutoria'] > 0 or regDetMes['mentoria'] > 0 or regDetMes['conserjeria'] > 0 or regDetMes['js'] > 0:
                    for servicio in range(1,5):
                        seg = 0
                        reg = RegistroDetalle.objects.filter(factura=facturaInstance.id, fechaHoraInicio__month = i, registro__proyecto_servicio__servicio=servicio)
                        #print('MES: ', i, ' ++++ serv', servicio)
                        for r in reg:
                            seg = seg + r.calcular_total_hs_segundos_detalle()

                        #print('seg en hs: ',convertir_tiempo(seg))
                        hs = convertir_tiempo(seg)
                        if servicio == 1:
                            regDetMes['tutoriaHs']  = hs
                            tutoriaHsTotal = tutoriaHsTotal + seg
                        if servicio == 2:
                            regDetMes['mentoriaHs']  = hs
                            mentoriaHsTotal = mentoriaHsTotal + seg
                        if servicio == 3:
                            regDetMes['conserjeriaHs']  = hs
                            conserjeriaHsTotal = conserjeriaHsTotal + seg
                        if servicio == 4:
                            regDetMes['jsHs']  = hs
                            jsHsTotal = jsHsTotal + seg
                    
                    regDetMes['mes'] = i
                    registrosPorMes[nro] = regDetMes
                    nro = nro+1

                    totalHorasServicios = tutoriaHsTotal + mentoriaHsTotal + conserjeriaHsTotal + jsHsTotal
        
        # TOTALES
        totTutoria = 0
        totMentoria = 0
        totConserjeria = 0
        totJs = 0

        for t in registrosPorMes.values():
            totTutoria+=t['tutoria']
            totMentoria+=t['mentoria']
            totConserjeria+=t['conserjeria']
            totJs+=t['js']
        
        registrosPorMes['TOTAL'] = {
            'tutoria': totTutoria,
            'mentoria': totMentoria,
            'conserjeria': totConserjeria,
            'js': totJs,
            'tutoriaHs': convertir_tiempo(tutoriaHsTotal),
            'mentoriaHs': convertir_tiempo(mentoriaHsTotal),
            'conserjeriaHs': convertir_tiempo(conserjeriaHsTotal),
            'jsHs': convertir_tiempo(jsHsTotal)
        }

        #print('registrosPorMes:::: ',registrosPorMes)
        
        context = {
            'factura': facturaInstance,
            'registrosDetalle': registrosDetalle,
            'usuariosList': usuariosList,

            'subtotalFactura': round(subtotal, 2),
            'totalFactura': round(total, 2),
            'precioTax': precioTax,
            'totalParticipantes': totalParticipantes,
            'totalHorasServicios': convertir_tiempo(totalHorasServicios),
            
            'serviciosList': Servicio.objects.all(),
            'serviciosFacturados': facturaInstance.proyectosServicios.values_list('servicio',flat=True),
            'registrosPorMes': registrosPorMes
        }

        html_template = template.render(context)
        #css_url = os.path.join(settings.BASE_DIR, 'static/lib/adminlte-3.1.0/css/adminlte.css')
        #pdf = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
        pdf = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()

        return HttpResponse(pdf, content_type='application/pdf')