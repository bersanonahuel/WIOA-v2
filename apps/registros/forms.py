from django import forms
from .models import RegistroHora

class RegistroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control mb-3'
            }
        self.fields['estudiante'].widget.attrs = {
            'class': 'form-control select2'
        }
        self.fields['servicio'].widget.attrs = {
            'class': 'form-control select2'
        }
        self.fields['fechaHoraInicio'].widget.attrs = {
            'class': 'form-control '
        }
        self.fields['fechaHoraFin'].widget.attrs = {
            'class': 'form-control '
        }
    
    class Meta:
        model = RegistroHora
        fields = [
            'comentario', 
            'estudiante', 
            'servicio',
            'fechaHoraInicio',
            'fechaHoraFin'
        ]
        labels = {
            'comentario':'Comentario',
            'estudiante':'Estudiante',
            'servicio':'Servicio',
        }
        widgets={
            'comentario': forms.Textarea(
                attrs = {
                    'placeholder':'',
                    'rows':'4'
                }
            ),
        }

