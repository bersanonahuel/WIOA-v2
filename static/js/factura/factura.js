$('#id_terminosPago.selectTerminoPagoFactura').on('change', function(){
    
    cambioTerminosPago( $(this).val() );

});

function cambioTerminosPago(valorTP){
    if(valorTP == 'Other'){
        $("#id_terminosPagoOtro").prop("disabled", false);
    }
    else{
        $("#id_terminosPagoOtro").prop("disabled", true);
        $("#id_terminosPagoOtro").val("");
    }
}

cambioTerminosPago('');
