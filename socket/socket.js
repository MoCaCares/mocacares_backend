var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);

// var redis = require('redis');
// var sub = redis.createClient();

//Subscribe to the Redis chat channel
// sub.subscribe('new_messages');


io.sockets.on('connection', function (socket) {
    console.log('connected')
    socket.emit('news', {
        hello: 'world'
    });
    socket.on('my other event', function (data) {
        console.log(data);
    });
    // // Grab message from Redis and send to client
    // sub.on('message', function (channel, message) {
    //     socket.send(message);
    // });
});