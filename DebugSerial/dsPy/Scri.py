from PyQt4 import QtCore, QtGui, uic

class Scri(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Scri, self).__init__()
		uic.loadUi('dsUis/Scri.ui', self)
		self.setWindowTitle('DS: Script')

		self.text = QtGui.QTextEdit()
		self.setCentralWidget(self.text)
		self.text.keyPressEvent = self.tx

		self.caller = caller
		self.ser = ser

		self.timer = QtCore.QTimer()
		self.timer.start(100.0)
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.rx)

		self.show()


	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndScri()


	def tx(self, e):
		self.ser.tx(ord(unicode(e.text())))


	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			self.text.insertPlainText(self.ser.rx())
			self.text.ensureCursorVisible()
		return




