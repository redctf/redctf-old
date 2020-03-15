$(document).ready(function() {
    $('.table').DataTable( {
      stateSave: true
    } );

    $( ".card" ).hover(
        function() {
          $(this).addClass('shadow').css('cursor', 'pointer'); 
        }, function() {
          $(this).removeClass('shadow');
        }
      );


} );

