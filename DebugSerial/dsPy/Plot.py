from PyQt4 import QtCore, QtGui, uic

class Plot(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Plot, self).__init__()
		uic.loadUi('dsUis/Plot.ui', self)
		self.setWindowTitle('DS: Plotter')

		self.text = QtGui.QTextEdit()
		self.setCentralWidget(self.text)
		self.text.keyPressEvent = self.tx

		self.caller = caller
		self.ser = ser

		self.timer = QtCore.QTimer()
		self.timer.start(100.0)
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.rx)

		self.state = "pre"
		self.show()




	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndPlot()


	def tx(self, e):
		self.ser.tx(ord(unicode(e.text())))


	def rx(self):
		limit = self.ser.wait()
		if(limit):
			for i in range(0,limit):
				data = ord(self.ser.rx())
				if(self.state == "pre"):
					if(data & 0x81):
						if(data & 0x06):
							self.state = "clear"
						else:
							self.state = "x1"
					else:
						self.state == "pre"		# Failed pre fixed bits
				elif(self.state == "x1"):
					self.state = "y1"
				elif(self.state == "y1"):
					self.state = "pre"
				elif(self.state == "clear"):
					self.satte = "pre"
				else:
					self.state == "pre"

		return




