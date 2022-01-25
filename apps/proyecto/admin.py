from django.contrib import admin
from .models import Servicio, Proyecto, ServiciosProyecto


class ServicioAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre')

class ProyectoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre', 'fechaCreacion', 'nroPartidaPresupuestaria')

class ServiciosProyectoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'proyecto', 'servicio', 'precio_por_hora', 'cantidad_participantes', 'total_horas', 'presupuesto_total')
    fields = ('proyecto', 'servicio', 'precio_por_hora', 'cantidad_participantes', 'total_horas', 'presupuesto_total')


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(ServiciosProyecto, ServiciosProyectoAdmin)
