#!/usr/bin/python3
import smbus
import math
import numpy as np

# Register
POWER_MGMT_1 = 0x6b
POWER_MGMT_2 = 0x6c
BCA_SIZE = 8;

def dist(a,b):
    return math.sqrt((a**2)+(b**2))

class Gyro(object):
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x68        
        self.bus.write_byte_data(self.address, POWER_MGMT_1, 0)
        self.acc = np.array([0,0,0])
        self.gyr = np.array([0,0,0])
        self.gyrScale = np.array([0,0,0])
        self.accScale = np.array([0,0,0])
        self.xrot = np.array([0])
        self.yrot = np.array([0])
        self.zrot = np.array([0])        

    def read_byte(self,reg):
        return self.bus.read_byte_data(self.address,reg)
    
    def read_word(self,reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        return (h << 8) + l
    
    def read_word_2c(self,reg):
        val = self.read_word(reg)
        return ( val,  -((65535 - val) + 1) ) [val >= 0x8000]

    def read_block_2c(self,reg):
        data = np.array([0,0,0])
        block = np.array(self.bus.read_i2c_block_data(self.address,reg,6)).reshape((3,2))
        for k in range(0,3):
            data[k] = (block[k,0] << 8) + block[k,1]
            data[k] = (data[k],  -((65535 - data[k]) + 1) ) [data[k] >= 0x8000]
        return data
    
    def get_sample(self):
        self.gyr = (self.gyr*(BCA_SIZE-1)+self.read_block_2c(0x43))/BCA_SIZE
        self.gyrScale = self.gyr / 131
        self.acc = (self.acc*(BCA_SIZE-1)+self.read_block_2c(0x3b))/BCA_SIZE        
        self.accScale = self.acc / 16384.0;
        self.compute_y_rotation()
        self.compute_x_rotation()
        self.compute_z_rotation()        
    
    def compute_y_rotation(self):
        self.yrot = math.atan2(self.accScale[0], dist(self.accScale[1],self.accScale[2]))
    
    def compute_x_rotation(self):
        self.xrot = math.atan2(self.accScale[1], dist(self.accScale[0],self.accScale[2]))

    def compute_z_rotation(self):
        self.zrot = math.atan2(self.accScale[2], dist(self.accScale[0],self.accScale[1]))
        
 
