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




// WEB-RTC CONNECTION FROM HERE

// WILL RUN ON THE CLIENT HOSTING THE FILE / OR EVERY CLIENT - I AM NOT SO SURE ABOUT IT
function init_conn(){
    lc = new RTCPeerConnection();
    dc = lc.createDataChannel("channel");

    dc.onmessage = e => console.log("Just got a message " + e.data);
    dc.onopen = e => console.log("Connection Open!");

    // EVERY TIME WE GET A NEW ICE CANDIDATE
    lc.onicecandidate = e =>{
        // console.log("New ICE Candidate! reprinting SDP" + JSON.stringify(lc.localDescription));
        ld = JSON.stringify(lc.localDescription);
    }

    lc.createOffer().then(o => lc.setLocalDescription(o));


    // RUN AFTER GETTING ANSWER AS RESPONSE FROM THE REQUESTEE
    // const answer = null // ANSWER GOES HERE
    // lc.setRemoteDescription(answer)
}
var ld;
var lc;
var dc;
$(document).ready(init_conn());


// WILL RUN ON THE CLIENT REQUESTING THE FILE
function client_request(){
    const offer = NULL; // CHANGE HERE

    const rc = new RTCPeerConnection();

    rc.onicecandidate = e => console.log(JSON.stringify(rc.localDescription));

    rc.ondatachannel = e => {
        rc.dc = e.channel;
        rc.dc.onmessage = e => console.log("new message - " + e.data);
        rc.dc.onopen = e => console.log("Connection OPEN!");
    }

    rc.setRemoteDescription(offer).then(a => console.log("offer set!"));
    rc.createAnswer().then(a => rc.setLocalDescription(a));
}
