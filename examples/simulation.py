import sys, time
sys.path.append("..")

import PyRO
import Joystick as js

robot = PyRO.RobotOpen()
joy1 = js.Joystick()

def test1(rob):
	for x in range(0, 255):
		joy1.set_axis(js.RIGHT_Y, x)
		joy1.set_axis(js.LEFT_Y, x)
		for_time((lambda y: rob.set_joystick(joy1)), t=0.5)
	joy1.states = js.NULL_JOY
	for_time((lambda y: rob.set_joystick(joy1)), t=1)

def test2(rob):
	for x in range(0, 255):
		joy1.set_axis(js.RIGHT_X, x)
		joy1.set_axis(js.LEFT_X, x)
		for_time((lambda y: rob.set_joystick(joy1)), t=0.5)
	joy1.states = js.NULL_JOY
	for_time((lambda y: rob.set_joystick(joy1)), t=1)

def for_time(x, t=1):
    st = time.time()
    while(time.time() - st < t):
        x(time.time())

def main():
	robot.start()
	robot.enable()

	robot.set_parameter(5, 0x00, PyRO.TYPES["b"])

	test1(robot)
	test2(robot)

main()