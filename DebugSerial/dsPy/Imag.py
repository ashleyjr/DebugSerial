from PyQt4 import QtCore, QtGui, uic

class Imag(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Imag, self).__init__()
		uic.loadUi('dsUis/Imag.ui', self)
		self.setWindowTitle('DS: Imager')

		self.caller = caller
		self.ser = ser

		self.btnLoad.clicked.connect(self.Load)


		self.data = []

		self.timer1 = QtCore.QTimer()
		self.timer1.start(100.0)
		self.connect(self.timer1, QtCore.SIGNAL('timeout()'), self.rx)

		self.show()

	def closeEvent(self, event):
		self.timer1.stop()
		self.caller.EndImag()

	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			self.data.append(self.ser.rx())


	def seek(self):
		run = True
		start = True
		count = 0
		for i in range(0,(len(self.data)-1)):
			count = count + 1
			if(self.data[i] == "\n"):
				if(self.data[i + 1] == "\n"):
					if(start):
						start = False
						startPos = i + 2
						self.info.insertPlainText("Begin\n\n")
					else:
						start = True
						endPos = i - 1
						self.info.insertPlainText("End\n\n")
						self.info.insertPlainText(str(count))
			if(run == False):
				break


	def Load(self):

		run = True
		start = True
		count = 0
		for i in range(0,(len(self.data)-1)):
			count = count + 1
			if(self.data[i] == "\n"):
				if(self.data[i + 1] == "\n"):
					if(start):
						start = False
						startPos = i + 2
						self.info.insertPlainText("Begin\n\n")
					else:
						start = True
						endPos = i - 1
						self.info.insertPlainText("End\n\n")
						self.info.insertPlainText(str(count))
			if(run == False):
				break

		#myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('dsImages/lenna.png'))
		#self.image.setPixmap(myPixmap)
		#self.image.show();





