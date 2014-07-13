#!/usr/bin/python
import serial, sys, os, threading, re, datetime
from Tkinter import *
from serial.tools.list_ports import comports
from strings import *


DAT = "DebuSerial.dat"
DIR = "dslogs"
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



	def menu(self,m):
		self.master = m
		self.frame = Frame(self.master)
		self.frame.pack()

		self.go_terminal = Button(self.frame)
		self.go_radix = Button(self.frame)
		self.go_graph = Button(self.frame)
		self.go_plotter = Button(self.frame)
		self.go_test = Button(self.frame)

		self.menuButtons()

		self.master.protocol('WM_DELETE_WINDOW', self.exit)
		self.master.mainloop()


	def menuButtons(self):
		self.go_terminal.configure(text="Terminal", state=NORMAL, command = self.terminal)
		self.go_terminal.pack(side=LEFT)
		self.go_radix.configure(text="Radix", state=NORMAL, command = self.radix)
		self.go_radix.pack(side=LEFT)
		self.go_graph.configure(text="Graph", state=NORMAL, command = self.graph)
		self.go_graph.pack(side=LEFT)
		self.go_plotter.configure(text="Plotter", state=NORMAL, command = self.plotter)
		self.go_plotter.pack(side=LEFT)
		self.go_test.configure(text="Test", state=NORMAL, command = self.test)
		self.go_test.pack(side=LEFT)



	def exit(self):
		self.async = 0
		self.master.destroy()
		self.ser.close()



	def terminal(self):
		self.go_radix['state'] = 'disabled'
		self.go_graph['state'] = 'disabled'
		self.go_plotter['state'] = 'disabled'
		self.go_test['state'] = 'disabled'
		self.go_terminal.configure(text="Close Terminal", command = self.terminalEnd)
		self.text = Text(self.master)
		self.scr = Scrollbar(self.master)
		self.text.insert(INSERT, "Terminal mode:\n")
		self.text.config(state=NORMAL)
		self.scr.pack(side="right", fill="y", expand=False)
		self.text.pack(side="left", fill="both", expand=True)
		self.text.pack()
		self.text.bind("<Key>",self.sendKeyTerm)
		self.async = 1
		rx = threading.Thread(target=self.asyncRxTerm)
		rx.start()
		self.text.mainloop()
		rx.join()
	def sendKeyTerm(self,event):
		self.text.mark_set("insert",END)
		self.text.delete(INSERT)
		char = event.char
		if(len(char) == 1):
			test = ord(char)
			if((test >= 0) and (test <= 255)):
				self.ser.write(char)
	def asyncRxTerm(self):
		while(self.async == 1):
			if(self.ser.inWaiting()):
				self.text.config(state=NORMAL)
				self.text.mark_set("insert",END)
				self.text.insert(INSERT,humanRead(self.ser.read(1),text=True))
				self.text.config(state=DISABLED)
				self.text.see(END)
	def terminalEnd(self):
		self.text.destroy()
		self.scr.destroy()
		self.async = 0
		self.menuButtons()





	def radix(self):
		self.go_terminal['state'] = 'disabled'
		self.go_graph['state'] = 'disabled'
		self.go_plotter['state'] = 'disabled'
		self.go_test['state'] = 'disabled'
		self.go_radix.configure(text="Close Radix", command = self.radixEnd)
		self.text = Text(self.master)
		self.scr = Scrollbar(self.master)
		self.text.insert(INSERT, "Radix mode:\n")
		self.text.config(state=NORMAL)
		self.scr.pack(side="right", fill="y", expand=False)
		self.text.pack(side="left", fill="both", expand=True)
		self.text.bind("<Key>",self.sendKeyRadix)
		self.async = 1
		rx = threading.Thread(target=self.asyncRxRadix)
		rx.start()
		self.text.mainloop()
		rx.join()
	def sendKeyRadix(self,event):
		self.text.mark_set("insert",END)
		self.text.delete(INSERT)
		char = event.char
		if(len(char) == 1):
			test = ord(char)
			if((test >= 0) and (test <= 255)):
				self.ser.write(char)
	def asyncRxRadix(self):
		self.text.config(state=NORMAL)
		self.text.insert(INSERT,"DEC     HEX     BIN          ASCII")
		#self.text.config(state=DISABLED)
		while(self.async == 1):
			if(self.ser.inWaiting()):
				char = self.ser.read(1)
				data = ord(char)
				s = "\n{0:d}".format(data)
				s = zeroPad(s,3)
				h = "{0:x}".format(data)
				h = zeroPad(h,2)
				s = s + "   	" + h.upper()
				b = "{0:b}".format(data)
				b = zeroPad(b,8)
				s = s + "      " + b + "     " + humanRead(char,text=False)
				self.text.config(state=NORMAL)
				self.text.insert(INSERT,s)
				self.text.config(state=DISABLED)
				self.text.see(END)
	def radixEnd(self):
		self.text.destroy()
		self.scr.destroy()
		self.async = 0
		self.menuButtons()






	def graph(self):
		self.rx = Graph(20)
		self.tx = Graph(20)
		self.go_terminal['state'] = 'disabled'
		self.go_radix['state'] = 'disabled'
		self.go_plotter['state'] = 'disabled'
		self.go_test['state'] = 'disabled'
		self.go_graph.configure(text="Close Graph", command = self.graphEnd)
		self.text = Text(self.master)
		self.text.insert(INSERT, "Graph mode:\n")
		self.text.config(state=NORMAL)
		self.text.pack()
		self.text.bind("<Key>",self.sendKeyGraph)
		self.async = 1

		self.rx = Graph(20)
		self.tx = Graph(20)

		#self.g.draw()
		#rx = threading.Thread(target=self.asyncRxGraph)
		temp = "Rx Data"
		drawRx = threading.Thread(target=self.rx.draw,args=(temp,))
		temp = "Tx Data"
		drawTx = threading.Thread(target=self.tx.draw,args=(temp,))

		#tx = threading.Thread(target=#)
		#grapher = threading.Thread(target=self.text.mainloop)

		self.tx.draw("Tx Data")
		self.rx.draw("Rx Data")
