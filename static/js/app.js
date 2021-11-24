//Date range picker with time picker
$('#reservationtime').daterangepicker({
  timePicker: true,
  timePickerIncrement: 30,
  locale: {
    format: 'MM/DD/YYYY hh:mm A'
  }
})


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

//ELIMINAR
function eliminarRegistro(id, url){
  Swal.fire({
      title: '¡Atención!',
      text: "¿Está seguro que desea eliminar este registro?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      cancelButtonText: 'Cancelar',
      confirmButtonText: 'Eliminar',
      reverseButtons: true
  }).then((result) => {            
      if (result.isConfirmed) {
          url = url + id

          $.ajax({
              url : url,
              type : 'POST',
              dataType:'json',
              data:{ 'csrfmiddlewaretoken' : getCookie('csrftoken')  },
              beforeSend: function() {
                Swal.fire({
                    title: 'Espere un momento..!',
                    text: 'Esta trabajando..',
                    onOpen: function() {
                        swal.showLoading()
                    }
                })
              },
              success : function(data) {
                Swal.fire({
                    title: '¡Eliminado!',
                    text: data.mensaje,
                    type: 'success',
                    showConfirmButton: false,
                    timer: 8000
                });

                window.setTimeout( function(){ 
                    location.reload();
                }, 300 );
              },
              complete: function() {
                  Swal.hideLoading();
              },
              error: function(jqXHR, textStatus, errorThrown) {
                  Swal.hideLoading();
                  Swal.fire("!Opps ", "Algo salió mal, inténtalo de nuevo más tarde", "error");
              }
          });
      }
  });   
}