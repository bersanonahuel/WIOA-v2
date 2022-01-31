from django.contrib import admin
from .models import Impuesto


class ImpuestoAdmin(admin.ModelAdmin):
    search_fields=['nombre']
    list_display=('id', 'nombre')


admin.site.register(Impuesto, ImpuestoAdmin)