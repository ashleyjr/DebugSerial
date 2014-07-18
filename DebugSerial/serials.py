#!/usr/bin/python
import serial, sys, os, threading, re, datetime
from Tkinter import *
from serial.tools.list_ports import comports
from strings import *


DAT = "DebuSerial.dat"
DIR = "dsLogs"
EXT = ".dslog"


class Serial:
	def __init__(self):
		try:
			if not os.path.exists(DIR):
				os.makedirs(DIR)
			timestamp = unicode(datetime.datetime.now()).replace("-","").replace(":","").replace(".","").replace(" ","")
			self.log = open(DIR + "/" + timestamp + EXT,'w')
			self.log.write(timestamp)
		except:
			print "Couldn't create log file"
		self.gotBaud = False
		self.gotCom = False
		self.Baud = 9600
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
			self.Baud = user
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
			self.Com = user
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
						self.Com = 0
						break
					else:														# Many Ports, choose
						num_ports = len(ports)
						print('\nMore than 1 serial port found.')
						for i in range(0,num_ports):
							print('%s:   %s' % (i,descs[i]))
						print("NUM: %s\n" % self.Com)
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
				print('\nBaud: %s\n' % self.Baud)
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
		lines = str(self.ser).replace(" ","").replace("(","").replace(")","").replace(">",",").replace("<",",").split(",")
		print("\n\nConnected:")
		for line in lines:
			print("          %s" % line)

		# Update dat file
		f = open(DAT,'w')
		f.write("%s,%s" % (self.Baud,self.Com))
		f.close()


	def disconnect(self):
		self.log.close()
		print("\nExiting...")
		self.ser.close()
		print("To invoke DebugSerial with the same settings...\n\n")
		print("$ python DebugSerial.py -c %s -b %s" % (self.Com,self.Baud))


	def tx(self, data):
		logStr = "t" + str(data)
		self.log.write(logStr)
		if((data >= 0) and (data <= 255)):
			self.ser.write(chr(data))

	def rx(self):
		data = self.ser.read(1)
		logStr = "r" + str(ord(data))
		self.log.write(logStr)
		return data

	def wait(self):
		return self.ser.inWaiting()

	def exit(self):
		self.async = 0
		self.master.destroy()
		self.ser.close()

