import os
import sys
import pygame as pg
import gyro2 as gy
import math
import numpy as np
from threading import *

import pigpio
pi = pigpio.pi()




         
KEY_REPEAT_SETTING = (200,70)         
POSITON_BUFFER_SIZE = 8         
POSITON_HISTORY_SIZE = 4

class LabelCollection(object):
    def __init__(self):
        self.font = pg.font.SysFont("monospace", 15)
        self.acc  = self.font.render("                                                    \
                                                                             ", 1, (255,255,255),(0,0,0))
        self.gyr  = self.font.render("                                                    \
                                                                             ", 1, (255,255,255),(0,0,0))
        self.pos  = self.font.render("                                                    \
                                                                             ", 1, (255,255,255),(0,0,0))
        self.rot  = self.font.render("                                                    \
                                                                             ", 1, (255,255,255),(0,0,0))
        self.fps  = self.font.render("                                       ", 1, (255,255,255),(0,0,0))
        

class TboxCollection(object):        
    def __init__(self,lbls):
        self.acc = lbls.acc.get_rect()
        self.acc.x = 10
        self.acc.y = 100
        
        self.gyr = lbls.gyr.get_rect()
        self.gyr.x = 10
        self.gyr.y = 150
        
        self.rot = lbls.rot.get_rect()
        self.rot.x = 10
        self.rot.y = 200
        
        self.pos = lbls.pos.get_rect()
        self.pos.x = 10        
        self.pos.y = 250
        
        self.fps = lbls.fps.get_rect()
        self.fps.x = 10        
        self.fps.y = 300



