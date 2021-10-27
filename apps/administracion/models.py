from django.db import models

# Create your models here.
class Alumno(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50, blank=False,null=False)
    apellido=models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name='Alumno'
        verbose_name_plural='Alumnos'
        ordering=['apellido']
    
    def __str__(self) :
        return self.apellido + ', ' +self.nombre

class Maestro(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50, blank=False,null=False)
    apellido=models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name='Maestro'
        verbose_name_plural='Maestros'
        ordering=['apellido']
    
    def __str__(self) :
        return self.apellido + ', ' +self.nombre

class CentroGestion(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50, blank=False,null=False)
    class Meta:
        verbose_name='Centro de Gestion'
        verbose_name_plural='Centros de Gestion'
        ordering=['nombre']
    
    def __str__(self) :
        return self.nombre

class Servicio(models.Model):
    # NOMBRE=(
    #     ('tutoria' , ('Tutoría')),
    #     ('seguimiento' , ('Seguimiento')),
    #     ('mentoria' , ('Mentoría')),
    #     ('conserjeria' , ('Conserjería')),
    #     ('jd' , ('JD'))
    # )
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50, blank=False,null=False)

    class Meta:
        verbose_name='Servicio'
        verbose_name_plural='Servicios'
        ordering=['nombre']
    
    def __str__(self) :
        return self.nombre


# class AlumnoMaestro(models.Model):
#     alumno=models.ForeignKey(Alumno, on_delete=models.PROTECT, blank=False, null=False)
#     maestro=models.ForeignKey(Maestro, on_delete=models.PROTECT, blank=False, null=False)
