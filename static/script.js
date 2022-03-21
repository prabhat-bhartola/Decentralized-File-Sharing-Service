// IMPLEMENTING UPLOAD
function myFile(){
    document.getElementById('file').click();
};

// SETS DELAY TO FUNCTION
function setDelay(callback){
    setTimeout(function(){
        callback();
      }, 100);
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

// loadchats; // This will run on page load

setInterval(function(){
    loadchats() // this will run after every 5 seconds
}, 5000);

function loadPageWithScroll(callback){
    loadchats();
    // callback();

    setDelay(callback);
};

// CLEARS CONTENT OF TEXT FIELD
function clearContent(){
    document.getElementById("msg").value="";
}

function sendButtonClick(){
    setDelay(clearContent);
    setDelay(scrollToBottom);
}

// PREVENT FORM FROM REFRESHING PAGE
$(function() {
    $("form").submit(function() { return false; });
});