'use strict'
var redis = require('redis');
var client = redis.createClient();

client.on("error", function (err) {
    console.log("Error " + err);
});

client.on("ready", function (msg) {
    console.log('client is ready');
});

client.keys('*', function (err, keys) {
    if (err) return console.log(err);
    for(var i = 0, len = keys.length; i < len; i++) {
        console.log(keys[i]);
        var block = client.get(keys[i], function(err, reply) {
            if(err) {
                console.log('error occured');
                console.log(err);
            }
            // reply is the block
            console.log(reply);
            block = JSON.parse(reply);
        });
    }
});   
