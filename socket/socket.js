var redis = require('redis');
var sub = redis.createClient();
//Subscribe to the Redis chat channel
sub.subscribe('new_messages');

var net = require('net');

var HOST = '0.0.0.0';
var PORT = 4000;


var connectionMapByUid = new Map();

function connectionHandler(sock) {
    // We have a connection - a socket object is assigned to the connection automatically
    var clientId = sock.remoteAddress + ':' + sock.remotePort;
    console.log('CONNECTED: ' + clientId);

    // Add a 'data' event handler to this instance of socket
    sock.on('data', function(data) {
        console.log('DATA from ' + sock.remoteAddress + ': \n' + data + '\n');
        var json = JSON.parse(data);
        if (json.hasOwnProperty('uid')) {
            connectionMapByUid.set(parseInt(json.uid), sock);
            console.log(connectionMapByUid.keys());
        }
    });
    
    // Add a 'close' event handler to this instance of socket
    sock.on('close', function(data) {
        console.log('CLOSED: ' + clientId);
    });
}

// Create a server instance, and chain the listen function to it
// The function passed to net.createServer() becomes the event handler for the 'connection' event
// The sock object the callback function receives UNIQUE for each connection
var server = net.createServer(connectionHandler);

server.listen(PORT, HOST);

sub.on('message', function (channel, message) {
    message_json = JSON.parse(message.replace(/\'/g, '"'));
    connectionMapByUid.get(message_json.sid).write(JSON.stringify({
        code: 2,
        msg: '聊天信息',
        info: {
            "id": String(message_json.id),
            "fid": String(message_json.fid),
            "sid": String(message_json.sid),
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

console.log('Server listening on ' + HOST +':'+ PORT);












