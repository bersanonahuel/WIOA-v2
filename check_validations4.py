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
form = form_class(data={'proyecto': '1', 'servicio': '1', 'tipo_facturacion': 'Por hora', 'precio_por_hora_participante': '10', 'cantidad_participantes': '0', 'total_horas': '0', 'presupuesto_total': '0', 'nroPartidaPresupuestaria': ''})
print(form.is_valid())
print(form.errors)
