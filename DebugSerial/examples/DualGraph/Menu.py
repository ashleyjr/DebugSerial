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
		self.setWindowTitle('DebugSerial')
		self.btnTerm.clicked.connect(self.Term)
		self.btnRadi.clicked.connect(self.Radi)
		self.btnGrap.clicked.connect(self.Grap)
		self.btnPlot.clicked.connect(self.Plot)
		self.btnTest.clicked.connect(self.Test)
		self.show()

	def Term(self):
		self.btnTerm.clicked.connect(self.Term)
		self.btnRadi.clicked.connect(self.Radi)
		self.btnGrap.clicked.connect(self.Grap)
		self.btnPlot.clicked.connect(self.Plot)
		self.btnTest.clicked.connect(self.Test)
		term = Term()
		self.root.addWindow(term)

	def TermEnd(self):


	def Radi(self):
		print "Radix"

	def Grap(self):
		print "Graph"

	def Plot(self):
		print "Plotter"

	def Test(self):
		print "Test script"



