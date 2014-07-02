from PyQt4 import QtCore, QtGui, uic

class Test(QtGui.QMainWindow):
	def __init__(self, caller, parent=None):
		super(Test, self).__init__()
		uic.loadUi('Test.ui', self)
		self.setWindowTitle('DS: Tester')
		self.show()
		print "done"
		self.caller = caller

	def closeEvent(self, event):
		self.caller.EndTest()
		print "close"





