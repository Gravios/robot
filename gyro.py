#!/usr/bin/python3
import smbus
import math

# Register
POWER_MGMT_1 = 0x6b
POWER_MGMT_2 = 0x6c

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

class Gyro(object):
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x68        
        self.bus.write_byte_data(self.address, POWER_MGMT_1, 0)
        self.xacc = 0
        self.yacc = 0
        self.zacc = 0
        self.xgyr = 0
        self.ygyr = 0
        self.zgyr = 0
        self.xgyrScale = 0
        self.ygyrScale = 0
        self.zgyrScale = 0
        self.xaccScale = 0
        self.yaccScale = 0
        self.zaccScale = 0
        
    def read_byte(self,reg):
        return self.bus.read_byte_data(self.addresss,reg)
    
    def read_word(self,reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        value = (h << 8) + l
        return value
    
    def read_word_2c(self,reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    def get_sample(self):
        self.xgyr = self.read_word_2c(0x43)
        self.ygyr = self.read_word_2c(0x45)
        self.zgyr = self.read_word_2c(0x47)
        self.xgyrScale = self.xgyr / 131
        self.ygyrScale = self.ygyr / 131
        self.zgyrScale = self.zgyr / 131
        self.xacc = self.read_word_2c(0x3b)
        self.yacc = self.read_word_2c(0x3d)
        self.zacc = self.read_word_2c(0x3f)
        self.xaccScale = self.xacc / 16384.0
        self.yaccScale = self.yacc / 16384.0
        self.zaccScale = self.zacc / 16384.0
        self.compute_y_rotation()
        self.compute_x_rotation()
    
    def compute_y_rotation(self):
        self.yrot = math.atan2(self.xaccScale, dist(self.yaccScale,self.zaccScale))
    
    def compute_x_rotation(self):
        self.xrot = math.atan2(self.yaccScale, dist(self.xaccScale,self.zaccScale))

 
