from PyQt4 import QtCore, QtGui, uic
import PyQt4.Qwt5 as Qwt

class Plot(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Plot, self).__init__()
		uic.loadUi('dsUis/Plot.ui', self)
		self.setWindowTitle('DS: Plotter')

		self.caller = caller
		self.ser = ser


		self.x = []
		self.y = []
		self.plot=Qwt.QwtPlotCurve()
		self.plot.attach(self.qwtPlot)


		self.timer = QtCore.QTimer()
		self.timer.start(100.0)
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.rx)


		self.x = []
		self.y = []

		self.pre = 0x03
		self.buff = 0x00
		self.state = "pre"
		self.show()




	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndPlot()



	def rx(self):
		limit = self.ser.wait()
		if(limit):
			for i in range(0,limit):
				data = ord(self.ser.rx())
				print self.state
				if(self.state == "pre"):
					self.pre = data
					if(data & 0x03):			# In pre bits one and two have to be 1
						if(data & 0x0C):
							self.x = []			# Clear the graph
							self.y = []
						else:
							self.state = "x1"
					else:
						self.state == "pre"		# Failed pre fixed bits



				# X Axis data
				elif(self.state == "x1"):
					if(self.pre & 0xC0):
						self.buff = data
						self.state = "x2"
					else:
						self.x.append(data)
						self.state = "y1"

				elif(self.state == "x2"):
					shifted = (self.buff << 8)|data
					if(self.pre & 0x80):
						self.buff = shifted
						self.state = "x3"
					else:
						self.x.append(shifted)
						self.state = "y1"

				elif(self.state == "x3"):
					shifted = (self.buff << 8)|data
					if(self.pre & 0x40):
						self.buff = shifted
						self.state = "x4"
					else:
						self.x.append(shifted)
						self.state = "y1"

				elif(self.state == "x4"):
					shifted = (self.buff << 8)|data
					self.x.append(shifted)
					self.state = "y1"



				# Y axis data
				elif(self.state == "y1"):
					if(self.pre & 0x30):
						self.buff = data
						self.state = "y2"
					else:
						self.y.append(data)
						self.state = "pre"

				elif(self.state == "y2"):
					shifted = (self.buff << 8)|data
					if(self.pre & 0x20):
						self.buff = shifted
						self.state = "y3"
					else:
						self.y.append(shifted)
						self.state = "pre"

				elif(self.state == "y3"):
					shifted = (self.buff << 8)|data
					if(self.pre & 0x10):
						self.buff = shifted
						self.state = "y4"
					else:
						self.y.append(shifted)
						self.state = "pre"

				elif(self.state == "y4"):
					shifted = (self.buff << 8)|data
					self.y.append(shifted)
					self.state = "pre"



			self.plot.setData(self.x, self.y)
			self.qwtPlot.replot()

		return




