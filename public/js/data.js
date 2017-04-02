window.addEventListener('load', function() {
    var socket = io();
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var mock = [{'noonce':'hello', 'prev_hash':'what', 'transactions':[{'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}, {'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}]}, {'noonce':'hello', 'prev_hash':'what', 'transactions':[{'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}]}, {'noonce':'hello', 'prev_hash':'what', 'transactions':[{'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}]}];

    
    socket.on('data', function (data) {
        console.log('event received');
        /*console.log(data);
        var new_arr = [];
        for(var i = 0; i < data.length; i++) {
            if(data[i].prev_hash == 'No hash') {
                new_arr.push(data[i]);
                cur_hash = data[i].hash;
            }
        }
        var counter = data.length - 1;
        while(counter--) {
            for(var i = 0; i < data.length; i++) {
                if(data[i].prev_hash == cur_hash) {
                    new_arr.push(data[i]);
                    cur_hash = data[i].hash;
                    break;
                }
            }
        }*/

        drawChain(mock);
    });

    var x = 0, y = 0;


    function drawChain(hello) {
        for(var i = 0; i < hello.length; i++) {
            ctx.font = '20px serif';
        
            var data = hello[i];

            ctx.fillStyle = '#CCCCCC';
            ctx.fillRect(x, y, 250, 420);
            var noonce = data.noonce;
            var prevHash = data.prev_hash;
            ctx.fillStyle = '#996699';
            y = 10;
            ctx.fillRect(x, y, 250, 50);
            ctx.fillStyle = 'black';
            ctx.fillText('Noonce :' + data.noonce, x, y+20);
            //ctx.fillText(data.noonce, x, y+00);
            ctx.fillStyle = '#996699';
            y = y + 70;
            ctx.fillRect(x, y, 250, 50);
            ctx.fillStyle = 'black';
            ctx.fillText('Prev Hash :' + data.prev_hash, x, y+20);
            //ctx.fillText(data.prev_hash, x, y+00);
            y = 160;
            ctx.lineWidth=10;
            if(i != 0) {
                ctx.beginPath();
                ctx.moveTo(x, 225);
                ctx.lineTo(x - 70, 225);
                ctx.stroke();
            }

            var transactions = data.transactions;
            ctx.font = '20px serif';
            for(var j = 0; j < transactions.length; j++) {
                var tr = transactions[j];
                ctx.fillStyle = '#996699';
                if(tr.type == 'create') ctx.fillStyle = 'green';
                ctx.fillRect(x, y, 250, 110);
                ctx.fillStyle = 'black';
                ctx.fillText('Sender: ' + tr.sender, x, y+20);
                ctx.fillText('Receiver: ' + tr.receiver, x, y+60);
                ctx.fillText('Sign: ' + tr.receiver, x, y+100);
                y = y + 130;
            }
            x = x + 320, y = 0;
        }
        x = 0, y = 0;
        return;
    }
});
