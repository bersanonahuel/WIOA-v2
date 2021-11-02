from django.contrib import admin
from .models import CentroGestion , Servicio, Proyecto, ServiciosProyecto

class CentroGestionAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre')

class ServicioAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre')

class ProyectoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre', 'fechaCreacion', 'nroPartidaPresupuestaria')

class ServiciosProyectoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'proyecto', 'servicio', 'precio_por_hora', 'cantidad_participantes', 'total_horas')


admin.site.register(CentroGestion, CentroGestionAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(ServiciosProyecto, ServiciosProyectoAdmin)