class Control(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption("Input Box")
        
        self.screen = pg.display.set_mode((1000,500))
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.color = (0,0,0)
        pg.key.set_repeat(*KEY_REPEAT_SETTING)
        
        self.font = pg.font.SysFont("monospace", 15)

        self.lbls = LabelCollection()
        self.tbox = TboxCollection(self.lbls)
        
        self.rect = pg.Rect((50,50,150,50));

        self.y = 0;
        self.yoffset = 16000
        self.ybuffer = np.zeros((1,POSITON_BUFFER_SIZE))
        self.yhistory = np.zeros((1,POSITON_HISTORY_SIZE))
        self.yind = 0;
        
        self.y = 0;
        self.yoffset = 16000
        self.ybuffer = np.zeros((1,POSITON_BUFFER_SIZE))
        self.yhistory = np.zeros((1,POSITON_HISTORY_SIZE))
        self.yind = 0;

        self.gyro = gy.Gyro();
        
        self.pwm = 0
        
    def event_loop(self):
        for event in pg.event.get():
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.y = 0;
                if event.key == pg.K_RIGHT:
                    self.rect.x = 0
                    self.rect.y = 0
                    pg.draw.rect(self.screen,(0,0,128), self.rect)                    

                if event.key == pg.K_UP:
                    self.yoffset += 100
                if event.key == pg.K_DOWN:
                    self.yoffset -= 100
                    
            if event.type == pg.QUIT:
                self.done = True


    def change_color(self,id,color):
        try:
            self.color = pg.Color(str(color))
        except ValueError:
            print("Please input a valid color name.")
            
    def update_position(self):
        for i in range(0,POSITON_BUFFER_SIZE-1):
            self.gyro.get_sample()
            self.ybuffer[0,i] = self.y + self.gyro.yacc - self.yoffset;
        #self.yhistory = np.roll(self.yhistory,1)
        self.yind = ( self.yind+1, 0 ) [ self.yind+1 == POSITON_HISTORY_SIZE ]        
        self.yhistory[self.yind] = np.sum(self.ybuffer) / POSITON_BUFFER_SIZE
        self.y = np.sum(self.yhistory) / POSITON_HISTORY_SIZE
        
    def update_gyro(self):
        #for i in range(0,POSITON_BUFFER_SIZE-1):
        #    self.gyro.get_sample()
        #    self.ybuffer[0,i] = self.gyro.yrot;
        #self.yind = ( 0, self.yind+1 ) [ self.yind+1 == POSITON_HISTORY_SIZE ]
        #self.yhistory[self.yind] = np.sum(self.ybuffer) / POSITON_BUFFER_SIZE
        #self.y = np.sum(self.yhistory) / POSITON_HISTORY_SIZE
        self.y = self.gyro.yrot
        
    def update_gyro_label(self):
        self.lbls.acc = self.font.render((f"xacc: {self.gyro.acc[0]:.5f} yacc: {self.gyro.acc[1]:.5f} zacc: {self.gyro.acc[2]:.5f}"),1,(255,255,255),(0,0,0))
        self.screen.blit(self.lbls.acc, self.tbox.acc)
        self.lbls.gyr = self.font.render((f"xgyr: {self.gyro.gyr[0]:.5f} ygyr: {self.gyro.gyr[1]:.5f} zgyr: {self.gyro.gyr[2]:.5f}"),1,(255,255,255),(0,0,0))
        self.screen.blit(self.lbls.gyr, self.tbox.gyr)
        self.lbls.rot = self.font.render((f"xrot: {self.gyro.xrot:.5f} yrot: {self.gyro.yrot:.5f} zrot: {self.gyro.zrot:.5f} "),1,(255,255,255),(0,0,0))
        self.screen.blit(self.lbls.rot, self.tbox.rot)
    
    def main_loop(self):

        self.screen.fill(self.color)
        pg.draw.rect(self.screen,(0,0,128), self.rect)        
        while not self.done:
            self.screen.fill(self.color)
            self.event_loop()
            pg.draw.rect(self.screen,(0,0,128), self.rect)        
            
            self.gyro.get_sample();
            self.update_gyro_label();

            self.pwm = (self.y/(math.pi/2))*1000+1500

            self.lbls.fps = self.font.render(f"fps: {self.clock.get_fps()}",1,(255,255,255),(0,0,0))
            self.screen.blit(self.lbls.fps, self.tbox.fps)
            #self.lbls.pos = self.font.render(f"pos: {self.y}",1,(255,255,255))
            self.lbls.pos = self.font.render(f"pos: {self.pwm}",1,(255,255,255),(0,0,0))
            self.screen.blit(self.lbls.pos, self.tbox.pos)
            
            pg.display.update((self.tbox.acc,self.tbox.gyr,self.tbox.rot,self.tbox.pos,self.tbox.fps))
            #pg.display.update()
            
            self.clock.tick(self.fps)
            
            # UPDATE y-position and rectangle position
            #self.update_position()
            self.update_gyro()
            #self.rect.move_ip(0,self.y/10);
            #self.rect.y = self.y/10;
            pi.set_servo_pulsewidth(18,self.pwm)

            

if __name__ == "__main__":
    app = Control()
    app.main_loop()
    pg.quit()
    sys.exit()

#print("Gyroscope")
#print("---------")

#print("gyroscope_xout: ", ("%5d" % gyroscope_xout), " scaled: ", (gyroscope_xout / 131))
#print("gyroscope_yout: ", ("%5d" % gyroscope_yout), " scaled: ", (gyroscope_yout / 131))
#print("gyroscope_zout: ", ("%5d" % gyroscope_zout), " scaled: ", (gyroscope_zout / 131))

#print()
#print("Accelerometer")
#print("-------------")


#print("acc_xout: ", ("%6d" % acc_xout), " scaled: ", (acc_xout_sc))
#print("acc_yout: ", ("%6d" % acc_yout), " scaled: ", (acc_yout_sc))
#print("acc_zout: ", ("%6d" % acc_zout), " scaled: ", (acc_zout_sc))
      
#print("X Rotation: ", get_x_rotation(acc_xout_sc,acc_yout_sc,acc_zout_sc))
#print("Y Rotation: ", get_y_rotation(acc_xout_sc,acc_yout_sc,acc_zout_sc))
