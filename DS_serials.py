#!/usr/bin/python
import sys
try:
	import serial
	from serial.tools.list_ports import comports
except ImportError:
	print('\nError: PySerial not found, exiting...')
	sys.exit(0)


class Serial:
	def __init__(self):
		ports = list()
		descs = list()
		for port,desc,hwid in comports():
			ports.append(port)
			descs.append(desc)
		if(len(descs) > 1):
			print('More than 1 serial port found.')
			for i in range(0,len(ports)):
				print('   %s' % descs[i])
			self.connect(ports[1],9600,8,1,serial.PARITY_NONE,0)
		else:
			print('Connecting to only available serial port.')
			print('   %s' % descs[1])
	def connect(self,p,bd,bs,p,s,t,parity,rtscts):
		try:
			self.ser = serial.Serial(com,baudrate,bytesize,timeout,parity,rtscts)
		except serial.serialutil.SerialException:
			print('Error: Connecting to serial port, exiting...')
			sys.exit(0)

