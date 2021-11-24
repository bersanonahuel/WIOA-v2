from django.contrib import admin
from .models import Alumno, Maestro, Escuela, Municipio, Cliente, Proveedor, Cargo

class AlumnoAdmin(admin.ModelAdmin):
    search_fields=['apellidoPaterno', 'apellidoMaterno', 'nombre']
    list_display = ('id', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'nivelEscolar', 'direccion', 'email', 'telefono', 'escuela', 'tipoEncargado', 'nombreEncargado', 'emailEncargado', 'telefonoEncargado')

class MaestroAdmin(admin.ModelAdmin):
    search_fields=['apellido']
    list_display = ('id', 'nombre', 'apellido', 'cargo', 'usuario')

class EscuelaAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre', 'municipio')

class MunicipioAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')

class ClienteAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')

class ProveedorAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre', 'telefono', 'fax', 'direccionFisica', 'direccionPostal')

class CargoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')


admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Maestro, MaestroAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Cargo, CargoAdmin)