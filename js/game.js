$(document).ready(function() {

    var headline_part_1 = '\
        <div class="row container">\
<div class="col s8 card-panel center-align white-text blue-grey darken-2">';
    var headline_part_2 = '</div>\
            <a class="col s4 l2 offset-l2 waves-effect waves-light btn amber darken-2"><i class="material-icons left">plus_one</i>UPVOTE</a></div>';

    $('a').click(function() {
        var headline = $(this).siblings().text();
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
                if (state['cleared']) {
                    $('[data-headlines="public"]').addClass('hide');
                    $('[data-headlines="private"]').addClass('hide');
                } else {
                    $('[data-headlines="public"]').removeClass('hide');
                    $('[data-headlines="private"]').removeClass('hide');
                }
                var len = $('[data-headlines="public"]').children().size();
                for (var i in state['public_headlines']) {
                    var headline = state['public_headlines'][i];
                    if (i >= len && headline) {
                        var elem = headline_part_1 + headline + headline_part_2;
                        $('[data-headlines="public"]').append(elem);
                    }
                }
            }
        });
    }, 1000);
});
