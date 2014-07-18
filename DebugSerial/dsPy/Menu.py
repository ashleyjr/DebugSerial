import sys
from PyQt4 import QtCore, QtGui, uic
from Term import Term
from Radi import Radi
from Grap import Grap

class Menu(QtGui.QMainWindow):
	def __init__(self,root,ser):
		super(Menu, self).__init__()
		uic.loadUi('dsUis/Menu.ui', self)
		self.root = root
		self.reset()
		self.ser = ser

	def reset(self):
		self.setWindowTitle('DebugSerial')
		self.btnTerm.clicked.connect(self.Term)
		self.btnRadi.clicked.connect(self.Radi)
		self.btnGrap.clicked.connect(self.Grap)
		self.show()



	def Term(self):
		self.hide()
		self.term = Term(self, self.ser)
		self.root.addWindow(self.term)

	def EndTerm(self):
		self.show()
		self.root.rmWindow(self.term)



	def Radi(self):
		self.hide()
		self.radi = Radi(self, self.ser)
		self.root.addWindow(self.radi)

	def EndRadi(self):
		self.show()
		self.root.rmWindow(self.radi)



	def Grap(self):
		self.hide()
		self.grap = Grap(self, self.ser)
		self.root.addWindow(self.grap)

	def EndGrap(self):
		self.show()
		self.root.rmWindow(self.grap)









