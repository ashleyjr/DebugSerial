from PyQt4 import QtCore, QtGui, uic
import threading

class Term(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Term, self).__init__()
		uic.loadUi('Term.ui', self)
		self.setWindowTitle('DS: Terminal')


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
		self.caller.EndTerm()


	def key(self, e):
		try:
			self.ser.tx(ord(unicode(e.text())))
		except:
			pass


	def asyncRx(self):
		while(self.async == True):
			if(self.ser.wait()):
				self.text.insertPlainText(self.ser.rx())
				self.text.ensureCursorVisible()
		return




