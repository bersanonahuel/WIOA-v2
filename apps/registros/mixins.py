from django.http import JsonResponse
from .models import ServiciosProyecto


class GetAlumnosPorProyectoMixin(object):

    def render_to_response(self, context, **response_kwargs):
        print('self.request::: ', self.request)
        if self.request.is_ajax():
            data = {}
            try:
                action = self.request.GET['action']
                if action == 'getAlumnosDelProyecto':
                    
                    serviciosProyecto = ServiciosProyecto.objects.get(id=self.request.GET['servicioProyectoId'])

                    p = Proyecto.objects.get(id=serviciosProyecto.proyecto.id)
                    alumnos = p.alumnos.values('id', 'nombre', 'apellidoPaterno', 'apellidoMaterno')
                    
                    if alumnos:
                        data = { 'alumnos': list(alumnos) }
                    else:
                        data['error'] = 'No se encontró ningún alumno asignado a este Proyecto y Servicio'
                else:
                    data['error'] = 'Ha ocurrido un error.'
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            response_kwargs.setdefault('content_type', self.content_type)
            return self.response_class(
                request=self.request,
                template=self.get_template_names(),
                context=context,
                using=self.template_engine,
                **response_kwargs
            )