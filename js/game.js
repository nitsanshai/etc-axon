$(document).ready(function() {

    var headline_part_1 = '\
        <div class="row container">\
<div class="col s8 card-panel center-align white-text blue-grey darken-2">';
    var headline_part_2 = '</div>\
<a class="col s4 l2 offset-l2 waves-effect waves-light btn amber darken-2"><i class="material-icons left">plus_one</i>UPVOTE</a></div>';

    function incrementHeadline(headline) {
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
    }

    $('a').click(function(event) {
        var headline = $($(event.target).siblings()[0]).text();
        incrementHeadline(headline);
        $(this).html('<i class="material-icons left">check_circle</i>');
        $(this).prop('disabled', true);
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
                if (state['cleared']) {
                    $('[data-headlines="public"]').empty();
                    $('[data-headlines="private"]').addClass('hide');
                } else {
                    $('[data-headlines="private"]').removeClass('hide');
                }
                var len = $('[data-headlines="public"]').children().length;
                for (var i in state['public_headlines']) {
                    var headline = state['public_headlines'][i];
                    if (i >= len && headline) {
                        console.log(i);
                        console.log(len);
                        var elem = headline_part_1 + headline + headline_part_2;
                        $('[data-headlines="public"]').append(elem);
                        $('[data-headlines="public"]>div:last a').click(function(event) {
                            var headline = $($(event.target).siblings()[0]).text();
                            incrementHeadline(headline);
                        });
                    }
                }
            }
        });
    }, 1000);
});
