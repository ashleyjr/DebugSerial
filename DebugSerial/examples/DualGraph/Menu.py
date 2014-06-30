import sys
from PyQt4 import QtCore, QtGui, uic
from Term import Term


class Menu(QtGui.QMainWindow):
	def __init__(self,root):
		super(Menu, self).__init__()
		uic.loadUi('Menu.ui', self)
		self.root = root
		self.reset()

	def reset(self):
		self.term = None
		self.setWindowTitle('DebugSerial')
		self.btnTerm.clicked.connect(self.Term)
		self.btnRadi.clicked.connect(self.Radi)
		self.btnGrap.clicked.connect(self.Grap)
		self.btnPlot.clicked.connect(self.Plot)
		self.btnTest.clicked.connect(self.Test)
		self.show()

	def Term(self):
		self.hide()
		self.term = Term(self)
		self.root.addWindow(self.term)



	def Radi(self):
		print "Radix"

	def Grap(self):
		print "Graph"

	def Plot(self):
		print "Plotter"

	def Test(self):
		print "Test script"

	def closeEvent(self, event):
		sys.exit(0)



