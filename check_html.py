import os
import django
import sys

sys.path.append(r'c:\s\Sistema\wiao\wioa')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WIOA.settings")
django.setup()

from apps.proyecto.admin import ServiciosProyectoAdmin
from apps.proyecto.models import ServiciosProyecto
from django.contrib.admin.sites import AdminSite

class MockRequest:
    pass

site = AdminSite()
admin = ServiciosProyectoAdmin(ServiciosProyecto, site)
form_class = admin.get_form(MockRequest())
form = form_class()

print(form['cantidad_participantes'].as_widget())
print(form['total_horas'].as_widget())

from apps.registros.forms import FacturaForm
fform = FacturaForm()
print(fform['terminosPagoOtro'].as_widget())

