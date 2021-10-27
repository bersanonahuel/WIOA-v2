jQuery(document).ready(function($){

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    
    $('select[name="marca"]').on('change', function(){
        var combo = $('select[name="modelo"]');
        var id = $(this).val();
        getElementosCombo(combo, 'buscarModelos', id);
    });
    
    $('select[name="familia"]').on('change', function(){
        var combo = $('select[name="subfamilia"]');
        var id = $(this).val();
        getElementosCombo(combo, 'buscarSubfamilias', id);
    });

    /*
        selectACompletar = combo 2 que se completa cuando selecciono la opcion del combo 1.
        accion = que funcion llama segun el combo que esta seleccionando.
        id = id del elemento que selecciono en el combo 1.
    */
    function getElementosCombo(selectACompletar, action, id) {
        var options;
        
        if(id === ''){
            selectACompletar.html(options);
            return false;
        }

        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': action,
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                selectACompletar.html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data
                });
                return false
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            
        });
    }
});