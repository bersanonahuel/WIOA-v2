from django.contrib import admin
from .models import Servicio, Proyecto, ServiciosProyecto


class ServicioAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre')

class ProyectoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre', 'fechaCreacion', 'participantes')

    def participantes(self, obj):
        return ", ".join([a.nombre +' '+ a.apellidoPaterno for a in obj.alumnos.all()])

class ServiciosProyectoAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'js/admin.js',   # project static folder
        )
    search_fields=['nombre']
    list_display = ('id', 'proyecto', 'servicio', 'tipo_facturacion', 'precio_por_hora_participante', 'cantidad_participantes', 'total_horas', 'presupuesto_total', 'nroPartidaPresupuestaria')
    fields = ('proyecto', 'servicio', 'tipo_facturacion', 'precio_por_hora_participante', 'cantidad_participantes', 'total_horas', 'presupuesto_total', 'nroPartidaPresupuestaria')
    list_filter = ('servicio','tipo_facturacion','proyecto')


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(ServiciosProyecto, ServiciosProyectoAdmin)
