#!/usr/bin/python
import sys, os
try:
	import serial
	from serial.tools.list_ports import comports
except ImportError:
	print('\nError: PySerial not found, exiting...')
	sys.exit(0)


class Serial:
	def __init__(self):
		# IMPORT STUFF
		try:
			import serial
			from serial.tools.list_ports import comports
		except ImportError:
			print('\nError: PySerial not found, exiting...')
			sys.exit(0)
		# USER SLECTS PORT
		while(1):
			try:
				ports = list()
				descs = list()
				for port,desc,hwid in comports():
					ports.append(port)
					descs.append(desc)
				if(len(descs) == 0):										# NO Ports
					print('\nError: No serial ports found, exiting...')
					sys.exit(0)
				elif(len(descs) == 1):										# One Port
					print('\nConnecting to only available serial port.')
					print('   %s' % descs[0])
					chosen = ports[0]
					break
				else:														# Many Ports, choose
					num_ports = len(ports)
					print('\nMore than 1 serial port found.')
					for i in range(0,num_ports):
						print('%s:   %s' % (i,descs[i]))
					user = ''
					user = input('NUM:')
					chosen = int(user)
					if((chosen < 0) or (chosen >= num_ports)):
						raise NameError('ChoiceError')
					else:
						break
			except NameError,ValueError:
				print('Invalid choice')
		# LOAD SETTINGS FILE
		try:
			f = open("DS_configs.dat", 'r')
			contents = f.read()
			if((contents.count('\n') > 1) or (contents.count(',') > 6)):
				print('Settings corrupt')
				raise NameError('SettingsError')
		except:									# Config file is missing or corrupt
			f = open("DS_configs.dat", 'w')
			f.write('9600,8,None,1,None,0,0')
		# CONNECT
		try:
			self.ser = serial.Serial(port=ports[chosen],baudrate=9600,bytesize=8,parity='N',stopbits=1,timeout=None,xonxoff=0,rtscts=0)
		except serial.serialutil.SerialException:
			print('Error: Connecting to serial port, exiting...')
			sys.exit(0)
		self.ser.write("sup")
