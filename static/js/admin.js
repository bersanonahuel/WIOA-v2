
django.jQuery(function($) { 
    
    $('#id_tipo_facturacion').on('change', function(){
        calcularPresupuestoTotal();
    });

    $('#id_cantidad_participantes').on('change', function(){
        calcularPresupuestoTotal();
    });
    
    $('#id_precio_por_hora_participante').on('change', function(){
        calcularPresupuestoTotal();
    });

    $('#id_total_horas').on('change', function(){
        calcularPresupuestoTotal();
    });

    function calcularPresupuestoTotal(){
        let tipo = $('#id_tipo_facturacion').val();
        let cantidad = 0;
        let precio = $('#id_precio_por_hora_participante').val();

        if(tipo == 'Por hora') cantidad = $('#id_total_horas').val();  
        if(tipo == 'Por participante') cantidad = $('#id_cantidad_participantes').val();

        let precioTotal = cantidad * precio;

        $('#id_presupuesto_total').val(precioTotal);
    }

})
