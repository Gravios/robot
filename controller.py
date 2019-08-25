# controller.py
#
# Setup server
# Setup video stream
# Setup movement library
#
# Currently implemented on a raspberry pi 2 B+
# Limited to python 2.7 and supported libraries

import pigpio
import pygame, sys, time
import pygame.camera
from pygame.locals import *
import socket, os
#import numpy as np
#import cv2
from imutils.video import VideoStream
import imutils
#import movement_library as mvnt

# Create server:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.2.101", 5000))
server.listen(5)

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(0).start()
time.sleep(2)
frame = vs.read()
(height, width) = frame.shape[:2]


# from multiprocessing import Process
#pio = mvnt.setup(True)


x = 0
while True:
    s, add = server.accept()
    print("Connected from", add)
    frame = vs.read()
    s.sendall(frame)

    # CV2 event handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord("a"):
        break
    elif key == ord("q"):
        break


    # PyGame event handling
    for event in pygame.event.get():
        print('event')
        #     if event.type == MOUSEMOTION:
        #         print('MM'+str(pygame.mouse.get_pos()))
        #         mpos = pygame.mouse.get_pos()
        #         rect.x = mpos[0]
        #         rect.y = mpos[1]
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #
    #     if event.type == KEYDOWN:
    #         print('key down')
    #         key = event.key
    #         if key == pygame.K_UP:
    #             print('key up')
    #             if x == 0:
    #                 mvnt.walk_forward_simple(pio)
    #                 x = 1
    #             elif x == 1:
    #                 mvnt.walk_forward_simple(pio)
    #                 x = 0
    #         elif key == pygame.K_DOWN:
    #             print('key down')
    #             mvnt.walk_backward_simple(pio)
    #         elif key == pygame.K_RIGHT:
    #             print('key right')
    #             mvnt.rotate_cw(pio)
    #         elif key == pygame.K_LEFT:
    #             print('key left')
    #             mvnt.rotate_ccw(pio)
# END while True:

print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()


                    
