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
		# LOAD SETTINGS FILE
		name = list()
		name.append("  Baudrate")
		name.append("      Bits")
		name.append("  StopBits")
		name.append("   TimeOut")
		name.append("    Parity")
		name.append("   XonXoff")
		name.append("    Rtscts")
		while(1):
			try:
				f = open("DS_configs.dat", 'r')
				settings = f.read().split(',')
				f.close()
				if(len(settings) != 7):
					print('Settings corrupt.')
					os.remove("DS_configs.dat")
					raise NameError('SettingsError')
				else:
					if(settings[0].isdigit()):
						baud = int(settings[0])
					else:
						raise NameError('SettingsError')
					print('Settings:')
					for i in range(0,6):
						print("%s: %s"% (name[i],settings[i]))
					user = raw_input('OK? (y/n):')
					if((user == 'n') or (user == 'N')):
						for i in range(0,4):
							print i
							while(1):
								settings[i] = raw_input("%s: " % name[i])
								if(settings[i].isdigit()):
									break
								else:
									print('Error: Must be an integer.')
						settings[4] = raw_input("%s: " % name[4])
						settings[5] = raw_input("%s: " % name[5])
						settings[6] = raw_input("%s: " % name[6])
					if((user == 'y') or (user == 'Y')):
						break
					f = open("DS_configs.dat", 'w')
					f.write('%s,%s,%s,%s,%s,%s,%s' % (settings[0],settings[1],settings[2],settings[3],settings[4],settings[5],settings[6]))
					f.close()
			except IOError,NameError:										# Config file is missing or corrupt
				print('Creating new settings file.')
				f = open("DS_configs.dat", 'w')
				f.write('9600,8,None,1,None,0,0')
				f.close();
		# CONNECT
		try:
			self.ser = serial.Serial(port=ports[chosen],baudrate=baud,bytesize=8,parity='N',stopbits=1,timeout=None,xonxoff=0,rtscts=0)
		except serial.serialutil.SerialException:
			print('Error: Connecting to serial port, exiting...')
			sys.exit(0)
		self.ser.write("sup")
