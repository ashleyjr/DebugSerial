from PyQt4 import QtGui

class Multi(QtGui.QMainWindow):
	def __init__(self):
		self.__windows = []

	def addWindow(self, window):
		self.__windows.append(window)

	def rmWindow(self, window):
		self.__windows.remove(window)

	def show(self):
		for current_child_window in self.__windows:
			current_child_window.exec_() # probably show will do the same trick



