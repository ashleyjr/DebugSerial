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

		#self.btnLoad.clicked.connect(self.Load)


		self.data = []

		self.timer1 = QtCore.QTimer()
		self.timer1.start(100.0)
		self.connect(self.timer1, QtCore.SIGNAL('timeout()'), self.rx)
		self.got = 0

		self.timer2 = QtCore.QTimer()
		self.timer2.start(2000.0)
		self.connect(self.timer2, QtCore.SIGNAL('timeout()'), self.Load)
		self.info.insertPlainText("Recieving data")



		self.show()

	def closeEvent(self, event):
		self.timer1.stop()
		self.timer2.stop()
		self.caller.EndImag()

	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			self.data.append(self.ser.rx())
			self.got = self.got + 1

	def Load(self):
		update = ("Recieved %s bytes\n" % self.got)

		# Remove the image sub array
		im_vec = []
		broke = False
		full = False
		for i in range(2,len(self.data)):
			if(self.data[i-2] == "\n"):
				if(self.data[i-1] == "\n"):
					if(broke == False):
						broke = True
					else:
						full = True
			if(broke):
				im_vec.append(self.data[i])
			if(full):
				break

		# Lock on the series of \n chars
		line = len(im_vec)
		lock = 0
		for i in range(0,line):
			locked = True
			index = i
			j = 0
			while(index < line):
				if(im_vec[index] != "\n"):
					locked = False
					break
				j = j + 1
				index = (j+1)*i + j
			if(locked):
				lock = i
				break

		# Display and save image if locked
		if(lock):
			im = []
			row = 0
			i = 0
			while(i < (line-lock)):
				im.append([])
				for j in range(0,lock):
					im[row].append(ord(im_vec[i]))
					i = i + 1
				i = i + 1
				row = row + 1
			im = numpy.array(im)
			im = im.astype(numpy.uint8)
			im = Image.fromarray(im)
			im.save("test.png")
			myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('test.png'))
			self.image1.setPixmap(myPixmap.scaled(200, 200))
			self.image1.show();
			self.image2.setPixmap(myPixmap.scaled(200, 200))
			self.image2.show();
			self.image3.setPixmap(myPixmap.scaled(200, 200))
			self.image3.show();
			self.image4.setPixmap(myPixmap.scaled(200, 200))
			self.image4.show();
			if(full):
				update = update + "Full lock"
			else:
				update = update + "Partial lock"
		else:
			update = update + "No lock"

		self.info.clear()
		self.info.insertPlainText(update)




