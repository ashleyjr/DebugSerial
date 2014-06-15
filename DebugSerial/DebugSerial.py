#!/usr/bin/python

# Why not ?
print("______     _                 _____           _       _" )
print("|  _  \   | |               /  ___|         (_)     | |")
print("| | | |___| |__  _   _  __ _\ `--.  ___ _ __ _  __ _| |")
print("| | | / _ \ '_ \| | | |/ _` |`--. \/ _ \ '__| |/ _` | |")
print("| |/ /  __/ |_) | |_| | (_| /\__/ /  __/ |  | | (_| | |")
print("|___/ \___|_.__/ \__,_|\__, \____/ \___|_|  |_|\__,_|_|")
print("                        __/ |                          ")
print("                       |___/                           ")
print("------- Ashley J. Robinson ----- ajrobinson.org -------")


from serials import Serial
import optparse
import sys

def main():
	print 'ARGV      :', sys.argv[1:]

	parser = optparse.OptionParser()
	parser.add_option('-t', '--output',
		dest="output_filename",
		default="default.out",
	)
	parser.add_option('-v', '--verbose',
	dest="verbose",
	default=False,
	action="store_true",
	)
	parser.add_option('--version',
	dest="version",
	default=1.0,
	type="float",
	)
	options, remainder = parser.parse_args()

	print 'VERSION   :', options.version
	print 'VERBOSE   :', options.verbose
	print 'OUTPUT    :', options.output_filename
	print 'REMAINING :', remainder
	u = Serial()
	u.menu()

if __name__ == "__main__":
	main()

