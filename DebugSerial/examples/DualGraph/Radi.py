from PyQt4 import QtCore, QtGui, uic
import threading
from strings import *

class Radi(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Radi, self).__init__()
		uic.loadUi('Box.ui', self)
		self.setWindowTitle('DS: Radix')


		self.text = QtGui.QTextEdit()
		self.setCentralWidget(self.text)
		self.text.keyPressEvent = self.key

		self.caller = caller
		self.ser = ser

		self.async = True
		self.rx = threading.Thread(target=self.asyncRx)
		self.rx.start()

		self.show()



	def closeEvent(self, event):
		self.async = False
		self.caller.EndRadi()


	def key(self, e):
		try:
			self.ser.tx(ord(unicode(e.text())))
		except:
			pass


	def asyncRx(self):
		self.text.insertPlainText("DEC     HEX     BIN          ASCII")
		while(self.async == 1):
			if(self.ser.wait()):
				char = self.ser.rx()
				data = ord(char)
				s = "\n{0:d}".format(data)
				s = zeroPad(s,3)
				h = "{0:x}".format(data)
				h = zeroPad(h,2)
				s = s + "   	" + h.upper()
				b = "{0:b}".format(data)
				b = zeroPad(b,8)
				s = s + "      " + b + "     " + humanRead(char,text=False)
				self.text.insertPlainText(s)
				self.text.ensureCursorVisible()
		return



