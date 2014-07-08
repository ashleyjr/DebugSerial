# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Grap.ui'
#
# Created: Sat Jul  5 14:25:29 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_win_plot(object):
    def setupUi(self, win_plot):
        win_plot.setObjectName(_fromUtf8("win_plot"))
        win_plot.resize(801, 686)
        self.Menu = QtGui.QWidget(win_plot)
        self.Menu.setEnabled(True)
        self.Menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Menu.setObjectName(_fromUtf8("Menu"))
        self.qwtPlotTx = QwtPlot(self.Menu)
        self.qwtPlotTx.setGeometry(QtCore.QRect(390, 70, 400, 200))
        self.qwtPlotTx.setObjectName(_fromUtf8("qwtPlotTx"))
        self.qwtPlotRx = QwtPlot(self.Menu)
        self.qwtPlotRx.setGeometry(QtCore.QRect(390, 300, 400, 200))
        self.qwtPlotRx.setObjectName(_fromUtf8("qwtPlotRx"))
        self.textEditTx = QtGui.QTextEdit(self.Menu)
        self.textEditTx.setGeometry(QtCore.QRect(10, 70, 341, 201))
        self.textEditTx.setObjectName(_fromUtf8("textEditTx"))
        self.textEditRx = QtGui.QTextEdit(self.Menu)
        self.textEditRx.setGeometry(QtCore.QRect(10, 310, 341, 181))
        self.textEditRx.setObjectName(_fromUtf8("textEditRx"))
        win_plot.setCentralWidget(self.Menu)

        self.retranslateUi(win_plot)
        QtCore.QMetaObject.connectSlotsByName(win_plot)

    def retranslateUi(self, win_plot):
        win_plot.setWindowTitle(QtGui.QApplication.translate("win_plot", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))

from qwt_plot import QwtPlot

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_plot = QtGui.QMainWindow()
    ui = Ui_win_plot()
    ui.setupUi(win_plot)
    win_plot.show()
    sys.exit(app.exec_())

