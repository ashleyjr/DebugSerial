#!/usr/bin/python
import sys, os
try:
	import serial
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
		# SELECT PORT
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
					chosen = 0
					break
				else:														# Many Ports, choose
					num_ports = len(ports)
					print('\nMore than 1 serial port found.')
					for i in range(0,num_ports):
						print('%s:   %s' % (i,descs[i]))
					user = ''
					user = raw_input('NUM:')
					if(False == user.isdigit()):
						raise NameError('ChoiceError')
					chosen = int(user)
					if((chosen < 0) or (chosen >= num_ports)):
						raise NameError('ChoiceError')
					else:
						break
			except NameError,ValueError:
				print('Invalid choice')
		# LOAD BAUD RATE
		while(1):
			try:
				f = open("DS_configs.dat", 'r')
				baud = int(f.read())
				f.close()
				print('\nBaud: %s' % baud)
				user = raw_input('Ok? (y/n)')
				if((user == 'y') or (user == 'Y')):
					break
				if((user == 'n') or (user == 'N')):
					f = open("DS_configs.dat", 'w')
					user = raw_input('New Baud: ')
					f.write(user)
					f.close();
					if(user.isdigit() == False):
						print('Invalid input.')
			except:
				f = open("DS_configs.dat", 'w')
				f.write('9600')
				f.close();
		# CONNECT
		try:
			self.ser = serial.Serial(port=ports[chosen],baudrate=baud,bytesize=8,parity='N',stopbits=1,timeout=None,xonxoff=0,rtscts=0)
		except serial.serialutil.SerialException:
			print('Error: Connecting to serial port, exiting...')
			sys.exit(0)
		print("Connected: %s" % self.ser)

	def Send(self,byte):
		self.ser.write(chr(byte))

	def Get(self):
		return int(self.ser.read(1))
