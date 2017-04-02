window.addEventListener('load', function() {
    var socket = io();
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    
    socket.on('data', function (data) {
        console.log('event received');
        console.log(data);
        drawChain(data);
    });

    function drawChain(data) {
        return;
    }
});
