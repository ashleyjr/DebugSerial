import sys
from PyQt4 import QtCore, QtGui, uic
from Term import Term
from Radi import Radi
from Grap import Grap
from Plot import Plot
from Test import Test

class Menu(QtGui.QMainWindow):
	def __init__(self,root,ser):
		super(Menu, self).__init__()
		uic.loadUi('Menu.ui', self)
		self.root = root
		self.reset()
		self.ser = ser

	def reset(self):
		self.setWindowTitle('DebugSerial')
		self.btnTerm.clicked.connect(self.Term)
		self.btnRadi.clicked.connect(self.Radi)
		self.btnGrap.clicked.connect(self.Grap)
		self.btnPlot.clicked.connect(self.Plot)
		self.btnTest.clicked.connect(self.Test)
		self.show()




	def Term(self,ser):
		self.hide()
		self.term = Term(self, self.ser)
		self.root.addWindow(self.term)

	def EndTerm(self):
		self.show()
		self.root.rmWindow(self.term)



	def Radi(self):
		self.hide()
		self.radi = Radi(self)
		self.root.addWindow(self.radi)

	def EndRadi(self):
		self.show()
		self.root.rmWindow(self.radi)






	def Grap(self):
		self.hide()
		self.grap = Grap(self)
		self.root.addWindow(self.grap)

	def EndGrap(self):
		self.show()
		self.root.rmWindow(self.grap)







	def Plot(self):
		self.hide()
		self.plot = Plot(self)
		self.root.addWindow(self.plot)

	def EndPlot(self):
		self.show()
		self.root.rmWindow(self.plot)





	def Test(self):
		self.hide()
		self.test = Test(self)
		self.root.addWindow(self.test)

	def EndTest(self):
		self.show()
		self.root.rmWindow(self.test)









