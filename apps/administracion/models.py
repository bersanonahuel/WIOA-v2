from django.db import models
from django.contrib.auth.models import User


class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)

    class Meta:
        verbose_name='Municipio'
        verbose_name_plural='Municipios'
        ordering=['nombre']

    def __str__(self) :
        return self.nombre

class Escuela(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name='Escuela'
        verbose_name_plural='Escuelas'
        ordering=['nombre']

    def __str__(self) :
        return self.nombre

class Alumno(models.Model):
    TIPO = (
       ('Madre', ('Madre')),
       ('Padre', ('Padre')),
       ('Otro',  ('Otro')),
    )
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    apellidoPaterno = models.CharField(max_length=100, verbose_name='Apellido Paterno', blank=True, null=True)
    apellidoMaterno = models.CharField(max_length=100, verbose_name='Apellido Materno', blank=True, null=True)
    nivelEscolar = models.CharField(max_length=20, verbose_name='Nivel escolar', blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)

    tipoEncargado = models.CharField(max_length=32, choices=TIPO, default='Madre', blank= False, null=False)
    nombreEncargado = models.CharField(max_length=50, verbose_name='Nombre del Encargado Legal', blank=True,null=True)
    emailEncargado = models.CharField(max_length=150, verbose_name='Email del Encargado Legal', blank=True,null=True)
    telefonoEncargado = models.CharField(max_length=100, verbose_name='Teléfono del Encargado Legal', blank=True,null=True)
    
    escuela = models.ForeignKey(Escuela, on_delete=models.PROTECT, blank=False, null=False)
    
    class Meta:
        verbose_name='Alumno'
        verbose_name_plural='Alumnos'
        ordering=['nombre', 'apellidoPaterno', 'apellidoMaterno']
    
    def __str__(self) :
        res = self.nombre+' '+self.apellidoPaterno+' '
        if self.apellidoMaterno != None:
            res+=self.apellidoMaterno

        return res 

class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)

    class Meta:
        verbose_name='Cargo'
        verbose_name_plural='Cargos'
        ordering=['nombre']
    
    def __str__(self) :
        return self.nombre

class Maestro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, blank=False, null=False)
    alumnos = models.ManyToManyField(Alumno, related_name='maestro')

    class Meta:
        verbose_name='Persona'
        verbose_name_plural='Personas'
        ordering=['apellido']
    
    def __str__(self) :
        return self.apellido + ', ' +self.nombre

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=False,null=False)
    direccionFisica = models.CharField(max_length=100, verbose_name='Direccion Física', blank=True, null=True)
    direccionPostal = models.CharField(max_length=100, verbose_name='Direccion Postal', blank=True, null=True)
    
    class Meta:
        verbose_name = ("Cliente")
        verbose_name_plural = ("Clientes")

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=False,null=False)
    telefono = models.CharField(max_length=200, blank=False,null=False)
    fax = models.CharField(max_length=200, blank=False,null=False)
    direccionFisica = models.CharField(max_length=100, verbose_name='Dirección Física', blank=True, null=True)
    direccionPostal = models.CharField(max_length=100, verbose_name='Dirección Postal', blank=True, null=True)
    
    class Meta:
        verbose_name = ("Proveedor")
        verbose_name_plural = ("Proveedores")

    def __str__(self):
        return self.nombre
