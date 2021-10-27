var date_range=null;
var date_now= new moment().format('YYYY-MM-DD hh:mm ');


function get_fechas(){
    if (date_range!= null){
        $('#fInicio').val(date_range.startDate.format('YYYY-MM-DD hh:mm:ss'));
        $('#fFin').val(date_range.endDate.format('YYYY-MM-DD hh:mm:ss'));
        
    }
}



$(function() {
  $('.reservationtime').daterangepicker({
    timePicker: true,
    
    // startDate: moment().startOf('hour'),
    // endDate: moment().startOf('hour').add(32, 'hour'),
    locale: {
      format: 'YYYY/MM/DD hh:mm ',
      applyLabel:'<i class="fa fa-check"></i> Aplicar',
      cancelLabel:'<i class="fa fa-times"></i> Cancelar',
    }
  });
  $('.reservationtime').on ('apply.daterangepicker', function(ev, picker) {
      console.log(picker)
        date_range=picker;
        get_fechas();
  });
  $('.reservationtime').on('cancel.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range=picker;
        get_fechas();
  });
});