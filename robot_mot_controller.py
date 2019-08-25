import socket
from imutils.video import VideoStream
import json5
import time

conf = json5.load(open('conf.json5'))

# Create server:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((conf['servers']['mot']['ip'],
             conf['servers']['mot']['port']))
server.listen(5)


# initialize the video stream and allow the camera sensor to warmup
#print("[INFO] warming up camera...")
#vs = VideoStream(0).start()
#time.sleep(2)
#frame = vs.read()
#(height, width) = frame.shape[:2]

while True:

    #frame = vs.read()

    # Receive data
    if timer < 1:
        server.connect((conf['servers']['web']['ip'],
                        conf['servers']['web']['port']))

        #server.sendall(frame)
        server.sendall(b'here is a picture')
        timer = 30

    else:
        timer -= 1

    data = server.recv(1024).decode()
    print(data)

