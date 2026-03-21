import os
import sys
import json
from unittest.mock import MagicMock

# Mock weasyprint (avoid GTK dependency)
sys.modules["weasyprint"] = MagicMock()
import django

# Setup Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
try:
    django.setup()
    from django.db import connection
    connection.ensure_connection()
    print("Django setup and database connection successful!")
except Exception as e:
    print(f"Error during Django/DB setup: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from apps.administracion.models import (
    Alumno, Maestro, Escuela, Municipio, Cargo
)
from apps.proyecto.models import Proyecto


def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'datos_carga.json')
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Create/Get Project "WIOA"
    proyecto, created = Proyecto.objects.get_or_create(nombre='WIOA')
    if created:
        print("Created Project: WIOA")

    # 2. Setup Default Cargo
    cargo, _ = Cargo.objects.get_or_create(nombre='Consultor Educativo')

    # 3. Load Instructors
    for inst_data in data.get('instructores', []):
        nombre_completo = inst_data['nombre']
        # Split name (simple split for now)
        parts = nombre_completo.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        username = (
            nombre_completo.lower().replace(' ', '.')
            .replace('á', 'a').replace('é', 'e')
            .replace('í', 'i').replace('ó', 'o')
            .replace('ú', 'u').replace('ñ', 'n')
        )

        user, u_created = User.objects.get_or_create(username=username)
        if u_created:
            user.set_password('wioa2026')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print(f"Created User: {username}")

        maestro, m_created = Maestro.objects.get_or_create(
            usuario=user,
            defaults={
                'nombre': first_name,
                'apellido': last_name,
                'cargo': cargo
            }
        )
        if m_created:
            print(f"Created Maestro: {nombre_completo}")

        # Associate with project
        proyecto.maestros.add(maestro)

    # 4. Load Students
    for est_data in data.get('estudiantes', []):
        nombre = est_data['nombre']
        municipio_nombre = est_data.get('localidad', 'Desconocido')
        escuela_nombre = est_data.get('escuela', 'Desconocida')

        # Get or Create Municipio
        municipio, _ = Municipio.objects.get_or_create(nombre=municipio_nombre)

        # Get or Create Escuela
        escuela, _ = Escuela.objects.get_or_create(
            nombre=escuela_nombre, municipio=municipio
        )
        # Create Alumno
        # split name safely
        nombre_parts = nombre.split(' ')
        nombre_first = nombre_parts[0]
        apellido_p = nombre_parts[1] if len(nombre_parts) > 1 else ''
        apellido_m = (
            ' '.join(nombre_parts[2:]) if len(nombre_parts) > 2 else ''
        )

        alumno, a_created = Alumno.objects.get_or_create(
            nombre=nombre_first,
            apellidoPaterno=apellido_p,
            apellidoMaterno=apellido_m,
            defaults={
                'nivelEscolar': est_data.get('grado', 'N/A'),
                'direccion': est_data.get('direccion', ''),
                'email': est_data.get('email', ''),
                'telefono': est_data.get('celular', ''),
                'tipoEncargado': 'Otro',
                'nombreEncargado': est_data.get('nombre_padre', ''),
                'emailEncargado': est_data.get('email_padre', ''),
                'telefonoEncargado': est_data.get('tel_padre', ''),
                'escuela': escuela
            }
        )
        if a_created:
            print(f"Created Student: {nombre}")

        # Associate with project
        proyecto.alumnos.add(alumno)

    print("Data loading completed successfully!")


if __name__ == '__main__':
    load_data()
