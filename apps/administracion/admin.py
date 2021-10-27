from django.contrib import admin
from.models import Alumno, Maestro ,CentroGestion ,Servicio 

class AlumnoAdmin(admin.ModelAdmin):
    search_fields=['apellido']
    list_display = ('apellido', 'nombre')

class MaestroAdmin(admin.ModelAdmin):
    search_fields=['apellido']
    list_display = ('apellido', 'nombre')

class CentroGestionAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('nombre',)

class ServicioAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('nombre',)

# class AlumnoMaestroAdmin(admin.ModelAdmin):
#     search_fields=['alumno']
#     list_display=('alumno', 'maestro')

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Maestro, MaestroAdmin)
admin.site.register(CentroGestion, CentroGestionAdmin)
admin.site.register(Servicio, ServicioAdmin)
# admin.site.register(AlumnoMaestro, oAdmin)