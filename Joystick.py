ON = 0xFF
OFF = 0x00

NULL_JOY = [127,127,127,127,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

LEFT_X = 0
LEFT_Y = 1
RIGHT_X = 2
RIGHT_Y = 3

BUTTON_A = 4
BUTTON_B = 5
BUTTON_X = 6
BUTTON_Y = 7

LEFT_SHOULDER = 8
RIGHT_SHOULDER = 9

LEFT_TRIGGER = 10
RIGHT_TRIGGER = 11

SELECT = 12
START = 13

LEFT_STICK_BUTTON = 14
RIGHT_STICK_BUTTON = 15

DPAD_UP = 16
DPAD_DOWN = 17
DPAD_LEFT = 18
DPAD_RIGHT = 19

AUX1 = 20
AUX2 = 21
AUX3 = 22
AUX4 = 23

class Joystick:
	def __init__(self, dat=NULL_JOY):
		self.states = dat

	def set_sticks(self, lx, ly, rx, ry):
		self.states[0:3] = [lx, ly, rx, ry]

	def set_axis(self, axis, val):
		self.states[axis] =  val

	def set_button(self, but, state):
		self.states[but] = state

	def set_aux(self, aux, val):
		self.states[aux] = val

	def get_states(self):
		return self.states

	def clear_states(self):
		self.states = NULL_JOY