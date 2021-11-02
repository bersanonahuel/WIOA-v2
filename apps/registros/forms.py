from django import forms
from .models import Registro

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

