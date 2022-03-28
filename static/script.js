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

// $(document).ready(function(){
//     var socket = io.connect('http://192.168.29.83:8080/');

//     socket.on('connect', function(){
//         socket.send("User has connected 6969");
//     });
// });






// WILL RUN ON THE CLIENT HOSTING THE FILE / OR EVERY CLIENT - I AM NOT SO SURE ABOUT IT
var ld;
var lc;
var dc;


function custom_callback(callback1, callback2){
    callback1();
    setTimeout(function(){
        callback2();
      }, 500);
}


// CREATE SOCKET AND SEND LD (LOCAL DESCRIPTION) TO THE SERVER
function createSocket(){
    var socket = io.connect('http://192.168.29.83:8080/');

    socket.on('connect', function(){
        socket.send(ld);
    });

    // $('#downloadButton').on('click', function(){

    // });
}


function init_conn(){
    lc = new RTCPeerConnection();
    dc = lc.createDataChannel("channel");

    // dc.onmessage = e => console.log("Just got a message " + e.data);
    // dc.onopen = e => console.log("Connection Open!");

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


// GET THE SDP OF THE COMPUTER HOSTING THE FILE
function get_host_sdp(){
    
    file_url = event.target.name.split("/");

    info_url = "/get-sdp-of-uploader/" + String(file_url[file_url.length-2]);

    var data;
    req = $.ajax({
        url: info_url,
        type: "GET",
        async: false,
        datatype: "string",
        success: function(response){
            data = response;
        }
    });

    return data;
}


function create_client_conn(callback1, callback2){
    var host_sdp = callback1();
    callback2(host_sdp);
}

// WILL RUN ON THE CLIENT REQUESTING THE FILE
function client_request(host_sdp){

    const rc = new RTCPeerConnection();

    rc.onicecandidate = e => console.log(JSON.stringify(rc.localDescription));

    rc.ondatachannel = e => {
        rc.dc = e.channel;
        // rc.dc.onmessage = e => console.log("new message - " + e.data);
        // rc.dc.onopen = e => console.log("Connection OPEN!");
    }

    rc.setRemoteDescription(JSON.parse(host_sdp));
    rc.createAnswer().then(a => rc.setLocalDescription(a));
}


$(document).ready(function(){
    custom_callback(init_conn, createSocket);

});
// $('#downloadLink').on('click', client_request());