import sys
import numpy
import threading
from strings import *
from PyQt4.Qwt5 import *
from PyQt4 import QtCore, QtGui, uic
import PyQt4.Qwt5 as Qwt

numPoints=1000
xs=numpy.arange(numPoints)
ys=numpy.sin(3.14159*xs*10/numPoints)



class Grap(QtGui.QMainWindow):
	def __init__(self, caller, ser, parent=None):
		super(Grap, self).__init__()

		uic.loadUi('Grap.ui', self)

		self.setWindowTitle('DS: Graph')
		self.show()
		self.ser = ser

		self.caller = caller


		self.rx=Qwt.QwtPlotCurve()
		self.rx.attach(self.qwtPlotRx)
		self.qwtPlotRx

		self.tx=Qwt.QwtPlotCurve()
		self.tx.attach(self.qwtPlotTx)
		self.qwtPlotTx

		self.timer =  QtCore.QTimer()
		self.timer.start(100.0)

		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.output)

		self.rx_x = []
		self.rx_y = []
		self.tx_x = []
		self.tx_y = []

		self.rx_count = 0
		self.tx_count = 0

		self.rx_x.append(0)
		self.rx_y.append(0)
		self.tx_x.append(0)
		self.tx_y.append(0)

		self.textEditTx.keyPressEvent = self.key

		self.async = True
		self.get = threading.Thread(target=self.asyncRx)
		self.get.start()

		self.show()

	def output(self):
		global ys
		self.rx.setData(self.rx_x, self.rx_y)
		self.qwtPlotRx.replot()
		self.tx.setData(self.tx_x, self.tx_y)
		self.qwtPlotTx.replot()

	def key(self, e):
		try:
			key = unicode(e.text())
			print humanRead(key,text=True)
			self.textEditTx.insertPlainText(humanRead(key,text=True))
			data = ord(key)
			self.ser.tx(data)
			self.tx_x.append(self.tx_count)
			self.tx_y.append(data)
			if(self.tx_count > 100):
				self.tx_x =  self.tx_x[1:]
				self.tx_y =  self.tx_y[1:]
			self.tx_count = self.tx_count + 1
		except e:
			print e

	def asyncRx(self):
		while(self.async == True):
			if(self.ser.wait()):
				data = self.ser.rx()
				self.textEditRx.insertPlainText(humanRead(data,text=True))
				self.textEditRx.ensureCursorVisible()
				self.rx_x.append(self.rx_count)
				self.rx_y.append(ord(data))
				if(self.rx_count > 100):
					self.rx_x =  self.rx_x[1:]
					self.rx_y =  self.rx_y[1:]
				self.rx_count = self.rx_count + 1


	def closeEvent(self, event):
		self.async = False
		self.timer.stop()
		self.caller.EndGrap()
		self.get.join()




