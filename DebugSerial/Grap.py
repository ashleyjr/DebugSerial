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


		self.rxPlot=Qwt.QwtPlotCurve()
		self.rxPlot.attach(self.qwtPlotRx)
		self.qwtPlotRx

		self.txPlot=Qwt.QwtPlotCurve()
		self.txPlot.attach(self.qwtPlotTx)
		self.qwtPlotTx

		self.timer =  QtCore.QTimer()
		self.timer.start(100.0)

		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.output)

		self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self.setAxis)

		self.xAxis = 100


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

		self.textEditTx.keyPressEvent = self.tx


		self.show()

	def setAxis(self,value):
		self.xAxis = value

	def output(self):
		global ys
		self.rxPlot.setData(self.rx_x, self.rx_y)
		end = self.rx_count - self.xAxis
		if(end < 0):
			end = 0
		self.qwtPlotRx.setAxisScale(Qwt.QwtPlot.xBottom, end, self.rx_count)
		self.qwtPlotRx.setAxisScale(Qwt.QwtPlot.yLeft, 0, 255)
		self.qwtPlotRx.replot()
		self.txPlot.setData(self.tx_x, self.tx_y)
		self.qwtPlotTx.replot()
		self.rx()


	def tx(self, e):
		key = unicode(e.text())
		if(len(key) != 0):
			self.textEditTx.insertPlainText(humanRead(key,text=True))
			self.textEditTx.ensureCursorVisible()
			data = ord(key)
			self.ser.tx(data)
			self.tx_x.append(self.tx_count)
			self.tx_y.append(data)
			if(self.tx_count > 1000):
				self.tx_x =  self.tx_x[1:]
				self.tx_y =  self.tx_y[1:]
			self.tx_count = self.tx_count + 1


	def rx(self):
		limit = self.ser.wait()
		for i in range(0,limit):
			data = self.ser.rx()
			self.textEditRx.insertPlainText(humanRead(data,text=True))
			self.textEditRx.ensureCursorVisible()
			self.rx_x.append(self.rx_count)
			self.rx_y.append(ord(data))
			if(self.rx_count > self.xAxis ):
				self.rx_x =  self.rx_x[1:]
				self.rx_y =  self.rx_y[1:]
			self.rx_count = self.rx_count + 1


	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndGrap()




