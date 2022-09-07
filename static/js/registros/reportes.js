//Para llamar a la vista y enviar los parametros del FORM.

function descargarExcelListadoRegistros(){
    console.log('URL:: ', window.location.pathname.split('/')[2]);
    var formulario = document.getElementById('formRegistrosFiltros');
        
    //formulario.append('accionDesde', window.location.pathname);

    formulario.elements["accionDesde"].value = window.location.pathname.split('/')[2];

    formulario.action = '../descargarExcelRegistros';
    //formulario.target = '_blank';
    formulario.submit().then( res => {
        res.action = '../listarRegistro';
    });
}