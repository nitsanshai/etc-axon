$(document).ready(function() {

    $('#user').keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
        }
    });

    $('#user').keyup(function(e) {
        e.preventDefault();
        if (e.keyCode == 13) {
            window.location.href = '/user?user='+$('#user').val();
        }
    });
});
