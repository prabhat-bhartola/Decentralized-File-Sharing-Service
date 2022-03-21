 // IMPLEMENTING UPLOAD
function myFile(){
    document.getElementById('file').click();
}

// SCROLL TO BOTTOM OF THE CHATS DIV
function scrollToBottom(){
    var elem = document.getElementById("chats-scroll");
    elem.scrollTop = elem.scrollHeight;
};

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
function loadchats(callback){

    req = $.ajax({
        url: "/chat",
        type: "GET",
        datatype: "html",
        success: function(response){
            $("#all-chats").html(response);
        }
    });
    callback();
};

loadchats();

loadchats; // This will run on page load
setInterval(function(){
    loadchats() // this will run after every 5 seconds
}, 5000);