from django import forms
from .models import Registro, RegistroDetalle, Factura

class RegistroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control mb-3'
            }
        self.fields['alumno'].widget.attrs = {
            'class': 'form-control select2 alumnoRegistro'
        }
        self.fields['proyecto_servicio'].widget.attrs = {
            'class': 'form-control select2 proyectoRegistro'
        }
    
    class Meta:
        model = Registro
        fields = [
            'comentario', 
            'alumno',
            'proyecto_servicio'
        ]
        labels = {
            'comentario':'Comentario',
            'alumno':'Participante',
        }
        widgets={
            'comentario': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
        }

class RegistroDetalleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroDetalleForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control mb-3'
            }
        self.fields['comentario'].widget.attrs = {
            'class': 'form-control w-25 mx-auto'
        }



    class Meta:
        model = RegistroDetalle
        fields = '__all__'

        widgets={
            'comentario': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
        }
    
class FacturaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control mb-3'
            }
        self.fields['cliente'].widget.attrs = {
            'class': 'form-control select2 clienteFactura'
        }
        self.fields['proveedor'].widget.attrs = {
            'class': 'form-control select2 proveedorFactura'
        }
        self.fields['terminosPago'].widget.attrs = {
            'class': 'form-control selectTerminoPagoFactura'
        }
        self.fields['impuesto'].widget.attrs = {
            'class': 'form-control select2 impuestoFactura'
        }

    class Meta:
        model = Factura
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        terminosPago = cleaned_data.get('terminosPago')
        terminosPagoOtro = cleaned_data.get('terminosPagoOtro')

        if terminosPago == 'Other':
            if not terminosPagoOtro:
                self.add_error('terminosPagoOtro', 'Este campo es requerido cuando selecciona la opción "Other".')
        else:
            cleaned_data['terminosPagoOtro'] = ''
            if 'terminosPagoOtro' in self._errors:
                del self._errors['terminosPagoOtro']
                
        return cleaned_data

        widgets={
            'descripcion': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
            'mensajeInstitucional': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
            'descripcionTareas': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
            'logrosObtenidos': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
        }
    