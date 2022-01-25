from django.db import models
from apps.administracion.models import Alumno, Maestro



class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)

    class Meta:
        verbose_name='Servicio'
        verbose_name_plural='Servicios'
        ordering=['nombre']
    
    def __str__(self) :
        return self.nombre

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False, verbose_name='Nombre del Proyecto')
    fechaCreacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Creación')
    nroPartidaPresupuestaria = models.CharField(max_length=200, blank=True,null=True, verbose_name='Número de Partida Presupuestaria')
    
    alumnos = models.ManyToManyField(Alumno, related_name='proyecto')
    maestros = models.ManyToManyField(Maestro, related_name='proyecto')

    class Meta:
        verbose_name = ("Proyecto")
        verbose_name_plural = ("Proyectos")
    
    def __str__(self) :
        return self.nombre

class ServiciosProyecto(models.Model):
    id = models.AutoField(primary_key=True)
    precio_por_hora = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    cantidad_participantes = models.IntegerField(blank=False, null=False, default=0)
    total_horas = models.IntegerField(blank=False, null=False, default=0)
    presupuesto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)

    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, blank=False, null=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = ("Servicios del Proyecto")
        verbose_name_plural = ("Servicios del Proyecto")
    
    def __str__(self) :
        return self.proyecto.nombre + ' || ' + self.servicio.nombre

    #Para el detalle de la factura multiplica la cant de participantes por el precio x hs.
    def calcular_precio_total(self):
        total = self.cantidad_participantes * self.precio_por_hora
        return round(total, 2)
    