$(document).ready(function() {
    $('#sign-up-button').on('click', function() {
       $(this).closest('div').hide();
       $('#sign-up-container').show();
    });
});

function errorMessage(errorMessage) {
    $("p").replaceWith("<p class='error-message'>" + errorMessage + "</p>");
}

function joinLeague(url, league_id, code) {
    if(code == '') {
        errorMessage('League code is required.')
        return;
    }

    $.ajax({
        url: url,
        data: {
            'league_id': league_id,
            'code': code,
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            window.location.href = data.url;
        },
        error: function (data) {
            errorMessage(data.responseText)
        }
    });
}

function startNewSeason(url, date) {
    if(date == '') {
        errorMessage('No date selected')
        return;
    }

    $.ajax({
        url: url,
        data: { 'date': date },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            window.location.href = data.url;
        },
        error: function (data) {
            errorMessage(data.responseText)
        }
    });
}