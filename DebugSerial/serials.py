#!/usr/bin/python
import serial, sys, os, threading
from Tkinter import *
from serial.tools.list_ports import comports
from strings import *
from graphs import *

DAT = "DebugSerial.dat"

class Serial:
	def __init__(self):
		self.char = Getch()								# Char handler
		self.gotBaud = False
		self.gotCom = False
		self.Baud = 0
		self.Com = 0
		try:
			f = open(DAT,'r+')
			data = f.read().split(",")
			if(len(data) != 2):
				raise NameError('Corrupt data file')
			self.Baud = int(data[0])
			self.Com = int(data[1])
		except:											# Covers not digits too
			f = open(DAT,'w')
			f.write("9600,0")
			f.close()




	def baud(self,b):
		try:
			if(False == b.isdigit()):
				raise NameError('ChoiceError')
			user = int(b)
			if(user < 0):
				raise NameError('ChoiceError')
			self.baud = user
		except:
			print("Invalid com!")
			sys.exit(0)
		self.gotBaud = True


	def com(self,c):
		try:
			ports = list()
			for port,desc,hwid in comports():
				ports.append(port)
			if(False == c.isdigit()):
				raise NameError('ChoiceError')
			user = int(c)
			if((user < 0) or (user >= len(ports))):
				raise NameError('ChoiceError')
			self.com = user
		except:
			print("Invalid com!")
			sys.exit(0)
		self.gotCom = True


	def connect(self):
		ports = list()															# comport info
		descs = list()
		for port,desc,hwid in comports():
			ports.append(port)
			descs.append(desc)


		if(self.gotCom == False):												# Already know
			while(1):
				try:
					if(len(descs) == 0):										# No Ports
						print('\nError: No serial ports found, exiting...')
						sys.exit(0)
					elif(len(descs) == 1):										# One Port
						print('\nConnecting to only available serial port.')
						print('   %s' % descs[0])
						Self.Com = 0
						break
					else:														# Many Ports, choose
						num_ports = len(ports)
						print('\nMore than 1 serial port found.')
						for i in range(0,num_ports):
							print('%s:   %s' % (i,descs[i]))
						print("NUM: %s" % self.Com)
						if(yesno("OK?")):
							break
						else:
							user = raw_input('\nNUM:')
							if(False == user.isdigit()):
								raise NameError('ChoiceError')
							self.Com = int(user)
							if((self.Com < 0) or (self.Com >= num_ports)):
								raise NameError('ChoiceError')
				except NameError,ValueError:
					print('Invalid choice')


		if(self.gotBaud == False):
			while(1):
				print('\nBaud: %s' % self.Baud)
				if(yesno("OK?")):
					break
				else:
					user = raw_input('\nNew Baud: ')
					if(user.isdigit() == False):
						print('Invalid input.')
					else:
						self.Baud = int(user)


		try:
			self.ser = serial.Serial(port=ports[self.Com],baudrate=self.Baud,bytesize=8,parity='N',stopbits=1,timeout=None,xonxoff=0,rtscts=0)
		except serial.serialutil.SerialException:
			print('Error: Connecting to serial port, exiting...')
			sys.exit(0)
		lines = str(self.ser).replace(" ","").split(',')
		print("\n\nConnected:")
		for line in lines:
			print("          %s" % line)


		# Update dat file
		f = open(DAT,'w')
		f.write("%s,%s" % (self.Baud,self.Com))
		f.close()


	def menu(self,master):
		frame = Frame(master)
		frame.pack()

		self.button = Button(
			frame, text="QUIT", fg="red", command=frame.quit
		)
		self.button.pack(side=RIGHT)

		self.go_radix = Button(frame, text="Radix", command=self.radix)
		self.go_radix.pack(side=LEFT)
		self.go_terminal = Button(frame, text="Terminal", command=self.terminal)
		self.go_terminal.pack(side=LEFT)
		self.go_graph = Button(frame, text="Graph", command=self.graph)
		self.go_graph.pack(side=LEFT)


		#if(yesno('Terminal')):
		#	self.terminal()
		#elif(yesno('Radix')):
		#	self.radix()
		#elif(yesno('Grpah')):
		#	self.graph()

	def say_hi(self):
		print "hi there, everyone!"


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


