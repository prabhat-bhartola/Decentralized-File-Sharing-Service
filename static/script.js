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

// LOAD NEW CHATS WITHOUT RELOAD
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

setInterval(function(){
    loadchats() // this will run after every 5 seconds
}, 5000);

function loadPageWithScroll(callback){
    loadchats();
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




// WEBRTC CONNECTION FROM HERE
// function create_webrtc_init_conn(){
//     var configuration = [];

//     peerConnection = new RTCPeerConnection(configuration);

//     console.log(peerConnection);
// }
// // create_webrtc_init_conn();


// function create_datachannel(){
//     const dataChannelOptions = {
//         ordered: true
//     }

//     send_datachannel = peerConnection.create_datachannel("New Channel", dataChannelOptions);
//     console.log(send_datachannel);

//     send_datachannel.onclose = onSend_ChannelCloseStateChange;
// }
// create_datachannel()
