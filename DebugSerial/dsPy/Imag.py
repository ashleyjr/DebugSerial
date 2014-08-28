from PyQt4 import QtCore, QtGui, uic
from PIL import Image
import numpy



class Imag(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Imag, self).__init__()
		uic.loadUi('dsUis/Imag.ui', self)
		self.setWindowTitle('DS: Imager')

		self.caller = caller
		self.ser = ser

		self.btnLoad.clicked.connect(self.Load)


		self.data = []

		self.timer1 = QtCore.QTimer()
		self.timer1.start(100.0)
		self.connect(self.timer1, QtCore.SIGNAL('timeout()'), self.rx)

		self.show()

	def closeEvent(self, event):
		self.timer1.stop()
		self.caller.EndImag()

	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			self.data.append(self.ser.rx())


	def Load(self):

		# Remove the image sub array
		im_vec = []
		broke = False
		full = False
		stop = len(self.data)
		for i in range(2,stop):
			if(self.data[i-2] == "\n"):
				if(self.data[i-1] == "\n"):
					if(broke == False):
						broke = True
					else:
						broke = False
						full = True
						stop = i
			if(broke):
				im_vec.append(self.data[i])

		# construct matrix
		if(full):
			print im_vec
			line = len(im_vec)
			print line

			lock = 0
			for i in range(0,line):
				if(im_vec[i] == "\n"):
					if(im_vec[(2*i) + 1] == "\n"):
						if(im_vec[(3*i) + 2] == "\n"):
							lock = i
				if(lock):
					break
			print lock

			im = []
			im.append([])
			col = 0
			row = 0
			for i in range(0,line):
				im[row].append(self.data[i])
				col = col + 1
				if(col == lock):
					im.append([])
					col = 0
					row = row + 1

			img = Image.open("dsImages/Lenna.png").convert("L")
			im = numpy.array(im)
			print im
			im.save("test.png")

			myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('test.png'))
			self.image.setPixmap(myPixmap)
			self.image.show();



			self.data = []
		else:
			print("not full yet")





