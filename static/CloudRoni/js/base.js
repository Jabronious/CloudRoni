$(document).ready(function() {
    $("#left-nav-bar > a, .login > a").hover(function() {
       $(this).css("background-color", "rgb(130,128,129)");
    }, function(){
        $(this).css("background-color", "rgb(60, 196, 124)");
    });
});