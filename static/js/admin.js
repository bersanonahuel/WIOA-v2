
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
        let cantidadHs = 0;
        let cantidadParticipantes = 0;
        let precio = $('#id_precio_por_hora_participante').val();

        //if(tipo == 'Por hora') 
        //if(tipo == 'Por participante') 
        
        cantidadHs = $('#id_total_horas').val();  
        cantidadParticipantes = $('#id_cantidad_participantes').val();

        let precioTotal = cantidadHs * cantidadParticipantes * precio;

        $('#id_presupuesto_total').val(precioTotal.toFixed(2));
    }

})
