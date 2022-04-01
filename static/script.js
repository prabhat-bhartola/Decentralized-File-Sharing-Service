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
}, 10000);


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
// server = my computer
// host = device hosting a file
// client = device requesting for download

// WILL RUN ON THE CLIENT HOSTING THE FILE / OR EVERY CLIENT - I AM NOT SO SURE ABOUT IT
var serverIP = 'http://192.168.29.83:8080/';
var ld;
var lc;
var dc;
var socket;

var client_lc = null;


function custom_callback(callback1, callback2){
    callback1();
    setTimeout(function(){
        callback2();
      }, 500);
}


// Creates socket and send the local description to the server on connect event
function createSocket(){
    socket = io.connect(serverIP);

    socket.on('connect', function(){
        var data = {
            "socket_id": socket.id,
            "local_desc": ld
        }
        
        JSON.stringify(data);
        socket.send(data);
    });

    // This will complete the WebRTC handshake
    socket.on('complete-handshake', (data) => {
        const answer = JSON.parse(data['local_desc']);
        lc.setRemoteDescription(answer)

        console.log("Connection created!")
    })
}


// Runs on every device on connect
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

    // if (client_lc != null){

    //     const answer = client_lc // ANSWER GOES HERE
    //     lc.setRemoteDescription(answer)
    // }

    // async function(){
    //     if (client_lc != null){

    //         const answer = client_lc // ANSWER GOES HERE
    //         lc.setRemoteDescription(answer)
    //     }
    // }
}


// Runs on the client machine and fetches the local description
// of the device hosting the file
function get_host_sdp(){
    
    file_url = event.target.name.split("/");
    file_no = String(file_url[file_url.length-2]);

    info_url = "/get-sdp-of-uploader/" + file_no;

    var data;
    req = $.ajax({
        url: info_url,
        type: "GET",
        async: false,
        datatype: "string",
        success: function(response){
            // data = response;
            data = {
                "host_sdp": response,
                "file_no": file_no
            }
        }
    });

    return data;
}


// Creates an RTCPeerConnection on the client machine and,
// send the local Description to server
function client_request(host_sdp, file_no){

    const rc = new RTCPeerConnection();

    rc.onicecandidate = e => {
        client_lc = JSON.stringify(rc.localDescription);
        // console.log(JSON.stringify(rc.localDescription))
    }

    rc.ondatachannel = e => {
        rc.dc = e.channel;
        rc.dc.onmessage = e => console.log("new message - " + e.data);
        // rc.dc.onopen = e => console.log("Connection OPEN!");
    }

    rc.setRemoteDescription(JSON.parse(host_sdp));
    rc.createAnswer().then(a => rc.setLocalDescription(a));


    // Create websocket to send local description to server

    setTimeout(function(){
        var data = {
            "local_desc": client_lc,
            "file_no": file_no
        }
        JSON.stringify(data);
        socket.emit('client_initialized', data);
    }, 500);
}


// This is called when user presses th download button
// It calls the get_host_sdp() and pases the result to client_request()
function create_client_conn(callback1, callback2){
    data = callback1();

    host_sdp = data['host_sdp'];
    file_no = data['file_no'];

    callback2(host_sdp, file_no);
}
    

$(document).ready(function(){
    custom_callback(init_conn, createSocket);

});
// $('#downloadLink').on('click', client_request());