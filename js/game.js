$(document).ready(function() {

    var headline_part_1 = '\
        <div class="row container">\
<div class="col s8 card-panel center-align white-text blue-grey darken-2">';
    var headline_part_2 = '</div>\
          <a class="col s4 l2 offset-l2 waves-effect waves-light btn amber darken-2"><i class="material-icons left">share</i>SHARE</a>\
        </div>';

    $('a').click(function() {
        var headline = $(this).siblings().text();
        console.log(headline);
        $.ajax({
            url: '/increment-headline',
            type: 'POST',
            data: headline,
            cache: false,
            contentType: false,
            processData: false,
            success: function() {
                console.log('GOT EM');
            }
        });
    });

    setInterval(function() {
        $.ajax({
            url: '/read-state',
            type: 'POST',
            data: $('#username').text(),
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function(state) {
                state = JSON.parse(state);
                $('[data-headlines="public"]').empty();
                for (var i in state['public_headlines']) {
                    console.log(state['public_headlines'][i]);
                    if (state['public_headlines'][i]) {
                        var headline = state['public_headlines'][i];
                        var elem = headline_part_1 + headline + headline_part_2;
                        $('[data-headlines="public"]').append(elem);
                    }
                }
            }
        });
    }, 1000);
});
