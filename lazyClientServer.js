'use strict'
var express = require('express');
var app = express();
var serv = require('http').Server(app);
var path = require('path');
app.use(express.static(path.join(__dirname,'public')));
var redis = require('redis');
var client = redis.createClient();
var fs = require('fs');
app.use(express.static(path.join(__dirname,'public')));
var io = require('socket.io')(serv,{});

client.on("error", function (err) {
    console.log("Error " + err);
});

client.on("ready", function (msg) {
    console.log('redis client is ready');
});

serv.listen(5000, function() {
    console.log("listening on port 5000");
});


function getBlocks() {
    client.keys('chain.block.*', function (err, keys) {
        console.log('printing keys');
        console.log(keys);
        var arr = [];
        if (err) return console.log(err);
        var counter = 0;
        for(var i = 0, len = keys.length; i < len; i++) {
            var block = client.get(keys[i], function(err, reply) {
                if(err) {
                    console.log('error occured');
                    console.log(err);
                }
                // reply is the block
                //console.log(reply);
                block = JSON.parse(reply);
                console.log('now printing block');
                console.log(block);
                console.log('now transactions');
                console.log(block['transactions']);
                arr.push(block);
                if(counter === keys.length) {
                    return arr;
                }
            });
        }
    });   
}

io.on('connection', function(socket) {
    console.log('A client connected');
    setInterval(function() {
        console.log('\n\nNew Iteration');
        socket.emit('data', getBlocks());
    }, 4000);
});

io.on('error', function(err) {
    console.log('error occured');
    console.log(err);
});

