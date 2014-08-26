#!/usr/bin/python
print("______     _                 _____           _       _" )
print("|  _  \   | |               /  ___|         (_)     | |")
print("| | | |___| |__  _   _  __ _\ `--.  ___ _ __ _  __ _| |")
print("| | | / _ \ '_ \| | | |/ _` |`--. \/ _ \ '__| |/ _` | |")
print("| |/ /  __/ |_) | |_| | (_| /\__/ /  __/ |  | | (_| | |")
print("|___/ \___|_.__/ \__,_|\__, \____/ \___|_|  |_|\__,_|_|")
print("                        __/ |                          ")
print("                       |___/                           ")

import sys
sys.path.append("dsPy")
from serials import Serial
import optparse
from PyQt4 import QtGui
from Multi import Multi
from Menu import Menu




if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-b', '--baud',
		dest="baud"
	)
	parser.add_option('-c', '--com',
		dest="com"
	)
	options, remainder = parser.parse_args()
	run = True
	while(run):
		u = None
		app = None
		root = None
		menu = None
		u = Serial()
		if(options.baud or options.com):
			print("User options...")
		if(options.baud):
			print 'Baud: ', options.baud
			u.baud(options.baud)
		if(options.com):
			print ' Com: ', options.com
			u.com(options.com)
		u.connect()
		print("\nLaunching GUI")
		app = QtGui.QApplication(sys.argv)
		root = Multi()
		menu = Menu(root,u)
		app.exec_()
		u.disconnect()
		run = menu.getReset()
	print("\nExiting.")
	print("To invoke DebugSerial with the same settings...\n\n")
	print("$ python DebugSerial.py -c %s -b %s" % (u.getCom(),u.getBaud()))
