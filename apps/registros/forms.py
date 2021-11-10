from django import forms
from .models import Registro, RegistroDetalle

class RegistroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control mb-3'
            }
        self.fields['alumno'].widget.attrs = {
            'class': 'form-control select2'
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
            'alumno':'Alumno',
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
    #fechaHoraInicio = forms.DateTimeField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(RegistroDetalleForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control mb-3'
            }

    class Meta:
        model = RegistroDetalle
        fields = '__all__'

        # widgets={
        #     'fechaHoraInicio': forms.DateTimeField(
        #         input_formats=['%Y-%m-%d %I:%M %p'],
        #     ),
        # }
        
    