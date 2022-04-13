from django.db import models
from django.conf import settings
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from apps.administracion.models import Alumno, Maestro, Cliente, Proveedor
from apps.proyecto.models import ServiciosProyecto


class Impuesto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0, verbose_name="Porcentaje (%)")


    class Meta:
        verbose_name='Impuesto'
        verbose_name_plural='Impuestos'
        ordering=['nombre']

    def __str__(self) :
        return self.nombre


class Factura(models.Model):
    TERMINOS_PAGO = (
       ('Due upon reciept', ('Due upon reciept')),
       ('Net 30 days', ('Net 30 days')),
       ('Other', ('Other')),
    )

    id = models.AutoField(primary_key=True)
    fechaCreacion = models.DateTimeField(auto_now=True)
    fechaInicio = models.DateTimeField(auto_now=False)
    fechaFin = models.DateTimeField(auto_now=False)
    eliminada = models.BooleanField(default=False)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    terminosPago = models.CharField(max_length=32, choices=TERMINOS_PAGO, verbose_name="Términos de Pago", default='', blank=True, null=False)
    terminosPagoOtro = models.CharField(max_length=200, verbose_name="Términos Otros", blank=True, null=True)
    mensajeInstitucional = models.CharField(max_length=500, verbose_name="Mensaje Institucional", blank=True, null=True)
    descripcionTareas = models.CharField(max_length=500, verbose_name="Descripción de Tareas", blank=True, null=True)
    logrosObtenidos = models.CharField(max_length=500, verbose_name="Logros Obtenidos", blank=True, null=True)

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, blank=False, null=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, blank=False, null=False)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.PROTECT, blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)

    proyectosServicios = models.ManyToManyField(ServiciosProyecto, related_name='factura')
    
 

# Create your models here.
class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    fechaCreacion = models.DateTimeField(auto_now=True)
    proyecto_servicio = models.ForeignKey(ServiciosProyecto, verbose_name="Proyecto y Servicio", on_delete=models.PROTECT, blank=False, null=False)
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, blank=False, null=False, verbose_name="Participante")
    comentario = models.CharField(max_length=400, blank=True, null=True)

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)

    def calcular_total_horas_por_alumno(self):
        segundos = 0
        for det in RegistroDetalle.objects.filter(registro=self):
            timediff = (det.fechaHoraFin - det.fechaHoraInicio)
            segundos+=timediff.seconds
        
        tiempo = convertir_tiempo(segundos)

        return tiempo

    def calcular_total_horas_faltantes_por_alumno(self):
        segundosRegistrado = self.calcular_total_horas_registradas_por_alumno()
        # for det in RegistroDetalle.objects.filter(registro=self):
        #     timediff = (det.fechaHoraFin - det.fechaHoraInicio)
        #     segundosRegistrado+=timediff.seconds
        
        totalHs = self.proyecto_servicio.total_horas

        totalHsEnSegundos = totalHs * 3600
        hsFaltantes = totalHsEnSegundos - segundosRegistrado
        tiempo = convertir_tiempo(hsFaltantes)

        return tiempo

    def calcular_total_horas_registradas_por_alumno(self):
        segundosRegistrado = 0
        for det in RegistroDetalle.objects.filter(registro=self):
            timediff = (det.fechaHoraFin - det.fechaHoraInicio)
            segundosRegistrado+=timediff.seconds
        
        return segundosRegistrado
    
class RegistroDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    fechaCreacion = models.DateTimeField(auto_now=True)
    fechaHoraInicio=models.DateTimeField(auto_now=False)
    fechaHoraFin=models.DateTimeField(auto_now=False)
    registro = models.ForeignKey(Registro, on_delete=models.PROTECT, blank=False, null=False)
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    comentario = models.CharField(max_length=400, blank=True, null=True)


    def calcular_total_hs_detalle(self):
        timediff = (self.fechaHoraFin - self.fechaHoraInicio)
        segundos = timediff.seconds

        tiempo = convertir_tiempo(segundos)

        return tiempo
    
    def calcular_total_hs_segundos_detalle(self):
        timediff = (self.fechaHoraFin - self.fechaHoraInicio)
        segundos = timediff.seconds

        return segundos

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

    tiempo = horas.__str__()+':'+minutos.__str__() #+':'+segundos.__str__()

    return tiempo
