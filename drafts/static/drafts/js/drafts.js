function draftPlayer(url, player_id, team_id) {
    $.ajax({
        url: url,
        data: {
            'player_id': player_id,
            'team_id': team_id
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) { ajaxSuccess(data) },
    });
}

function autoDraft(periods) {
    if ($.countdown.periodsToSeconds(periods) === 0) {
        $.ajax({
            url: '/draft/auto_draft/',
            data: {
                'team_id': $('#current-draftee').data('team-id'),
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) { ajaxSuccess(data) },
        });
    }
}

function ajaxSuccess(data) {
    //set up time
    var endTimer = new Date(data.end_time);
    endTimer = new Date(endTimer.getTime());
    $('#countdown').countdown('option', {until: endTimer});

    //move draft along or display end message
    if (data.ended) {
        $('#nav-bar').append("<div id='pop-up-container'><div class='pop-up'><h3>Draft Ended</h3><p><button id='draft-ended-button'>End Draft</button></p></div>")
        $('#draft-ended-button').on('click', function() {
           $.ajax({
               url: data.url,
               data: {},
               type: 'POST',
               dataType: 'json',
               success: function(data) {
                   window.location.href = data.url;
               }
           });
        });
    } else {
        $("#current-draftee").data('team-id', data.current_team_id);
        $("#drafting-team-name").replaceWith("<span id='drafting-team-name' style='font-weight: normal'>" + data.current_team_name + "</span>")
        $("#drafting-team").replaceWith("<ol id='drafting-team'></ol>")

        if (data.current_team_players.length > 0) {
            for (var i = 0; i < data.current_team_players.length; i++) {
                $("#drafting-team").append("<li>" + data.current_team_players[i] + "</li>");
            }
        }
        $(".waiting-team").remove()
        $('.five-px-spacer').remove()

        for (i in data.teams_player_list) {
            if (i == data.current_team_name) {
                continue;
            }
            $('#other-teams').append("<div class='waiting-team'><h4>" + i.replace(/ /g,"_") + "</h4><ol class='" + i.replace(/ /g,"_") + "'></ol></div><div class='five-px-spacer'></div>");
            for (var k = 0; k < data.teams_player_list[i].length; k++) {
                $("." + i.replace(/ /g,"_")).append("<li>" + data.teams_player_list[i][k] + "</li>")
            }
        }
        $(".draft-button[data-player-id=" + data.drafted_player_id + "]").remove()
    }
}