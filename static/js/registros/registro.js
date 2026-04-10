var date_range=null;
var last_start_date = null;
var last_end_date = null;

function set_fechas(inicio, fin){
  if (inicio != null){
    $('#fInicio').val(inicio);
  }
  if (fin != null){
    $('#fFin').val(fin);
  }
}

$(function() {
  
  var stored_start = localStorage.getItem('last_start_date');
  var stored_end = localStorage.getItem('last_end_date');
  if(stored_start) last_start_date = moment(stored_start);
  if(stored_end) last_end_date = moment(stored_end);

  //##### DATE TIME PICKER REGISTRO HORAS #####
  var $reservationTime = $('.reservationtime');
  
  $reservationTime.daterangepicker({
    timePicker: true,
    startDate: last_start_date ? last_start_date : moment(),
    endDate: last_end_date ? last_end_date : moment().add(1, 'hour'),
    autoUpdateInput: false,
    locale: {
      format: 'MM-DD-YYYY hh:mm a',
      applyLabel:'<i class="fa fa-check"></i> Aplicar',
      cancelLabel:'<i class="fa fa-times"></i> Cancelar',
    }
  });

  if (last_start_date && last_end_date) {
    $reservationTime.val(last_start_date.format('MM-DD-YYYY hh:mm a') + ' - ' + last_end_date.format('MM-DD-YYYY hh:mm a'));
    set_fechas(last_start_date.format('YYYY-MM-DD HH:mm'), last_end_date.format('YYYY-MM-DD HH:mm'));
  }

  $reservationTime.on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('MM-DD-YYYY hh:mm a') + ' - ' + picker.endDate.format('MM-DD-YYYY hh:mm a'));
      date_range = picker;
      // Recordar ultima fecha usada
      last_start_date = picker.startDate.clone();
      last_end_date = picker.endDate.clone();
      localStorage.setItem('last_start_date', picker.startDate.toISOString());
      localStorage.setItem('last_end_date', picker.endDate.toISOString());
      
      set_fechas(date_range.startDate.format('YYYY-MM-DD HH:mm'), date_range.endDate.format('YYYY-MM-DD HH:mm'));
      //Desp que selecciona la fecha habilito el boton para crear.
      let inicio = date_range.startDate.format('YYYY-MM-DD');
      let fin = date_range.endDate.format('YYYY-MM-DD');
      
      if(fin > inicio){
        alert('La fecha de inicio y fin deben ser las mismas.');
        $(this).val('');
      }
      else{
        $("#crearRegistro").prop("disabled", false);
      }
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
      format: 'MM-DD-YYYY',
      applyLabel:'<i class="fa fa-check"></i> Aplicar',
      cancelLabel:'<i class="fa fa-times"></i> Cancelar',
    }
  });
  $('#periodoFacturacion').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('MM-DD-YYYY') + ' - ' + picker.endDate.format('MM-DD-YYYY'));
      date_range = picker;
      set_fechas(date_range.startDate.format('YYYY-MM-DD'), date_range.endDate.format('YYYY-MM-DD'));
  });
  

  /* ##### Listar los Alumnos del Proyecto seleccionado. ##### */

  $('#id_proyecto_servicio.proyectoRegistro').on('change', function(){
    var servicioProyectoId = $(this).val();
    getAlumnosDelProyecto(servicioProyectoId, null, 'POST');
  });
  
  $('#id_proyecto_servicio__proyecto.proyectoRegistroFilter').on('change', function(){ //Cambia el Proyecto, en la vista ListarRegistro
    var proyectoId = $(this).val();
    getAlumnosDelProyecto(null, proyectoId, 'GET');
  });
  
  $('#selProyectoRegistro').on('change', function(){
    getAlumnosDelProyectoMasivo($(this).val());
  });

  function getAlumnosDelProyectoMasivo(proyectoServicioId) {
      $.ajax({
          url: window.location.pathname,
          type: 'POST',
          data: {
            'action': 'getAlumnosDelProyecto',
            'servicioProyectoId': proyectoServicioId
          },
          dataType: 'json',
      }).done(function (data) {

          if (!data.hasOwnProperty('error')) {
              var alumnosList = data.alumnos
              $('#checkAlumnosRegistro .contenidoCheck').remove()
              html = '<div class="contenidoCheck">';
              for(var i=0; i < alumnosList.length; i++){
                  html+= '<div class="form-check">'
                  html+= '<input class="form-check-input" type="checkbox" name="alumnosCheck" value="'+ alumnosList[i].id +'" id="flexCheckDefault">'
                  html+= '<label class="form-check-label" for="flexCheckDefault">'+ alumnosList[i].nombre + ' ' + alumnosList[i].apellidoPaterno + ' ' + alumnosList[i].apellidoMaterno +'</label>'
                  html+= '</div>'
              }
              html+='</div>'
              $('#checkAlumnosRegistro').append(html);

              $('#proyectoServicioSelectId').val(proyectoServicioId);
          }
          else{
              alert(data.error);
          }
      }).fail(function (jqXHR, textStatus, errorThrown) {
          alert(textStatus + ': ' + errorThrown);
      }).always(function (data) {
          
      });
  } 
  verificarComboAlumnos();
  
  //Busca los alumnos del proyecto o servicio, o ambos; segun parametros
  function getAlumnosDelProyecto(servicioProyectoId, proyectoId, type) {
    if(servicioProyectoId > 0 || proyectoId > 0){

      $.ajax({
          url: window.location.pathname,
          type: type,
          data: {
              'action': 'getAlumnosDelProyecto',
              'servicioProyectoId': servicioProyectoId,
              'proyectoId': proyectoId
          },
          dataType: 'json',
      })
      .done(function (data) {
          
          var cboAlumnos = document.getElementById('id_alumno');
          
          if (!data.hasOwnProperty('error')) {
              vaciarCombo(cboAlumnos);
              cargarCombo(cboAlumnos, data.alumnos);
          }
          else{
              vaciarCombo(cboAlumnos);
              alert('Data error getAlumnosDelProyecto: ', data.error);
          }
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
          alert('ERROR: ', textStatus + ': ' + errorThrown);
      }).always(function (data) {
      });
    }
    else{
      verificarComboAlumnos();
    }

  } 

  //Verifica si el combo de Alumnos tiene que vaciarlo o dejarlo completo. Cuando se registran hs hay que vaciarlo, para el filtro del listado queda completo
  function verificarComboAlumnos(){
    var selectAlumnos = document.getElementById("id_alumno");

    if(selectAlumnos){
      var selectAlumnosResult = selectAlumnos.classList.contains('alumnoRegistro');
      
      if(selectAlumnosResult){
        vaciarCombo(document.getElementById('id_alumno'));
      }
      else{         
        var selectAlumnosFilter = selectAlumnos.classList.contains('alumnoRegistroFilter');
        var idProy = $('#id_proyecto_servicio__proyecto.proyectoRegistroFilter').val();
        if(selectAlumnosFilter){ //Para el Filtro en listarRegistros. Para que liste solo los alumnos del Proyecto seleccionado.
          if(idProy) {
             getAlumnosDelProyecto(null, idProy, 'GET');
          } else {
             // Limpiar posibles duplicados nativos en el HTML del filtro si no hay ningun proyecto
             var seen = {};
             $('#id_alumno option').each(function() {
                 var txt = $(this).text().trim();
                 if(txt === '---------') return;
                 if (seen[txt]) {
                     $(this).remove();
                 } else {
                     seen[txt] = true;
                 }
             });
          }
        }
      }
    }
  }


  // **************** FUNCIONES GENERALES **************** //
  function vaciarCombo(combo){
    if(combo){
      var $combo = $(combo);
      // Empty all options except the placeholder and reset the value
      $combo.find('option:not(:first)').remove();
      $combo.val(null).trigger('change');
    }
  }

  function cargarCombo(combo, datos){
    var $combo = $(combo);
    var nombre = '';
    var setNombres = new Set();
    // Primero vaciar para evitar duplicados
    $combo.find('option:not(:first)').remove();
    
    for(var i=0; i < datos.length; i++){
      nombre = datos[i].nombre;
      if (datos[i].apellidoPaterno) {
        nombre = nombre + ' ' + datos[i].apellidoPaterno;
      }
      if(datos[i].apellidoMaterno){
        nombre = nombre +' '+ datos[i].apellidoMaterno;
      }
      nombre = nombre.trim();
      
      if (!setNombres.has(nombre)) {
        setNombres.add(nombre);
        // Use the Select2 documented way to add options dynamically
        $combo.append(new Option(nombre, datos[i].id, false, false));
      }
    }
    // This trigger('change') tells Select2 to re-read the underlying select element
    $combo.trigger('change');
  }
  
});

function listarRegistroPorProyecto(){
  var formulario = document.getElementById('formRegistrosFiltros');
  formulario.action = '../listarRegistroPorProyecto';
  formulario.submit();
}
