import os
import sys
import django
from django.db import transaction
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WIOA.settings")
django.setup()

from apps.administracion.models import Alumno
from apps.proyecto.models import Proyecto
from apps.registros.models import Registro, RegistroDetalle

def run_fix():
    print("1. Buscando correos duplicados en Alumno...")
    dupes = Alumno.objects.values('email').annotate(c=Count('email')).filter(c__gt=1, email__isnull=False).exclude(email="")
    
    total_borrados = 0
    total_movidos = 0

    for d in dupes:
        email = d['email']
        alumnos = list(Alumno.objects.filter(email=email).order_by('id'))
        if not alumnos:
            continue

        target = alumnos[0]
        basuras = alumnos[1:]
        
        print(f"\nTarget: ID {target.id} - {target.nombre} {target.apellidoPaterno}")
        for basura in basuras:
            print(f"-> Basura a procesar: ID {basura.id} - {basura.nombre} {basura.apellidoPaterno}")
                
if __name__ == '__main__':
    run_fix()
