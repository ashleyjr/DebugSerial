import sys, os
from PyQt4 import QtCore, QtGui, uic
from Term import Term
from Radi import Radi
from Grap import Grap
from Plot import Plot
from Scri import Scri

class Menu(QtGui.QMainWindow):
	def __init__(self,root,ser):
		super(Menu, self).__init__()
		uic.loadUi('dsUis/Menu.ui', self)
		self.root = root
		self.ser = ser
		self.reset = False
		self.Run()

	def Run(self):
		self.setWindowTitle('DebugSerial')
		self.btnTerm.clicked.connect(self.Term)
		self.btnRadi.clicked.connect(self.Radi)
		self.btnGrap.clicked.connect(self.Grap)
		self.btnPlot.clicked.connect(self.Plot)
		self.btnScri.clicked.connect(self.Scri)
		self.btnReset.clicked.connect(self.Reset)
		com = "Com: " + str(self.ser.getCom())
		self.labelCom.setText(com)
		baud = "Baud: " + str(self.ser.getBaud())
		self.labelBaud.setText(baud)
	 	reset = "Reset to change settings"
		self.labelReset.setText(reset)
		self.show()



	def Term(self):
		self.hide()
		self.term = Term(self, self.ser)
		self.root.addWindow(self.term)

	def EndTerm(self):
		self.root.rmWindow(self.term)
		self.show()



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


	def Plot(self):
		self.hide()
		self.plot = Plot(self, self.ser)
		self.root.addWindow(self.plot)

	def EndPlot(self):
		self.show()
		self.root.rmWindow(self.plot)



	def Scri(self):
		self.hide()
		self.scri = Scri(self, self.ser)
		self.root.addWindow(self.scri)

	def EndScri(self):
		self.show()
		self.root.rmWindow(self.scri)


	def Reset(self):
		print("\n\n------ Reset ------\n")
		self.reset = True
		QtCore.QCoreApplication.instance().quit()

	def getReset(self):
		return self.reset










