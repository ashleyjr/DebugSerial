from PyQt4 import QtCore, QtGui, uic

class Term(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		#uic.loadUi('Term.ui', self)
		self.setWindowTitle('DS: Terminal')
		self.show()
		print "done"




