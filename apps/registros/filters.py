import django_filters
from django.forms import NumberInput, Select, DateInput, MultiWidget
from django_filters import filters

from apps.registros.models import Registro, Factura
from apps.administracion.models import Alumno
from apps.proyecto.models import Proyecto, Servicio, ServiciosProyecto


def proyecto_servicio_filtered_queryset(request):
    return ServiciosProyecto.get_servicios_proyectos_del_usuario(request.user)

def proyecto_filtered_queryset(request):
    return Proyecto.get_proyectos_del_usuario(request.user)

class RegistroFilter(django_filters.FilterSet):
    proyecto_servicio = filters.ModelChoiceFilter(
        queryset = proyecto_servicio_filtered_queryset,
        label = 'Proyecto | Servicio',
        widget = Select(attrs={'class':'form-control select2 proyectoServicioFilter'})
    )
    alumno = filters.ModelChoiceFilter(
        queryset = Alumno.objects.all(),
        label = 'Participante',
        widget = Select(attrs={'class':'form-control select2 alumnoRegistroFilter'})
    )
    proyecto_servicio__servicio = filters.ModelChoiceFilter(
        queryset = Servicio.objects.all(),
        label = 'Servicio',
        widget = Select(attrs={'class':'form-control'})
    )
    proyecto_servicio__proyecto = filters.ModelChoiceFilter(
        queryset = proyecto_filtered_queryset,
        label = 'Proyecto',
        widget = Select(attrs={'class':'form-control'})
    )
    
    class Meta:
        model: Registro

class FacturaFilter(django_filters.FilterSet):
    fechaCreacion = django_filters.DateTimeFromToRangeFilter(
        widget=MultiWidget(
            widgets={
                'from': DateInput(attrs={'class': 'datepicker form-control', 'placeholder':'Desde'}),
                'to': DateInput(attrs={'class': 'datepicker form-control', 'placeholder':'Hasta'})
            }
        ),
        label='Rango de Fechas'
    )
    
    
    class Meta:
        model: Factura