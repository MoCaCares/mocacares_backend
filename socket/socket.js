var redis = require('redis');
var sub = redis.createClient();
//Subscribe to the Redis chat channel
sub.subscribe('new_messages');

var net = require('net');

var HOST = '0.0.0.0';
var PORT = 4000;


var connections = new Map();


// Create a server instance, and chain the listen function to it
// The function passed to net.createServer() becomes the event handler for the 'connection' event
// The sock object the callback function receives UNIQUE for each connection
net.createServer(function(sock) {
    // We have a connection - a socket object is assigned to the connection automatically
    var clientId = sock.remoteAddress + ':' + sock.remotePort;
    console.log('CONNECTED: ' + clientId);
    connections.set(clientId, sock);
    
    sub.on('message', function (channel, message) {
        message_json = JSON.parse(message.replace(/\'/g, '"'));
        sock.write(JSON.stringify({
            code: 2,
            msg: '聊天信息',
            info: {
                "id": String(message_json.id),
                "fid": String(message_json.fid),
                "sid": "1",
                "msg": message_json.msg,
                "c_time": message_json.c_time,
                "status": message_json.status,
                "f_username": message_json.f_username,
                "f_img": message_json.f_img,
                "s_username": message_json.s_username,
                "s_img": message_json.s_img
            }
        }));
    });

    // Add a 'data' event handler to this instance of socket
    sock.on('data', function(data) {
        console.log('DATA ' + sock.remoteAddress + ': ' + data);
        // Write the data back to the socket, the client will receive it as data from the server
        sock.write('You said "' + data + '"');
    });
    
    // Add a 'close' event handler to this instance of socket
    sock.on('close', function(data) {
        console.log('CLOSED: ' + clientId);
        connections.delete(clientId);
    });
    
}).listen(PORT, HOST);

console.log('Server listening on ' + HOST +':'+ PORT);