#		drawTx.start()
#		print "2"
#		#drawRx.start()
#		#print "3"
#
#		while(self.async == 1):
#			pass
#
#		rx.join()
#		drawTx.join()
#		#drawRx.join()
#
		#grapher.join()
		#update.join()
	def sendKeyGraph(self,event):
		self.text.delete(INSERT)
		char = event.char
		if(len(char) == 1):
			test = ord(char)
			if((test >= 0) and (test <= 255)):
				self.ser.write(char)
				self.tx.new(test)
				print test
	def grapher(self):
		while(self.async == 1):
			time.sleep(1)
			self.rx.update()
		self.rx.kill()
	def asyncRxGraph(self):
		self.text.config(state=NORMAL)
		self.text.insert(INSERT,"DEC     HEX     BIN          ASCII")
		while(self.async == 1):
			if(self.ser.inWaiting()):
				char = self.ser.read(1)
				data = ord(char)
				s = "\n{0:d}".format(data)
				s = zeroPad(s,3)
				h = "{0:x}".format(data)
				h = zeroPad(h,2)
				s = s + "   	" + h.upper()
				b = "{0:b}".format(data)
				b = zeroPad(b,8)
				s = s + "      " + b + "     " + humanRead(char,0)
				self.text.configure(state="normal")
				self.text.insert(INSERT,s)
				self.text.configure(state="disable")
				self.rx.new(data)
		self.rx.kill()
		self.tx.kill()
	def graphEnd(self):
		self.text.destroy()
		self.async = 0
		self.menuButtons()






#	def asyncRxRadix(self):
#		sys.stdout.write("\n\rDEC     HEX     BIN          ASCII")
#		while(self.async == 1):
#			char = self.ser.read(1)
#			data = ord(char)
#			s = "{0:d}".format(data)
#			s = zeroPad(s,3)
#			h = "{0:x}".format(data)
#			h = zeroPad(h,2)
#			s = s + "   	" + h.upper()
#			b = "{0:b}".format(data)
#			b = zeroPad(b,8)
#			s = s + "      " + b + "     " + humanRead(char,0)
#			sys.stdout.write("\n\r%s" % s)
#			sys.stdout.flush()
#		print("\n\n")

#	def asyncRxGraph(self):
#		sys.stdout.write("\n\rDEC     HEX     BIN          ASCII")
#		while(self.async == 1):
#			char = self.ser.read(1)
#			data = ord(char)
#			s = "{0:d}".format(data)
#			s = zeroPad(s,3)
#			h = "{0:x}".format(data)
#			h = zeroPad(h,2)
#			s = s + "   	" + h.upper()
#			b = "{0:b}".format(data)
#			b = zeroPad(b,8)
#			s = s + "      " + b + "     " + humanRead(char,0)
#			sys.stdout.write("\n\r%s" % s)
#			sys.stdout.flush()
#			self.g.new(data)
#		self.g.kill()
#		print("\n\n")




	def plotter(self):
		pass

	def test(self):
		pass
