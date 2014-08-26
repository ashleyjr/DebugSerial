from PyQt4 import QtCore, QtGui, uic

class Imag(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Imag, self).__init__()
		uic.loadUi('dsUis/Imag.ui', self)
		self.setWindowTitle('DS: Imager')
		self.btnLoad.clicked.connect(self.Load)
		self.show()

	def Load(self):
		image.setPixmap("lenna.png");
		image.show();





