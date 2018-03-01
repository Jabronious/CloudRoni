function draftPlayer(url, player_id, team_id) {
    $.ajax({
        url: url,
        data: {
            'player_id': player_id,
            'team_id': team_id
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
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
                $('#other-teams').append("<div class='waiting-team'><h4>" + i + "</h4><ol class='" + i + "'></ol></div><div class='five-px-spacer'></div>");
                for (var k = 0; k < data.teams_player_list[i].length; k++) {
                    $("." + i).append("<li>" + data.teams_player_list[i][k] + "</li>")
                }
            }
            $(".draft-button[data-player-id=" + data.drafted_player_id + "]").remove()
        },
    });
}

$(document).ready(function() {
    
});