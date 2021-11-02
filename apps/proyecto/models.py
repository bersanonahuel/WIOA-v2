from django.db import models
from apps.administracion.models import Alumno, Maestro

class CentroGestion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    class Meta:
        verbose_name='Centro de Gestión'
        verbose_name_plural='Centros de Gestión'
        ordering=['nombre']
    
    def __str__(self) :
        return self.nombre

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
    nombre = models.CharField(max_length=50, blank=False,null=False)
    fechaCreacion = models.DateTimeField(auto_now=True)
    nroPartidaPresupuestaria = models.CharField(max_length=200, blank=True,null=True)
    
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

    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, blank=False, null=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = ("Servicios del Proyecto")
        verbose_name_plural = ("Servicios del Proyecto")
    
    def __str__(self) :
        return self.proyecto.nombre + ' || ' + self.servicio.nombre