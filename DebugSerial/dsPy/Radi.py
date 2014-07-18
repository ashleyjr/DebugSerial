from PyQt4 import QtCore, QtGui, uic
from strings import *

class Radi(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Radi, self).__init__()
		uic.loadUi('dsUis/Radi.ui', self)
		self.setWindowTitle('DS: Radix')

		self.textEditTx.insertPlainText("DEC     HEX     BIN                  ASCII\n")
		self.textEditRx.insertPlainText("DEC     HEX     BIN                  ASCII\n")
		self.textEditTx.keyPressEvent = self.tx

		self.caller = caller
		self.ser = ser

		self.timer = QtCore.QTimer()
		self.timer.start(100.0)
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.rx)

		self.show()



	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndRadi()


	def tx(self, e):
		char = unicode(e.text())
		data = ord(char)
		self.ser.tx(data)
		s = "{0:d}".format(data)
		s = zeroPad(s,3)
		h = "{0:x}".format(data)
		h = zeroPad(h,2)
		s = s + "     " + h.upper()
		b = "{0:b}".format(data)
		b = zeroPad(b,8)
		s = "\n" + s + "        " + b + "        " + humanRead(char,text=False)
		self.textEditTx.insertPlainText(s)
		self.textEditTx.ensureCursorVisible()


	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			char = self.ser.rx()
			data = ord(char)
			s = "{0:d}".format(data)
			s = zeroPad(s,3)
			h = "{0:x}".format(data)
			h = zeroPad(h,2)
			s = s + "     " + h.upper()
			b = "{0:b}".format(data)
			b = zeroPad(b,8)
			s = "\n" + s + "        " + b + "        " + humanRead(char,text=False)
			self.textEditRx.insertPlainText(s)
			self.textEditRx.ensureCursorVisible()
