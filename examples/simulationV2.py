import sys, time, argparse
sys.path.append("..")
import PyRO
import Joystick as js

def for_time(x, t=1):
    st = time.time()
    while(time.time() - st < t):
        x(time.time())

def main():
	parser = argparse.ArgumentParser(description='RobotOpen Sim')
	
	parser.add_argument('-v','--vel', help='Velocity', required=True)
	parser.add_argument('-r','--rot', help='Rotation', required=True)

	args = vars(parser.parse_args())

	robot = PyRO.RobotOpen()

	robot.start()
	robot.enable()

	robot.set_parameter(5, 0x00, PyRO.TYPES["b"])

	v = int(args['vel'])
	r = int(args['rot'])
	print(v, r)
	joy1 = js.Joystick()
	joy1.set_axis(js.RIGHT_Y, v)
	joy1.set_axis(js.LEFT_Y, v)
	joy1.set_axis(js.RIGHT_X, r)
	joy1.set_axis(js.LEFT_X, r)

	for_time((lambda y: robot.set_joystick(joy1)), t=5)
	joy1.clear_states()
	for_time((lambda y: robot.set_joystick(joy1)), t=1)

	robot.stop()

main()