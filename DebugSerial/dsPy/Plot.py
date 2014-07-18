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

		self.state = "pre"
		self.show()




	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndPlot()



	def rx(self):
		limit = self.ser.wait()
		pre = 0x81
		if(limit):
			for i in range(0,limit):
				data = ord(self.ser.rx())
				print self.state
				if(self.state == "pre"):
					pre = data
					if(data & 0x81):
						if(data & 0x06):
							self.x = []			# Clear the graph
							self.y = []
						else:
							self.state = "x1"
					else:
						self.state == "pre"		# Failed pre fixed bits
				elif(self.state == "x1"):
					self.x.append(data)
					self.state = "y1"
				elif(self.state == "y1"):
					self.y.append(data)
					self.state = "pre"
			self.plot.setData(self.x, self.y)
			self.qwtPlot.replot()

		return




