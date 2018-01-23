function getIdArray(selector, data_attr) {
    var returned_array = []
    $(selector).each(function() {
       returned_array.push($(this).data(data_attr)); 
    });
    return returned_array;
}

function tradeProposedError(errorMessage) {
    $("p").append("<p>" + errorMessage + "</p>");
}

function submitTrade(url) {
    var requesting_team_ids = getIdArray("#requesting-team input:checked", "player-id")
    var receiving_team_ids = getIdArray("#receiving-team input:checked", "player-id")
    
    if(requesting_team_ids.length == 0 || receiving_team_ids.length == 0) {
        tradeProposedError("No players selected");
        return;
    }
    
    $.ajax({
        url: url,
        data: {
            'requesting_team_ids': requesting_team_ids,
            'receiving_team_ids': receiving_team_ids,
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.trade) {
                $("#player-table").replaceWith("<h3>" + data.trade + " created" + "</h3>")
            }
        }
    });
}

$(document).ready(function() {
    $(".player-select").on('click', function() {
        if ($(this).is(":checked")) {
            $(this).closest("tr").addClass("selected-player");
        } else {
            $(this).closest("tr").removeClass("selected-player")
        }
    });
});