import os
import django
import sys

# setup django
sys.path.append(r'c:\s\Sistema\wiao\wioa')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WIOA.settings")
django.setup()

from apps.registros.forms import FacturaForm

form = FacturaForm({'terminosPago': 'Net 30 days', 'proyectoSelId': '1', 'cliente': '1', 'proveedor': '1', 'impuesto': '1'})
form.is_valid()
print("Errors for FacturaForm with missing terminosPagoOtro:", form.errors)
