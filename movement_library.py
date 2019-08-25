
import pigpio
import time

verbose = False

actuators = {'legFrontLeft':  {'channel': 18, 'offset': 100},
             'legFrontRight': {'channel': 27, 'offset': 10 },
             'legBackLeft':   {'channel': 17, 'offset': 210},
             'legBackRight':  {'channel': 22, 'offset': 10 }}

startPosition = 1500;
offset = -60;
gaitSwingMag = 100;




def setup(verbosityState=False):
    global verbose
    global actuators
    verbose = verbosityState
    pi = pigpio.pi()
    #for a in actuators.items():
    #        pi.set_mode(actuators[a]['channel'],pigpio.OUTPUT)
    return pi

def rotate_cw(pi):
    global verbose
    if verbose==True:
        print('rotate cw')

def rotate_ccw(pi):
    global verbose
    if verbose==True:
        print('rotate ccw')

def walk_backward_simple(pi,delay=0.3):
    global verbose
    if verbose==True:
        print('walk backward')

def walk_forward_simple(pi,delay=0.3):
    global verbose
    if verbose==True:
        print('walk forward')

    # Standing Position
    for a in actuators.items():
        pi.set_servo_pulsewidth(actuators[a]['channel'], startPosition+offset+actuators[a]['offset'])

        # First half step
        time.sleep(delay)
        pi.set_servo_pulsewidth(actuators['legFrontRight']['channel'],
                                actuators['legFrontRight']['offset'] + startPosition - gaitSwingMag + offset)
        pi.set_servo_pulsewidth(actuators['legBackRight']['channel'],
                                actuators['legBackRight']['offset'] + startPosition + gaitSwingMag + offset)
        pi.set_servo_pulsewidth(actuators['legFrontLeft']['channel'],
                                actuators['legFrontLeft']['offset'] + startPosition - gaitSwingMag + offset)
        pi.set_servo_pulsewidth(actuators['legBackLeft']['channel'],
                                actuators['legBackLeft']['offset'] + startPosition + gaitSwingMag + offset)

        # Second half step
        time.sleep(delay)
        pi.set_servo_pulsewidth(actuators['legFrontRight']['channel'],
                                actuators['legFrontRight']['offset'] + startPosition + gaitSwingMag + offset)
        pi.set_servo_pulsewidth(actuators['legBackRight']['channel'],
                                actuators['legBackRight']['offset'] + startPosition - gaitSwingMag + offset)
        pi.set_servo_pulsewidth(actuators['legFrontLeft']['channel'],
                                actuators['legFrontLeft']['offset'] + startPosition + gaitSwingMag + offset)
        pi.set_servo_pulsewidth(actuators['legBackLeft']['channel'],
                                actuators['legBackLeft']['offset'] + startPosition - gaitSwingMag + offset)

    # Return to original position (testing purposes only)
    for a in actuators.items():
        pi.set_servo_pulsewidth(actuators[a]['channel'],
                                actuators[a]['offset'] + startPosition + offset)
        time.sleep(delay);
# END def walk_forward_simple
