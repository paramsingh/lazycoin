window.addEventListener('load', function() {
    var socket = io();
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var mock = [{'nonce':'hello', 'prev_hash':'what', 'transactions':[{'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}, {'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}]}, {'nonce':'hello', 'prev_hash':'what', 'transactions':[{'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}]}, {'noonce':'hello', 'prev_hash':'what', 'transactions':[{'sender': 'ram', 'receiver': 'shyam', 'signature': 'sig'}]}];

    
    socket.on('data', function (msg) {
        data = msg.data;
        //console.log(data[0]);
        var new_arr = [];
        data = msg.data
        console.log('server send data');
        console.log(data);
        //console.log(msg.data);
        var cur_hash;
        for(var i = 0; i < data.length; i++) {
            if(data[i].prev_hash == null) {
                new_arr.push(data[i]);
                cur_hash = data[i].hash;
                break;
            }
        }
        var counter = data.length - 1;
        while(counter--) {
            for(var i = 0; i < data.length; i++) {
                if(data[i].prev_hash == cur_hash) {
                    console.log(data[i]);
                    console.log('pushing');
                    new_arr.push(data[i]);
                    console.log(new_arr[new_arr.length-1]);
                    cur_hash = data[i].hash;
                    break;
                }
            }
        }

        console.log('fdfdd');
        console.log(new_arr);
        drawChain(new_arr);
    });

    var x = 10, y = 0;


    function drawChain(hello) {
        for(var i = 0; i < hello.length; i++) {
            ctx.font = '20px Monaco';
        
            var data = hello[i];

            ctx.fillStyle = '#CCCCCC';
            ctx.fillRect(x, y, 250, 420);
            var nonce = data.nonce;
            var prevHash = data.prev_hash;
            ctx.fillStyle = '#006699';
            y = 10;
            ctx.fillRect(x, y, 250, 50);
            ctx.fillStyle = '#ddd';
            ctx.fillText('Nonce :' + data.nonce, x, y+20);
            //ctx.fillText(data.nonce, x, y+00);
            ctx.fillStyle = '#006699';
            y = y + 70;
            ctx.fillRect(x, y, 250, 50);
            ctx.fillStyle = '#ddd';
            if(data.prev_hash != null)
                ctx.fillText('Prev Hash :' + data.prev_hash.substr(0, 10), x, y+20);
            else
                ctx.fillText('Prev Hash : Null', x , y+20);
            y = 160;
            ctx.lineWidth=10;
            if(i != 0) {
                ctx.beginPath();
                ctx.moveTo(x, 225);
                ctx.lineTo(x - 70, 225);
                ctx.stroke();
            }

            var transactions = data.transactions;
            //console.log(transactions);
            ctx.font = '20px Monaco';
            for(var j = 0; j < transactions.length; j++) {
                var tr = transactions[j]['data'];
                //console.log("printing tr")
                //console.log(tr);
                ctx.fillStyle = '#006699';
                if(tr.type == 'CREATE') ctx.fillStyle = 'green';
                ctx.fillRect(x, y, 250, 110);
                ctx.fillStyle = '#ddd';
                var senderkey = tr.sender.e.toString(16) + tr.sender.n.toString(16);
                senderkey = senderkey.substr(0, 10);
                var receiverkey = tr.receiver.e.toString(16) + tr.receiver.n.toString(16);
                receiverkey = receiverkey.substr(0, 10);
                ctx.fillText('Sender: ' + senderkey, x, y+20);
                ctx.fillText('Receiver: ' + receiverkey, x, y+60);
                ctx.fillText('Sign: ' + tr.receiver.n.toString(16).substr(0, 15), x, y+100);
                y = y + 130;
            }
            x = x + 320, y = 0;
        }
        x = 10, y = 0;
        return;
    }
});
