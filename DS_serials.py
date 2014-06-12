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
		startBAUD = 100								# Warning dynamic update to persist
		BAUD = startBAUD							# Redundancy required for persistence
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

	def radix(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Radix Mode:")
		self.async = 1
		rx = threading.Thread(target=self.asyncRxRadix)
		tx = threading.Thread(target=self.asyncTx)
		rx.start()
		tx.start()
		rx.join()
		tx.join()

	def terminal(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Terminal Mode:")
		self.async = 1
		rx = threading.Thread(target=self.asyncRxTerm)
		tx = threading.Thread(target=self.asyncTx)
		rx.start()
		tx.start()
		rx.join()
		tx.join()

	def asyncRxTerm(self):
		while(self.async == 1):
			sys.stdout.write(self.humanRead(self.ser.read(1)))
			sys.stdout.flush()
		print("\n\n")


	def zeroPad(self,s,length):
		while(len(s) < length):
			s = "0" + s
		return(s)

	def asyncRxRadix(self):
		sys.stdout.write("\n\rDEC     HEX     BIN          ASCII")
		while(self.async == 1):
			char = self.ser.read(1)
			data = ord(char)
			s = "{0:d}".format(data)
			s = self.zeroPad(s,3)
			h = "{0:x}".format(data)
			h = self.zeroPad(h,2)
			s = s + "   	" + h.upper()
			b = "{0:b}".format(data)
			b = self.zeroPad(b,8)
			s = s + "      " + b + "     " + self.humanRead(char)
			sys.stdout.write("\n\r%s" % s)
			sys.stdout.flush()
		print("\n\n")

	def asyncTx(self):
		state = 0
		f1 = [27,79,80]
		buff3 = [0,0,0]
		while(self.async == 1):
			user = self.char()
			test = ord(user)
			if(state == 0):
				buff3[0] = test
				state = 1
			elif(state == 1):
				buff3[1] = test
				state = 2
			else:
				buff3[2] = test
				state = 0
			shift = buff3
			for i in range(3):
				temp = shift[0]
				shift[0] = shift[1]
				shift[1] = shift[2]
				shift[2] = temp
				if(shift == f1):
					self.async = 0
			if((test >= 0) and (test <= 255)):
				self.ser.write(user)


	def humanRead(self,char):
		data = ord(char)
		if(data == 0):
			return "<Null char>"
		elif(data == 1):
			return "<datatart of Heading>"
		elif(data == 2):
			return "<Start of Text>"
		elif(data == 3):
			return "<End of Text>"
		elif(data == 4):
			return "<End of Transmission>"
		elif(data == 5):
			return "<Enquiry>"
		elif(data == 6):
			return "<Acknowledgment>"
		elif(data == 7):
			return "<Bell>"
		elif(data == 8):
			return "<Back Space>"
		elif(data == 9):
			return "<Horizontal Tab>"
		elif(data == 10):
			return "<Line Feed>"
		elif(data == 11):
			return "<Vertical Tab>"
		elif(data == 12):
			return "<Form Feed>"
		elif(data == 13):
			return "\n\r"	#"<Carriage Return>"
		elif(data == 14):
			return "<Shift Out / X-On>"
		elif(data == 15):
			return "<Shift In / X-Off>"
		elif(data == 16):
			return "<Data Line Escape>"
		elif(data == 17):
			return "<Device Control 1 (oft. XON)>"
		elif(data == 18):
			return "<Device Control 2>"
		elif(data == 19):
			return "<Device Control 3 (oft. XOFF)>"
		elif(data == 20):
			return "<Device Control 4>"
		elif(data == 21):
			return "<Negative Acknowledgement>"
		elif(data == 22):
			return "<Synchronous Idle>"
		elif(data == 23):
			return "<End of Transmit Block>"
		elif(data == 24):
			return "<Cancel>"
		elif(data == 25):
			return "<End of Medium>"
		elif(data == 26):
			return "<Substitute>"
		elif(data == 27):
			return "<Escape>"
		elif(data == 28):
			return "<File Separator>"
		elif(data == 29):
			return "<Group Separator>"
		elif(data == 30):
			return "<Record Separator>"
		elif(data == 31):
			return "<Unit Separator>"
		elif(data == 32):
			return " "#"<Space>"
		elif(data == 127):
			return "\b"
		else:
			if((data > 255) or (data < 0)):
				print("Invalid!")
				sys.exit(0)
			else:
				return char




