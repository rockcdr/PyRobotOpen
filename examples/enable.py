"""
Example of how to use PyRO
Enables device and sends over
joystick data for right stick
at 50 and right shoulder button
being depressed
"""
import sys, time
sys.path.append("..")

import PyRO
import Joystick as js
robot = PyRO.RobotOpen()
joy1 = js.Joystick()

def for_time(x, t=1):
    st = time.time()
    while(time.time() - st < t):
        x(time.time())
        #time.sleep(0.03)
        
def testX(rob, dx):
    joy1.clear_states()
    dx1 = 1
    if dx < 0 :
        dx1 = -1
    for x in range(127, 127+dx, dx1):
        joy1.set_axis(js.LEFT_X, x)
        for_time((lambda y: rob.set_joystick(joy1)), t=0.2)
    joy1.clear_states()
    for_time((lambda y: rob.set_joystick(joy1)), t=1)

def test(rob, axis, dx, dt):
    joy1.clear_states()
    joy1.set_axis(axis, 127+dx)#127
    #print joy1.get_states()
    for_time((lambda y: rob.set_joystick(joy1)), t=dt)
    
robot.start()
robot.enable()
time.sleep(1)  #wait device ready
#joy1.set_axis(js.RIGHT_Y, 50)
#joy1.set_button(js.RIGHT_SHOULDER, js.ON)

#while 1:
#robot.set_joystick(joy1)

#testX(robot, -100)
#testX(robot, 100)

#test(robot, js.LEFT_X, -70, 2)
#test(robot, js.LEFT_X, 70, 2)  #??
#test(robot, js.LEFT_Y, -43, 5)
#test(robot, js.LEFT_Y, 43, 5)

robot.disable()
robot.stop()
