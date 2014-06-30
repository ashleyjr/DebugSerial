from PyQt4 import QtCore, QtGui, uic

class Term(QtGui.QMainWindow):
	def __init__(self, caller, parent=None):
		#QtGui.QDialog.__init__(self, parent)
		super(Term, self).__init__()
		uic.loadUi('Term.ui', self)
		self.setWindowTitle('DS: Terminal')
		self.show()
		print "done"
		self.caller = caller

	def closeEvent(self, event):
		self.caller.reset()





