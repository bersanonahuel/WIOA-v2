var date_range=null;

function set_fechas(inicio, fin){
    if (inicio!= null && fin!=null){
        $('#fInicio').val(inicio);
        $('#fFin').val(fin);
    }
}

$(function() {
  
  //Setear por defecto fecha hora Inicio y Fin.
  var date_now = new moment().format('YYYY-MM-DD hh:mm');
  var date_now_fin = new moment().add(1, 'h').format('YYYY-MM-DD hh:mm'); 
  set_fechas(date_now, date_now_fin);

  //##### DATE TIME PICKER #####
  $('.reservationtime').daterangepicker({
    timePicker: true,
    startDate: moment(),
    endDate: moment().add(1, 'hour'),
    autoUpdateInput: false,
    locale: {
      format: 'YYYY-MM-DD hh:mm a',
      applyLabel:'<i class="fa fa-check"></i> Aplicar',
      cancelLabel:'<i class="fa fa-times"></i> Cancelar',
    }
  });
  $('.reservationtime').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('YYYY-MM-DD hh:mm a') + ' - ' + picker.endDate.format('YYYY-MM-DD hh:mm a'));
      console.log(picker)
      date_range=picker;
      set_fechas(date_range.startDate.format('YYYY-MM-DD HH:mm'), date_range.endDate.format('YYYY-MM-DD HH:mm'));
  });
  $('.reservationtime').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
  

  //##### Listar los Alumnos del Proyecto seleccionado. #####
  $('#id_proyecto_servicio.proyectoRegistro').on('change', function(){
    var servicioProyectoId = $(this).val();
    getAlumnosDelProyecto(servicioProyectoId);
  });

  vaciarCombo(document.getElementById('id_alumno'));
  
  function getAlumnosDelProyecto(servicioProyectoId) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'getAlumnosDelProyecto',
            'servicioProyectoId': servicioProyectoId
        },
        dataType: 'json',
    }).done(function (data) {
        
        var cboAlumnos = document.getElementById('id_alumno');

        if (!data.hasOwnProperty('error')) {
            console.log("ALUMNOS DEL PROY: "+data.alumnos);
            
            vaciarCombo(cboAlumnos);
            cargarCombo(cboAlumnos, data.alumnos);
        }
        else{
            vaciarCombo(cboAlumnos);
            alert(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        
    });
  } 

  // **************** FUNCIONES GENERALES **************** //
  function vaciarCombo(combo){
    for (var i = combo.length - 1; i > 0; --i) {
        combo.remove(i);
    }
  }

  function cargarCombo(combo, datos){
    var nombre = '';
    
    for(var i=0; i < datos.length; i++){
      nombre = datos[i].nombre +' '+ datos[i].apellidoPaterno +' '+ datos[i].apellidoMaterno
      combo.add(new Option(nombre, datos[i].id, false, false));
    }
  }


});