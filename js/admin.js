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
});
