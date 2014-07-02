from PyQt4 import QtCore, QtGui, uic

class Radi(QtGui.QMainWindow):
	def __init__(self, caller, parent=None):
		super(Radi, self).__init__()
		uic.loadUi('Radi.ui', self)
		self.setWindowTitle('DS: Radix')
		self.show()
		print "done"
		self.caller = caller

	def closeEvent(self, event):
		self.caller.EndRadi()
		print "close"





