// Terminos de Pago Change
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

// Sale Tax Change
$('#id_saleTax.selectSaleTaxFactura').on('change', function(){
    cambioTax( $(this).val() );
});

function cambioTax(valorTax){
    if(valorTax == 'Other'){
        $("#id_saleTaxOtro").prop("readonly", false);
    }
    else{
        $("#id_saleTaxOtro").prop("readonly", true);
        $("#id_saleTaxOtro").val("");
    }
}
cambioTax('');


//Seleccion Proyecto -> Mostrar Servicios de ese Proyecto
$('#selProyectoFactura').on('change', function(){
    
    getServiciosDelProyecto( $(this).val() );

});

function getServiciosDelProyecto(proyectoId) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'getServiciosDelProyecto',
            'proyectoId': proyectoId
        },
        dataType: 'json',
    }).done(function (data) {
        
        //var cboAlumnos = document.getElementById('id_alumno');

        if (!data.hasOwnProperty('error')) {
            
            var serv = data.servicios
            $('#checkServiciosFactura .contenidoCheck').remove()
            html = '<div class="contenidoCheck">';
            for(var i=0; i < serv.length; i++){
                console.log("SERVICIOS DEL PROY: "+serv[i].id);
                html+= '<div class="form-check">'
                html+= '<input class="form-check-input" type="checkbox" name="serviciosCheck" value="'+ serv[i].id +'" id="flexCheckDefault">'
                html+= '<label class="form-check-label" for="flexCheckDefault">'+ serv[i].nombre +'</label>'
                html+= '</div>'
            }
            html+='</div>'
            $('#checkServiciosFactura').append(html);
            
            $('#proyectoSelId').val(proyectoId);

        }
        else{
            //vaciarCombo(cboAlumnos);
            alert(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        
    });
  } 