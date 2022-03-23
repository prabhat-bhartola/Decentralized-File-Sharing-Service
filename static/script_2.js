$(document).ready(function(){
    req = $.ajax({
        url: "/get-ip",
        type: "GET",
        success: function(response){
            console.log(response);
            $("#ip").val(response);
        }
    });
});