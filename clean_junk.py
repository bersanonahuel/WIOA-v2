import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
import django
django.setup()

from apps.administracion.models import Alumno

def clean_junk_students():
    # Buscar estudiantes con caracteres raros, probablemente desde =SUMA
    junk_students = Alumno.objects.filter(nombre__contains='=')
    count = junk_students.count()
    if count > 0:
        print(f"Found {count} junk student records (with '='). Deleting...")
        for student in junk_students:
            print(f"Deleting: {student.nombre} {student.apellidoPaterno}")
            student.delete()
        print("Cleanup complete.")
    else:
        print("No junk student records found containing '='.")

if __name__ == '__main__':
    clean_junk_students()
