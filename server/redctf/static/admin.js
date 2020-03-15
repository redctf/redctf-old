$(document).ready(function() {
    $('.table').DataTable();

    $( ".card" ).hover(
        function() {
          $(this).addClass('shadow').css('cursor', 'pointer'); 
        }, function() {
          $(this).removeClass('shadow');
        }
      );


} );

