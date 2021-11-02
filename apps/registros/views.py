from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import *
from django.urls.base import reverse_lazy
from .forms import RegistroForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

CREAR_REGISTRO_FILE  = 'registros/crearRegistro.html'

class CrearRegistro(CreateView):
    models=Registro
    form_class=RegistroForm
    template_name= 'registros/crearRegistro.html'
    success_url=reverse_lazy('registros:crearRegistro')
    #print('*****Vista crear registro')
    def get_context_data(self, *args, **kwargs):
        kwargs['titulo'] = 'Crear registro'
        
        return super(CrearRegistro,self).get_context_data(**kwargs)

    # def form_valid(self, form):
    #     print('******Vista form_valid')
    #     form.instance.usuario = self.request.user
    #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         print('----- POST')
    #         print(request.POST['fechaHoraInicio'])
    #         request.POST._mutable = True
    #         request.POST['fechaHoraInicio'] = datetime.strptime(request.POST['fechaHoraInicio'],'%Y-%m-%d %I:%M:%S')
    #         print(request.POST['fechaHoraInicio'])
    #         request.POST['fechaHoraFin'] = datetime.strptime(request.POST['fechaHoraFin'],'%Y-%m-%d %I:%M:%S')
    #         request.POST._mutable = False
    #         print("----------POST CON MODIFICACIONES ----------")
    #         print(request.POST)
    #         form = RegistroForm(request.POST)
    #         print ("-----------FORM--------")
    #         print(request.POST['fechaHoraInicio'])
    #         reg = form.save(commit=False)
    #         print ("------------------reg cambios------------")

    #         # reg.fechaHoraInicio = datetime.strptime(request.POST['fechaHoraInicio'],'%Y-%m-%d %I-%M-%S %p')
    #         # reg.fechaHoraFin = datetime.strptime(request.POST['fechaHoraFin'],'%Y-%m-%d %I-%M-%S %p')
    #         print(reg.fechaHoraInicio)
    #         reg.save()

    #         return super().form_valid(form)

class ListarRegistro(ListView):
    model = Registro
    template_name = 'registros/listarRegistro.html'
    context_object_name = 'registros'
    queryset = Registro.objects.all()
