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

    def calcular_total_horas_por_alumno(self):
        segundos = 0
        for det in RegistroDetalle.objects.filter(registro=self):
            timediff = (det.fechaHoraFin - det.fechaHoraInicio)
            segundos+=timediff.seconds
        
        tiempo = convertir_tiempo(segundos)

        return tiempo
    
class RegistroDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    fechaHoraInicio=models.DateTimeField(auto_now=False)
    fechaHoraFin=models.DateTimeField(auto_now=False)
    registro = models.ForeignKey(Registro, on_delete=models.PROTECT, blank=False, null=False)

    def calcular_total_hs_detalle(self):
        timediff = (self.fechaHoraFin - self.fechaHoraInicio)
        segundos = timediff.seconds

        tiempo = convertir_tiempo(segundos)

        return tiempo

#Convierte segundos al formato hh:mm:ss
def convertir_tiempo(segundos):
    horas = segundos // 3600
    if horas < 10:
        horas = '0'+horas.__str__()

    minutos = (segundos % 3600) // 60
    if minutos < 10:
        minutos = '0'+minutos.__str__()

    segundos = segundos % 60
    if segundos < 10:
        segundos = '0'+segundos.__str__()

    tiempo = horas.__str__()+':'+minutos.__str__()+':'+segundos.__str__()

    return tiempo

