from PyQt4 import QtCore, QtGui, uic
import threading
from strings import *

class Radi(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Radi, self).__init__()
		uic.loadUi('Radi.ui', self)
		self.setWindowTitle('DS: Radix')


		#self.text = QtGui.QTextEdit()
		#self.setCentralWidget(self.text)
		#self.text.keyPressEvent = self.key

		self.textEditTx.insertPlainText("DEC     HEX     BIN                  ASCII\n")
		self.textEditTx.keyPressEvent = self.key

		self.caller = caller
		self.ser = ser

		self.async = True
		self.rx = threading.Thread(target=self.asyncRx)
		self.rx.start()

		self.show()



	def closeEvent(self, event):
		self.async = False
		self.rx.join()
		self.caller.EndRadi()


	def key(self, e):

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




	def asyncRx(self):
		self.textEditRx.insertPlainText("DEC     HEX     BIN                  ASCII\n")
		while(self.async == 1):
			if(self.ser.wait()):
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
