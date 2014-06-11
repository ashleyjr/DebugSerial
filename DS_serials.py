#!/usr/bin/python
import sys, os, curses, threading
try:
	import serial
except ImportError:
	print('\nError: PySerial not found, exiting...')
	sys.exit(0)


class _Getch:
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self):
		return self.impl()

class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()



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


	def terminal(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print('Terminal mode: Press F1 to exit')
		self.async = 1
		rx = threading.Thread(target=self.asyncRx)
		tx = threading.Thread(target=self.asyncTx)
		rx.start()
		tx.start()
		rx.join()
		tx.join()

	def asyncRx(self):
		while(self.async == 1):
			sys.stdout.write(self.ser.read(self.ser.inWaiting() + 1))

	def asyncTx(self):
		char = _Getch()
		while(1):
			user = char()
			self.ser.write(user)
			if(user == 'q'):
				break
		self.async = 0














