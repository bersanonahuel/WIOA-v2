from import_export import resources
from .models import Alumno
from tablib import Dataset

class AlumnoResource(resources.ModelResource):
    class Meta:
        model = Alumno