import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
    django.setup()
    print("Django setup successful!")
    
    from apps.administracion.models import Alumno
    print("Models imported successfully!")
except Exception as e:
    import traceback
    traceback.print_exc()
