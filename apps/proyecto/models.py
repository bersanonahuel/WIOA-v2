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
    logoCliente = models.ImageField(upload_to="logos", null=True, blank=True, verbose_name="Logo del Cliente")
    logoAdmin1 = models.ImageField(upload_to="logos", null=True, blank=True, verbose_name="Logo Uno a Uno Admin")
    logoAdmin2 = models.ImageField(upload_to="logos", null=True, blank=True, verbose_name="Logo WIOA Admin")
    
    alumnos = models.ManyToManyField(Alumno, related_name='proyecto', verbose_name="Participantes")
    maestros = models.ManyToManyField(Maestro, related_name='proyecto', verbose_name="Consultores Educativos")

    class Meta:
        verbose_name = ("Proyecto")
        verbose_name_plural = ("Proyectos")
        ordering = ['nombre']
    
    def __str__(self) :
        return self.nombre

    def get_proyectos_del_usuario(usuarioInstance):
        if usuarioInstance.is_superuser:
            proyectos = Proyecto.objects.all()
        else:
            #Son los que brindan servicios, solo hay que mostrar los proyectos que tenga asignados
            maestro = Maestro.objects.filter(usuario=usuarioInstance.id)
            proyectos = Proyecto.objects.filter(maestros__id__in=maestro)

        return proyectos

class ServiciosProyecto(models.Model):
    TIPO_FACTURACION = (
       ('Por hora', ('Por hora')),
       ('Por participante', ('Por participante')),
    )

    id = models.AutoField(primary_key=True)
    precio_por_hora_participante = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0, verbose_name="Precio (por Hora | Participante)") #El precio puede ser por hora o por participante, segun opcion elegida en tipo_facturacion
    cantidad_participantes = models.IntegerField(blank=False, null=False, default=0, verbose_name='Límite de participantes')
    total_horas = models.IntegerField(blank=False, null=False, default=0, verbose_name="Total de horas por participante")
    
    presupuesto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    nroPartidaPresupuestaria = models.CharField(max_length=200, blank=True,null=True, verbose_name='Número de Partida Presupuestaria')
    tipo_facturacion = models.CharField(max_length=32, choices=TIPO_FACTURACION, verbose_name="Tipo de Facturación", default='', blank=False, null=False)

    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, blank=False, null=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        verbose_name = ("Servicios del Proyecto")
        verbose_name_plural = ("Servicios del Proyecto")
        ordering = ['proyecto', 'servicio']
    
    def __str__(self) :
        return self.proyecto.nombre + ' || ' + self.servicio.nombre

    #Para el detalle de la factura multiplica la cant de participantes matriculados por el precio x hs.
    def calcular_precio_total(self):
        total = self.cantidad_participantes * self.precio_por_hora
        return round(total, 2)
    
    #Para el detalle de la factura multiplica la cant de participantes servidos por el precio x hs.
    def calcular_precio_total_participantes(cantPart, precioPorHora):
        total = cantPart * precioPorHora
        return round(total, 2)

    def get_servicios_proyectos_del_usuario(usuarioInstance):
        if usuarioInstance.is_superuser:
            serviciosProyecto = ServiciosProyecto.objects.all()
        else:
            #Son los que brindan servicios, solo hay que mostrar los Servicios-Proyectos que tenga asignados
            maestro = Maestro.objects.filter(usuario=usuarioInstance.id)
            proyectos = Proyecto.objects.filter(maestros__id__in=maestro)
            serviciosProyecto = ServiciosProyecto.objects.filter(proyecto__id__in=proyectos)

        return serviciosProyecto
    
    #Cuando la facturacion es por participante, pero no completo sus horas totales del proyecto, hay sacar el calculo de cada participante por hora.
    def calcular_precio_por_hora(self):
        return round(self.precio_por_hora_participante / self.total_horas, 2)