var redis = require('redis');
var redisSub = redis.createClient();
//Subscribe to the Redis chat channel
redisSub.subscribe('new_message');

var net = require('net');
var axios = require('axios');

var HOST = '0.0.0.0';
var PORT = 4000;
var SOCKET_CONNECTION_DURATION_IN_MILLISEC = 1000 * 60 * 60 * 6;

var uidToSocketMap = new Map();
var ipportToUidMap = new Map();

function inspect() {
    console.log(ipportToUidMap);
    console.log(uidToSocketMap.keys());
}

function shutdownSocket(sock, clientIpport) {
    if (ipportToUidMap.get(clientIpport) !== undefined) {
        uidToSocketMap.delete(ipportToUidMap.get(clientIpport));
        ipportToUidMap.delete(clientIpport);
    }
    sock.end();
    sock.destroy();
}


function connectionHandler(sock) {
    // We have a connection - a socket object is assigned to the connection automatically
    var clientIpport = sock.remoteAddress + ':' + sock.remotePort;
    console.log('CONNECTED: ' + clientIpport);

    // Add a 'data' event handler to this instance of socket
    sock.on('data', function(data) {
        console.log('DATA from ' + sock.remoteAddress + ': \n' + data);
        var json = JSON.parse(data);

        if (json.hasOwnProperty('sessionKey')) {
            var sessionKey = json.sessionKey;
            axios.get('http://0.0.0.0:8000/get-uid-by-sessionkey?_token=' + sessionKey).then(function (res) {
                console.log(sessionKey + ': ' + res.data);
                if (res.data == 'None')
                    return;
                var uid = parseInt(res.data);
                var oldUid = ipportToUidMap.get(clientIpport);
                if (oldUid !== undefined)
                    uidToSocketMap.delete(oldUid);
                ipportToUidMap.set(clientIpport, uid);
                uidToSocketMap.set(uid, sock);
                inspect();
            });
        }
    });
    
    // Add a 'close' event handler to this instance of socket
    sock.on('close', function(data) {
        console.log('CLIENT CLOSED: ' + clientIpport);
        shutdownSocket(sock, clientIpport);
        inspect();
    });

    sock.setTimeout(SOCKET_CONNECTION_DURATION_IN_MILLISEC);
    sock.on('timeout', function() {
        console.log('TIMEOUT and CLOSE: ' + clientIpport);
        shutdownSocket(sock, clientIpport);
        inspect();
    });
}

// Create a server instance, and chain the listen function to it
// The function passed to net.createServer() becomes the event handler for the 'connection' event
// The sock object the callback function receives UNIQUE for each connection
var server = net.createServer(connectionHandler);

server.listen(PORT, HOST);

redisSub.on('message', function (channel, message) {
    if (channel == 'new_message') {
        message_json = JSON.parse(message.replace(/\'/g, '"'));
        if (uidToSocketMap.get(message_json.sid) === undefined)
            return;
        uidToSocketMap.get(message_json.sid).write(JSON.stringify({
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
    } 
});

console.log('Server listening on ' + HOST +':'+ PORT);












