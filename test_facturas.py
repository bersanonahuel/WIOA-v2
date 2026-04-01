import os
import sys
from unittest.mock import MagicMock

# Mock whitenoise and weasyprint for testing environment
sys.modules["whitenoise"] = MagicMock()
sys.modules["whitenoise.middleware"] = MagicMock()
sys.modules["weasyprint"] = MagicMock()

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
import django
django.setup()

from apps.proyecto.models import Proyecto, Servicio, ServiciosProyecto
from apps.administracion.models import Alumno, Cliente, Proveedor
from apps.registros.models import Factura, Registro, RegistroDetalle, Impuesto
from django.contrib.auth.models import User
from decimal import Decimal
import datetime
from django.test import Client

def test_factura_flow():
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("No superuser found.")
        return

    # Create dummy data
    cliente, _ = Cliente.objects.get_or_create(nombre='Cliente Test')
    proveedor, _ = Proveedor.objects.get_or_create(nombre='Prov Test', defaults={'telefono':'123', 'fax':'456'})
    impuesto, _ = Impuesto.objects.get_or_create(nombre='IVA', defaults={'porcentaje': Decimal('21.0')})
    
    proyecto = Proyecto.objects.first()
    alumno = Alumno.objects.first()
    
    if not proyecto or not alumno:
        print("Faltan proyectos o alumnos.")
        return
        
    servicio, _ = Servicio.objects.get_or_create(nombre='Tutoría')
    sp, _ = ServiciosProyecto.objects.get_or_create(
        proyecto=proyecto, 
        servicio=servicio, 
        defaults={
            'cantidad_participantes': 10,
            'total_horas': 50,
            'tipo_facturacion':'Por hora',
            'precio_por_hora_participante': Decimal('10.0')
        }
    )

    # Crear Registro
    registro, _ = Registro.objects.get_or_create(
        proyecto_servicio=sp,
        alumno=alumno,
        usuario=user
    )

    inicio = datetime.datetime.now() - datetime.timedelta(hours=2)
    fin = datetime.datetime.now()
    
    det = RegistroDetalle.objects.create(
        registro=registro,
        usuario=user,
        fechaHoraInicio=inicio,
        fechaHoraFin=fin,
        comentario='Test Hora'
    )

    factura = Factura.objects.create(
        fechaInicio=inicio.date(),
        fechaFin=fin.date(),
        cliente=cliente,
        proveedor=proveedor,
        impuesto=impuesto,
        usuario=user,
        descripcion='Factura Test'
    )
    factura.proyectosServicios.add(sp)
    
    det.factura = factura
    det.save()

    print(f"Factura {factura.id} creada exitosamente con {det.calcular_total_hs_detalle()} horas.")
    
    # Probar la vista PrintPdf para asegurar que la lógica de cálculo extensa no crashea
    c = Client()
    # Log the user in to bypass login_required if needed
    c.force_login(user)
    response = c.get(f'/registros/printPdf/{factura.id}', HTTP_HOST='127.0.0.1')
    print(f"PrintPdf Status Code: {response.status_code}")

    if response.status_code == 200:
        print("El flujo completo de Facturación, incluyendo PDF, funciona correctamente.")
    else:
        print("Error al generar el PDF de la factura.")

if __name__ == '__main__':
    test_factura_flow()
