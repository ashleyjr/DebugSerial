from PyQt4 import QtCore, QtGui, uic

class Plot(QtGui.QMainWindow):
	def __init__(self, caller, parent=None):
		super(Plot, self).__init__()
		uic.loadUi('Plot.ui', self)
		self.setWindowTitle('DS: Plotter')
		self.show()
		print "done"
		self.caller = caller

	def closeEvent(self, event):
		self.caller.EndPlot()
		print "close"





