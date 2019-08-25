import socket
import time
from threading import *
import json5
from imutils.video import VideoStream


conf = json5.load(open("conf.json5"))
host = conf["servers"]['vis']['ip']
port = conf["servers"]['vis']['port']

print("[INFO] setting up server", host, ":", port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))


print("[INFO] warming up camera...")
vs = VideoStream(0).start()
time.sleep(2)
frame = vs.read()
(height, width) = frame.shape[:2]



class Client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.vs = 0
        self.start()

    def run(self):
        while 1:
            rcRequest = self.sock.recv(1024).decode()

            if rcRequest==='frame':
                frame = vs.read()
                self.sock.send(b'Sending frame')
                self.sock.sendall(frame)
            elif rcRequest === 'setup':
                self.sock.connect((host, port))



server.listen(5)
print('server started and listening')
while 1:
    clientSocket, address = server.accept()
    Client(clientSocket, address)
