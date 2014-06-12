#!/usr/bin/python
import sys, os, fileinput, threading

# PySerial needs to be installed
try:
	import serial
	from serial.tools.list_ports import comports
except ImportError:
	print('\nError: PySerial not found, exiting...')
	sys.exit(0)

# Cross platform grab character
class Getch:
	def __init__(self):
		try:				self.impl = GetchWindows()
		except ImportError:	self.impl = GetchUnix()
	def __call__(self):
		return self.impl()
class GetchUnix:
	def __init__(self):
		import tty
	def __call__(self):
		import tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
class GetchWindows:
	def __init__(self):
		import msvcrt
	def __call__(self):
		import msvcrt
		return msvcrt.getch()


# Deal with serial port
class Serial:
	def __init__(self):
		self.char = Getch()

		# SELECT PORT
		while(1):
			try:
				ports = list()
				descs = list()
				for port,desc,hwid in comports():
					ports.append(port)
					descs.append(desc)
				if(len(descs) == 0):										# No Ports
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
					user = raw_input('\nNUM:')
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
		startBAUD = 1234567								# Warning dynamic update to persist
		BAUD = startBAUD
		while(1):
			print('\nBaud: %s' % BAUD)
			sys.stdout.write('Ok? [y/n]')
			user = self.char()
			if((user == 'y') or (user == 'Y')):
				break
			if((user == 'n') or (user == 'N')):
				user = raw_input('\nNew Baud: ')
				if(user.isdigit() == False):
					print('Invalid input.')
				else:
					BAUD = int(user)
		for line in fileinput.input('DS_serials.py', inplace=True):		# Dynamic updaate
			old = ("startBAUD = %s" % startBAUD)
			new = ("startBAUD = %s" % BAUD)
			print line.replace(old, new),


		# CONNECT - Don't care about other parameters, standard
		try:
			self.ser = serial.Serial(port=ports[chosen],baudrate=BAUD,bytesize=8,parity='N',stopbits=1,timeout=None,xonxoff=0,rtscts=0)
		except serial.serialutil.SerialException:
			print('Error: Connecting to serial port, exiting...')
			sys.exit(0)
		print("Connected: %s" % self.ser)

	def terminal(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Terminal Mode:")
		self.async = 1
		rx = threading.Thread(target=self.asyncRx)
		tx = threading.Thread(target=self.asyncTx)
		rx.start()
		tx.start()
		rx.join()
		tx.join()

	def asyncRx(self):
		while(self.async == 1):
			sys.stdout.write(self.ser.read(1))
			sys.stdout.flush()

	def asyncTx(self):
		while(1):
			user = self.char()
			test = ord(user)
			if((test >= 0) and (test <= 255)):
				self.ser.write(user)
			if(user == 'q'):
				break
		self.async = 0






