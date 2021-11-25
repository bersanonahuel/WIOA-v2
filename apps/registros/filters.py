import django_filters
from django.forms import NumberInput, Select
from django_filters import filters

from apps.registros.models import Registro
from apps.administracion.models import Alumno
from apps.proyecto.models import Proyecto, Servicio, ServiciosProyecto


class RegistroFilter(django_filters.FilterSet):
    proyecto_servicio = filters.ModelChoiceFilter(
        queryset = ServiciosProyecto.objects.all(),
        label = 'Proyecto | Servicio',
        widget = Select(attrs={'class':'form-control select2'})
    )
    alumno = filters.ModelChoiceFilter(
        queryset = Alumno.objects.all(),
        label = 'Alumno',
        widget = Select(attrs={'class':'form-control select2'})
    )
    proyecto_servicio__servicio = filters.ModelChoiceFilter(
        queryset = Servicio.objects.all(),
        label = 'Servicio',
        widget = Select(attrs={'class':'form-control'})
    )
    proyecto_servicio__proyecto = filters.ModelChoiceFilter(
        queryset = Proyecto.objects.all(),
        label = 'Proyecto',
        widget = Select(attrs={'class':'form-control'})
    )
    
    class Meta:
        model: Registro