$(document).ready(function() {
    $('#inc').click(function() {
        console.log("NEXT ROUND LET'S GO");
        $.ajax({
            url: '/increment-round',
            type: 'POST',
            cache: false,
            contentType: false,
            processData: false,
            success: function() {
                console.log('NAILED IT');
            }
        });
    });

    $('#clear').click(function() {
        console.log("WAX ON");
        $.ajax({
            url: '/clear-page',
            type: 'POST',
            cache: false,
            contentType: false,
            processData: false,
            success: function() {
                console.log('WAX OFF');
            }
        });
    });

    $('#reset').click(function() {
        console.log("REBOOT");
        $.ajax({
            url: '/reset',
            type: 'POST',
            cache: false,
            contentType: false,
            processData: false,
            success: function() {
                console.log('RESET');
            }
        });
    });

    setInterval(function() {
        $.ajax({
            url: '/unity-read',
            type: 'GET',
            cache: false,
            contentType: false,
            processData: false,
            success: function(state) {
                var state = JSON.parse(state);
                $('#showInfo').empty();
                for (var i in state['public_headlines']) {
                    $('#showInfo').append('<h4 class="col s6">'+state['public_headlines'][i]+'</h4>');
                    $('#showInfo').append('<h4 class="col s6">'+state['likes'][state['public_headlines'][i]]+'</h4>');
                }
            }
        });
    }, 1000);
});
