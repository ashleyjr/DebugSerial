#!/usr/bin/python
import serial, sys, os, fileinput, threading
from serial.tools.list_ports import comports
from strings import *
from graphs import *

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
		startBAUD = 57600								# Warning dynamic update to persist
		BAUD = startBAUD							# Redundancy required for persistence
		while(1):
			print('\nBaud: %s' % BAUD)
			if(yesno("OK?")):
				break
			else:
				user = raw_input('\nNew Baud: ')
				if(user.isdigit() == False):
					print('Invalid input.')
				else:
					BAUD = int(user)
		for line in fileinput.input('serials.py', inplace=True):		# Dynamic updaate
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


	def menu(self):
		if(yesno('Terminal')):
			self.terminal()
		elif(yesno('Radix')):
			self.radix()
		elif(yesno('Terminal')):
			self.graph()


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



	def graph(self):
		self.g = Graph(2048)
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Graph Mode:")
		self.async = 1
		rx = threading.Thread(target=self.asyncRxGraph)
		tx = threading.Thread(target=self.asyncTx)
		rx.start()
		tx.start()
		self.g.update()
		rx.join()
		tx.join()

	def asyncRxTerm(self):
		while(self.async == 1):
			sys.stdout.write(humanRead(self.ser.read(1),1))
			sys.stdout.flush()
		print("\n\n")


	def asyncRxRadix(self):
		sys.stdout.write("\n\rDEC     HEX     BIN          ASCII")
		while(self.async == 1):
			char = self.ser.read(1)
			data = ord(char)
			s = "{0:d}".format(data)
			s = zeroPad(s,3)
			h = "{0:x}".format(data)
			h = zeroPad(h,2)
			s = s + "   	" + h.upper()
			b = "{0:b}".format(data)
			b = zeroPad(b,8)
			s = s + "      " + b + "     " + humanRead(char,0)
			sys.stdout.write("\n\r%s" % s)
			sys.stdout.flush()
		print("\n\n")

	def asyncRxGraph(self):
		sys.stdout.write("\n\rDEC     HEX     BIN          ASCII")
		while(self.async == 1):
			char = self.ser.read(1)
			data = ord(char)
			s = "{0:d}".format(data)
			s = zeroPad(s,3)
			h = "{0:x}".format(data)
			h = zeroPad(h,2)
			s = s + "   	" + h.upper()
			b = "{0:b}".format(data)
			b = zeroPad(b,8)
			s = s + "      " + b + "     " + humanRead(char,0)
			sys.stdout.write("\n\r%s" % s)
			sys.stdout.flush()
			self.g.new(data)
		self.g.kill()
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


