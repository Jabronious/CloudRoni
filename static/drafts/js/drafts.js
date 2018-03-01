$(document).ready(function() {
    var newYear = new Date(); 
    newYear = new Date(newYear.getFullYear() + 1, 1 - 1, 1); 
    $('#countdown').countdown({until: newYear}); 
     
    $('#removeCountdown').click(function() { 
        var destroy = $(this).text() === 'Remove'; 
        $(this).text(destroy ? 'Re-attach' : 'Remove'); 
        $('#defaultCountdown').countdown(destroy ? 'destroy' : {until: newYear}); 
    });
});