#Import - Export Excel
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from django.contrib import admin
from .models import Alumno, Maestro, Escuela, Municipio, Cliente, Proveedor, Cargo, CentroGestion
from .resources import AlumnoResource



@admin.register(Alumno)
class AlumnoAdmin(ImportExportModelAdmin, ExportActionMixin):
    #ExportActionMixin: es para que aparezca la opcion de exportar en el combo de acciones.

    resource_class = AlumnoResource
    search_fields=['apellidoPaterno', 'apellidoMaterno', 'nombre']
    list_display = ('id', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'nivelEscolar', 'direccion', 'email', 'telefono', 'escuela', 'tipoEncargado', 'nombreEncargado', 'emailEncargado', 'telefonoEncargado')
    list_filter = ('escuela',)
    
    change_list_template  = "admin/import_export/change_list_import.html"
    
   
    #Para excluir formatos que no se utilizan.
    def get_export_formats(self):
        formats = ( base_formats.XLS, base_formats.XLSX, )
        return [f for f in formats if f().can_export()]
    
    def get_import_formats(self):
        formats = ( base_formats.XLS, base_formats.XLSX, )
        return [f for f in formats if f().can_export()]
    



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
    list_display=('id', 'nombre', 'direccionFisica', 'direccionPostal', 'att', 'departamento', 'centroGestion')

class ProveedorAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre', 'telefono', 'fax', 'direccionFisica', 'direccionPostal', 'numeroFiscal')

class CargoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')

class CentroGestionAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display = ('id', 'nombre')


admin.site.register(Maestro, MaestroAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(CentroGestion, CentroGestionAdmin)