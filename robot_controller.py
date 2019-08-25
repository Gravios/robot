import socket
from threading import *
import json5

conf = json5.load(open("conf.json5"))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((conf["servers"]['web']['ip'],
             conf["servers"]['web']['port']))
print(host, ":", port)


class Client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            print('Client sent:', self.sock.recv(1024).decode())
            self.sock.send(b'Oi you sent something to me')


server.listen(5)
print('server started and listening')
while 1:
    clientsocket, address = server.accept()
    Client(clientsocket, address)