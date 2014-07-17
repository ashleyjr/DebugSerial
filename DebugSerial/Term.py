from PyQt4 import QtCore, QtGui, uic

class Term(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Term, self).__init__()
		uic.loadUi('uis/Term.ui', self)
		self.setWindowTitle('DS: Terminal')

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
		self.caller.EndTerm()


	def tx(self, e):
		self.ser.tx(ord(unicode(e.text())))


	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			self.text.insertPlainText(self.ser.rx())
			self.text.ensureCursorVisible()
		return




