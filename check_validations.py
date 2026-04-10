import os
import django
import sys

# setup django
sys.path.append(r'c:\s\Sistema\wiao\wioa')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WIOA.settings")
django.setup()

from apps.registros.forms import FacturaForm
from apps.proyecto.models import ServiciosProyecto
from django.forms.models import modelform_factory

form = FacturaForm()
print("FacturaForm terminosPagoOtro required?", form.fields['terminosPagoOtro'].required)
print("FacturaForm terminosPagoOtro validators:", form.fields['terminosPagoOtro'].validators)

admin_form_cls = modelform_factory(ServiciosProyecto, fields='__all__')
admin_form = admin_form_cls()
print("ServiciosProyectoAdmin cantidad_participantes validations default:", admin_form.fields['cantidad_participantes'].validators)
print("ServiciosProyectoAdmin total_horas validations default:", admin_form.fields['total_horas'].validators)
