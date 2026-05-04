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

    with transaction.atomic():
        for d in dupes:
            email = d['email']
            alumnos = list(Alumno.objects.filter(email=email).order_by('id'))
            if len(alumnos) < 2:
                continue

            target = alumnos[0]
            basuras = alumnos[1:]
            
            print(f"Target: ID {target.id} - {target.nombre} {target.apellidoPaterno}")
            for basura in basuras:
                print(f"-> Movilizando desde Basura: ID {basura.id} - {basura.nombre}...")
                
                # 1. Mover los Registros de la Basura al Target
                registros_basura = Registro.objects.filter(alumno=basura)
                for r in registros_basura:
                    existing_r = Registro.objects.filter(alumno=target, proyecto_servicio=r.proyecto_servicio).first()
                    
                    if existing_r:
                        detalles = RegistroDetalle.objects.filter(registro=r)
                        for det in detalles:
                            det.registro = existing_r
                            det.save()
                            total_movidos += 1
                        r.delete()
                    else:
                        r.alumno = target
                        r.save()
                        total_movidos += RegistroDetalle.objects.filter(registro=r).count()

                # 2. Reasignar a Proyectos
                proyectos = basura.proyecto.all()
                for p in proyectos:
                    p.alumnos.add(target)
                
                # 3. Reasignar a Maestros
                maestros = basura.maestro.all() 
                for m in maestros:
                    m.alumnos.add(target)
                
                # 4. Eliminar el alumno Basura
                basura.delete()
                total_borrados += 1
                
        print(f"\n----- RESUMEN -----")
        print(f"Total de detalles de horas transladados exitosamente: {total_movidos}")
        print(f"Total de perfiles fantasma eliminados: {total_borrados}")

if __name__ == '__main__':
    run_fix()
    print("MIGRACION TERMINADA COMPLETAMENTE")
