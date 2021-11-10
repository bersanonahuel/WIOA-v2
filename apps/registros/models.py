from django.db import models
from django.conf import settings
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from apps.administracion.models import Alumno, Maestro
from apps.proyecto.models import ServiciosProyecto


# Create your models here.
class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    proyecto_servicio = models.ForeignKey(ServiciosProyecto, verbose_name="Proyecto y Servicio", on_delete=models.PROTECT, blank=False, null=False)
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, blank=False, null=False)
    comentario = models.CharField(max_length=400, blank=True, null=True)
    
class RegistroDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    fechaHoraInicio=models.DateTimeField(auto_now=False)
    fechaHoraFin=models.DateTimeField(auto_now=False)
    registro = models.ForeignKey(Registro, on_delete=models.PROTECT, blank=False, null=False)

