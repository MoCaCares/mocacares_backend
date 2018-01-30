import redis
REDIS_DOMAIN = '0.0.0.0'
REDIS_PORT = 6379

subscriber = redis.StrictRedis(
    host=REDIS_DOMAIN,
    port=REDIS_PORT,
    db=0
).pubsub()  
subscriber.subscribe(['new_message'])


# import socketserver

# class MyTCPHandler(socketserver.BaseRequestHandler):
#     """
#     The RequestHandler class for our server.

#     It is instantiated once per connection to the server, and must
#     override the handle() method to implement communication to the
#     client.
#     """

#     def handle(self):
#         address,pid = self.client_address
#         print('%s connected!'%address)
#         while True:
#             # self.request is the TCP socket connected to the client
#             self.data = self.request.recv(1024).strip()
#             print("{} wrote:".format(self.client_address[0]))
#             print(self.data)
#             # just send back the same data, but upper-cased
#             r = 'test'
#             self.request.sendall(self.data)

# if __name__ == "__main__":
#     HOST, PORT = "0.0.0.0", 4000

#     # Create the server, binding to localhost on port 9999
#     server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

#     # Activate the server; this will keep running until you
#     # interrupt the program with Ctrl-C
#     server.serve_forever(）


#! /usr/bin/env python
#coding=utf-8
from socket import *
from time import ctime
import os, sys
import django


sys.path.append('./mocacares_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocacares_backend.settings')
django.setup()

serverClient = socket(AF_INET, SOCK_STREAM)
HOST=''
PORT=4000
BUFSIZ=1024
ADDR=(HOST, PORT)

from event_platform.models import *

print(list(Event.objects.all()))

serverClient.bind(ADDR)
serverClient.listen(5)

while True:
    print('waiting for input')
    clientSocket, addr = serverClient.accept()
    print('connect from ', addr)
    for item in subscriber.listen():
        print(item)
        print(item['data'])
        print()
    print('test\n\n')
    while True:
        try:
            data= clientSocket.recv(BUFSIZ)
        except:
            print(e)
            clientSocket.close()
            break
        if not data:
            break
        s='Hi,you send me :[%s] %s' %(ctime(), data.decode('utf8'))
        clientSocket.send(s.encode('utf8'))
        print([ctime()], ':', data.decode('utf8'))

clientSocket.close()
serverClient.close()






