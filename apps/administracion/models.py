from django.db import models


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

class EncargadoLegal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    email = models.CharField(max_length=150, blank=False,null=False)
    telefono = models.CharField(max_length=100, blank=False,null=False)
    
    class Meta:
        verbose_name='Encargado Legal'
        verbose_name_plural='Encargados Legales'
        ordering=['nombre']
    
    def __str__(self) :
        return self.nombre
    
class Alumno(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    apellidoPaterno = models.CharField(max_length=100, verbose_name='Apellido Paterno', blank=True, null=True)
    apellidoMaterno = models.CharField(max_length=100, verbose_name='Apellido Materno', blank=True, null=True)
    nivelEscolar = models.CharField(max_length=20, verbose_name='Nivel escolar', blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    
    escuela  =models.ForeignKey(Escuela, on_delete=models.PROTECT, blank=False, null=False)
    escargado_legal = models.ForeignKey(EncargadoLegal, on_delete=models.PROTECT, blank=False, null=True)
    
    class Meta:
        verbose_name='Alumno'
        verbose_name_plural='Alumnos'
        ordering=['nombre', 'apellidoPaterno', 'apellidoMaterno']
    
    def __str__(self) :
        return self.nombre+' '+self.apellidoPaterno+' '+self.apellidoMaterno

class Maestro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)

    alumnos = models.ManyToManyField(Alumno, related_name='maestro')

    class Meta:
        verbose_name='Maestro'
        verbose_name_plural='Maestros'
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
