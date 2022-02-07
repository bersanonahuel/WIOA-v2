from import_export import resources
from .models import Alumno

class AlumnoResource(resources.ModelResource):
    class Meta:
        model = Alumno