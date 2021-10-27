from django.db import models
from django.conf import settings
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from apps.administracion.models import Alumno, Maestro , Servicio, CentroGestion


# Create your models here.
class RegistroHora(models.Model):
    id=models.AutoField(primary_key=True)
    fechaHoraInicio=models.DateTimeField(auto_now=False)
    fechaHoraFin=models.DateTimeField(auto_now=False)
    estudiante=models.ForeignKey(Alumno, on_delete=models.PROTECT, blank=False, null=False)
    servicio=models.ForeignKey(Servicio,on_delete=models.PROTECT, blank=False, null=False)
    comentario=models.CharField(max_length=400, blank=True, null=True)
    #facturado=models.BooleanField(blank=False, null=True)

