import time
import pigpio

pi = pigpio.pi()

pi.set_servo_pulsewidth(18,2500)
time.sleep(0.5)
pi.set_servo_pulsewidth(18,500)
time.sleep(0.5)
pi.set_servo_pulsewidth(18,2500)
time.sleep(0.5)
pi.set_servo_pulsewidth(18,1500)
time.sleep(0.5)
