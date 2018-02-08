function getIdArray(selector, data_attr) {
    var returned_array = []
    $(selector).each(function() {
       returned_array.push($(this).data(data_attr)); 
    });
    return returned_array;
}

function tradeProposedError(errorMessage) {
    $("p").append(errorMessage);
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
                $("#player-table").replaceWith("<h1 style='text-align: center;'>Trade Submitted</h1>" + "<h3 style='text-align: center;'>" + data.trade + " created" + "</h3>")
            }
        }
    });
}

function postTradeOutcome(url, _this) {
    var outcome = $(_this).data("outcome")
    var trade_id = $(_this).data("trade-id")
    
    $.ajax({
        url: url,
        data: {
            'outcome': outcome,
            'trade_id': trade_id,
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.outcome) {
                $(_this).closest("td").replaceWith("<td>" + data.outcome + "</td>")
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