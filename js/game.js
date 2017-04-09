$(document).ready(function() {
    setInterval(function() {
        console.log($('#username').text());
        $.ajax({
            url: '/read-state',
            type: 'POST',
            data: $('#username').text(),
            dataType: 'json',
            cache: false,
            contentType:false,
            processData: false,
            success: function(state) {
                console.log(state);
            }
        });
    }, 1000);
});
