import os
import sys
import pygame as pg
import gyro as gy
import math
import numpy as np
from threading import *
         
KEY_REPEAT_SETTING = (200,70)         
POSITON_BUFFER_SIZE = 10         
POSITON_HISTORY_SIZE = 5

class LabelCollection(object):
    def __init__(self):
        self.font = pg.font.SysFont("monospace", 15)
        self.gyro = self.font.render("                                       ", 1, (255,255,0))
        self.pos  = self.font.render("                                       ", 1, (255,255,0))
        self.fps  = self.font.render("                                       ", 1, (255,255,0))        
        

class TboxCollection(object):        
    def __init__(self,lbls):
        self.gyro = lbls.gyro.get_rect()
        self.gyro.x = 10
        self.gyro.y = 100
        
        self.pos = lbls.pos.get_rect()
        self.pos.x = 10        
        self.pos.y = 200
        
        self.fps = lbls.fps.get_rect()
        self.fps.x = 10        
        self.fps.y = 300
        
class Control(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption("Input Box")
        
        self.screen = pg.display.set_mode((500,500))
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
        self.yoffset = 16000;
        self.ybuffer = np.zeros((1,POSITON_BUFFER_SIZE))
        self.yhistory = np.zeros((1,POSITON_HISTORY_SIZE))

        self.gyro = gy.Gyro();
        
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
        self.yhistory = np.roll(self.yhistory,1)
        self.yhistory[0] = np.sum(self.ybuffer) / POSITON_BUFFER_SIZE
        self.y = np.sum(self.yhistory) / POSITON_HISTORY_SIZE
        
    def update_gyro_label(self):
        self.lbls.gyro = self.font.render(("xacc: %5d yacc: %5d zacc: %5d" % (self.gyro.xacc,self.gyro.yacc,self.gyro.zacc)),1,(255,255,255))
        self.screen.blit(self.lbls.gyro, self.tbox.gyro)
    
    def main_loop(self):

        pg.draw.rect(self.screen,(0,0,128), self.rect)
        self.screen.fill(self.color)
        while not self.done:
            self.screen.fill(self.color)
            self.event_loop()
            
            
            self.gyro.get_sample();
            self.update_gyro_label();

            # UPDATE y-position and rectangle position
            self.update_position()            
            #self.rect.move_ip(0,self.y/10);
            #self.rect.y = self.y/10;

            self.lbls.fps = self.font.render(f"fps: {self.clock.get_fps()}",1,(255,255,255))
            self.screen.blit(self.lbls.fps, self.tbox.fps)

            

            pg.display.update((self.tbox.gyro,self.tbox.pos,self.tbox.fps))
            #pg.display.update()            
            self.clock.tick(self.fps)

            

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
