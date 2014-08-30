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

		self.screen = 1

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
		for i in range(3,len(self.data)):
			if(self.data[i-3] == "\n"):
				if(self.data[i-1] == "\n"):
					if(broke == False):
						broke = True
					else:
						colour = self.data[i-2]
						full = True
			if(broke):
				im_vec.append(self.data[i])
			if(full):
				break
		update = update + ("Colour %s \n" % colour)

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

			if(colour == 'W'):
				update = update + ("Screen %s \n" % self.screen)
				if(self.screen == 1):
					self.image1.setPixmap(myPixmap.scaled(200, 200))
					self.image1.show();
					self.screen = 2
				elif(self.screen == 2):
					self.image2.setPixmap(myPixmap.scaled(200, 200))
					self.image2.show();
					self.screen = 3
				elif(self.screen == 3):
					self.image3.setPixmap(myPixmap.scaled(200, 200))
					self.image3.show();
					self.screen = 4
				else:
					self.image4.setPixmap(myPixmap.scaled(200, 200))
					self.image4.show();
					self.screen = 1

			elif(colour == 'R'):
				self.red = im

				im = numpy.array(im)
				im = im.astype(numpy.uint8)
				rgbArray = numpy.zeros((10,10,3), 'uint8')
				rgbArray[..., 0] = im
				rgbArray[..., 1] = im*0
				rgbArray[..., 2] = im*0
				im = Image.fromarray(rgbArray)
				im.save("test.png")
				myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('test.png'))

				self.image1.setPixmap(myPixmap.scaled(200, 200))
				self.image1.show();
			elif(colour == 'G'):
				self.green = im

				im = numpy.array(im)
				im = im.astype(numpy.uint8)
				rgbArray = numpy.zeros((10,10,3), 'uint8')
				rgbArray[..., 0] = im*0
				rgbArray[..., 1] = im
				rgbArray[..., 2] = im*0
				im = Image.fromarray(rgbArray)
				im.save("test.png")
				myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('test.png'))


				self.image2.setPixmap(myPixmap.scaled(200, 200))
				self.image2.show();
			elif(colour == 'B'):
				self.blue = im

				im = numpy.array(im)
				im = im.astype(numpy.uint8)
				rgbArray = numpy.zeros((10,10,3), 'uint8')
				rgbArray[..., 0] = im*0
				rgbArray[..., 1] = im*0
				rgbArray[..., 2] = im
				im = Image.fromarray(rgbArray)
				im.save("test.png")
				myPixmap = QtGui.QPixmap(QtCore.QString.fromUtf8('test.png'))

				self.image3.setPixmap(myPixmap.scaled(200, 200))
				self.image3.show();

			if(self.red and self.green and self.blue):

				self.image4.setPixmap(myPixmap.scaled(200, 200))
				self.image4.show();


			if(full):
				update = update + "Full lock"
				self.data = []
			else:
				update = update + "Partial lock"
		else:
			update = update + "No lock"

		self.info.clear()
		self.info.insertPlainText(update)




