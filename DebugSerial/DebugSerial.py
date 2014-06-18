#!/usr/bin/python
print("______     _                 _____           _       _" )
print("|  _  \   | |               /  ___|         (_)     | |")
print("| | | |___| |__  _   _  __ _\ `--.  ___ _ __ _  __ _| |")
print("| | | / _ \ '_ \| | | |/ _` |`--. \/ _ \ '__| |/ _` | |")
print("| |/ /  __/ |_) | |_| | (_| /\__/ /  __/ |  | | (_| | |")
print("|___/ \___|_.__/ \__,_|\__, \____/ \___|_|  |_|\__,_|_|")
print("                        __/ |                          ")
print("                       |___/                           ")

from Tkinter import *
from serials import Serial
import optparse
import sys

def main():
	parser = optparse.OptionParser()
	parser.add_option('-b', '--baud',
		dest="baud"
	)
	parser.add_option('-c', '--com',
		dest="com"
	)
	options, remainder = parser.parse_args()

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
	root = Tk()
	root.wm_title("DebugSerial")
	app = u.menu(root)
	u.disconnect()




if __name__ == "__main__":
	main()

