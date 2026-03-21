import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
import django
django.setup()

from apps.administracion.models import Alumno, Escuela, Municipio, Maestro, Cargo

def clean_all_junk():
    models_to_check = [Alumno, Escuela, Municipio, Maestro, Cargo]
    
    for model in models_to_check:
        # Check 'nombre' field which exists in all these models
        junk_records = model.objects.filter(nombre__contains='=')
        count = junk_records.count()
        if count > 0:
            print(f"Found {count} junk records in {model.__name__}. Deleting...")
            for record in junk_records:
                print(f"Deleting from {model.__name__}: {record.nombre}")
                record.delete()
        else:
            print(f"No junk records found in {model.__name__} containing '='.")

if __name__ == '__main__':
    clean_all_junk()
