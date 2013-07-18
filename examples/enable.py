"""
Example of how to use PyRO
Enables device and sends over
joystick data for right stick
at 50 and right shoulder button
being depressed
"""
import sys
sys.path.append("..")

import PyRO
import Joystick as js
robot = PyRO.RobotOpen()
joy1 = js.Joystick()

robot.start()
robot.enable()

joy1.set_axis(js.RIGHT_Y, 50)
joy1.set_button(js.RIGHT_SHOULDER, js.ON)

while 1:
	robot.set_joystick(joy1)