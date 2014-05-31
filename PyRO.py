"""Module to control RobotOpen protocol supporting devices
without Driver Station while using provided methods
"""

import sys
import socket
import struct
import crcmod
import threading
import time
import signal
import Joystick as js

if sys.version_info[0] > 2:
	from queue import *
else:
	from Queue import *

# Default IP and Port
UDP_IP = "10.0.0.22"
UDP_PORT = 22211

# Packet headers/enders
HEARTBEAT = [0x68, 0xEE, 0x01]
CONTROL = [0x63]
PARAMETER= [0x73]
GET_PARAM = [0x67, 0xEA, 0x41]

# Function object for crc-16 algorithm
CRC16FUN = crcmod.predefined.mkCrcFun('crc-16')

# Dictionaries to lookup datatype and packing format for parameters
TYPES = {"b":0x62, "c":0x63, "i":0x69, "l":0x6C, "f":0x66}
TYPE_DICT = {0x62:'<i', 0x63:'<i', 0x69:'>i', 0x6C:'>i', 0x66:'>f'}
TYPE_DICTc = {"b":'<i', "c":'<i', "i":'>h', "l":'>i', "f":'>f'}

# Necessary in order to work on both python 2 and 3
copy = (lambda x: [i for i in x])

def append_crc16(pack):
	""" Utility function to append crc-16 to UDP packets """
	pack
	c = CRC16FUN(struct.pack('%iB' % len(pack), *pack))
	pack += [c>>8]
	pack += [c&0xFF]

class RobotOpen:
	""" Class to represent RobotOpen device """
	def __init__(self, ip = UDP_IP, port = UDP_PORT):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.queue = Queue()
		self._enabled = False
		signal.signal(signal.SIGINT, self._cc_handle)

	# Thread that runs on start to maintain connection
	def _thread(self):
		while self.started:
			if self._enabled:
				if self.queue.empty():
					self.send_packet(self.assemble_control_packet([js.NULL_JOY]))
				else:
					dat = self.queue.get()
					#print(dat)
					self.send_packet(self.assemble_control_packet(dat))
			else:
				self.send_packet(HEARTBEAT)
			#time.sleep(0.03)
			self.recv_packets(0.1) #100ms

	# handler so thread is killed on ctrl-c
	def _cc_handle(self, signum, frame):
		self.stop()
		raise SystemExit(0)

	def start(self):
		""" starts connection thread """
		self.started = True
		self.t = threading.Thread(target=self._thread)
		self.t.start()

	def stop(self):
		""" salts connection thread and disabled device """
		self.started = False
		self._enabled = False
		self.t.join()

	def enable(self):
		""" enables device """
		self._enabled = True

	def disable(self):
		""" disables device """
		self._enabled = False

	def send_packet(self, pack):
		""" takes array and sends to device """
		self.sock.sendto(struct.pack('%iB' % len(pack), *pack), (self.ip, self.port))

	def recv_packets(self, dt):
		""" recv all packets, in non-blocking mode """
		self.sock.setblocking(0)
		st = time.time()
		while time.time() - st < dt:
			data = []
			try:
				data,addr = self.sock.recvfrom(65535)
			except:  #no data since non-blocking recv()
				break
			if len(data) == 0: 
				break
			else:
				print addr
				self.parseData(data)
		self.sock.setblocking(1)
		
	def set_joystick(self, state):
		""" sends control packet with values passed for joystick """
		self.queue.put([state])

	def assemble_control_packet(self, dat):
		""" formats control packets from dat to be sent over """
		pck = copy(CONTROL)
		try:
			for x in dat:
				try:
					pck += x.states
				except AttributeError:
					pck += x
					pck += [0 for y in range(0,(24-len(x)))]
		except TypeError:
			try:
				pck += dat.states
			except AttributeError:
					pck += dat
					pck += [0 for y in range(0,(24-len(dat)))]
		append_crc16(pck)
		return pck

	def assemble_parameter_packet(self, addr, data):
		""" formats parameter packets from addr and dat to be sent over """
		pck = copy(PARAMETER)
		pck += [addr]
		pck += data
		append_crc16(pck)
		return pck

	def parseData(self, data):
		#print data
		#print ":".join("{:02x}".format(ord(c)) for c in data)
		if data[0] == 'p':
			self.parsePrint(data)
		elif data[0] == 'd':
			self.parseDS(data)
		else:
			print 'TODO:',data[0] #
	def parseDS(self, data):
		data = data[1:]
		name = ''
		num = 0
		while len(data) > 0:
			length = ord(data[0])
			typ = data[1]
			if typ == 'b': #0x62: #'b'
				num = data[2]
				name = data[3:length]
			elif typ == 'c': #0x63: #'c'
				num = data[2]
				name = data[3:length]
			elif typ == 'i': #0x69: #'i'
				num = struct.unpack(TYPE_DICTc[typ], data[2:4])[0]
				name = data[4:length]
			elif typ == 'l': #0x6C: #'l'
				num = struct.unpack(TYPE_DICTc[typ], data[2:6])[0]
				name = data[6:length]
			elif typ == 'f': #0x66: #'f'
				num = struct.unpack(TYPE_DICTc[typ], data[2:6])[0]
				name = data[6:length]
			else:
				print 'TODO-DS'
			print name,"====>", num
			data = data[length:]
	def parsePrint(self, data):
		print 'TODO-print' #
	
	def get_parameter_list(self):
		""" returns list of parameters on device """
		r = [[0]]
		data = 0
		values = []
		self.send_packet(GET_PARAM)
		r = sock.recvfrom(128)
		while r[0][0] != ord('r'):
			self.send_packet(GET_PARAM)
			r = self.sock.recvfrom(128)
			data = r[0][1:]
		while len(data) > 0:
			length = data[0]
			address = data[1]
			typ = data[2]
			num = struct.unpack(TYPE_DICT[typ], data[3:7])[0]
			if typ == 0x69:
				num = num >> 16
			name = "".join([chr(x) for x in data[7:length]])
			values.append([address, typ, num, name])

			data = data[length:]
		return values

	def set_parameter(self, addr, data, typ):
		""" sets parameter at addr, requires type of the parameter """
		data = struct.pack(TYPE_DICT[typ], data)
		if sys.version_info[0] > 2:
			data = [x for x in data]
		else:
			data = [ord(x) for x in data]
		self.send_packet(self.assemble_parameter_packet(addr, data))