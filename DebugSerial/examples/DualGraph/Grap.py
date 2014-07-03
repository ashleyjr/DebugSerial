import sys
import numpy
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

	def output(self):
		global ys
		print "time"





		self.rx.setData(self.rx_x, self.rx_y)
		self.qwtPlotRx.replot()

		self.tx.setData(self.tx_x, self.tx_y)
		self.qwtPlotTx.replot()

	def key(self, e):
		try:
			print "caught"
			data = ord(unicode(e.text()))
			self.ser.tx(data)
			self.tx_x.append(self.tx_count)
			self.tx_y.append(data)
			if(self.tx_count > 100):
				self.rx_x =  self.tx_x[1:]
				self.tx_y =  self.tx_y[1:]
			self.tx_count = self.tx_count + 1
		except:
			pass

	def closeEvent(self, event):
		self.timer.stop()
		self.caller.EndGrap()
		print "close"




