var date_range=null;

function set_fechas(inicio, fin){
  if (inicio != null){
    $('#fInicio').val(inicio);
  }
  //console.log('SET FECHAS fin', fin);
  $('#fFin').val(fin);
}

$(function() {
  
  //##### DATE TIME PICKER REGISTRO HORAS #####
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
      date_range = picker;
      set_fechas(date_range.startDate.format('YYYY-MM-DD HH:mm'), date_range.endDate.format('YYYY-MM-DD HH:mm'));
      //Desp que selecciona la fecha habilito el boton para crear.
      $("#crearRegistro").prop("disabled", false);
  });
  $('.reservationtime').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
  
  //##### DATE TIME PICKER PERIODO FACTURACION #####
  $('#periodoFacturacion').daterangepicker({
    timePicker: false,
    startDate: moment(),
    endDate: moment().add(1, 'M'),
    autoUpdateInput: false,
    locale: {
      format: 'YYYY-MM-DD',
      applyLabel:'<i class="fa fa-check"></i> Aplicar',
      cancelLabel:'<i class="fa fa-times"></i> Cancelar',
    }
  });
  $('#periodoFacturacion').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
      date_range = picker;
      set_fechas(date_range.startDate.format('YYYY-MM-DD'), date_range.endDate.format('YYYY-MM-DD'));
  });
  $('#periodoFacturacion').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
  

  //##### Listar los Alumnos del Proyecto seleccionado. #####
  $('#id_proyecto_servicio.proyectoRegistro').on('change', function(){
    var servicioProyectoId = $(this).val();
    getAlumnosDelProyecto(servicioProyectoId);
  });

  verificarComboAlumnos();
  
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

  //Verifica si el combo de Alumnos tiene que vaciarlo o dejarlo completo. Cuando se registran hs hay que vaciarlo, para el filtro del listado queda completo
  function verificarComboAlumnos(){
    var selectAlumnos = document.getElementById("id_alumno");

    if(selectAlumnos){
      var selectAlumnosResult = selectAlumnos.classList.contains('alumnoRegistro');
      if(selectAlumnosResult){
        vaciarCombo(document.getElementById('id_alumno'));
      }
    }
  }


  // **************** FUNCIONES GENERALES **************** //
  function vaciarCombo(combo){
    if(combo){
      console.log('long: ', combo.length);
      for (var i = combo.length - 1; i > 0; --i) {
          combo.remove(i);
      }
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