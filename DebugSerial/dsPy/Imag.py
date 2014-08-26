from PyQt4 import QtCore, QtGui, uic

class Imag(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Imag, self).__init__()
		uic.loadUi('dsUis/Imag.ui', self)
		self.setWindowTitle('DS: Imager')

		self.caller = caller
		self.ser = ser

		self.btnLoad.clicked.connect(self.Load)
		self.show()

	def closeEvent(self, event):
		self.caller.EndImag()

	def Load(self):
		myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('dsImages/lenna.png'))
		self.image.setPixmap(myPixmap)
		self.image.show();





