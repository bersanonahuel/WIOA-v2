import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
import django
django.setup()

from apps.administracion.models import Escuela

def clean_numeric_schools():
    all_schools = Escuela.objects.all()
    junk_schools = [s for s in all_schools if s.nombre.isdigit()]
    
    if junk_schools:
        print(f"Found {len(junk_schools)} junk schools (numeric names). Deleting...")
        for school in junk_schools:
            print(f"Deleting Escuela: {school.nombre}")
            school.delete()
    else:
        print("No numeric-named schools found.")

if __name__ == '__main__':
    clean_numeric_schools()
