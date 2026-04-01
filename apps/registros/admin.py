from django.contrib import admin
from .models import Impuesto, Registro, RegistroDetalle

class ImpuestoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')

class RegistroDetalleInline(admin.TabularInline):
    model = RegistroDetalle
    extra = 0

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'proyecto_servicio', 'usuario')
    search_fields = ('alumno__nombre', 'alumno__apellidoPaterno', 'alumno__apellidoMaterno')
    inlines = [RegistroDetalleInline]

class RegistroDetalleAdmin(admin.ModelAdmin):
    list_display = ('id', 'registro', 'fechaHoraInicio', 'fechaHoraFin', 'usuario')
    search_fields = ('registro__alumno__nombre',)
    list_filter = ('fechaHoraInicio', 'fechaHoraFin')

admin.site.register(Impuesto, ImpuestoAdmin)
admin.site.register(Registro, RegistroAdmin)
admin.site.register(RegistroDetalle, RegistroDetalleAdmin)