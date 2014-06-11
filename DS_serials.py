#!/usr/bin/python
from __future__ import curses
import sys, os, curses, threading, time, locale

try:
	import serial
except ImportError:
	print('\nError: PySerial not found, exiting...')
	sys.exit(0)


# Cross platform grab character
class Getch:
	def __init__(self):
		try:
			self.impl = GetchWindows()
		except ImportError:
			self.impl = GetchUnix()
	def __call__(self):
		return self.impl()
class GetchUnix:
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
class GetchWindows:
	def __init__(self):
		import msvcrt
	def __call__(self):
		import msvcrt
		return msvcrt.getch()


# Deal with serial port
class Serial:
	def __init__(self):
		# IMPORT STUFF
		try:
			import serial
			from serial.tools.list_ports import comports
		except ImportError:
			print('\nError: PySerial not found, exiting...')
			sys.exit(0)
		self.char = Getch()
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
				sys.stdout.write('Ok? (y/n)')
				user = self.char()
				if((user == 'y') or (user == 'Y')):
					break
				if((user == 'n') or (user == 'N')):
					f = open("DS_configs.dat", 'w')
					user = raw_input('New Baud: ')
					f.write(user)
					f.close();
					if(user.isdigit() == False):
						print('Invalid input.')
			except:									# Overwrite with a default
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


		term = curses.initscr()
		curses.noecho()
		while(1):
			term.addch(curses.KEY_F1)
			user = term.get_wch()
			term.addch(user)
			print unichr(user)
			print curses.KEY_F1
			if(user == curses.KEY_F1):
				break
			term.refresh()
		curses.endwin()
#		#curses.noecho()
#		#curses.echo()
#		begin_x = 20
#		begin_y = 7
#		height = 5
#		width = 40
#		win = curses.newwin(10,10)
#		tb = curses.textpad.Textbox(win)
#		text = tb.edit()
#		curses.addstr(4,1,text.encode('utf_8'))
#
#		for y in range(0, 100):
#			for x in range(0, 100):
#				try:
#					tb.addch(y,x, ord('a') + (x*x+y*y) % 26)
#				except curses.error:
#					pass
#
#

		#self.async = 1
		#rx = threading.Thread(target=self.asyncRx)
		#rx.start()


		#rx.join()

	def asyncRx(self):
		while(self.async == 1):
			sys.stdout.write(self.ser.read(1))
			sys.stdout.flush()

	def asyncTx(self):
		while(1):
			stdscr = curses.initscr()
			#curses.noecho()
			#curses.echo()
			begin_x = 20
			begin_y = 7
			height = 5
			width = 40
			win = curses.newwin(height, width, begin_y, begin_x)
			tb = curses.textpad.Textbox(win)
			text = tb.edit()
			curses.addstr(4,1,text.encode('utf_8'))
			user = self.char()
			print user
			test = ord(user)
			if((test >= 0) and (test <= 255)):
				self.ser.write(user)
			else:
				print "Invalid Tx"
			if(user == "q"):
				break
			#sys.stdout(unicode(user))
			if(user == "\x1bOP"):
				break
		self.async = 0






