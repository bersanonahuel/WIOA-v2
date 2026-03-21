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
    querystring_auth = False

class MunicipioAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')
    querystring_auth = False

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




def app_resort(func):                                                                                            
    def inner(*args, **kwargs):                                                                                            
        app_list = func(*args, **kwargs)
        # Useful to discover your app and module list:
        #import pprint                                                                                          
        #pprint.pprint(app_list)

        app_sort_key = 'name'
        app_ordering = {
            "Administracion": 1,
            "Proyecto": 2,
            "Registros": 3
        }

        resorted_app_list = sorted(app_list, key=lambda x: app_ordering[x[app_sort_key]] if x[app_sort_key] in app_ordering else 1000)

        model_sort_key = 'object_name'
        model_ordering = {
            "Escuela": 1,
            "Alumno": 2,
            "Maestro": 3,
            "Cliente": 4,
            "Proveedor": 5,
            "Municipio": 6,
            "Cargo": 7,
            "CentroGestion": 8
        }
        for app in resorted_app_list:
            app['models'].sort(key=lambda x: model_ordering[x[model_sort_key]] if x[model_sort_key] in model_ordering else 1000)
        return resorted_app_list
    return inner                                                                                            
                   
admin.site.get_app_list = app_resort(admin.site.get_app_list)


admin.site.register(Maestro, MaestroAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(CentroGestion, CentroGestionAdmin)