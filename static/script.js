// IMPLEMENTING UPLOAD
function myFile(){
    document.getElementById('file').click();
}


// IMPLEMENTING LOAD NEW CHATS WITHOUT RELOAD
$(document).ready(function(){

    $('.sendButton').on('click', function(event){
        let message = $('#msg').val();

        req = $.ajax({
            url: "/chat",
            type: "POST",
            data : {message: message}
        });

        req.done(function(){

            req = $.ajax({
                url: "/chat",
                type: "GET",
                datatype: "html",
                success: function(response){
                    $("#all-chats").html(response);
                }
            });

        });

    });
});


// LOAD NEW CHATS EVERY 5 SECONDS
function loadchats(){

    req = $.ajax({
        url: "/chat",
        type: "GET",
        datatype: "html",
        success: function(response){
            $("#all-chats").html(response);
        }
    });

};

loadchats();

loadchats; // This will run on page load
setInterval(function(){
    loadchats() // this will run after every 5 seconds
}, 5000);