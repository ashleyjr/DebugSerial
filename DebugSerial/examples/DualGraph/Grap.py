from PyQt4 import QtCore, QtGui, uic

class Grap(QtGui.QMainWindow):
	def __init__(self, caller, parent=None):
		super(Grap, self).__init__()
		uic.loadUi('Grap.ui', self)
		self.setWindowTitle('DS: Graph')
		self.show()
		print "done"
		self.caller = caller

	def closeEvent(self, event):
		self.caller.EndGrap()
		print "close"





